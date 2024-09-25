# 使用 Python 3.9 镜像作为基础镜像
FROM registry.cn-hangzhou.aliyuncs.com/lcy-dockerhub/python:3.9

# 设置工作目录
WORKDIR /test_automation


# 复制 requirements.txt 并安装依赖
COPY requirements.txt .

# 升级 pip 并安装依赖
RUN pip install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple

RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple --timeout=400

# 复制项目代码
COPY . .

# 设置默认命令
# 设置默认命令，运行 test_suites 目录下的测试，并将 Allure 结果生成到 report/allure-results 目录
CMD ["pytest", "test_suites/", "--alluredir=report/allure-results"]
