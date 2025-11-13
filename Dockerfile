# ----------------------------
# Lightweight Python 3.10 Alpine
# ----------------------------
FROM python:3.10-alpine

# Set working directory
WORKDIR /app

# Install build tools and dependencies
RUN apk add --no-cache \
    bash \
    gcc \
    g++ \
    musl-dev \
    libffi-dev \
    ffmpeg \
    aria2 \
    make \
    cmake \
    unzip \
    wget \
    curl

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the bot code
COPY . .

# Install Bento4 (single layer for smaller image)
RUN wget -q https://github.com/axiomatic-systems/Bento4/archive/v1.6.0-639.zip && \
    unzip v1.6.0-639.zip && \
    cd Bento4-1.6.0-639 && \
    mkdir build && cd build && \
    cmake .. && make -j$(nproc) && \
    cp mp4decrypt /usr/local/bin/ && \
    cd ../.. && \
    rm -rf Bento4-1.6.0-639 v1.6.0-639.zip

# Optional: expose port for webhooks if needed
# EXPOSE 8080

# Command to run bot
CMD ["python3", "main.py"]
