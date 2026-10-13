"""Console chat for testing the assistant (multi-turn).

Run:  python chat_cli.py
Commands: /new = start a new conversation, /quit = exit
"""
from assistant import answer, format_sources


def main():
    history = []
    print("GSC SOP Assistant - console test. Type a question (/new = new conversation, /quit = exit).\n")
    while True:
        try:
            q = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not q:
            continue
        if q == "/quit":
            break
        if q == "/new":
            history = []
            print("-- new conversation --\n")
            continue

        ans = answer(q, history)
        print(f"\nAssistant:\n{ans.text}\n")
        if ans.sources:
            print("Sources:")
            for line in format_sources(ans):
                print("  " + line)
        print(f"\n  [debug] search query: {ans.query}")
        print("  [debug] top chunks: " + ", ".join(
            f"{h['score']:.2f} {h['meta']['doc_id']} > {h['meta']['section']}" for h in ans.hits))
        for i, s in enumerate(ans.sections, 1):
            print(f"  [debug] S{i} = {s['title']} > {s['section']} ({len(s['text'])} chars"
                  f"{', trimmed' if s.get('trimmed') else ''})")
        if ans.model:
            print(f"  [debug] model: {ans.model}")
        if ans.timings:
            print("  [debug] time: " + ", ".join(f"{k} {v:.1f}s" for k, v in ans.timings.items())
                  + f" | total {sum(ans.timings.values()):.1f}s")
        if ans.gated:
            print("  [debug] blocked by relevance threshold - no LLM call")
        print()
        history += [{"role": "user", "content": q}, {"role": "assistant", "content": ans.text}]


if __name__ == "__main__":
    main()
