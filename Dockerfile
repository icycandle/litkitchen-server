FROM debian:bookworm-slim

# 安裝系統相依套件
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv git \
    fonts-noto-cjk imagemagick libusb-1.0-0-dev curl systemd pipx && \
    rm -rf /var/lib/apt/lists/*

# 確保 python 指向 python3
RUN ln -sf /usr/bin/python3 /usr/bin/python

# 建立專案目錄
WORKDIR /app

# 複製專案檔案
COPY . /app

# 安裝 poetry
RUN pipx install poetry
# 安裝 pipx 與 poetry
RUN pipx ensurepath && pipx install poetry

# 安裝專案依賴
ENV PATH="/root/.local/bin:$PATH"
RUN poetry install --no-root

# 預設使用 systemd 來模擬服務啟動
STOPSIGNAL SIGRTMIN+3

# 啟用 systemd，並以 service 模式啟動 FastAPI
CMD ["/lib/systemd/systemd"]
