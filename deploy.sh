#!/bin/bash
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")" && pwd)"
cd "$repo_dir"

container_name="stock-kline-spot"
image_name="stock-kline-spot"
remote_latest="tbdavid2019/stock-kline-spot:latest"
remote_version="tbdavid2019/stock-kline-spot:v1.3"

if docker ps -a --format '{{.Names}}' | grep -qx "$container_name"; then
  docker stop "$container_name" >/dev/null 2>&1 || true
  docker rm "$container_name" >/dev/null 2>&1 || true
fi

docker build --no-cache -t "$image_name" .
docker run -d \
  -p 5678:5678 \
  --name "$container_name" \
  --restart unless-stopped \
  "$image_name"
docker tag "$image_name" "$remote_latest"
docker tag "$image_name" "$remote_version"
docker push "$remote_latest"
docker push "$remote_version"
