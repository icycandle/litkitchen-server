[Unit]
Description=LitKitchen FastAPI Server
After=network.target

[Service]
Type=simple
User=${username}
WorkingDirectory=/app
Environment=PATH=$HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart=${poetry_path} run uvicorn litkitchen_server.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
