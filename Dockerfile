FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --timeout 1000 --retries 10 \
    torch --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir --timeout 1000 --retries 10 -r requirements.txt

COPY src/ ./src/
COPY chroma_db/ ./chroma_db/

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "src"]