# 使用官方 Python 作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装必要的系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    libatlas-base-dev \
    build-essential \
    wget \
    && apt-get clean

# 下载并安装 TA-Lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# 将项目文件复制到容器中
COPY . /app

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露应用端口
EXPOSE 5678

# 运行主程序
CMD ["python", "app.py"]