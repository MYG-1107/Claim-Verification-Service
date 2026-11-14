# Claim Verification Service

An evidence-first FastAPI microservice that indexes trusted reference text in a local ChromaDB vector store and verifies incoming claims against the closest retrieved source excerpt.

## Features

- Strict Pydantic request and response schemas.
- CPU-friendly `all-MiniLM-L6-v2` sentence embeddings.
- Persistent local ChromaDB storage under `data/chroma_db`.
- Deterministic `VERIFIED`/`UNVERIFIED` results with a confidence score and source excerpt.
- Docker and GitHub Codespaces support.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The interactive API is available at `http://localhost:8000/docs`.

## API examples

```bash
curl -X POST http://localhost:8000/api/v1/ingest \
  -H 'content-type: application/json' \
  -d '{"document_id":"annual-report","content":"Revenue grew by 15 percent in Q3."}'

curl -X POST http://localhost:8000/api/v1/verify \
  -H 'content-type: application/json' \
  -d '{"claim":"Revenue grew by 15 percent in Q3."}'
```

Configuration can be supplied with `CHROMA_PATH`, `CHROMA_COLLECTION`,
`EMBEDDING_MODEL`, `VERIFICATION_THRESHOLD`, and `MAX_CHUNK_CHARACTERS`.

## Test

```bash
pytest
```

See [`architecture/README.md`](architecture/README.md) for the architecture
design set, including component, sequence, deployment, and data-flow diagrams.
