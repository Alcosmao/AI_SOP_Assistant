# AI SOP Assistant

A learning project for **RAG** (Retrieval-Augmented Generation) on technical SOP documents.

I built this step by step to understand how document Q&A works: load a file, split it into chunks, find the best matching parts for a question, and generate a **grounded answer** using OpenAI — or say *"I don't know"* when the document is not good enough.

This is not a production app yet. It runs in the terminal and reads the question from a file.

---

## What it does

1. Loads an SOP text file (`documents/sop_oes.txt`)
2. Reads your question from `input/question.txt`
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

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your-key-here
```

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

## Project structure

```
AI_SOP_Assistant/
├── main.py                   # Runs the full pipeline
├── requirements.txt
├── .env                      # API key (not in git)
├── app/
│   ├── config.py             # API key + model names
│   ├── loaders.py            # Load document and question files
│   ├── text_utils.py         # Clean text
│   ├── chunking.py           # Split text into chunks
│   ├── embeddings.py         # Old keyword embeddings (learning only)
│   ├── openai_embeddings.py  # Real OpenAI embeddings
│   ├── retrieval.py          # Cosine similarity + ranking
│   ├── answering.py          # Build context, call LLM answer
│   ├── openai_answer.py      # OpenAI Chat API for grounded answer
│   ├── checklist.py          # Checklist from numbered steps
│   ├── validation.py         # Validate checklist items
│   └── export.py               # Save checklist to reports/
├── documents/
│   └── sop_oes.txt           # OES troubleshooting SOP (longer demo doc)
├── input/
│   ├── question.txt          # Your question (used on each run)
│   └── question_off_topic.txt
├── reports/                  # Generated checklist (gitignored)
└── examples/                 # Sample outputs for portfolio
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
top 5 chunks → filter by score >= 0.71
    ↓
build context + sources
    ↓
OpenAI Chat → grounded answer
    ↓
checklist + export to reports/checklist.txt
```

---

## Settings in `main.py`

| Constant | Current value | What it does |
|---|---|---|
| `DOCUMENT_PATH` | `documents/sop_oes.txt` | SOP file |
| `QUESTION_PATH` | `input/question.txt` | Question file |
| `CHUNK_SIZE` | `300` | Chunk size in characters |
| `CHUNK_OVERLAP` | `50` | Overlap between chunks |
| `TOP_K` | `5` | How many best chunks to retrieve |
| `MINIMUM_RELEVANCE_SCORE` | `0.71` | Min cosine score to use a chunk |
| `REPORTS_PATH` | `reports` | Checklist export folder |

**Note on scores:** with OpenAI embeddings, similarity scores are between **0 and 1** (not 3 or 5 like the old keyword version). Higher = more similar meaning.

**Note on TOP_K:** I use `5` because my question has multiple topics. With `TOP_K = 3` the LLM sometimes missed the fiber troubleshooting chunk.

---

## How retrieval works (short)

- Each text becomes a vector of **1536 numbers** (embedding)
- `calculate_cosine_similarity()` compares question vs chunk
- Example from testing: similar texts ~0.68, unrelated texts ~0.05
- Only chunks above the threshold go to the LLM

The old `app/embeddings.py` (6 keywords) is still in the project from early learning steps but is **not used** in `main.py` anymore.

---

## Examples folder

Sample outputs from the **current OpenAI version** — no API key needed to preview:

| File | What it shows |
|---|---|
| [examples/run_openai_success_output.txt](examples/run_openai_success_output.txt) | Good question → cosine scores, LLM answer, checklist |
| [examples/run_openai_i_dont_know_output.txt](examples/run_openai_i_dont_know_output.txt) | Off-topic question → "I don't know" |
| [examples/validated_checklist.txt](examples/validated_checklist.txt) | Checklist only (6 items) |
| [examples/checklist_report.txt](examples/checklist_report.txt) | Exported checklist sample |
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

## What I still want to add

- [ ] FastAPI endpoint
- [ ] Support step numbers like `10.`, `11.`
- [ ] Load multiple SOP files
- [ ] Deploy to cloud
- [x] Updated examples/ with OpenAI run outputs

---

## Project status

Learning project — built step by step with AI-assisted coding while studying RAG, embeddings, and OpenAI API. I can explain the pipeline and each module.

---

## License

Educational project — free to use for learning.
