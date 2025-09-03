# NLP + SQLite: Plain-English QA

A tiny demo that answers plain-English questions about a fixed SQLite table using **regular expressions** and **SQLite**.  
No external deps, just Python’s standard library.

## What it does

- Understands simple questions like:
  - “how many files do I have?”
  - “list files”
  - “how many versions of `sample.json`?”
  - “list versions of `parsed`”
- Looks up answers from a single table named **`files`** in `test.db` (same folder as the script).

- **Data lineage:** `test.db` was generated with the **JSON-to-SQLite** repo, using a JSON file created by the **Python-XML-Parser** repo. You don’t need those to run this demo, but they’re how the sample data was built.
  
### Make sure test.db is next to the script (already provided in this repo)

### Run some questions
```Bash
python nlp_sqlite.py "how many files do i have"
python nlp_sqlite.py "list files"
python nlp_sqlite.py "how many versions of parsed"
python nlp_sqlite.py "list versions of 'my file.json'"
```
