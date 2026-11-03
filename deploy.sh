#!/usr/bin/env bash
set -e
IMAGE="ghcr.io/ouassim-elkoutbi/rag-agent-investment-research:latest"
ENV_FILE="/home/ubuntu/rag-agent-investment-research/.env"

echo "==> Pulling latest image from GHCR..."
docker pull "$IMAGE"

echo "==> Replacing the running container..."
docker stop rag-agent 2>/dev/null || true
docker rm rag-agent 2>/dev/null || true

docker run -d \
  -p 8000:8000 \
  --env-file "$ENV_FILE" \
  --name rag-agent \
  --restart unless-stopped \
  "$IMAGE"

echo "==> Waiting for the app to become healthy..."
for i in $(seq 1 30); do
  if curl -fsS http://localhost:8000/health >/dev/null 2>&1; then
    echo "Deploy OK - app is healthy:"
    curl -fsS http://localhost:8000/health; echo ""
    exit 0
  fi
  echo "   ...not ready yet ($i/30), waiting 5s"
  sleep 5
done

echo "App did not become healthy in time. Recent logs:"
docker logs --tail 50 rag-agent
exit 1