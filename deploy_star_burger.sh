#!/bin/bash
set -Eeuo pipefail

cd /opt/star-burger/

git pull origin master
echo "git is pulled"

npm ci --dev
echo "frontend libraries are ready"
./venv/bin/pip3 install -r requirements.txt
echo "backend libraries are ready"

./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
echo "frontend is ready"
./venv/bin/python manage.py collectstatic --noinput
./venv/bin/python manage.py migrate --noinput
echo "backend is ready"

systemctl daemon-reload
systemctl restart star_burger_back.service
echo "restarted system services"

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
