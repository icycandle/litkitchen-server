# litkitchen-server

litkitchen-server 是一個基於 FastAPI 的 Python 專案，使用 Poetry 管理依賴。

## 主要特性
- FastAPI 高效能 Web API 框架
- SQLModel 資料庫操作
- 支援 ESC/POS 印表機 (python-escpos)
- 日期處理工具 (dateutils)
- 自動格式化工具 (black, isort) 與 pre-commit 整合
- 單元測試 (pytest)

## 安裝方式

```bash
# 安裝 Poetry
pip install poetry

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

```bash
poetry run uvicorn main:app --reload
```

> 請將 `main:app` 替換為你的 FastAPI 入口檔案與 application 物件名稱。

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
