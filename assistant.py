"""Answer pipeline:
(rewrite follow-up) -> retrieve chunks -> relevance gate -> expand to whole sections
-> build context -> Gemini (retry + fallback model) -> answer + sources.

Used by the CLI (chat_cli.py), the tests (eval/test_answers.py) and the web UI (E6).
"""
import re
import warnings
import time
from dataclasses import dataclass, field
from functools import lru_cache

import config
from rag import _clients, catalog_text, expand_to_sections, retrieve, sop_catalog

# SDK warning for finish reasons it does not know yet (e.g. MALFORMED_RESPONSE) - handled in _generate.
warnings.filterwarnings("ignore", message=r".* is not a valid FinishReason")

PROMPTS = config.ROOT / "prompts"
HISTORY_MESSAGES = 6  # last 3 exchanges (operator + assistant) are sent to the model
NOT_FOUND = "I couldn't find this in the GSC SOPs."
OUT_OF_SCOPE = "This is outside my scope."
def scope_hint():
    """One sentence listing the procedures in the knowledge base (built from the DB, not hard-coded)."""
    return "I can help with these procedures: " + "; ".join(sop_catalog()) + "."


@dataclass
class Answer:
    text: str
    query: str                                     # query used for retrieval (after rewriting)
    hits: list = field(default_factory=list)       # retrieved chunks with similarity scores
    sections: list = field(default_factory=list)   # whole sections sent to the model as S1..Sn
    sources: list = field(default_factory=list)    # sections the answer actually cites
    gated: bool = False                            # True = blocked by the threshold, no LLM call
    model: str = ""                                # model that generated the answer
    timings: dict = field(default_factory=dict)    # seconds per pipeline step (debug / tuning)


@lru_cache(maxsize=None)
def _prompt(name):
    return (PROMPTS / name).read_text(encoding="utf-8")


_THINKING_OK = {}  # model -> False when the API rejected the thinking setting


def _make_config(system, temperature, model):
    from google.genai import types

    kwargs = dict(system_instruction=system, temperature=temperature)
    level = config.THINKING_LEVEL
    if level and _THINKING_OK.get(model, True):
        try:
            kwargs["thinking_config"] = types.ThinkingConfig(thinking_level=level)
        except Exception:  # older SDK without thinking_level
            _THINKING_OK[model] = False
    return types.GenerateContentConfig(**kwargs)


def _generate(contents, system, temperature):
    """Call Gemini; on overload (503) / rate limit (429) retry, then switch to FALLBACK_MODEL.

    Gemini 3 models "think" before answering. A short procedure lookup does not need deep
    reasoning, so THINKING_LEVEL (config) keeps it low - this is the main latency setting.
    """
    from google.genai import errors

    last_exc = None
    for model in (config.GEN_MODEL, config.FALLBACK_MODEL):
        for wait in (0, 5, 15):
            time.sleep(wait)
            try:
                resp = gemini_client().models.generate_content(
                    model=model, contents=contents, config=_make_config(system, temperature, model)
                )
                text = (resp.text or "").strip()
                if text:
                    return text, model
                # 2026-10-13: the model sometimes ends with finish reason MALFORMED_RESPONSE and
                # no text - treat an empty answer like an overload: retry, then the fallback model.
                reason = getattr(resp.candidates[0], "finish_reason", "?") if resp.candidates else "no candidates"
                last_exc = RuntimeError(f"empty response ({reason})")
                print(f"  [retry] {model}: empty response ({reason})")
                continue
            except errors.APIError as exc:
                last_exc = exc
                code = getattr(exc, "code", None)
                if code == 400 and _THINKING_OK.get(model, True) and config.THINKING_LEVEL:
                    _THINKING_OK[model] = False  # model does not accept the setting - retry without it
                    print(f"  [info] {model}: thinking level not supported, using model default")
                    continue
                if code not in (429, 500, 503):
                    raise
                print(f"  [retry] {model}: Gemini {code}")
    raise RuntimeError(f"Gemini is unavailable right now, please try again in a minute ({last_exc})")


