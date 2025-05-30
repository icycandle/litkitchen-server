import argparse
import os
import subprocess
import socket

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "../nginx/litkitchen.conf.tpl")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "../nginx/litkitchen.conf")
DEFAULT_OUTPUT_PATH = "/etc/nginx/conf.d/litkitchen.conf"

DEFAULT_STATIC_ROOT = "/app/frontend/dist"
DEFAULT_SERVER_NAME = "_"
DEFAULT_SSL_CERT = "/etc/nginx/certs/mkcert.crt"
DEFAULT_SSL_KEY = "/etc/nginx/certs/mkcert.key"


def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 連到一個不存在的 IP 以取得本機 IP
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def ensure_mkcert_cert(cert_path: str, key_path: str, domains: list[str]):
    if not (os.path.exists(cert_path) and os.path.exists(key_path)):
        print(
            f"🔐 用 mkcert 產生憑證: {cert_path}, {key_path} for {', '.join(domains)}"
        )
        os.makedirs(os.path.dirname(cert_path), exist_ok=True)
        # 檢查 mkcert 是否存在
        if (
            subprocess.call(
                ["which", "mkcert"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            != 0
        ):
            print("[ERROR] 請先安裝 mkcert，參考 https://github.com/FiloSottile/mkcert")
            exit(1)
        cmd = [
            "mkcert",
            "-cert-file",
            cert_path,
            "-key-file",
            key_path,
        ] + domains
        subprocess.run(cmd, check=True)
    else:
        print(f"🔑 憑證已存在: {cert_path}, {key_path}")


def render_template(template_path: str, output_path: str, context: dict):
    with open(template_path, "r", encoding="utf-8") as f:
        tpl = f.read()
    for k, v in context.items():
        tpl = tpl.replace(f"{{{{ {k} }}}}", v)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(tpl)
    print(f"✅ 已產生 nginx 設定檔: {output_path}")


def reload_nginx():
    print("🔄 重新載入 nginx 服務...")
    try:
        subprocess.run(["sudo", "systemctl", "reload", "nginx"], check=True)
        print("✅ nginx 已重新載入")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] 重新載入 nginx 失敗: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="產生 nginx 設定檔並自動用 mkcert 產生憑證（如需要）"
    )
    parser.add_argument(
        "--static-root", default=DEFAULT_STATIC_ROOT, help="前端靜態檔案路徑"
    )
    parser.add_argument(
        "--server-name", default=DEFAULT_SERVER_NAME, help="nginx server_name"
    )
    parser.add_argument("--ssl-cert", default=DEFAULT_SSL_CERT, help="SSL 憑證路徑")
    parser.add_argument("--ssl-key", default=DEFAULT_SSL_KEY, help="SSL 私鑰路徑")
    parser.add_argument(
        "--domains", nargs="*", help="mkcert 憑證 domain 清單（預設自動偵測）"
    )
    parser.add_argument(
        "--output-path",
        default=DEFAULT_OUTPUT_PATH,
        help="nginx 設定檔輸出路徑 (預設 /etc/nginx/conf.d/litkitchen.conf)",
    )
    args = parser.parse_args()

    if args.domains:
        domains = args.domains
    else:
        local_ip = get_local_ip()
        domains = ["raspberrypi.local", "localhost", "127.0.0.1", local_ip]

    ensure_mkcert_cert(args.ssl_cert, args.ssl_key, domains)

    context = {
        "static_root": args.static_root,
        "server_name": args.server_name,
        "ssl_cert": args.ssl_cert,
        "ssl_key": args.ssl_key,
    }
    # 若 output_path 沒有被指定，則同時寫入 repo 內與 /etc/nginx/conf.d/
    if args.output_path == DEFAULT_OUTPUT_PATH:
        render_template(TEMPLATE_PATH, OUTPUT_PATH, context)
    render_template(TEMPLATE_PATH, args.output_path, context)
    reload_nginx()


if __name__ == "__main__":
    main()
