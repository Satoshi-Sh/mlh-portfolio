#!/bin/sh
cd ~/mlh-portfolio
git fetch && git reset origin/main --hard
docker compose -f docker-compose.prod.yml down # avoid memory issues on vps 
docker compose -f docker-compose.prod.yml up -d --build



# Before docker 
# git fetch && git reset origin/main --hard
# source python3-virtualenv/bin/activate
# pip install -r requirements.txt
# systemctl daemon-reload
# systemctl restart myportfolio