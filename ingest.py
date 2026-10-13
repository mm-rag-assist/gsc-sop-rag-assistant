"""Ingest pipeline: Markdown SOPs -> chunks -> Gemini embeddings -> ChromaDB.

Run:
    python ingest.py            # build / rebuild the vector database
    python ingest.py --dry-run  # only show how documents are chunked (no API calls)
"""
import argparse
import re
import sys
import time

import yaml

import config


# ---------------------------------------------------------------- loading
def load_documents():
    """Read every Markdown file in data/sop and split YAML front matter from body."""
    docs = []
    for path in sorted(config.DATA_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta, body = {}, text
        m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if m:
            meta = yaml.safe_load(m.group(1)) or {}
            body = text[m.end():]
        meta.setdefault("doc_id", path.stem)
        meta.setdefault("title", path.stem)
        docs.append({"meta": meta, "body": body, "file": path.name})
    return docs


# --------------------------------------------------------------- chunking
def split_sections(body):
    """Split a document on ## and ### headings.

    Returns a list of (section_path, text). The H1 title and intro text
    before the first ## become the "Overview" section.
    """
    sections, h2, h3, buf = [], "Overview", None, []
    in_code = False

    def flush():
        text = "\n".join(buf).strip()
        if text:
            path = f"{h2} > {h3}" if h3 else h2
            sections.append((path, text))

    for line in body.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
        if not in_code and line.startswith("## "):
            flush(); buf = []
            h2, h3 = line[3:].strip(), None
            continue
        if not in_code and line.startswith("### "):
            flush(); buf = []
            h3 = line[4:].strip()
            continue
        if not in_code and line.startswith("# "):
            continue  # document title is stored in metadata
        buf.append(line)
    flush()
    # The short intro ("This document is intended to provide...") is not
    # useful on its own - merge it into the first real section.
    if len(sections) > 1 and sections[0][0] == "Overview":
        intro = sections.pop(0)[1]
        path, text = sections[0]
        sections[0] = (path, intro + "\n\n" + text)
    return sections


def split_blocks(text):
    """Split text into blocks: on blank lines and before every top-level
    numbered step ("12. ..."), never inside a ``` code block."""
    blocks, cur, in_code = [], [], False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
        if not in_code and re.match(r"^\d+\.\s", line) and cur:
            blocks.append("\n".join(cur)); cur = []
        if not line.strip() and not in_code:
            if cur:
                blocks.append("\n".join(cur)); cur = []
            continue
        cur.append(line)
    if cur:
        blocks.append("\n".join(cur))
    return blocks


def split_long(text):
    """Keep a section whole if it fits; otherwise pack blocks into parts with overlap."""
    if len(text) <= config.MAX_CHUNK_CHARS:
        return [text]
    blocks = split_blocks(text)
    parts, cur = [], []
    for block in blocks:
        if cur and len("\n\n".join(cur + [block])) > config.MAX_CHUNK_CHARS:
            parts.append("\n\n".join(cur))
            cur = cur[-config.OVERLAP_BLOCKS:] if config.OVERLAP_BLOCKS else []
        cur.append(block)
    if cur:
        parts.append("\n\n".join(cur))
    return parts


def build_chunks(docs):
    chunks = []
    for doc in docs:
        meta = doc["meta"]
        for section, text in split_sections(doc["body"]):
            parts = split_long(text)
            for i, part in enumerate(parts, 1):
                label = section if len(parts) == 1 else f"{section} (part {i}/{len(parts)})"
                # The header is embedded together with the text, so the vector
                # "knows" which procedure and section the fragment belongs to.
                content = f"Procedure: {meta['title']}\nSection: {label}\n\n{part}"
                chunks.append({
                    "id": f"{meta['doc_id']}::{len(chunks):03d}",
                    "text": content,
                    "meta": {
                        "doc_id": meta["doc_id"],
                        "title": meta["title"],
                        "section": label,
                        # top-level (##) section: used at query time to pull in the
                        # whole section (steps + reply templates), see rag.py
                        "h2": section.split(" > ")[0],
                        "order": len(chunks),
                        "file": doc["file"],
                    },
                })
    return chunks


# -------------------------------------------------------------- embedding
def embed_documents(client, texts, batch_size=20):
    from google.genai import types

    vectors = []
    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]
        for attempt in range(5):
            try:
                resp = client.models.embed_content(
                    model=config.EMBED_MODEL,
                    contents=batch,
                    config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
                )
                vectors.extend(e.values for e in resp.embeddings)
                break
            except Exception as exc:  # free tier rate limits -> wait and retry
                wait = 10 * (attempt + 1)
                print(f"  embedding batch failed ({exc}); retry in {wait}s")
                time.sleep(wait)
        else:
            sys.exit("Embedding failed after 5 attempts.")
        print(f"  embedded {min(start + batch_size, len(texts))}/{len(texts)}")
    return vectors


# ------------------------------------------------------------------- main
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="show chunks, no API calls")
    args = parser.parse_args()

    docs = load_documents()
    chunks = build_chunks(docs)
    print(f"Documents: {len(docs)} | chunks: {len(chunks)}")
    sizes = [len(c["text"]) for c in chunks]
    print(f"Chunk size (chars): min {min(sizes)}, avg {sum(sizes)//len(sizes)}, max {max(sizes)}")

    if args.dry_run:
        for c in chunks:
            print(f"  {c['id']:<48} {len(c['text']):>5}  {c['meta']['section']}")
        return

    if not config.GEMINI_API_KEY:
        sys.exit("No GEMINI_API_KEY in .env")

    import chromadb
    from google import genai

    client = genai.Client(api_key=config.GEMINI_API_KEY)
    vectors = embed_documents(client, [c["text"] for c in chunks])

    db = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    try:
        db.delete_collection(config.COLLECTION)  # full rebuild keeps the index in sync with data/sop
    except Exception:
        pass
    col = db.create_collection(
        name=config.COLLECTION,
        metadata={"hnsw:space": "cosine", "embed_model": config.EMBED_MODEL},
    )
    col.add(
        ids=[c["id"] for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[c["meta"] for c in chunks],
        embeddings=vectors,
    )
    print(f"Saved {col.count()} chunks to {config.CHROMA_DIR} (collection '{config.COLLECTION}').")


if __name__ == "__main__":
    main()
