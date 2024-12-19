cd /home/bitnami/stock-kline-spot
source myenv/bin/activate
nohup python app.py > /tmp/kline.log 2>&1 &



docker build -t stock-kline-spot .

docker tag stock-kline-spot tbdavid2019/stock-kline-spot:v1.0
docker push tbdavid2019/stock-kline-spot:v1.0
