#!/bin/bash
# 產生並安裝 litkitchen-server systemd 服務
set -e

poetry run python "$(dirname "$0")/gen_systemd_service.py"
sudo cp "$(dirname "$0")/litkitchen-server.service" /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable litkitchen-server
sudo systemctl start litkitchen-server

echo "[INFO] systemd 服務已安裝並啟動，可用 sudo systemctl status litkitchen-server 查看狀態。"
