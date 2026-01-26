FROM lscr.io/linuxserver/webtop

# 更新软件源并安装 tmux 和 micro
RUN apt-get update && \
    apt-get install -y tmux micro && \
    rm -rf /var/lib/apt/lists/*

# 安装 node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g yarn \ 
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple