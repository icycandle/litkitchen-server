# ADR (Architecture Decision Record)

## 2025-05-17
- 將 install-printer.md 文件整理為正式、結構化的技術文件格式，增加目錄、章節標題、表格與步驟說明，提升可讀性與維護性。

## 2025-05-17 (2)
- 根據 install-printer.md 實作 infra printer service，整合 python-escpos、Pillow，支援繁體中文收據列印與狀態查詢。
- poetry 新增 python-escpos pillow pyusb。
- Printer service 已可被 web api (printjob/printer-status) 注入與呼叫。

## 2025-05-18
- 新增 script/install.sh 腳本，協助於 Raspberry Pi Zero 2W (Debian) 快速安裝執行環境、相依套件、poetry、udev 規則。
- 提供 litkitchen-server systemd 服務單元檔，可自動於開機時啟動 FastAPI 應用。
- 文件中提示如何啟用 systemd 服務，確保服務穩定自動重啟。
