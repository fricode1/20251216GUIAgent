FROM python:3.10-slim

# 设置环境变量，防止 Python 生成 .pyc 文件和缓冲输出
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# 1. 统一安装系统依赖
# 将所有 apt-get 操作合并，包括 Chromium 依赖、基础工具(curl, gnupg)
# 使用 --no-install-recommends 避免安装不必要的推荐包
RUN apt-get update && apt-get install -y --no-install-recommends \
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
    curl \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 2. 安装 Node.js (V20 LTS)
# 放在 Python 之前或之后均可，但建议尽早，因为系统环境变动少于 Python 包变动
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g yarn \ 
    && rm -rf /var/lib/apt/lists/*

# 3. 安装 Python 包
# 建议显式安装 opencv-python-headless 避免图形界面依赖报错
# 放在后面是因为开发过程中改动最频繁
RUN pip install --no-cache-dir \
    opencv-python-headless \
    rapidocr-onnxruntime \
    pillow \
    DrissionPage \
    fastapi \
    onnxruntime \
    minio \
    uvicorn \
    -i https://pypi.tuna.tsinghua.edu.cn/simple

# 4. 安装 Opencode
# 这是一个脚本安装，变动可能较小，也可以放在 Node 之后
RUN curl -fsSL https://opencode.ai/install -o install_opencode.sh \
    && bash install_opencode.sh \
    && rm install_opencode.sh

RUN pip install --no-cache-dir httpx aiofiles aiosqlite openai -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN apt-get update && apt-get install -y --no-install-recommends wget && rm -rf /var/lib/apt/lists/*

RUN wget https://dl.min.io/server/minio/release/linux-amd64/minio && chmod +x minio

# 如果有代码需要复制，通常放在最后
# COPY . .

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]