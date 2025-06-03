#!/bin/bash
set -e

# 這個 script 記錄在 Raspberry Pi 上部署 cloudflare tunnel 的過程，理論上不用再執行了。

# === 基本變數設定 ===
DOMAIN="literary-kitchen-tw.uk"
TUNNEL_NAME="literary-kitchen-page"
TUNNEL_DIR="$HOME/.cloudflared"
NGINX_ROOT="/var/www/html"
CONFIG_FILE="$TUNNEL_DIR/config.yml"

echo "🔧 安裝必要套件..."
sudo apt update
sudo apt install -y nginx curl

echo "🔐 安裝 cloudflared..."
wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb
sudo dpkg -i cloudflared-linux-arm64.deb

echo "🌐 登入 Cloudflare 帳戶..."
cloudflared tunnel login

echo "🚇 建立 Tunnel 名稱：$TUNNEL_NAME"
cloudflared tunnel create "$TUNNEL_NAME"

# 取得 tunnel ID 與 credentials 路徑
TUNNEL_ID=$(cat "$TUNNEL_DIR"/*.json | jq -r .TunnelID)
CREDENTIALS_FILE=$(ls "$TUNNEL_DIR"/*.json)

echo "📁 建立 config.yml 設定檔..."
cat <<EOF > "$CONFIG_FILE"
tunnel: $TUNNEL_ID
credentials-file: $CREDENTIALS_FILE

ingress:
  - hostname: $DOMAIN
    service: http://localhost:80
  - service: http_status:404

# 控制 tunnel 連線數
connections: 1
EOF

echo "🌐 將 DNS CNAME 指向 tunnel..."
cloudflared tunnel route dns "$TUNNEL_NAME" "$DOMAIN"

echo "🚀 執行 tunnel..."
cloudflared tunnel --config "$CONFIG_FILE" run &
sleep 5

echo "🔁 重新啟動 nginx"
sudo systemctl restart nginx

echo "✅ 完成部署！請造訪：https://$DOMAIN/"
