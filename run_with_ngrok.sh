#!/bin/bash
# 啟動 FastAPI server 並用 ngrok 對外公開 swagger docs

# 啟動 uvicorn（背景執行，log 輸出到 uvicorn.log）
echo "[INFO] 啟動 FastAPI server..."
poetry run uvicorn litkitchen_server.main:app --reload --port 8000 > uvicorn.log 2>&1 &
UVICORN_PID=$!

# 等待 server 啟動
sleep 3

# 啟動 ngrok
if ! command -v ngrok &> /dev/null; then
  echo "[ERROR] ngrok 未安裝，請先安裝 ngrok (brew install ngrok 或參考 https://ngrok.com/download)"
  kill $UVICORN_PID
  exit 1
fi

echo "[INFO] 啟動 ngrok..."
ngrok http 8000

# ngrok 結束時關閉 uvicorn
kill $UVICORN_PID
