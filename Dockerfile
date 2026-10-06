FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    git \
    gcc \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# Restore missing mime_types.txt in installed stdgram package
RUN python3 -c "import importlib.util, pathlib, shutil; spec = importlib.util.find_spec('stdgram'); spec and shutil.copy('StdMusic/assets/mime_types.txt', pathlib.Path(spec.origin).parent / 'mime_types.txt')" || true

CMD ["python3", "-m", "StdMusic"]
