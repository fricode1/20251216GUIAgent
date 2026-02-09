FROM lscr.io/linuxserver/webtop:ubuntu-xfce

WORKDIR /app

# 安装 Python 依赖
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .