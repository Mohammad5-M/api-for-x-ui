#!/bin/sh
apt-get update
apt-get install nginx
pip3 install -r requirement.txt
# # pip3 install gunicorn

# # sudo -S cp ./fastapi_demo.service /etc/systemd/system/fastapi_demo.service
uvicorn main:app --reload

tmux attach
tmux -c pip3 -V 
