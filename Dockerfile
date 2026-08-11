FROM python:3.11-slim

WORKDIR /app

# 安裝編譯工具與 TA-Lib C 函式庫
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    ca-certificates \
    && wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
    && tar -xzf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib/ \
    && ./configure --prefix=/usr \
    && make \
    && make install \
    && cd .. \
    && rm -rf ta-lib ta-lib-0.4.0-src.tar.gz \
    && apt-get purge -y --auto-remove build-essential wget \
    && rm -rf /var/lib/apt/lists/*

# 先複製 requirements.txt 並安裝 Python 套件 (利用 Docker 快取)
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# 複製其餘專案檔案
COPY . .

EXPOSE 5678

CMD ["python", "app.py"]