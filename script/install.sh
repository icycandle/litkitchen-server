#!/bin/bash
# 安裝 litkitchen-server 執行環境與印表機相依套件（適用 Raspberry Pi Zero 2W, Debian）

set -e

# 1. 系統更新與必要套件
if command -v sudo >/dev/null 2>&1; then
    SUDO=sudo
else
    SUDO=
fi

$SUDO apt update
$SUDO apt install -y python3 python3-pip python3-venv git \
    libnss3-tools mkcert \
    fonts-noto-cjk imagemagick libusb-1.0-0-dev cups

# 2. 安裝 pipx 與 poetry
sudo apt install -y pipx
pipx ensurepath
pipx install poetry
# 根據目前 user 設定 PATH
if [ "$(id -u)" = "0" ]; then
    export PATH="/root/.local/bin:$PATH"
else
    export PATH="$HOME/.local/bin:$PATH"
fi
# 3. 安裝專案相依
cd /app
poetry install

# 4. 設定 udev 規則（Epson TM-T88VI）
echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="04b8", ATTRS{idProduct}=="0202", MODE="0666", GROUP="plugdev"' \
  | $SUDO tee /etc/udev/rules.d/99-escpos.rules > /dev/null
$SUDO udevadm control --reload
$SUDO udevadm trigger

# 5. 安裝 Epson TM 系列 CUPS 驅動
printf '\n[INFO] 安裝 Epson TM 系列 CUPS 驅動（使用內建 vendor/tmx-cups-src-ThermalReceipt-3.0.0.0.tar）\n'
tar -xvf vendor/tmx-cups-src-ThermalReceipt-3.0.0.0.tar
cd "Thermal Receipt"
$SUDO ./build.sh
$SUDO ./install.sh
cd /app

# 6. 提示用戶重插印表機
printf '\n[INFO] 請重新插拔印表機，或重啟 Raspberry Pi 以套用 USB 權限設定\n'

# 6. 建議建立 systemd 服務自動啟動
printf '\n[INFO] 建議執行：\n'
printf '    bash script/setup_systemd_service.sh\n'
