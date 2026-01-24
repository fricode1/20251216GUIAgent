FROM python:3.10-slim

WORKDIR /app

# 1. 安装系统依赖 (保持不变，这是大头)
RUN apt-get update && apt-get install -y \
    chromium \
    libgl1 \
    libglib2.0-0 \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# 2. 直接安装 Python 包，不再 COPY requirements.txt
RUN pip install --no-cache-dir \
    rapidocr \
    pillow \
    DrissionPage \
    fastapi \
    onnxruntime \
    minio \
    uvicorn \
    -i https://pypi.tuna.tsinghua.edu.cn/simple
