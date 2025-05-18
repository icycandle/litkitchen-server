# litkitchen-server

litkitchen-server 是一個基於 FastAPI 的 Python 專案，使用 Poetry 管理依賴。

## 主要特性
- FastAPI 高效能 Web API 框架
- SQLModel 資料庫操作
- 支援 ESC/POS 印表機 (python-escpos)
- 日期處理工具 (dateutils)
- 自動格式化工具 (black, isort) 與 pre-commit 整合
- 單元測試 (pytest)

## 下載專案原始碼

建議於 `/app` 目錄下下載專案原始碼：

```bash
sudo mkdir -p /app
sudo chown $(whoami):$(whoami) /app
cd /app
git clone https://github.com/icycandle/litkitchen-server .
```

---

## 安裝方式（含 Raspberry Pi Zero 2W）

### 一鍵安裝（建議於 Raspberry Pi Zero 2W 上執行）

```bash
bash script/install.sh
```

- 會自動安裝 Python、相依套件、poetry、印表機字型、Epson TM 系列 CUPS 驅動（從 repo vendor 目錄）與權限設定
- 安裝完畢請依提示重插印表機或重啟

### 手動安裝（開發機/非 Pi）

#### 若需手動安裝 Epson TM 系列 CUPS 驅動，請執行：
```bash
# 直接使用 repo 內 vendor/tmx-cups-src-ThermalReceipt-3.0.0.0.tar
 tar -xvf vendor/tmx-cups-src-ThermalReceipt-3.0.0.0.tar
 cd tmx-cups-src-ThermalReceipt-3.0.0.0/Thermal\ Receipt

# 編譯與安裝
 sudo ./build.sh
 sudo ./install.sh
 cd /app
```

```bash
sudo apt update && sudo apt install pipx python3
pipx ensurepath
pipx install poetry

# 安裝專案依賴
poetry install
```

## 開發建議流程

1. 建議使用 pre-commit 進行程式碼格式檢查：
   ```bash
   poetry run pre-commit run --all-files
   ```
2. 執行測試：
   ```bash
   poetry run pytest
   ```

## CLI 指令

初始化資料庫（若 DB 檔不存在）：
```bash
sqlite3 db.sqlite3 < sql/schema.sql
```

批次匯入 TextVariant 資料：
```bash
LITKITCHEN_DB_PATH=db.sqlite3 poetry run python -m litkitchen_server.cli_textvariant tests/fixtures/example_textvariant.csv
```

## 啟動 FastAPI 服務

### 開發模式
```bash
poetry run uvicorn main:app --reload
```
> 請將 `main:app` 替換為你的 FastAPI 入口檔案與 application 物件名稱。

### 生產模式（自動啟動，建議於 Raspberry Pi）

1. 複製 systemd 服務單元檔
```bash
poetry run python /app/script/gen_service.py
sudo cp /app/script/litkitchen-server.service /etc/systemd/system/
# 請注意：User=請改成自己的帳號，例如 User=pi 或 User=icycandle
sudo systemctl daemon-reload
sudo systemctl enable litkitchen-server
sudo systemctl start litkitchen-server
```

#### 察看服務狀態
```bash
sudo systemctl status litkitchen-server
```

#### 查詢 systemd 服務最近 50 行日誌
```bash
sudo journalctl -u litkitchen-server.service -n 50
```

2. 開機自動啟動、異常自動重啟
3. 預設服務運行於 `0.0.0.0:8000`

### 使用 Docker 測試 install.sh 與 systemd 啟動（建議正式部署前驗證）

1. 啟動 container 並進入 bash：
```bash
docker compose up --build -d
docker exec -it litkitchen-server bash
```
2. 在 container 內執行安裝與 systemd 測試：
```bash
bash /app/script/install.sh
poetry run python /app/script/gen_service.py
sudo cp /app/script/litkitchen-server.service /etc/systemd/system/
# 請注意：User=請改成自己的帳號，例如 User=pi 或 User=icycandle
sudo systemctl daemon-reload
sudo systemctl enable litkitchen-server
sudo systemctl start litkitchen-server
sudo systemctl status litkitchen-server
```
> 可驗證腳本、udev 權限、systemd 啟動行為於 Debian 環境下的正確性。

## 套件清單
- fastapi
- python-escpos
- sqlmodel
- dateutils
- pytest
- black
- isort
- pre-commit


## 資料庫 schema 管理規範

- 專案資料表結構統一維護於 `sql/schema.sql`，所有 SQLite 資料表皆以此檔案為唯一來源。
- **何時要修改？**
  - 需要新增、修改、刪除資料表或欄位時，請直接編輯 `sql/schema.sql`。
  - 修改 schema 後，請同步確認 `repository.py` 的 CRUD 操作是否需要一併調整。
  - 直接刪除之後再重新初始化
  - 要準備 import from CSV 的 typer cli 指令
- **新環境初始化：**
  - 專案啟動時若偵測到資料庫檔案不存在，會自動執行 `sql/schema.sql` 初始化所有資料表。
