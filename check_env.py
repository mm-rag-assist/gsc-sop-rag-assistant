"""E3 environment check: packages, API key, Gemini embedding + generation.
Run:  python check_env.py
"""
import os
import sys

print(f"Python: {sys.version.split()[0]}")
missing = []
for mod in ("google.genai", "chromadb", "streamlit", "dotenv", "yaml"):
    try:
        __import__(mod)
        print(f"  [OK] {mod}")
    except Exception as e:  # noqa: BLE001
        missing.append(mod)
        print(f"  [MISSING] {mod}: {e}")
if missing:
    sys.exit("Install packages first: python -m pip install -r requirements.txt")

from dotenv import load_dotenv
from google import genai

load_dotenv()
key = os.getenv("GEMINI_API_KEY", "")
if not key or key.startswith("paste-"):
    sys.exit("No GEMINI_API_KEY in .env (copy .env.example to .env and paste the key).")

embed_model = os.getenv("EMBED_MODEL", "gemini-embedding-001")
gen_model = os.getenv("GEN_MODEL", "gemini-flash-lite-latest")
client = genai.Client(api_key=key)

print("\nAvailable models (embedding / flash):")
try:
    for m in client.models.list():
        name = m.name.replace("models/", "")
        if "embedding" in name or "flash" in name:
            print("  -", name)
except Exception as e:  # noqa: BLE001
    print("  could not list models:", e)

try:
    r = client.models.embed_content(model=embed_model, contents="How many URLs can I submit for indexing per day?")
    print(f"\n[OK] Embedding ({embed_model}): vector length {len(r.embeddings[0].values)}")
except Exception as e:  # noqa: BLE001
    sys.exit(f"\n[FAIL] Embedding ({embed_model}): {e}")

try:
    r = client.models.generate_content(model=gen_model, contents="Reply with exactly: OK")
    print(f"[OK] Generation ({gen_model}): {r.text.strip()}")
except Exception as e:  # noqa: BLE001
    sys.exit(f"[FAIL] Generation ({gen_model}): {e}")

print("\nEnvironment ready.")
