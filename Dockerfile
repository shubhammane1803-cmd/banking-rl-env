FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Set PYTHONPATH so banking_rl_env is importable
ENV PYTHONPATH=/app

# Override sys.path setup inside files (needed for Docker)
ENV BANKING_ROOT=/app

EXPOSE 7860

# Launch the FastAPI server
CMD ["uvicorn", "banking_rl_env.server.app:app", "--host", "0.0.0.0", "--port", "7860"]
