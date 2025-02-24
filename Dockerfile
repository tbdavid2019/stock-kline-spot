FROM continuumio/miniconda3

WORKDIR /app

# 使用 conda 安裝 ta-lib，免除編譯問題
RUN conda install -y -c conda-forge ta-lib

COPY . /app

RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5678

CMD ["python", "app.py"]