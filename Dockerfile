FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app:/app/banking_rl_env

EXPOSE 7860

# Correct entrypoint using the main() function
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
