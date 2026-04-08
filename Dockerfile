FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

EXPOSE 7860

# ENTRY POINT — OpenEnv validator requires "main:app"
# cache-bust: v4
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
