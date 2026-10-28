# Investment Research & Risk Assistant

A Python RAG agent for investment research, combining document retrieval, tool calling and automated evaluation. Built with LangChain and LangGraph, containerized with Docker and served through a FastAPI REST API.

**Tech:** Python · RAG · LLM Agents · Tool Use · LangChain · LangGraph · Chroma · FastAPI · Docker · Evaluation

## Overview

This project is a question answering agent over a set of investment and risk documents. Instead of answering from the model's own memory, it retrieves relevant passages from a document collection and reasons over them, and it can run exact financial calculations through a dedicated tool. It is instructed to decline requests outside its supported scope (personalized investment advice, market predictions, real time data and off topic questions) rather than making something up.

The focus is not only on building the agent, but on evaluating it systematically. A 30 question test set measures conceptual answer correctness, numerical calculation results and abstention behaviour. The agent is packaged as a container and exposed over HTTP, so it can be run anywhere with a single command.

## How it works

The system has two stages.

**1. Ingestion (`src/ingest.py`)**, run once to build the knowledge base:

- Loads the PDF documents and removes print headers and footers (dates, URLs, page markers) with regex.
- Splits the text into overlapping chunks (1000 characters, 150 overlap), which helps preserve context across chunk boundaries.
- Embeds each chunk into a vector with a local embedding model and stores the vectors in a Chroma vector database on disk.

**2. The agent (`src/agent.py`)**, answers questions at runtime:

- A ReAct agent (built with `create_react_agent`) decides, per question, which tool to use.
- **`search_investment_documents`** retrieves the most relevant chunks from Chroma (the RAG tool) for conceptual questions.
- **`compound_interest`** is a deterministic Python function for compound growth calculations.
- A system prompt constrains the agent to answer only from tool results, and to abstain (prefixing its reply with `ABSTAIN:`) on unsupported requests.

`src/rag.py` contains the plain RAG pipeline (retrieval and generation with sources) without the agent layer, kept as a simpler reference.

The agent is wrapped by a small API layer (`src/api.py`) so it can be queried over HTTP instead of only from the command line.

## API

The service is built with FastAPI and exposes two endpoints:

| Method | Endpoint  | Description                                        |
| ------ | --------- | -------------------------------------------------- |
| GET    | `/health` | Health check. Returns `{"status": "ok"}`.          |
| POST   | `/ask`    | Sends a question to the agent and returns the answer. |

`POST /ask` request body:

```json
{ "question": "What is risk?" }
```

Response:

```json
{
  "question": "What is risk?",
  "answer": "In finance, risk refers to the degree of uncertainty ..."
}
```

Interactive documentation (Swagger UI) is available at `http://localhost:8000/docs` once the service is running.

## Design decisions

A few choices worth explaining:

- **Local embeddings instead of an API.** Embedding 140+ chunks hit the free API's rate limit. Using a local embedding model (`all-MiniLM-L6-v2`) removed the embedding API quota constraint and let documents be embedded locally. The assistant still uses Gemini for generation, so it requires API access to answer.
- **A calculator tool instead of the LLM doing arithmetic.** LLMs are unreliable at exact arithmetic. Financial figures are calculated deterministically in Python, which reduces the risk of arithmetic errors from the model; correctness still depends on the formula and its inputs. The LLM only decides *when* to calculate and with which values.
- **Evaluating each answer type differently.** There is no single metric. Conceptual answers are judged by an LLM as a judge (meaning, not literal text match); calculations are verified numerically in Python within a tolerance; abstention is checked with an explicit `ABSTAIN:` marker. This came from a real failure: the first evaluator used literal string matching and reported false negatives.
- **CPU only PyTorch in the image.** The default PyTorch build pulls over 1 GB of CUDA GPU libraries that this service never uses, since embeddings run on CPU. The Docker image installs the CPU only build of PyTorch, which keeps the image smaller and the build faster.
- **Prebuilt index baked into the image, secrets injected at runtime.** The Chroma vector database is copied into the image so the container does not re-embed on startup. The `GOOGLE_API_KEY` is never baked into the image; it is passed when the container starts, and `.env` is excluded through `.dockerignore`.

