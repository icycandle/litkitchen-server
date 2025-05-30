server {
    listen 443 ssl;
    server_name {{ server_name }};

    ssl_certificate     {{ ssl_cert }};
    ssl_certificate_key {{ ssl_key }};

    # 靜態檔案
    location / {
        root {{ static_root }};
        try_files $uri $uri/ /index.html;
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