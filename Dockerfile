FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./

# 1) Install CPU-only PyTorch from the official CPU wheel index (GPU almost takes 10GB)
RUN pip install --no-cache-dir torch==2.9.1 --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
