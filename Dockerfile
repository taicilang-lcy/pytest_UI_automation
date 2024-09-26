# 使用官方 Python 3.9.20 slim 镜像作为基础镜像
FROM registry.cn-hangzhou.aliyuncs.com/lcy-dockerhub/python:3.9.20-slim

# 设置工作目录
WORKDIR /pytest_UI_automation

# 设置阿里云的 apt 源并安装必要的依赖
RUN sed -i 's|http://deb.debian.org|http://mirrors.aliyun.com|g' /etc/apt/sources.list && \
    apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# 下载并安装 Google Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb || apt-get -fy install && \
    rm google-chrome-stable_current_amd64.deb

# 复制 requirements.txt 并安装依赖
COPY requirements.txt .

# 升级 pip 并安装依赖
RUN pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple

# 安装依赖，使用 --no-cache-dir 以避免缓存增加镜像体积
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple --timeout=400

# 复制项目代码
COPY . .

# 设置默认命令，运行 test_suites 目录下的测试，并将 Allure 结果生成到 report/allure-results 目录
CMD ["pytest", "test_suites/", "--alluredir=report/allure-results"]