## Evaluation

The evaluation (`evaluation/`) runs a 30 question test set across three categories and checks each with the appropriate method.

| Category      | Questions | Passed |
| ------------- | --------- | ------ |
| Concept       | 17        | 17/17  |
| Calculation   | 7         | 7/7    |
| Out of scope  | 6         | 6/6    |
| **Overall**   | **30**    | **30/30** |

The current run reaches a 100% pass rate on this test set. This is an initial benchmark, not a guarantee of general reliability: the set is small, it was written for this project, and each category is checked by a different method. The out of scope questions exist to test that the agent abstains instead of hallucinating, which is the hardest and most important property for a reliable assistant.

Reaching this took iteration. An early run scored 90%. Inspecting the actual outputs showed the failures were mostly in the evaluator itself (literal string matching rejected some valid refusals) and in the agent's abstention wording. Both were diagnosed from the real responses and fixed, the evaluator by switching to an explicit abstention marker.

## Setup

Requires Python 3.12 and a Google Gemini API key.

```bash
# 1. Clone and enter the project
git clone https://github.com/ouassim-elkoutbi/rag-agent-investment-research.git
cd rag-agent-investment-research

# 2. Create a virtual environment and install dependencies
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Add your API key
cp .env.example .env
# then edit .env and set GOOGLE_API_KEY
```

## Usage

### From the command line

```bash
# Build the vector database from the documents (run once)
python src/ingest.py

# Ask the agent a question
python src/agent.py

# Run the evaluation suite
python evaluation/evaluate.py
```

### As an API (local)

```bash
# With the virtual environment active
uvicorn api:app --app-dir src --port 8000
```

Then open `http://localhost:8000/docs` to try it, or query it directly:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is diversification?"}'
```

### With Docker

```bash
# Build the vector database first if it does not exist (creates chroma_db/)
python src/ingest.py

# Build the image
docker build -t rag-agent .

# Run the container (reads GOOGLE_API_KEY from .env at runtime)
docker run -p 8000:8000 --env-file .env rag-agent
```

The API is then available at `http://localhost:8000` exactly as above. The prebuilt Chroma index is included in the image, so the container is ready to answer on startup.

## Deployment

The service runs as a container, so it deploys unchanged on any Docker host. It has been deployed on an AWS EC2 instance (Ubuntu, arm64 / Graviton), with the image built natively for the instance architecture. The `GOOGLE_API_KEY` is injected at runtime with `--env-file`, so no credentials are baked into the image, and the container runs detached with a restart policy so it comes back up automatically after a reboot.



## Project structure

```
.
├── documents/              # Source PDFs (investor.gov investing and risk guides)
├── chroma_db/              # Prebuilt Chroma vector database (baked into the image)
├── src/
│   ├── ingest.py           # Load, clean, chunk, embed and store documents
│   ├── tools.py            # The two agent tools (document search + calculator)
│   ├── agent.py            # ReAct agent that selects between the tools
│   ├── rag.py              # Plain RAG pipeline (reference, no agent)
│   └── api.py              # FastAPI layer exposing /ask and /health
├── evaluation/
│   ├── test_questions.py   # 30 question evaluation dataset
│   └── evaluate.py         # Runs the agent and scores each answer type
├── Dockerfile              # Container definition (CPU only PyTorch)
├── .dockerignore
├── requirements.txt
└── .env.example
```

## Limitations and future work

- The knowledge base is limited to the included documents; it does not cover real time market data by design.
- Abstention relies on the agent following its system prompt. The marker check confirms the agent declined, but does not by itself verify that the reply avoids giving unsupported advice afterwards. A production system would represent abstention as an explicit state rather than inferring it from text.
- The LLM as a judge is useful but not infallible; it would ideally be validated against human labelled examples.
- Retrieval parameters (chunk size, overlap, number of retrieved chunks) are fixed; a larger study could tune them against the evaluation set.

Created by **Ouassim El Koutbi**, Computer Engineering student (Universitat de València / TH Ingolstadt).