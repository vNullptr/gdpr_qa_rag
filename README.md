# GDPR Q&A

> Grounded document Q&A over the EU General Data Protection Regulation (GDPR). Answers will be derived only from retrieved source text, will cite the chunks they used, and will be evaluated with RAGAS rather than judged by feel.

**Status:** 🚧 In development.

---

## What this is

A retrieval-augmented question-answering service over the GDPR legal text. The focus of the project is the parts that usually get skipped: deliberate chunking, measured retrieval quality, citation fidelity, and a real evaluation harness. A user will be able to ask a question and get an answer that is grounded in the regulation, shows its sources, and responds with *"I don't know based on the provided documents"* when the answer is not present in the corpus.

## Why it's structured this way

Two separate pipelines that will share only a persisted vector store on disk:

- **Ingestion**, a batch job run when the corpus changes: load, clean, chunk (with metadata), embed, and write to the vector store. It is not a running service.
- **Query**, the live path: embed the question, retrieve the top-k chunks, build a grounded prompt, and answer with citations.

The retrieval and answer logic will live in plain functions under `rag/`. The HTTP API will be a thin wrapper in `api/` that calls that logic, so the core never needs to know it is being served over HTTP, and the same logic can later be driven from a CLI, the tests, or an agent.

## Architecture

```
ingestion (batch)            query (live)
  load docs                    question
  clean                          |
  chunk + metadata               v
  embed                     embed query
    |                            |
    v                            v
 vector store  ---read--->  retrieve top-k
  (Chroma, on disk)              |
                                 v
                          grounded prompt -> LLM
                                 |
                                 v
                          answer + citations
                                 |
                                 v
                       FastAPI  POST /ask  -->  client
```

## Tech stack

- **Orchestration:** LangChain
- **Vector store:** ChromaDB (local, on disk)
- **Embeddings:** OpenAI `text-embedding-3-small`, swappable behind one interface
- **LLM:** configurable chat model
- **Evaluation:** RAGAS over a hand-written gold question set
- **Tracing:** LangSmith
- **API:** FastAPI and Uvicorn
- **Config:** pydantic-settings (typed settings from `.env`)

## Project layout

```
grounded-rag-qa/
  rag/
    config.py          # typed Settings (pydantic-settings)
    ingestion/         # batch: load, chunk, embed, write
    query/             # retrieve + answer logic (pipeline.py)
  api/                 # FastAPI app, thin wrapper over rag.query
  eval/                # gold question set + RAGAS scripts
  tests/               # pytest
  documents/           # contains the source document(s)
  .env.example
  requirements.txt
  README.md
```

## Getting started

> Still working on skeleton...

### Run the tests

Run `pytest` to check test cases.
> Current ones are placeholders and just check stubbed hardcoded answers 

## Configuration

All knobs will live in `.env` (see `.env.example`) and load as a typed `Settings` object.

## Evaluation

Quality will be measured. A hand-written gold set of question and ground-truth pairs (including deliberately unanswerable questions) will be scored with RAGAS on:

- **Faithfulness:** is the answer supported by the retrieved context?
- **Answer relevancy:** does it actually address the question?
- **Context precision and recall:** did retrieval surface the right chunks?

> _Results table to be added once the eval harness is built (T6)._
