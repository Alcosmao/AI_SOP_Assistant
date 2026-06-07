# AI SOP Assistant

A simple project for learning **RAG** (Retrieval-Augmented Generation) on SOP documents (Standard Operating Procedures).

This is not a full AI chat app yet. It is a **Python pipeline** that shows step by step how to search a document for relevant information and build an answer from the retrieved chunks.

---

## What does this project do?

1. Loads a text file with a procedure (e.g. an OES signal SOP).
2. Cleans the text and splits it into smaller pieces (**chunks**).
3. Creates simple **embeddings** (number vectors based on keywords).
4. Compares the user's question with chunks and picks the best matches.
5. Filters out chunks with a low **relevance score**.
6. Builds **context** and an **answer** only from good chunks.
7. Generates a **checklist** from numbered procedure steps.
8. Validates the checklist (format, length, duplicates).

If the document does not contain good enough context, the program responds with:

> *I don't know based on the provided document...*

---

## Requirements

- Python **3.10+** (also works on 3.14)
- **No external libraries** — only Python's standard library

---

## How to run

1. Clone the repository:

```bash
git clone <your-repo-url>
cd AI_SOP_Assistant
```

2. Run the program:

```bash
python main.py
```

3. The output will appear in the terminal.

---

## Project structure

```
AI_SOP_Assistant/
├── main.py                 # Main file — connects all pipeline steps
├── app/
│   ├── loaders.py          # Loads a .txt file
│   ├── text_utils.py       # Cleans text (empty lines, etc.)
│   ├── chunking.py         # Splits text into chunks
│   ├── embeddings.py       # Simple keyword-based embeddings
│   ├── retrieval.py        # Ranks chunks by similarity
│   ├── answering.py        # Builds context and answer
│   ├── checklist.py        # Creates a checklist from steps 1., 2., 3. ...
│   └── validation.py       # Validates the checklist
└── documents/
    └── sop_oes.txt         # Sample SOP document
```

---

## How the pipeline works (step by step)

```
SOP document
    ↓
load_document()              → load the file
    ↓
clean_text()                 → remove empty lines
    ↓
chunk_text()                 → split into 300-character pieces
    ↓
create_simple_embedding()    → number vector for each chunk
    ↓
rank_chunks_by_similarity()  → which chunks match the question?
    ↓
get_top_k_chunks()           → pick the TOP 3 best chunks
    ↓
relevance filter             → only chunks with score >= threshold
    ↓
build_context()              → source text for the answer
build_source_list()          → list of sources
    ↓
generate_checlist_from_text() → checklist from steps
validate_checklist_items()    → clean checklist
    ↓
create_grounded_answer()     → answer or "I don't know..."
```

---

## Settings in `main.py`

You can change these values at the top of `main.py`:

| Constant | Default | What it does |
|---|---|---|
| `DOCUMENT_PATH` | `documents/sop_oes.txt` | Path to the document |
| `CHUNK_SIZE` | `300` | Size of one chunk (characters) |
| `CHUNK_OVERLAP` | `50` | How many characters overlap between chunks |
| `TOP_K` | `3` | How many best chunks to retrieve |
| `MINIMUM_RELEVANCE_SCORE` | `4` | Minimum score for a chunk to be used |

**Note:** with the current test question, the best chunks have a score of **3**, but the threshold is **4** — so the program correctly says *"I don't know"*. To see a full answer and checklist, set e.g. `MINIMUM_RELEVANCE_SCORE = 3`.

You can also change the test question in `main.py` (the line with `question = ...`).

---

## How embeddings work (simplified)

This is **not** OpenAI or a real language model. It is a simple version for learning.

The program uses a list of keywords:

`oes`, `signal`, `fiber`, `alarm`, `safety`, `test`

For each text, it counts how many times each keyword appears. Example:

- question *"What is the replacement cost of the OES sensor?"* → `[1, 0, 0, 0, 0, 0]`
- a chunk about OES → higher score because it has more matching words

Then `calculate_similarity()` multiplies the vectors and sums the result — the higher the score, the more similar they are.

---

## Checklist — what happens

1. **`generate_checlist_from_text()`** looks for lines in the format `1.`, `2.`, `3.` ...
2. Removes the number and adds `[ ]` at the start.
3. **`validate_checklist_items()`** checks:
   - does it start with `[ ] `?
   - is the text at least 15 characters long?
   - does it end with a period `.`?
   - are there any duplicates?

Example output:

```
[ ] Confirm that the tool is in a safe state.
[ ] Check if there are any active alarms on the tool.
[ ] Inspect the OES fiber connection.
```

The checklist is built **only** from relevant chunks (after the score filter).

---

## Sample document

`documents/sop_oes.txt` contains the **OES Signal Troubleshooting SOP** — what to do when the OES signal is unstable after maintenance.

---

## What this project **does not do yet**

This is intentionally a simple learning project:

- no real LLM (ChatGPT, etc.)
- no API or web interface
- no vector database
- embeddings based on only 6 keywords
- step numbering works only for the `1.` format (not `10.` or `1)`)

---

## Ideas for future improvements

- [ ] Connect a real embedding model
- [ ] Integrate an LLM to generate answers
- [ ] CLI interface with a custom question
- [ ] Load multiple SOP documents
- [ ] Export checklist to a `.txt` or `.md` file
- [ ] Support steps like `10.`, `11.`, etc.

---

## Project status

Work in progress — I am building this step by step to understand RAG from the ground up.

If something does not work or you have an idea for improvement, feel free to open an issue or PR.

---

## License

Educational project — free to use for learning and modify as you like.