def gemini_client():
    return _clients()[0]


def _history_contents(history):
    """history: list of {"role": "user"|"assistant", "content": str}. Keep only the last N."""
    out = []
    for msg in history[-HISTORY_MESSAGES:]:
        role = "user" if msg["role"] == "user" else "model"
        out.append({"role": role, "parts": [{"text": msg["content"]}]})
    return out


def rewrite_query(question, history):
    """Normalise every question into one English search query in SOP vocabulary.

    - multi-turn: a follow-up ("and if it fails?") becomes a standalone query,
    - language: questions in Polish (or any language) are translated, so retrieval and
      the answer do not depend on the operator's language,
    - vocabulary: "admin", "owner" -> "full access" etc. (the words the SOPs use).
    Added 2026-10-13 after a test: the same question in Polish got "not found" while
    the English one got an answer, and "admin access" missed the full-access section.
    """
    convo = "\n".join(
        f"{'Operator' if m['role'] == 'user' else 'Assistant'}: {m['content'][:600]}"
        for m in history[-HISTORY_MESSAGES:]
    )
    text, _ = _generate(
        f"SOP catalog (procedure: sections):\n{catalog_text()}\n\n"
        f"Conversation:\n{convo or '(none)'}\n\nLatest message: {question}", _prompt("query_rewrite.md"), 0.0
    )
    lines = text.splitlines()
    return lines[0].strip() if lines else question


# ---------------------------------------------------------------- reply templates
# Test 2026-10-13: the model shortened repeated template footers no matter how the rule was
# phrased (2/4 complete templates on two different models). Templates are therefore NOT
# retyped by the model: each ```text block in the sources is tagged with an ID, the model
# only writes {{T1}}, and the application pastes the exact text from the SOP.
_TEMPLATE_RE = re.compile(r"^([ \t]*)```text[ \t]*\n(.*?)\n\1```[ \t]*$", re.M | re.S)


def _template_name(before):
    for line in reversed(before.rstrip().splitlines()):
        s = line.strip()
        if s:
            s = re.sub(r"^\d+\.\s*", "", s).replace("**", "").replace("*", "").rstrip(":").strip()
            # a named template ("Template 2 - one domain property ...") keeps its name;
            # a step sentence ("Respond to the requestor ..., for example") does not
            return s if re.match(r"(Template|Reply)", s, re.I) else "Reply to requestor (customer visible)"
    return "Reply template"


def tag_templates(text, registry):
    def repl(m):
        indent, body = m.group(1), m.group(2)
        body = "\n".join(l[len(indent):] if l.startswith(indent) else l for l in body.splitlines())
        tid = f"T{len(registry) + 1}"
        registry[tid] = {"name": _template_name(text[:m.start()]), "text": body}
        return f'{indent}<template id="{tid}">\n{body}\n{indent}</template>'

    return _TEMPLATE_RE.sub(repl, text)


def render_templates(text, registry):
    """Replace {{T1}} markers written by the model with the verbatim SOP template."""
    def block(tid):
        tpl = registry.get(tid)
        if not tpl:
            return None
        title = "" if tpl["name"].lower().startswith("reply to requestor") else f"*{tpl['name']}*\n\n"
        return f"{title}```text\n{tpl['text']}\n```"

    def line_repl(m):
        # Marker on its own line: keep the indentation so the block stays inside a list step.
        indent, out = m.group(1), block(m.group(2))
        if out is None:
            return m.group(0)
        pad = " " * max(len(indent.expandtabs(4)), 3) if indent else ""
        return "\n".join(pad + ln if ln else ln for ln in out.split("\n"))

    def inline_repl(m):
        out = block(m.group(1))
        return m.group(0) if out is None else "\n\n" + out + "\n\n"

    # A marker the model left unindented right below a numbered step still belongs to that step.
    lines, in_step = text.split("\n"), False
    for i, ln in enumerate(lines):
        if re.fullmatch(r"`?\{\{\s*T\d+\s*\}\}`?\s*", ln):
            if in_step:
                lines[i] = "   " + ln
        elif re.match(r"\s*\d+\.\s", ln):
            in_step = True
        elif ln.strip() and not ln[0].isspace():
            in_step = False
    text = "\n".join(lines)
    text = re.sub(r"(?m)^([ \t]*)`?\{\{\s*(T\d+)\s*\}\}`?[ \t]*$", line_repl, text)
    return re.sub(r"`?\{\{\s*(T\d+)\s*\}\}`?", inline_repl, text)


