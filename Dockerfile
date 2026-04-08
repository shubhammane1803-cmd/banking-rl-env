
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app:/app/banking_rl_env

EXPOSE 7860

# Use the 'main' function we added in server/app.py
CMD ["uvicorn", "server.app:main", "--host", "0.0.0.0", "--port", "7860"]
