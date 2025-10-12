FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY pyproject.toml ./
RUN uv venv .venv
RUN . .venv/bin/activate && uv sync --active

COPY ./ ./

ENV PYTHONPATH=/app

CMD ["uv" "run" "python", "-m", "uvicorn", "service.service:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
