# DDD 架構下的 litkitchen-server 專案目錄規劃

本專案依據 Domain-Driven Design（DDD）原則進行分層與模組劃分，強調核心領域邏輯、邊界清晰、易於擴展與測試。

## 頂層目錄結構

```
litkitchen_server/
├── main.py                 # FastAPI 入口
├── api/                    # API 路由層（Application Service）
├── domain/                 # 核心領域模型與邏輯（所有聚合根 Entity/ValueObject/Service 直接放於此）
│   ├── author.py
│   ├── artform.py
│   ├── theme.py
│   ├── textvariant.py
│   ├── printjob.py
│   ├── barcodemapping.py
│   └── ...
├── application/            # 應用服務層（協調用例、流程、狀態管理）
├── infrastructure/         # 基礎設施層（DB、印表機、外部 API 整合）
├── repository/             # 資料存取介面（建議以 domain 聚合根分類，或直接集中管理）
├── schemas/                # Pydantic 輸入/輸出 schema
├── settings.py             # 設定檔
├── tests/                  # 測試
└── ...
```

## 各層說明

- **domain/**：所有聚合根（Aggregate）Entity、ValueObject、Domain Service 直接放於此層，不再細分子資料夾，適合小型專案。
- **api/**：各功能對應的 FastAPI 路由，僅負責接收/回應請求，呼叫 application 層服務。
- **application/**：用例服務（UseCase/Application Service），協調 domain 物件、處理流程、狀態管理。
- **infrastructure/**：外部系統整合，如資料庫 ORM、印表機、外部 LLM API。
- **repository/**：資料存取介面與實作，依據 domain 聚合根分類。
- **schemas/**：Pydantic schema，專責資料驗證與序列化。
- **tests/**：單元測試與整合測試。

## DDD 實踐重點
- 嚴格區分核心邏輯（domain）與應用流程（application）、介面（api）、基礎設施（infrastructure）
- 聚合根（如 Author、TextVariant、PrintJob、BarcodeMapping）為 domain 子模組
- 狀態管理、Reset、Timeout 可由 application 層協調
- infrastructure 提供 DB/印表機/外部 API 實作

---

> 本檔案僅為初步 DDD 架構規劃，實際可依團隊需求調整。
