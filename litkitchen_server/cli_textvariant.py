import typer
import csv
from pathlib import Path
from litkitchen_server.repository import create_textvariant
from litkitchen_server.models import TextVariant


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
            tv = TextVariant(
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
            create_textvariant(tv)
    typer.echo("批次匯入完成")


if __name__ == "__main__":
    typer.run(import_csv)
