"""
產生 litkitchen-server systemd 服務檔，根據目前使用者自動帶入 User。
用法：
    poetry run python script/gen_systemd_service.py
產生結果：
    script/litkitchen-server.service
"""

import shutil
from pathlib import Path
import getpass
import os

TEMPLATE_PATH = Path(__file__).parent / "litkitchen-server.service.tpl"
OUTPUT_PATH = Path(__file__).parent / "litkitchen-server.service"


def main():
    username = os.environ.get("USER") or getpass.getuser()
    poetry_path = shutil.which("poetry")
    if not poetry_path:
        raise RuntimeError("找不到 poetry，請確認已安裝並在 PATH 中")
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    service = template.replace("${username}", username).replace(
        "${poetry_path}", poetry_path
    )
    OUTPUT_PATH.write_text(service, encoding="utf-8")
    print(f"[INFO] Service file generated for user: {username}")
    print(f"[INFO] poetry 路徑: {poetry_path}")
    print(
        "[INFO] 請執行 sudo cp script/litkitchen-server.service /etc/systemd/system/ 以安裝 systemd 服務"
    )


if __name__ == "__main__":
    main()
