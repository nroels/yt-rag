FROM python:3.11-slim

WORKDIR /usr/src/app

# Install Python deps first (use caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

CMD ["sleep", "infinity"]
