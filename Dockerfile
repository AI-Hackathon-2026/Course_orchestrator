FROM python:3.12-slim
RUN pip install uv
WORKDIR /app
COPY requirements.txt .
RUN uv venv && uv pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8067
CMD ["uv", "run", "python", "-m", "orchestrator.rest_handler"]
