import typer
import csv
from pathlib import Path
from litkitchen_server.application.services import TextVariantService
from sqlmodel import Session
from litkitchen_server.infrastructure.text_variant_repository import (
    TextVariantRepository,
)
from litkitchen_server.infrastructure.repository_sqlite import engine
from litkitchen_server.infrastructure.models import TextVariantOrm
import os


def import_csv(csv_path: str):
    """
    批次匯入 TextVariant 資料。
    CSV 欄位：main_dish_text_id,side_dish_media_id,drink_style_id,content,variant_index,length,approved,print_count
    """
    file = Path(csv_path)
    if not file.exists():
        typer.echo(f"找不到檔案: {csv_path}")
        raise typer.Exit(1)
    with file.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tv = TextVariantOrm(
                main_dish_text_id=int(row["main_dish_text_id"]),
                side_dish_media_id=int(row["side_dish_media_id"]),
                drink_style_id=int(row["drink_style_id"]),
                content=row["content"],
                variant_index=int(row["variant_index"])
                if row.get("variant_index")
                else 0,
                length=int(row["length"]) if row.get("length") else 0,
                approved=row.get("approved", "False").lower() in ("1", "true", "yes"),
                print_count=int(row["print_count"]) if row.get("print_count") else 0,
            )
            with Session(engine) as session:
                repo = TextVariantRepository(session)
                service = TextVariantService(repo)
                service.create_textvariant(tv)
    typer.echo("批次匯入完成")


def main(csv_path: str):
    # 若環境變數未設，嘗試自動尋找 schema.sql 並設置
    if not os.environ.get("LITKITCHEN_SCHEMA_PATH"):
        candidate = os.path.join(os.path.dirname(__file__), "../sql/schema.sql")
        if os.path.exists(candidate):
            os.environ["LITKITCHEN_SCHEMA_PATH"] = candidate
    import_csv(csv_path)


if __name__ == "__main__":
    typer.run(main)
