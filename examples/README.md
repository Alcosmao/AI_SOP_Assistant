# Examples

Sample outputs from the AI SOP Assistant pipeline. Use these to see what the project produces without running it yourself.

---

## Files

| File | What it shows |
|---|---|
| `run_i_dont_know_output.txt` | Default `main.py` run — question not answered well enough (relevance threshold blocks answer) |
| `run_success_output.txt` | Successful run — good question, chunks pass filter, answer + checklist generated |
| `validated_checklist.txt` | Final checklist only (7 validated steps from the success example) |

---

## Example 1: "I don't know" (default run)

**Question:** `What is the replacement cost of the OES sensor?`

**Settings:** `MINIMUM_RELEVANCE_SCORE = 4` (as in `main.py`)

**What happens:**
- Retrieval finds OES-related chunks (score 3), but they are below the threshold
- No sources, no checklist, no grounded answer
- System correctly refuses: *"I don't know based on the provided document..."*

This shows **grounding + safety** — the pipeline does not invent an answer when context is weak or off-topic.

See: `run_i_dont_know_output.txt`

---

## Example 2: Successful RAG run

**Question:** `What should I do when the OES signal is unstable after maintenance?`

**Settings:** `MINIMUM_RELEVANCE_SCORE = 3` (lower threshold for demo)

**What happens:**
- Chunks score 5, 5, 3 — all pass the filter
- Sources listed with similarity scores
- Checklist built from numbered procedure steps (7 items after validation)
- Grounded answer draft built from retrieved context only

See: `run_success_output.txt` and `validated_checklist.txt`

---

## How to reproduce

**Default output (Example 1):**
```bash
python main.py
```

**Success output (Example 2):**
Change in `main.py`:
- `MINIMUM_RELEVANCE_SCORE = 3`
- `question = "What should I do when the OES signal is unstable after maintenance?"`

Then run `python main.py` again.
