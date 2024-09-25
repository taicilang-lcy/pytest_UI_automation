# 基础镜像
FROM centos:7

# 使用阿里云的源
RUN curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo && \
    yum makecache

# 安装 EPEL 和 Python 依赖
RUN yum install -y epel-release && \
    yum install -y python38 python38-pip java-1.8.0-openjdk-devel && \
    yum clean all

# 设置工作目录为 /test_automation
WORKDIR /test_automation

# 复制 requirements.txt 并安装依赖
COPY requirements.txt .

# 升级 pip 并安装依赖
RUN pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple --timeout=400

# 复制项目代码到工作目录
COPY . .

# 设置默认命令，运行所有测试脚本
CMD ["pytest", "tests/"]