def build_context(sections, registry):
    blocks = [
        f'<source id="S{i}" procedure="{s["title"]}" section="{s["section"]}">\n'
        f'{tag_templates(s["text"], registry)}\n</source>'
        for i, s in enumerate(sections, 1)
    ]
    return "<sources>\n" + "\n".join(blocks) + "\n</sources>"


def cited_labels(text, n_sources):
    """Find S-labels in any bracket form: [S1], [S1, S4], [S2][S3]."""
    nums = set()
    for group in re.findall(r"\[([^\]]*)\]", text):
        nums.update(int(n) for n in re.findall(r"S(\d+)", group))
    return sorted(n for n in nums if 1 <= n <= n_sources)


def retrieve_multi(queries):
    """Search with several phrasings and keep the best score per chunk (multi-query retrieval).

    The rewrite step can over-simplify (e.g. "add ADMIN access" -> "grant GSC access"), so the
    operator's original wording is searched too - a detail lost in one query is kept by the other.
    """
    best = {}
    for q in dict.fromkeys(q for q in queries if q):  # unique, keep order
        for h in retrieve(q):
            if h["id"] not in best or h["score"] > best[h["id"]]["score"]:
                best[h["id"]] = h
    return sorted(best.values(), key=lambda h: h["score"], reverse=True)[: config.TOP_K]


def answer(question, history=None):
    history = history or []
    timings = {}
    t0 = time.perf_counter()
    query = rewrite_query(question, history)
    timings["rewrite"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    hits = retrieve_multi([query, question])
    timings["retrieve"] = time.perf_counter() - t0

    # Guardrail 1: nothing similar enough in the knowledge base -> no LLM call at all.
    if not hits or hits[0]["score"] < config.RELEVANCE_THRESHOLD:
        return Answer(text=f"{NOT_FOUND} {scope_hint()}", query=query, hits=hits, gated=True, timings=timings)

    t0 = time.perf_counter()
    sections = expand_to_sections(hits)
    timings["expand"] = time.perf_counter() - t0

    templates = {}
    user_turn = (f"{build_context(sections, templates)}\n\nOperator question: {question}\n"
                 f"Same question in English, in SOP terms: {query}")
    contents = _history_contents(history) + [{"role": "user", "parts": [{"text": user_turn}]}]
    t0 = time.perf_counter()
    system = _prompt("system_prompt.md").replace("{PROCEDURES}", "; ".join(sop_catalog()))
    text, model = _generate(contents, system, 0.2)
    timings["generate"] = time.perf_counter() - t0
    text = render_templates(text, templates)

    # Grounding: the source list is built by the app from the metadata of the cited
    # sections, so the model cannot invent a source.
    sources = [dict(sections[n - 1], label=f"S{n}") for n in cited_labels(text, len(sections))]
    if text.startswith((NOT_FOUND, OUT_OF_SCOPE)) and not sources:
        sources = []
    return Answer(text=text, query=query, hits=hits, sections=sections, sources=sources,
                  model=model, timings=timings)


def format_sources(ans):
    return [f"[{s['label']}] {s['title']} › {s['section']}" for s in ans.sources]
