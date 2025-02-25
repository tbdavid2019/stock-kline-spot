cd /home/bitnami/stock-kline-spot
source myenv/bin/activate
nohup python app.py > /tmp/kline.log 2>&1 &


docker builder prune
docker build --no-cache -t stock-kline-spot .



docker build -t stock-kline-spot .
docker run -d -p 5678:5678 --name stock-kline-spot stock-kline-spot


docker tag stock-kline-spot tbdavid2019/stock-kline-spot:latest
docker tag stock-kline-spot tbdavid2019/stock-kline-spot:v1.3

docker push tbdavid2019/stock-kline-spot:latest
docker push tbdavid2019/stock-kline-spot:v1.3