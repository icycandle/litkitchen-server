# ADR

- 2025-05-10: 將原本 litkitchen_server/api.py 移除，API router 聚合點改為 litkitchen_server/api/routers.py，main.py 等引用點同步修正。
- 2025-05-10: 將 application.py、infrastructure.py 移除，內容分別搬移到 application/state.py、application/worker.py、infrastructure/printer.py，並同步修正所有 import 路徑。
- 2025-05-11: infra 下所有 repository interface 均統一依賴與回傳 domain model，ORM 僅限於 repo 實作內部轉換使用，ORM 不得成為 interface 依賴或直接 expose。

