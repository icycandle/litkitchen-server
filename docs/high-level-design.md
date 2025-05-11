# 文學跨界廚房 AI 文本藝術裝置

## 高階架構設計與 Domain Model 推論

### 主要參數與 Domain Model（依 PM 實際資料）

#### 參數A：主食／文本
- 對應「作家」與其代表文本、主食
- 範例：
  - 1 寺尾哲也《子彈是餘生》 洋芋片 聯經，小說
  - 2 張嘉祥《夜官巡場 Iā-Kuan Sûn-Tiûnn》 虱目魚粥 九歌，小說
  - ...

#### 參數B：配餐／媒材
- 對應文本的媒材/跨界形式與配餐
- 範例：
  - 1 電影／劇集 爆米花
  - 2 戲劇 生菜沙拉
  - ...

#### 參數C：飲品／改編風格
- 對應文本的改編風格與飲品
- 範例：
  - 1 蒙太奇 烏龍茶
  - 2 懸疑 咖啡
  - ...

---

### Domain Model

1. **MainDishText (主食文本)**
   - id
   - author_name
   - work_title
   - main_dish
   - publisher
   - genre
   - description

2. **SideDishMedia (配餐媒材)**
   - id
   - media_type (如電影/劇集/戲劇/電玩...)
   - side_dish

3. **DrinkStyle (飲品風格)**
   - id
   - style (如蒙太奇/懸疑/後設...)
   - drink

4. **TextVariant (文本變體)**
   - id
   - main_dish_text_id (外鍵)
   - side_dish_media_id (外鍵)
   - drink_style_id (外鍵)
   - content (實際文本)
   - variant_index (第幾變體)
   - length (字數)
   - created_at

5. **PrintJob (列印任務)**
   - id
   - text_variant_id (外鍵)
   - status (queued, printing, done, failed)
   - created_at
   - printed_at

#### 印表機狀態與非同步設計
- 熱感應印表機（如 Epson TM-T88VI）有自身的狀態（就緒、列印中、缺紙、錯誤等），列印請求需非同步處理。
- PrintJob 需設計為佇列（Queue）與狀態輪詢（Polling/Callback），API 只負責送出列印任務，不保證立即完成。
- 建議：
  - 新增印表機狀態查詢 API，例如 `GET /printer/status`
  - PrintJob 狀態可由後端背景任務（Background Worker）定期更新
  - 前端可透過查詢 PrintJob 狀態與印表機狀態，顯示「列印中」、「等待中」、「錯誤」等資訊
- 可考慮採用 asyncio、Celery、或 FastAPI BackgroundTasks 處理列印任務與狀態管理

---

### 主要 API 設計

#### 1. 前台互動 API

- `GET /options/maindish`：取得所有主食文本（MainDishText）選項 (開發除錯用，非必要)
- `GET /options/sidedish`：取得所有配餐媒材（SideDishMedia）選項 (開發除錯用，非必要)
- `GET /options/drinkstyle`：取得所有飲品風格（DrinkStyle）選項 (開發除錯用，非必要)
- `GET /pick-best`：參數 main_dish_text_id, side_dish_media_id, drink_style_id，回傳推薦預生成文本（TextVariant）
- `POST /print-jobs`：參數 text_variant_id，送出列印任務（PrintJob）
- `GET /print-jobs/{job_id}`：查詢列印任務狀態（PrintJob）

#### 2. 管理/內容審核 API

- `GET /barcode-mappings`：查詢所有條碼映射
- `POST /barcode-mappings`：新增條碼映射
- `DELETE /barcode-mappings/{item_id}`：刪除條碼映射
- `GET /text-variants/{item_id}`：查詢單一預生成文本（TextVariant）

#### 3. PrintJob 管理

- `GET /print-jobs`：查詢所有列印任務（PrintJob）
- `PUT /print-jobs/{job_id}`：更新列印任務狀態
- `DELETE /print-jobs/{job_id}`：刪除列印任務

#### 4. 系統狀態與印表機

- `GET /printer-status`：查詢印表機狀態
- `GET /system-state`：查詢系統狀態
- `POST /system-state/reset`：重置系統狀態

---

### 系統流程對應

1. 使用者從前端（平板/網頁）webcam 掃 barcode 選擇參數（主食文本、配餐媒材、飲品風格）
2. 前端呼叫 `GET /pick-best` 傳入三個參數 ID，取得隨機文本，確定文本存在
3. 前端呼叫 `POST /print-jobs` 傳入文本 ID，送出列印任務
4. 後端查詢本地資料庫，將文本送至熱感應印表機
5. 前端每隔一秒呼叫 `GET /print-jobs/{id}`，查詢列印任務狀態
6. 前端根據列印任務狀態顯示不同畫面，列印完成後 5 秒自動呼叫 `POST /system-state/reset` 重置系統

---

### 系統狀態 State 設計

本裝置前端互動流程明確分為下列狀態：
- **待命中**（Idle）
- **收到主食文本**（MainDishText Selected）
- **收到配餐媒材**（SideDishMedia Selected）
- **收到飲料風格**（DrinkStyle Selected）
- **列印文本中**（Printing）
- **完成列印**（Printed/Done）

本裝置後端互動流程明確分為下列狀態：
- **待命中**（Idle）
- **列印文本中**（Printing）
- **完成列印**（Printed/Done）

#### State 控制需求
1. **Reset Action**：
   - 提供 API 或控制方式讓系統隨時可優雅回到「待命中」狀態（例如 POST /state/reset）。
2. **自動重置機制**：
   - 若無人操作 60 秒，由前端自動呼叫 Reset API。

#### 實作建議
- State 儲存在後端資料庫，前端定期查詢。
- 每次互動（如參數選擇、條碼掃描、列印啟動）前端都應重設計時器。
- 前端可根據狀態顯示不同畫面，並於需要時主動呼叫 Reset API。

