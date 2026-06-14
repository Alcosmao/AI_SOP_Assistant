# AI SOP Assistant

A learning project for **RAG** (Retrieval-Augmented Generation) on technical SOP documents.

I built this step by step to understand how document Q&A works: load a file, split it into chunks, find the best matching parts for a question, and generate a **grounded answer** using OpenAI — or say *"I don't know"* when the document is not good enough.

It runs two ways: in the **terminal** (reads the question from a file) and as a **REST API** built with **FastAPI** (send a question over HTTP, get JSON back). Both use the same RAG pipeline under the hood.

---

## Demo

> The flow: `GET /documents` to see what is available → `POST /ask` with a
> question and a `document_name` → grounded answer + sources + checklist.

<!--
TODO: record a short clip and save it as docs/demo.gif, then uncomment the line below.
Suggested clip: GET /documents -> pick a document -> POST /ask -> answer + checklist.

![Demo: list documents, ask a question, get a grounded answer](docs/demo.gif)
-->
_Demo GIF coming soon._

---

## What it does

1. Loads the chosen document through the storage layer (e.g. `sop_oes.txt`)
2. Reads your question (from `input/question.txt` in the CLI, or the request in the API)
3. Splits the document into **chunks** (300 chars, 50 overlap)
4. Creates **OpenAI embeddings** for each chunk and the question
5. Ranks chunks with **cosine similarity** (score 0–1)
6. Keeps only chunks above the relevance threshold
7. Sends the best chunks to **OpenAI Chat** for a grounded answer
8. Builds a **checklist** from numbered SOP steps
9. Saves the checklist to `reports/checklist.txt`

If context is too weak → *"I don't know based on the provided document..."*

---

## Requirements

- Python **3.10+**
- OpenAI API key

Install packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root. The easiest way is to copy the
provided template and fill in your own values:

```bash
copy .env.example .env   # Windows
# cp .env.example .env   # macOS / Linux
```

Minimum you need:

```env
OPENAI_API_KEY=your-key-here
```

