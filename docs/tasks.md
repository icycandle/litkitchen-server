# LitKitchen Server 開發任務追蹤

## 已完成任務

- [x] 重構 Domain Model，改為 MainDishText、SideDishMedia、DrinkStyle、TextVariant、PrintJob、BarcodeMapping
- [x] Schemas 與 Domain Model 對齊，並補齊 print_count 欄位
- [x] API endpoints 結構精簡，移除/合併不必要檔案
- [x] `/text-variants/pick-best` endpoint（依三參數選取 挑選 print_count、id 最小的 TextVariant）
- [x] `/options` endpoints 整合，統一查詢主食、配餐、飲品選項
- [x] TextVariant 支援 print_count 輪動查詢（查詢時僅推薦 print_count 最小者）
- [x] print_count 僅於 PrintJob create 時遞增，達到真實持久化
- [x] BarcodeMapping endpoints 實作（CRUD）
- [x] PrintJob/Printer/State endpoint 整合
- [x] 所有 API 路由與 high-level-design.md 對齊


# API e2e test 可參考 /tests/test_textvariant_e2e.py

#### /barcode-mappings
- [x] e2e-test GET /barcode-mappings
- [x] e2e-test POST /barcode-mappings
- [x] e2e-test DELETE /barcode-mappings/{item_id}

#### /options
- [x] e2e-test GET /options/maindish
- [x] e2e-test GET /options/sidedish
- [x] e2e-test GET /options/drinkstyle

#### /print-jobs
- [x] e2e-test GET /print-jobs
- [x] e2e-test POST /print-jobs
- [x] e2e-test GET /print-jobs/{job_id}
- [x] e2e-test PUT /print-jobs/{job_id}
- [x] e2e-test DELETE /print-jobs/{job_id}

#### 其他系統 API
- [ ] e2e-test GET /printer-status
- [ ] e2e-test GET /system-state
- [ ] e2e-test POST /system-state/reset

## 尚未完成/可優化任務

- [x] Repo 資料持久化（接 SQLite）
    - [x] 用 SQLModel 定義所有資料表。
    - [x] init_db() 每次都執行 schema.sql，確保所有 table 存在（CREATE TABLE IF NOT EXISTS）
- [x] TextVariant 支援批次上傳/匯入（support CSV）
    - [x] 實作 typer cli 指令
- [x] Repo class 的 unit-test
- [x] print job e2e 測試修正狀態自動更新（背景任務、非同步印表機整合）
- [ ] API 權限管理與驗證（如管理端操作）
- [ ] 完善自動化測試與 API 文件
- [ ] 前端 UI 串接與互動設計
- [ ] 其他進階錯誤處理與例外狀況
