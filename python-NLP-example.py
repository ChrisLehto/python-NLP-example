import argparse, re, sqlite3
from contextlib import closing

DB_FILE = "test.db" 

def connect():
    return sqlite3.connect(DB_FILE)

def extract_name(q: str):
    m = re.search(r"\b(?:of|for)\s+([^\s\"']+|\"[^\"]+\"|'[^']+')", q)
    if not m:
        return None
    raw = m.group(1)
    if (raw.startswith('"') and raw.endswith('"')) or (raw.startswith("'") and raw.endswith("'")):
        raw = raw[1:-1]
    return raw

def find_doc_key(cur, name: str):
    row = cur.execute(
        "SELECT doc_key FROM files WHERE doc_key = ? LIMIT 1", (name,)
    ).fetchone()
    if row:
        return row[0]

    row = cur.execute("""
        SELECT doc_key
        FROM files
        WHERE filename = ?
        ORDER BY version DESC, created_at DESC
        LIMIT 1
    """, (name,)).fetchone()
    return row[0] if row else None

def answer(question: str) -> str:
    ql = question.strip().lower()

    with closing(connect()) as c:
        cur = c.cursor()

        if re.search(r"\b(how many|count)\b.*\b(files?)\b", ql):
            n = cur.execute("SELECT COUNT(DISTINCT doc_key) FROM files").fetchone()[0]
            return f"You have {n} unique files (by doc_key)."
        
        if re.search(r"\b(list|show)\b.*\b(files?)\b", ql):
            n = cur.execute("SELECT COUNT(DISTINCT doc_key) FROM files").fetchone()[0]
            return f"There are {n} distinct files in the database."

        if re.search(r"\b(how many|count)\b.*\b(versions?)\b", ql):
            name = extract_name(question)
            if name:
                dk = find_doc_key(cur, name)
                if not dk:
                    return f'I couldn’t find a file matching "{name}".'
                n = cur.execute(
                    "SELECT COUNT(*) FROM files WHERE doc_key = ?",
                    (dk,)
                ).fetchone()[0]
                return f'File "{dk}" has {n} version(s) stored.'
            else:
                n = cur.execute("SELECT COUNT(*) FROM files").fetchone()[0]
                return f"There are {n} total file versions stored."

        if re.search(r"\b(list|show)\b.*\b(versions?)\b", ql):
            name = extract_name(question)
            if not name:
                return "Please specify which file (e.g., 'list versions of myfile.json')."

            rows = cur.execute(
                "SELECT version FROM files WHERE doc_key = ? ORDER BY version", (name,)
            ).fetchall()

            if not rows:
                rows = cur.execute(
                    "SELECT version FROM files WHERE filename = ? ORDER BY version", (name,)
                ).fetchall()
                if not rows:
                    return f'I couldn’t find a file matching "{name}".'

            return "Versions:\n" + "\n".join(f"v{v[0]}" for v in rows)

        return ("Sorry, I didn’t understand. Try:\n"
                "- How many files do I have?\n"
                "- How many versions of \"sample.json\"?\n"
                "- List files\n"
                "- List versions of \"sample.json\"")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("question", nargs="+", help="Ask a question in plain English")
    args = ap.parse_args()
    print(answer(" ".join(args.question)))

if __name__ == "__main__":
    main()
