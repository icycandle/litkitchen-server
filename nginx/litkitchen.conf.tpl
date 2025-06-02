server {
    listen 80;
    server_name {{ server_name }} lk-raspberrypi.local literary-kitchen-tw.uk;

    # 啟用 gzip 壓縮
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript image/svg+xml;
    gzip_min_length 1024;
    gzip_comp_level 6;
    gzip_vary on;

    # 靜態檔案
    location / {
        root {{ static_root }};
        try_files $uri $uri/ /index.html;
        # 靜態資源快取 30 天
        if ($request_uri ~* \.(js|css|png|jpg|jpeg|gif|svg|ico|woff|woff2|ttf|eot)$) {
            expires 30d;
            add_header Cache-Control "public";
        }
    }

    # API 反向代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}