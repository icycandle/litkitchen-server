# LitKitchen Server 開發任務追蹤

## 已完成任務

- [x] 重構 Domain Model，改為 MainDishText、SideDishMedia、DrinkStyle、TextVariant、PrintJob、BarcodeMapping
- [x] Schemas 與 Domain Model 對齊，並補齊 print_count 欄位
- [x] API endpoints 結構精簡，移除/合併不必要檔案
- [x] `/options` endpoints 整合，統一查詢主食、配餐、飲品選項
- [x] TextVariant 支援 print_count 輪動查詢（查詢時僅推薦 print_count 最小者）
- [x] print_count 僅於 PrintJob create 時遞增，達到真實持久化
- [x] BarcodeMapping endpoints 實作（CRUD）
- [x] PrintJob/Printer/State endpoint 整合
- [x] 所有 API 路由與 high-level-design.md 對齊


## 尚未完成/可優化任務

- [x] Repo 資料持久化（接 SQLite）
    - [x] 用 SQLModel 定義所有資料表。
- [ ] TextVariant 支援批次上傳/匯入（如 CSV）
- [ ] `/select` endpoint（依三參數隨機選取 TextVariant）
- [ ] PrintJob 狀態自動更新（背景任務、非同步印表機整合）
- [ ] API 權限管理與驗證（如管理端操作）
- [ ] 完善自動化測試與 API 文件
- [ ] 前端 UI 串接與互動設計
- [ ] 其他進階錯誤處理與例外狀況

