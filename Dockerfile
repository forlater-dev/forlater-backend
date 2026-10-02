FROM python:3.14-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:0.12.22 /uv /usr/local/bin/uv

WORKDIR /app
RUN useradd --create-home --uid 10001 appuser

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-cache

COPY . .
USER appuser
CMD ["/app/.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
