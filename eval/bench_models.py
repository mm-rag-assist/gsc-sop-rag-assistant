"""Latency / quality check of the generation models on one fixed question.

Run from the repo folder:  python eval/bench_models.py
Uses 1 embedding call + 1 generation call per model (free tier friendly).
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config  # noqa: E402
from assistant import _make_config, _prompt, build_context, gemini_client, render_templates  # noqa: E402
from rag import expand_to_sections, retrieve  # noqa: E402

QUESTION = "i need to add access to gsc"
MODELS = [config.GEN_MODEL, config.FALLBACK_MODEL]

sections = expand_to_sections(retrieve(QUESTION))
templates = {}
contents = [{"role": "user", "parts": [{"text": f"{build_context(sections, templates)}\n\nOperator question: {QUESTION}"}]}]
print(f"Question: {QUESTION} | context: {sum(len(s['text']) for s in sections)} chars "
      f"| thinking level: {config.THINKING_LEVEL or 'model default'}\n")

for model in MODELS:
    t0 = time.perf_counter()
    try:
        resp = gemini_client().models.generate_content(
            model=model, contents=contents, config=_make_config(_prompt("system_prompt.md"), 0.2, model))
        raw = (resp.text or "").strip()
        secs = time.perf_counter() - t0
        text = render_templates(raw, templates)
        templates_ok = text.count("Kind regards")
        print(f"{model:<24} {secs:6.1f}s  model wrote {len(raw):5} chars  complete templates: {templates_ok}/4")
    except Exception as exc:  # noqa: BLE001
        print(f"{model:<24} ERROR {exc}")
    time.sleep(6)
