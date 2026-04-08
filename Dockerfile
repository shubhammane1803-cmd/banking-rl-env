FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Set PYTHONPATH so banking_rl_env is importable
ENV PYTHONPATH=/app

EXPOSE 7860

# OpenEnv validator requires entry point as "main:app"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
