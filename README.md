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

---

如需更多協助，請參考各套件官方文件或聯絡專案維護者。
