# 基础镜像
FROM centos:latest

# 安装 EPEL 和 Python 依赖
RUN yum install -y epel-release && \
    yum install -y python38 python38-pip java-1.8.0-openjdk-devel && \
    yum clean all

# 设置工作目录为 /test_automation
WORKDIR /test_automation

# 复制 requirements.txt 并安装依赖
COPY requirements.txt .

# 升级 pip 并安装依赖
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt --timeout=400

# 复制项目代码到工作目录
COPY . .

# 设置默认命令
CMD ["pytest", "tests/test_example.py"]