The `.env.example` file also lists the storage settings (see
[Storage abstraction](#storage-abstraction) below). Your real `.env` is
gitignored and must never be committed.

Models used (in `app/config.py`):
- Embeddings: `text-embedding-3-small` (1536 dimensions)
- Chat: `gpt-5.4-mini`

---

## How to run

1. Clone the repo and install requirements (see above)
2. Add your API key to `.env`
3. Edit `input/question.txt` with your question
4. Run:

```bash
python main.py
```

5. Check the terminal output
6. If a checklist was created, see `reports/checklist.txt`

**Try an off-topic question:** copy text from `input/question_off_topic.txt` into `input/question.txt` and run again.

---

## Run as an API (FastAPI)

The same pipeline is also exposed as a REST API. Start the server:

```bash
python -m uvicorn api:app --reload
```

> On Windows, use `python -m uvicorn ...` (the bare `uvicorn` command may not be on PATH).

Then open the interactive docs (Swagger UI):

```
http://127.0.0.1:8000/docs
```

### Endpoints

| Method | Path | What it does |
|---|---|---|
| `GET` | `/health` | Health check → `{"status": "ok"}` |
| `GET` | `/documents` | List the document names available in the current storage |
| `POST` | `/ask` | Ask a question **about a chosen document**, get a grounded answer + sources + checklist |

### Choosing a document (important)

The app can hold **several independent documents** (knowledge bases). A request
has **two separate inputs**:

- `document_name` — **which** document to search in (the knowledge base)
- `question` — **what** you want to know

The system answers **only** from the chosen document. If you ask something that
the selected document does not cover, you get an honest *"I don't know"* — this
is intentional (grounding), not a bug.

> The repo ships with two **unrelated** troubleshooting documents on purpose
> (e.g. an OES fiber SOP and a network connectivity SOP). This demonstrates that
> documents are independent: pick one, ask a question relevant to it. Asking an
> OES question against the network document will correctly return *"I don't know"*.

Typical flow: call `GET /documents` to see what is available, pick one, then
send it with your question to `POST /ask`.

### Example request

`POST /ask` with body:

```json
{
  "question": "How do I inspect and reseat the OES fiber connector?",
  "document_name": "sop_oes.txt"
}
```

Example response: see [examples/api_response.json](examples/api_response.json).

### Error handling

| Situation | Status code |
|---|---|
| Question is empty (`""`) or `document_name` missing | `422` (Pydantic validation) |
| Question is only whitespace | `400` Bad Request |
| Chosen document not found in storage | `404` Not Found |
| Valid question + existing document | `200` OK |

> `POST /ask` calls OpenAI (embeddings + chat), so a response takes a few seconds. You cannot test `POST /ask` by typing the URL in a browser — a browser address bar sends a `GET`. Use Swagger `/docs` or a tool like `curl` / Postman.

---

## Storage abstraction

The app does **not** read documents from a hardcoded file path anymore. Instead
it talks to a small **storage layer**, so the same pipeline can read documents
from different places without changing any logic.

This is a common, beginner-friendly design pattern (often called *strategy* +
*factory*). It makes the project **cloud-ready** and easy to extend.

**How it works (plain words):**

- `app/storage/base.py` — defines *what* a storage must look like (one method:
  `read_document(name) -> str | None`). It is just a contract.
- `app/storage/local_storage.py` — reads documents from the **local filesystem**.
- `app/storage/blob_storage.py` — reads documents from **Azure Blob Storage**
  (or the **Azurite** local emulator). The Azure library is imported lazily, so
  local mode works without installing it.
- `app/storage/factory.py` — `get_storage()` picks the right backend based on
  the `STORAGE_MODE` setting.

```
run_rag_pipeline()
    -> get_storage()        # factory picks backend from STORAGE_MODE
    -> storage.read_document("sop_oes.txt")
                            # local: reads documents/sop_oes.txt
                            # blob:  reads blob from the container
```

The pipeline only asks for a document **by name** — it does not know (or care)
whether the file comes from disk or the cloud.

### Storage settings (in `.env`)

| Variable | What it does | Example |
|---|---|---|
| `STORAGE_MODE` | Which backend to use: `local` or `blob` | `local` |
| `DOCUMENTS_PATH` | Local folder with documents (local mode) | `documents` |
| `AZURE_STORAGE_CONNECTION_STRING` | Connection string (blob mode) | `UseDevelopmentStorage=true` |
| `AZURE_STORAGE_CONTAINER_NAME` | Container name (blob mode) | `documents` |

### Run in local mode (default)

Nothing special to do — `STORAGE_MODE` defaults to `local`:

```bash
python main.py
```

It reads `documents/sop_oes.txt` exactly like before.

### Run in blob mode with Azurite (optional, no real Azure needed)

[Azurite](https://learn.microsoft.com/azure/storage/common/storage-use-azurite)
is a free **local emulator** of Azure Storage. It lets you test blob mode on your
own machine **without creating any real Azure resources or paying anything**.

1. Install the Azure library (only needed for blob mode):

```bash
pip install azure-storage-blob
```

2. Start Azurite (needs Node.js or Docker):

```bash
npm install -g azurite && azurite
# or with Docker:
# docker run -p 10000:10000 mcr.microsoft.com/azure-storage/azurite
```

3. In `.env` switch to blob mode:

```env
STORAGE_MODE=blob
AZURE_STORAGE_CONNECTION_STRING=UseDevelopmentStorage=true
AZURE_STORAGE_CONTAINER_NAME=documents
```

4. Upload your SOP file into the `documents` container, then run `python main.py`.
   The result is the same — only the source of the file changed.

> Real Azure Blob Storage would work the same way: just use a real connection
> string instead of the Azurite one. **No code changes needed.**

---

## Running the tests

The project has **unit tests** for the deterministic logic (storage, cosine
similarity, ranking, chunking, text cleaning, checklist building/validation).
They do **not** call OpenAI, so they are fast and free.

```bash
pip install pytest
python -m pytest -q
```

Expected: all tests pass (currently 22). The OpenAI-dependent parts
(embeddings, chat answer, full pipeline) are intentionally not unit-tested to
avoid paid API calls.

---

## Project structure

```
AI_SOP_Assistant/
├── main.py                   # Terminal entry point (CLI)
├── api.py                    # FastAPI app (REST API)
├── requirements.txt
├── .env                      # API key + storage settings (not in git)
├── .env.example              # Template for .env (placeholders only)
├── app/
│   ├── config.py             # API key + model names + storage settings
│   ├── pipeline.py           # run_rag_pipeline() — shared RAG logic (CLI + API)
│   ├── schemas.py            # Pydantic models (AskRequest, AskResponse)
│   ├── loaders.py            # Load the question file (CLI)
│   ├── text_utils.py         # Clean text
│   ├── chunking.py           # Split text into chunks
│   ├── embeddings.py         # Old keyword embeddings (learning only)
│   ├── openai_embeddings.py  # Real OpenAI embeddings
│   ├── retrieval.py          # Cosine similarity + ranking
│   ├── answering.py          # Build context, call LLM answer
│   ├── openai_answer.py      # OpenAI Chat API for grounded answer
│   ├── checklist.py          # Checklist from numbered steps
│   ├── validation.py         # Validate checklist items
│   ├── export.py             # Save checklist to reports/
│   └── storage/              # Storage abstraction (local / blob)
│       ├── base.py           # DocumentStorage contract (interface)
│       ├── local_storage.py  # Read from local filesystem
│       ├── blob_storage.py   # Read from Azure Blob / Azurite
│       └── factory.py        # get_storage() picks backend
├── documents/                # Your private documents (gitignored)
│   └── .gitkeep              # Keeps the empty folder in git
├── input/
│   ├── question.txt          # Your question (used on each run)
│   └── question_off_topic.txt
├── reports/                  # Generated checklist (gitignored)
├── examples/                 # Sample outputs + safe sample SOP for portfolio
│   └── sample_sop.txt        # Fake SOP, safe to share publicly
└── tests/                    # pytest functionality tests (no OpenAI calls)
```

---

## Pipeline (simple view)

```
SOP file + question file
    ↓
chunk document (15 chunks from current SOP)
    ↓
OpenAI embeddings (text → 1536 numbers)
    ↓
cosine similarity (question vs each chunk)
    ↓
top 5 chunks → filter by score >= 0.65
    ↓
build context + sources
    ↓
OpenAI Chat → grounded answer
    ↓
checklist + export to reports/checklist.txt
```

---

## Settings

The pipeline constants live in `app/pipeline.py` (shared by the CLI and the API). The question file path lives in `main.py` (CLI only).

| Constant | Where | Current value | What it does |
|---|---|---|---|
| `DOCUMENT_NAME` | `main.py` | `sop_oes.txt` | Which document the CLI analyzes (the API takes it from the request instead) |
| `QUESTION_PATH` | `main.py` | `input/question.txt` | Question file (CLI) |
| `CHUNK_SIZE` | `app/pipeline.py` | `300` | Chunk size in characters |
| `CHUNK_OVERLAP` | `app/pipeline.py` | `50` | Overlap between chunks |
| `TOP_K` | `app/pipeline.py` | `5` | How many best chunks to retrieve |
| `MINIMUM_RELEVANCE_SCORE` | `app/pipeline.py` | `0.65` | Min cosine score to use a chunk |
| `REPORTS_PATH` | `app/pipeline.py` | `reports` | Checklist export folder |

**Note on scores:** with OpenAI embeddings, similarity scores are between **0 and 1** (not 3 or 5 like the old keyword version). Higher = more similar meaning.

**Note on TOP_K:** I use `5` because my question has multiple topics. With `TOP_K = 3` the LLM sometimes missed the fiber troubleshooting chunk.

---

## How retrieval works (short)

- Each text becomes a vector of **1536 numbers** (embedding)
- `calculate_cosine_similarity()` compares question vs chunk
- Example from testing: similar texts ~0.68, unrelated texts ~0.05
- Only chunks above the threshold go to the LLM

The old `app/embeddings.py` (6 keywords) is kept on purpose as a **legacy /
learning** file (it has a comment saying so at the top). It is **not used** in
the pipeline anymore — the project moved to real semantic embeddings in
`app/openai_embeddings.py`, which understand meaning instead of counting words.

---

## Examples folder

Sample outputs from the **current OpenAI version** — no API key needed to preview:

| File | What it shows |
|---|---|
| [examples/run_openai_success_output.txt](examples/run_openai_success_output.txt) | Good question → cosine scores, LLM answer, checklist |
| [examples/run_openai_i_dont_know_output.txt](examples/run_openai_i_dont_know_output.txt) | Off-topic question → "I don't know" |
| [examples/validated_checklist.txt](examples/validated_checklist.txt) | Checklist only (6 items) |
| [examples/checklist_report.txt](examples/checklist_report.txt) | Exported checklist sample |
| [examples/api_response.json](examples/api_response.json) | Sample `POST /ask` JSON response from the API |
| [examples/README.md](examples/README.md) | Explains each example |

---

## What works now

- [x] Full RAG pipeline
- [x] OpenAI embeddings
- [x] Cosine similarity
- [x] Relevance filtering
- [x] OpenAI grounded answers
- [x] Checklist generation + export
- [x] Custom question from `input/question.txt`
- [x] Examples folder
- [x] FastAPI REST API (`GET /health`, `POST /ask`) with error handling

## What I still want to add

- [ ] Support step numbers like `10.`, `11.`
- [ ] Load multiple SOP files
- [ ] Deploy to cloud
- [x] FastAPI endpoint
- [x] Updated examples/ with OpenAI run outputs

---

## Project status

Learning project — built step by step with AI-assisted coding while studying RAG, embeddings, the OpenAI API, and FastAPI. I can explain the pipeline, the API layer, and each module.

---

## License

Educational project — free to use for learning.
