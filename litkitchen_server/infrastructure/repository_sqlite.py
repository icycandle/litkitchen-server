import os
import sqlite3
from datetime import datetime
from typing import Optional

from litkitchen_server.domain.models import PrintJobStatus
from litkitchen_server.infrastructure.models import (
    BarcodeMappingOrm,
    DrinkStyleOrm,
    MainDishTextOrm,
    PrintJobOrm,
    SideDishMediaOrm,
    TextVariantOrm,
)

DB_PATH = os.environ.get(
    "LITKITCHEN_DB_PATH", os.path.join(os.path.dirname(__file__), "../db.sqlite3")
)


class SqliteRepository:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or os.environ.get(
            "LITKITCHEN_DB_PATH",
            os.path.join(os.path.dirname(__file__), "../db.sqlite3"),
        )
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        schema_path = os.environ.get(
            "LITKITCHEN_SCHEMA_PATH",
            os.path.join(os.path.dirname(__file__), "../sql/schema.sql"),
        )
        with open(schema_path, "r", encoding="utf-8") as f:
            sql_script = f.read()
        for stmt in sql_script.split(";"):
            if stmt.strip():
                self.cursor.execute(stmt)
        self.conn.commit()

    # --- MainDishText ---
    def get_maindishtexts(self):
        self.cursor.execute(
            "SELECT id, author_name, work_title, main_dish, publisher, genre, description FROM maindishtexts"
        )
        rows = self.cursor.fetchall()
        return [
            MainDishTextOrm(
                id=row[0],
                author_name=row[1],
                work_title=row[2],
                main_dish=row[3],
                publisher=row[4],
                genre=row[5],
                description=row[6] or "",
            )
            for row in rows
        ]

    def create_maindishtext(self, item: MainDishTextOrm) -> MainDishTextOrm:
        self.cursor.execute(
            """
            INSERT INTO maindishtexts (author_name, work_title, main_dish, publisher, genre, description)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (
                item.author_name,
                item.work_title,
                item.main_dish,
                item.publisher,
                item.genre,
                item.description,
            ),
        )
        self.conn.commit()
        item.id = self.cursor.lastrowid
        return item

    def get_maindishtext(self, item_id: int) -> Optional[MainDishTextOrm]:
        self.cursor.execute(
            "SELECT id, author_name, work_title, main_dish, publisher, genre, description FROM maindishtexts WHERE id=?",
            (item_id,),
        )
        row = self.cursor.fetchone()
        if row:
            return MainDishTextOrm(
                id=row[0],
                author_name=row[1],
                work_title=row[2],
                main_dish=row[3],
                publisher=row[4],
                genre=row[5],
                description=row[6] or "",
            )
        return None

    def update_maindishtext(self, item_id: int, item: MainDishTextOrm) -> bool:
        self.cursor.execute(
            """
            UPDATE maindishtexts SET author_name=?, work_title=?, main_dish=?, publisher=?, genre=?, description=? WHERE id=?""",
            (
                item.author_name,
                item.work_title,
                item.main_dish,
                item.publisher,
                item.genre,
                item.description,
                item_id,
            ),
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_maindishtext(self, item_id: int) -> bool:
        self.cursor.execute("DELETE FROM maindishtexts WHERE id=?", (item_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    # --- SideDishMedia ---
    def get_sidedishmedias(self):
        self.cursor.execute("SELECT id, media_type, side_dish FROM sidedishmedias")
        rows = self.cursor.fetchall()
        return [
            SideDishMediaOrm(id=row[0], media_type=row[1], side_dish=row[2])
            for row in rows
        ]

    def create_sidedishmedia(self, item: SideDishMediaOrm) -> SideDishMediaOrm:
        self.cursor.execute(
            "INSERT INTO sidedishmedias (media_type, side_dish) VALUES (?, ?)",
            (item.media_type, item.side_dish),
        )
        self.conn.commit()
        item.id = self.cursor.lastrowid
        return item

    def get_sidedishmedia(self, item_id: int) -> Optional[SideDishMediaOrm]:
        self.cursor.execute(
            "SELECT id, media_type, side_dish FROM sidedishmedias WHERE id=?",
            (item_id,),
        )
        row = self.cursor.fetchone()
        if row:
            return SideDishMediaOrm(id=row[0], media_type=row[1], side_dish=row[2])
        return None

    def update_sidedishmedia(self, item_id: int, item: SideDishMediaOrm) -> bool:
        self.cursor.execute(
            "UPDATE sidedishmedias SET media_type=?, side_dish=? WHERE id=?",
            (item.media_type, item.side_dish, item_id),
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_sidedishmedia(self, item_id: int) -> bool:
        self.cursor.execute("DELETE FROM sidedishmedias WHERE id=?", (item_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    # --- DrinkStyle ---
    def get_drinkstyles(self):
        self.cursor.execute("SELECT id, style, drink FROM drinkstyles")
        rows = self.cursor.fetchall()
        return [DrinkStyleOrm(id=row[0], style=row[1], drink=row[2]) for row in rows]

    def create_drinkstyle(self, item: DrinkStyleOrm) -> DrinkStyleOrm:
        self.cursor.execute(
            "INSERT INTO drinkstyles (style, drink) VALUES (?, ?)",
            (item.style, item.drink),
        )
        self.conn.commit()
        item.id = self.cursor.lastrowid
        return item

    def get_drinkstyle(self, item_id: int) -> Optional[DrinkStyleOrm]:
        self.cursor.execute(
            "SELECT id, style, drink FROM drinkstyles WHERE id=?",
            (item_id,),
        )
        row = self.cursor.fetchone()
        if row:
            return DrinkStyleOrm(id=row[0], style=row[1], drink=row[2])
        return None

    def update_drinkstyle(self, item_id: int, item: DrinkStyleOrm) -> bool:
        self.cursor.execute(
            "UPDATE drinkstyles SET style=?, drink=? WHERE id=?",
            (item.style, item.drink, item_id),
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_drinkstyle(self, item_id: int) -> bool:
        self.cursor.execute("DELETE FROM drinkstyles WHERE id=?", (item_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    # --- TextVariant ---
    def get_textvariants(self):
        self.cursor.execute(
            "SELECT id, main_dish_text_id, side_dish_media_id, drink_style_id, content, variant_index, length, approved, created_at, print_count FROM textvariants"
        )
        rows = self.cursor.fetchall()
        return [
            TextVariantOrm(
                id=row[0],
                main_dish_text_id=row[1],
                side_dish_media_id=row[2],
                drink_style_id=row[3],
                content=row[4],
                variant_index=row[5],
                length=row[6],
                approved=bool(row[7]),
                created_at=datetime.fromisoformat(row[8]) if row[8] else datetime.now(),
                print_count=row[9],
            )
            for row in rows
        ]

    def create_textvariant(self, item: TextVariantOrm) -> TextVariantOrm:
        self.cursor.execute(
            """
            INSERT INTO textvariants (main_dish_text_id, side_dish_media_id, drink_style_id, content, variant_index, length, approved, created_at, print_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                item.main_dish_text_id,
                item.side_dish_media_id,
                item.drink_style_id,
                item.content,
                item.variant_index,
                item.length,
                int(item.approved),
                item.created_at.isoformat(),
                item.print_count,
            ),
        )
        self.conn.commit()
        item.id = self.cursor.lastrowid
        return item

    def get_textvariant(self, item_id: int) -> Optional[TextVariantOrm]:
        self.cursor.execute(
            "SELECT id, main_dish_text_id, side_dish_media_id, drink_style_id, content, variant_index, length, approved, created_at, print_count FROM textvariants WHERE id=?",
            (item_id,),
        )
        row = self.cursor.fetchone()
        if row:
            return TextVariantOrm(
                id=row[0],
                main_dish_text_id=row[1],
                side_dish_media_id=row[2],
                drink_style_id=row[3],
                content=row[4],
                variant_index=row[5],
                length=row[6],
                approved=bool(row[7]),
                created_at=datetime.fromisoformat(row[8]) if row[8] else datetime.now(),
                print_count=row[9],
            )
        return None

    def update_textvariant(self, item_id: int, item: TextVariantOrm) -> bool:
        self.cursor.execute(
            """
            UPDATE textvariants SET main_dish_text_id=?, side_dish_media_id=?, drink_style_id=?, content=?, variant_index=?, length=?, approved=?, created_at=?, print_count=? WHERE id=?""",
            (
                item.main_dish_text_id,
                item.side_dish_media_id,
                item.drink_style_id,
                item.content,
                item.variant_index,
                item.length,
                int(item.approved),
                item.created_at.isoformat(),
                item.print_count,
                item_id,
            ),
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_textvariant(self, item_id: int) -> bool:
        self.cursor.execute("DELETE FROM textvariants WHERE id=?", (item_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    # --- PrintJob ---
    def get_printjobs(self):
        self.cursor.execute(
            "SELECT id, text_variant_id, status, created_at, printed_at FROM printjobs"
        )
        rows = self.cursor.fetchall()
        return [
            PrintJobOrm(
                id=row[0],
                text_variant_id=row[1],
                status=PrintJobStatus(row[2]),
                created_at=datetime.fromisoformat(row[3]) if row[3] else datetime.now(),
                printed_at=datetime.fromisoformat(row[4]) if row[4] else None,
            )
            for row in rows
        ]

    def create_printjob(self, item: PrintJobOrm) -> PrintJobOrm:
        self.cursor.execute(
            "INSERT INTO printjobs (text_variant_id, status, created_at, printed_at) VALUES (?, ?, ?, ?)",
            (
                item.text_variant_id,
                item.status.value,
                item.created_at.isoformat(),
                item.printed_at.isoformat() if item.printed_at else None,
            ),
        )
        self.conn.commit()
        item.id = self.cursor.lastrowid
        return item

    def get_printjob(self, item_id: int) -> Optional[PrintJobOrm]:
        self.cursor.execute(
            "SELECT id, text_variant_id, status, created_at, printed_at FROM printjobs WHERE id=?",
            (item_id,),
        )
        row = self.cursor.fetchone()
        if row:
            return PrintJobOrm(
                id=row[0],
                text_variant_id=row[1],
                status=PrintJobStatus(row[2]),
                created_at=datetime.fromisoformat(row[3]) if row[3] else datetime.now(),
                printed_at=datetime.fromisoformat(row[4]) if row[4] else None,
            )
        return None

    def update_printjob(self, item_id: int, item: PrintJobOrm) -> bool:
        self.cursor.execute(
            "UPDATE printjobs SET text_variant_id=?, status=?, created_at=?, printed_at=? WHERE id=?",
            (
                item.text_variant_id,
                item.status.value,
                item.created_at.isoformat(),
                item.printed_at.isoformat() if item.printed_at else None,
                item_id,
            ),
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_printjob(self, item_id: int) -> bool:
        self.cursor.execute("DELETE FROM printjobs WHERE id=?", (item_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    # --- BarcodeMapping ---
    def get_barcodemappings(self):
        self.cursor.execute(
            "SELECT id, barcode, main_dish_text_id, side_dish_media_id, drink_style_id, description, created_at FROM barcodemappings"
        )
        rows = self.cursor.fetchall()
        return [
            BarcodeMappingOrm(
                id=row[0],
                barcode=row[1],
                main_dish_text_id=row[2],
                side_dish_media_id=row[3],
                drink_style_id=row[4],
                description=row[5] or "",
                created_at=datetime.fromisoformat(row[6]) if row[6] else datetime.now(),
            )
            for row in rows
        ]

    def create_barcodemapping(self, item: BarcodeMappingOrm) -> BarcodeMappingOrm:
        self.cursor.execute(
            "INSERT INTO barcodemappings (barcode, main_dish_text_id, side_dish_media_id, drink_style_id, description, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (
                item.barcode,
                item.main_dish_text_id,
                item.side_dish_media_id,
                item.drink_style_id,
                item.description,
                item.created_at.isoformat(),
            ),
        )
        self.conn.commit()
        item.id = self.cursor.lastrowid
        return item

    def get_barcodemapping(self, item_id: int) -> Optional[BarcodeMappingOrm]:
        self.cursor.execute(
            "SELECT id, barcode, main_dish_text_id, side_dish_media_id, drink_style_id, description, created_at FROM barcodemappings WHERE id=?",
            (item_id,),
        )
        row = self.cursor.fetchone()
        if row:
            return BarcodeMappingOrm(
                id=row[0],
                barcode=row[1],
                main_dish_text_id=row[2],
                side_dish_media_id=row[3],
                drink_style_id=row[4],
                description=row[5] or "",
                created_at=datetime.fromisoformat(row[6]) if row[6] else datetime.now(),
            )
        return None

    def update_barcodemapping(self, item_id: int, item: BarcodeMappingOrm) -> bool:
        self.cursor.execute(
            "UPDATE barcodemappings SET barcode=?, main_dish_text_id=?, side_dish_media_id=?, drink_style_id=?, description=?, created_at=? WHERE id=?",
            (
                item.barcode,
                item.main_dish_text_id,
                item.side_dish_media_id,
                item.drink_style_id,
                item.description,
                item.created_at.isoformat(),
                item_id,
            ),
        )
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_barcodemapping(self, item_id: int) -> bool:
        self.cursor.execute("DELETE FROM barcodemappings WHERE id=?", (item_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0
