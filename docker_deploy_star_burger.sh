#!/bin/bash
set -Eeuo pipefail

cd /opt/star-burger/

git pull origin master
echo "git is pulled"

docker-compose up --build -d
docker-compose exec -it starburger-backend python manage.py migrate --noinput
docker-compose exec -it starburger-backend python manage.py collectstatic --noinput

systemctl reload nginx.service
echo "Server is reloaded"

last_commit_hash=$(git rev-parse HEAD)

source .env
export ROLLBAR_ACCESS_TOKEN
curl --http1.1 -X POST \
  https://api.rollbar.com/api/1/deploy \
  -H "X-Rollbar-Access-Token: $ROLLBAR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"environment": "production", "revision": "'"$last_commit_hash"'", "local_username": "root", "comment": "auto_deployed", "status": "succeeded"}'

echo "Project is deployed"
