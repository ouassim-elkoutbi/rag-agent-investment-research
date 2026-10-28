import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from agent import ask_raw

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Investment Research & Risk Assistant",
    version="0.1.0",
)


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


class AskResponse(BaseModel):
    question: str
    answer: str


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    try:
        answer = ask_raw(request.question)
        return AskResponse(question=request.question, answer=answer)
    except Exception as exc:
        logger.exception("Failed to process agent request")
        raise HTTPException(
            status_code=500,
            detail="The assistant could not process the request.",
        ) from exc