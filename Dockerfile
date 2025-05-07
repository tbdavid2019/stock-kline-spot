FROM continuumio/miniconda3

WORKDIR /app

# 先安裝指定版本的 Python，然後安裝特定版本的 numpy 和 ta-lib
RUN conda install -y python=3.10 && \
    conda install -y numpy=1.23.5 && \
    conda install -y -c conda-forge ta-lib

COPY . /app

RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt 

EXPOSE 5678

CMD ["python", "app.py"]