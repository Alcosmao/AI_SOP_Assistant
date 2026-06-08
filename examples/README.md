# Examples

Sample outputs from the project. I added these so you can see what the pipeline does **without running it yourself** or paying for OpenAI API calls.

These examples are from the **current OpenAI version** of the project:
- OpenAI embeddings (`text-embedding-3-small`)
- Cosine similarity scores (0–1)
- OpenAI Chat answer (`gpt-5.4-mini`)
- `TOP_K = 5`, relevance threshold `0.71`

---

## Files in this folder

| File | What it shows |
|---|---|
| `run_openai_success_output.txt` | Good question → chunks found → LLM answer + checklist |
| `run_openai_i_dont_know_output.txt` | Off-topic question → no relevant chunks → "I don't know" |
| `validated_checklist.txt` | Checklist only (6 items from success run) |
| `checklist_report.txt` | Same checklist saved to `reports/checklist.txt` |

---

## Example 1 — Success (OpenAI RAG works)

**Question:** multi-topic OES question from `input/question.txt`  
(fiber troubleshooting + safety + escalation)

**Settings when captured:**
- 15 chunks from the longer SOP
- `TOP_K = 5`
- `MINIMUM_RELEVANCE_SCORE = 0.71`

**What happened:**
- Best scores: ~0.78, 0.73, 0.71, 0.71
- Worst chunk (pricing / out of scope): ~0.37
- 4 chunks passed the relevance filter
- Checklist: 6 validated items
- LLM answered fiber + safety steps from the SOP
- Escalation contact was **not** in the retrieved chunks → LLM honestly said *"I don't know"* for that part (good grounding)

See: `run_openai_success_output.txt`

---

## Example 2 — "I don't know" (safety works)

**Question:** from `input/question_off_topic.txt`  
*"What is the replacement cost and part number for OES sensor... purchase order..."*

**What happened:**
- Best chunk score only ~0.49 (below 0.71 threshold)
- `Has relevant context: False`
- No sources, no checklist, no report file
- Answer: *"I don't know based on the provided document..."*
- LLM was **not called** (Python returns this before OpenAI Chat)

This is correct — the SOP says pricing is out of scope.

See: `run_openai_i_dont_know_output.txt`

---

## How to reproduce

**Success example:**
1. Put the multi-topic question in `input/question.txt` (see current file in repo)
2. Make sure `.env` has `OPENAI_API_KEY`
3. Run `python main.py`

**"I don't know" example:**
1. Copy text from `input/question_off_topic.txt` into `input/question.txt`
2. Run `python main.py`

---

## Old examples (removed)

The previous files `run_success_output.txt` and `run_i_dont_know_output.txt` were from the **old keyword embedding version** (scores like 3 and 5). They are outdated and were replaced by the `run_openai_*` files above.
