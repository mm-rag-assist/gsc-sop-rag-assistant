"""Retrieval: question -> Gemini query embedding -> top-k chunks from ChromaDB
-> expansion of each hit to its whole ## section ("small-to-big")."""
from functools import lru_cache

import config


@lru_cache(maxsize=1)
def _clients():
    import chromadb
    from google import genai

    if not config.GEMINI_API_KEY:
        raise RuntimeError("No GEMINI_API_KEY in .env")
    gemini = genai.Client(api_key=config.GEMINI_API_KEY)
    db = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    try:
        col = db.get_collection(config.COLLECTION)
    except Exception as exc:
        raise RuntimeError("Vector database not found - run: python ingest.py") from exc
    return gemini, col


RETRYABLE = (429, 500, 503)  # rate limit / server error / model overloaded


def with_retry(call, waits=(5, 15, 30, 60)):
    """Run call(); on free-tier rate limits (429) or overload (503) wait and retry.
    A 429 quota window on the free tier lasts up to a minute, hence the long waits."""
    import time

    from google.genai import errors

    for wait in (0,) + tuple(waits):
        time.sleep(wait)
        try:
            return call()
        except errors.APIError as exc:
            if getattr(exc, "code", None) not in RETRYABLE:
                raise
            last = exc
            print(f"  [retry] Gemini {exc.code} - waiting before next attempt...")
    raise RuntimeError(f"Gemini is unavailable right now, please try again in a minute ({last})")


def embed_query(text):
    from google.genai import types

    gemini, _ = _clients()
    resp = with_retry(lambda: gemini.models.embed_content(
        model=config.EMBED_MODEL,
        contents=text,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
    ))
    return resp.embeddings[0].values


def retrieve(question, k=config.TOP_K):
    """Return the k most similar chunks as dicts: id, text, meta, score (cosine similarity)."""
    _, col = _clients()
    res = col.query(
        query_embeddings=[embed_query(question)],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    hits = []
    for cid, doc, meta, dist in zip(
        res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0]
    ):
        hits.append({"id": cid, "text": doc, "meta": meta, "score": round(1 - dist, 4)})
    return hits


def _body(chunk_text):
    """Chunk text without the 'Procedure: / Section:' header added at ingest time."""
    parts = chunk_text.split("\n\n", 1)
    return parts[1] if len(parts) == 2 and parts[0].startswith("Procedure:") else chunk_text


def _merge(prev, nxt):
    """Join consecutive chunks of one section, removing ONLY the overlap repeated at ingest
    (the start of the next part equal to the end of the previous one).

    Bug fixed 2026-10-13: the first version removed any paragraph already seen nearby,
    which also deleted the identical closing lines of consecutive reply templates
    ("Once this ticket is closed...", "Kind regards," + the closing ```), so templates 2 and 4 lost
    their footer before the model ever saw them.
    """
    if not prev:
        return nxt
    cuts = [i for i in range(len(nxt)) if nxt.startswith("\n\n", i)]
    for i in reversed(cuts):  # longest overlap first
        head = nxt[:i]
        if head.strip() and prev.endswith(head):
            return prev + nxt[i:]
    return prev + "\n\n" + nxt


def expand_to_sections(hits, max_sections=config.MAX_SECTIONS):
    """Group hits by (procedure, ## section) and load the chunks of that section.

    Small chunks give precise search; whole sections give the model complete context
    (e.g. the steps AND the reply templates stored in a separate ### chunk).
    If a section is longer than MAX_SECTION_CHARS (long SOPs), only the hit chunks,
    their neighbours and every chunk with a reply template are kept, so the context
    does not grow with the length of the documents.
    Returns sections ordered by their best hit score.
    """
    _, col = _clients()
    groups = {}
    for h in hits:  # hits are sorted by score, so dict order = best first
        m = h["meta"]
        key = (m["doc_id"], m.get("h2", m["section"]))
        groups.setdefault(key, {"meta": m, "score": h["score"], "hits": []})["hits"].append(h)

    sections = []
    for key, g in list(groups.items())[:max_sections]:
        m = g["meta"]
        rows = []
        if "h2" in m:
            got = col.get(
                where={"$and": [{"doc_id": {"$eq": key[0]}}, {"h2": {"$eq": key[1]}}]},
                include=["documents", "metadatas"],
            )
            rows = sorted(zip(got["documents"], got["metadatas"]), key=lambda r: r[1].get("order", 0))
        if not rows:
            rows = [(h["text"], h["meta"]) for h in g["hits"]]

        trimmed = False
        if sum(len(_body(d)) for d, _ in rows) > config.MAX_SECTION_CHARS:
            hit_orders = {h["meta"].get("order") for h in g["hits"]}
            keep = {o + d for o in hit_orders if o is not None for d in (-1, 0, 1)}
            rows = [r for r in rows if r[1].get("order") in keep or "```text" in r[0]]
            trimmed = True

        merged, prev_order = "", None
        for doc, meta in rows:
            order = meta.get("order")
            if trimmed and prev_order is not None and order is not None and order != prev_order + 1:
                merged += "\n\n[...]"  # gap: part of a long section was left out
            merged = _merge(merged, _body(doc))
            prev_order = order
        sections.append({
            "doc_id": key[0],
            "title": m["title"],
            "section": key[1],
            "score": g["score"],
            "text": merged,
            "trimmed": trimmed,
            "hit_ids": [h["id"] for h in g["hits"]],
        })
    return sections


@lru_cache(maxsize=1)
def sop_catalog():
    """Procedures and their sections, read from the vector DB metadata.

    Built automatically from whatever was ingested, so new SOPs extend the
    vocabulary used by query rewriting and the list of supported procedures
    without editing any prompt by hand.
    Returns {procedure title: [section names in document order]}.
    """
    _, col = _clients()
    got = col.get(include=["metadatas"])
    catalog = {}
    for meta in sorted(got["metadatas"], key=lambda m: m.get("order", 0)):
        sections = catalog.setdefault(meta["title"], [])
        name = meta["section"].split(" (part ")[0]
        if name not in sections:
            sections.append(name)
    return catalog


def catalog_text():
    return "\n".join(f"- {title}: " + "; ".join(secs) for title, secs in sop_catalog().items())


if __name__ == "__main__":
    import sys

    q = " ".join(sys.argv[1:]) or "How many URLs can I request indexing for per day?"
    print(f"Q: {q}\n")
    hits = retrieve(q)
    for h in hits:
        print(f"  {h['score']:.3f}  {h['meta']['title']} > {h['meta']['section']}")
    print("\nSections sent to the model:")
    for i, s in enumerate(expand_to_sections(hits), 1):
        print(f"[S{i}] {s['score']:.3f}  {s['title']} > {s['section']}  ({len(s['text'])} chars)")
