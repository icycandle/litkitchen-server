# ADR

- 2025-05-10: 將原本 litkitchen_server/api.py 移除，API router 聚合點改為 litkitchen_server/api/routers.py，main.py 等引用點同步修正。
- 2025-05-10: 將 application.py、infrastructure.py 移除，內容分別搬移到 application/state.py、application/worker.py、infrastructure/printer.py，並同步修正所有 import 路徑。

