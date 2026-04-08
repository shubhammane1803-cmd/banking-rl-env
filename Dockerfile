
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything
COPY . .

# Important: Make sure Python can find your modules
ENV PYTHONPATH=/app:/app/banking_rl_env

EXPOSE 7860

# Use the main function we added earlier
CMD ["uvicorn", "server.app:main", "--host", "0.0.0.0", "--port", "7860"]
