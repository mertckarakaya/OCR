FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr tesseract-ocr-tur poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY batch.py .

RUN mkdir -p /data/in /data/out
VOLUME ["/data"]

ENV OCR_LANG=tur+eng \
    OCR_DPI=300 \
    OCR_PSM=6 \
    OCR_FORCE=0

ENTRYPOINT ["python", "batch.py"]