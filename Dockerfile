FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /usr/local/share/nltk_data

RUN python -c "import nltk; \
    nltk.download('punkt', download_dir='/usr/local/share/nltk_data'); \
    nltk.download('punkt_tab', download_dir='/usr/local/share/nltk_data')"

ENV NLTK_DATA=/usr/local/share/nltk_data

COPY . .

RUN python app/nlp/train_intents.py

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
