"""GSC SOP Assistant - web chat interface (Streamlit).

Run:  python -m streamlit run app.py      then open http://localhost:8501
"""
import streamlit as st

import config

st.set_page_config(page_title="GSC SOP Assistant", page_icon="🔎", layout="wide")

EXAMPLES = [
    "How many URLs can I request indexing for per day?",
    "I want to add admin access to GSC for a user",
    "The requestor attached a sitemap file instead of a URL. What do I do?",
    "GSC says 'Failed to add user: email not found'. What now?",
]


@st.cache_resource(show_spinner="Loading knowledge base...")
def load_backend():
    """Import the RAG pipeline once and check the vector DB is ready."""
    import assistant
    from rag import sop_catalog

    return assistant, sop_catalog()


def render_details(d):
    """'How this answer was found' panel - makes the retrieval step visible."""
    with st.expander("How this answer was found"):
        st.markdown(f"**Search query** (normalised by the model): `{d['query']}`")
        if d["gated"]:
            st.warning(
                f"Best match below the relevance threshold ({config.RELEVANCE_THRESHOLD}) - "
                "answered without calling the language model."
            )
        st.markdown("**Top fragments found in the vector database** (cosine similarity)")
        st.table([
            {"score": f"{h['score']:.3f}", "procedure": h["meta"]["title"], "section": h["meta"]["section"]}
            for h in d["hits"]
        ])
        if d["sections"]:
            st.markdown("**Context sent to the model** (whole SOP sections)")
            st.markdown("\n".join(
                f"- S{i} · {s['title']} › {s['section']} ({len(s['text'])} chars"
                f"{', trimmed' if s.get('trimmed') else ''})"
                for i, s in enumerate(d["sections"], 1)
            ))
        timing = ", ".join(f"{k} {v:.1f}s" for k, v in d["timings"].items())
        st.caption(f"Model: {d['model'] or '-'} · {timing} · total {sum(d['timings'].values()):.1f}s")


def render_assistant(msg):
    st.markdown(msg["content"])
    if msg.get("sources"):
        st.markdown("**Sources**")
        st.markdown("\n".join(f"- {s}" for s in msg["sources"]))
    if msg.get("details"):
        render_details(msg["details"])


# ------------------------------------------------------------------ state
if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    assistant, catalog = load_backend()
except Exception as exc:  # missing key, missing DB, ...
    st.error(f"The assistant could not start: {exc}")
    st.info("Check the .env file (GEMINI_API_KEY) and build the database: `python ingest.py`")
    st.stop()

# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.title("🔎 GSC SOP Assistant")
    st.caption(
        "Answers Search Support operators' questions about handling Google Search Console "
        "tickets - only from the team's SOPs (RAG). Data is anonymised (DemoCorp)."
    )
    if st.button("🗑️ New conversation", width="stretch"):
        st.session_state.messages = []
        st.rerun()

    st.subheader("Try an example")
    for q in EXAMPLES:
        if st.button(q, width="stretch"):
            st.session_state.pending = q

    st.subheader(f"Knowledge base · {len(catalog)} SOPs")
    for title, sections in catalog.items():
        with st.expander(title):
            st.markdown("\n".join(f"- {s}" for s in sections))

    st.caption(
        f"Embeddings: {config.EMBED_MODEL} · LLM: {config.GEN_MODEL} "
        f"(fallback {config.FALLBACK_MODEL}) · top-k {config.TOP_K} · "
        f"threshold {config.RELEVANCE_THRESHOLD}"
    )

# ------------------------------------------------------------------- chat
st.header("Ask about a GSC ticket")
if not st.session_state.messages:
    st.info("Ask in English or Polish - e.g. how to grant access, request indexing or submit a sitemap. "
            "Answers cite the SOP sections they come from.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            render_assistant(msg)
        else:
            st.markdown(msg["content"])

question = st.chat_input("Describe the ticket or ask about a procedure...")
question = question or st.session_state.pop("pending", None)

if question:
    history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the SOPs..."):
            try:
                ans = assistant.answer(question, history)
            except Exception as exc:
                st.error(f"Something went wrong: {exc}")
                st.stop()
        msg = {
            "role": "assistant",
            "content": ans.text,
            "sources": assistant.format_sources(ans),
            "details": {
                "query": ans.query,
                "gated": ans.gated,
                "hits": ans.hits,
                "sections": ans.sections,
                "model": ans.model,
                "timings": ans.timings,
            },
        }
        render_assistant(msg)
    st.session_state.messages.append(msg)
