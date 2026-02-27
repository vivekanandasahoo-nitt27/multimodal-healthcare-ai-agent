FROM python:3.10-slim

# ---------- ENV ----------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DEFAULT_TIMEOUT=1000
ENV GRADIO_ANALYTICS_ENABLED=False

# ---------- SYSTEM DEPENDENCIES ----------
RUN apt-get update && apt-get install -y \
    ffmpeg \
    gcc \
    g++ \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---------- WORKDIR ----------
WORKDIR /app

# ---------- INSTALL PYTHON DEPS (layer cache friendly) ----------
COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r requirements.txt

# ---------- COPY PROJECT ----------
COPY . .

# ---------- PORT ----------
EXPOSE 7860

# ---------- START APP ----------
CMD ["python",  "-u","app.py"]