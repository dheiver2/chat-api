FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    python3-dev \
    && apt-get clean

WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]