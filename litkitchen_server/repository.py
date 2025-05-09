import os
import sqlite3
from datetime import datetime
from typing import Optional

from litkitchen_server.domain import (
    BarcodeMapping,
    DrinkStyle,
    MainDishText,
    PrintJob,
    PrintJobStatus,
    SideDishMedia,
    TextVariant,
)

DB_PATH = os.environ.get(
    "LITKITCHEN_DB_PATH", os.path.join(os.path.dirname(__file__), "../db.sqlite3")
)

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()


def init_db():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS maindishtexts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author_name TEXT,
        work_title TEXT,
        main_dish TEXT,
        publisher TEXT,
        genre TEXT,
        description TEXT
    )"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS sidedishmedias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        media_type TEXT,
        side_dish TEXT
    )"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS drinkstyles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        style TEXT,
        drink TEXT
    )"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS textvariants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        main_dish_text_id INTEGER,
        side_dish_media_id INTEGER,
        drink_style_id INTEGER,
        content TEXT,
        variant_index INTEGER,
        length INTEGER,
        approved BOOLEAN,
        created_at TEXT,
        print_count INTEGER
    )"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS printjobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text_variant_id INTEGER,
        status TEXT,
        created_at TEXT,
        printed_at TEXT
    )"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS barcodemappings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        barcode TEXT,
        main_dish_text_id INTEGER,
        side_dish_media_id INTEGER,
        drink_style_id INTEGER,
        description TEXT,
        created_at TEXT
    )"""
    )
    conn.commit()


init_db()


def get_maindishtexts():
    cursor.execute(
        "SELECT id, author_name, work_title, main_dish, publisher, genre, description FROM maindishtexts"
    )
    rows = cursor.fetchall()
    return [
        MainDishText(
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


def get_sidedishmedias():
    cursor.execute("SELECT id, media_type, side_dish FROM sidedishmedias")
    rows = cursor.fetchall()
    return [
        SideDishMedia(id=row[0], media_type=row[1], side_dish=row[2]) for row in rows
    ]


def get_drinkstyles():
    cursor.execute("SELECT id, style, drink FROM drinkstyles")
    rows = cursor.fetchall()
    return [DrinkStyle(id=row[0], style=row[1], drink=row[2]) for row in rows]


def get_textvariants():
    cursor.execute(
        "SELECT id, main_dish_text_id, side_dish_media_id, drink_style_id, content, variant_index, length, approved, created_at, print_count FROM textvariants"
    )
    rows = cursor.fetchall()
    return [
        TextVariant(
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


def get_printjobs():
    cursor.execute(
        "SELECT id, text_variant_id, status, created_at, printed_at FROM printjobs"
    )
    rows = cursor.fetchall()
    return [
        PrintJob(
            id=row[0],
            text_variant_id=row[1],
            status=PrintJobStatus(row[2]),
            created_at=datetime.fromisoformat(row[3]) if row[3] else datetime.now(),
            printed_at=datetime.fromisoformat(row[4]) if row[4] else None,
        )
        for row in rows
    ]


# --- MainDishText CRUD ---
def create_maindishtext(item: MainDishText) -> MainDishText:
    cursor.execute(
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
    conn.commit()
    item.id = cursor.lastrowid
    return item


def get_maindishtext(item_id: int) -> Optional[MainDishText]:
    cursor.execute(
        "SELECT id, author_name, work_title, main_dish, publisher, genre, description FROM maindishtexts WHERE id=?",
        (item_id,),
    )
    row = cursor.fetchone()
    if row:
        return MainDishText(
            id=row[0],
            author_name=row[1],
            work_title=row[2],
            main_dish=row[3],
            publisher=row[4],
            genre=row[5],
            description=row[6] or "",
        )
    return None


def update_maindishtext(item_id: int, item: MainDishText) -> bool:
    cursor.execute(
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
    conn.commit()
    return cursor.rowcount > 0


def delete_maindishtext(item_id: int) -> bool:
    cursor.execute("DELETE FROM maindishtexts WHERE id=?", (item_id,))
    conn.commit()
    return cursor.rowcount > 0


# --- SideDishMedia CRUD ---
def create_sidedishmedia(item: SideDishMedia) -> SideDishMedia:
    cursor.execute(
        "INSERT INTO sidedishmedias (media_type, side_dish) VALUES (?, ?)",
        (item.media_type, item.side_dish),
    )
    conn.commit()
    item.id = cursor.lastrowid
    return item


def get_sidedishmedia(item_id: int) -> Optional[SideDishMedia]:
    cursor.execute(
        "SELECT id, media_type, side_dish FROM sidedishmedias WHERE id=?", (item_id,)
    )
    row = cursor.fetchone()
    if row:
        return SideDishMedia(id=row[0], media_type=row[1], side_dish=row[2])
    return None


def update_sidedishmedia(item_id: int, item: SideDishMedia) -> bool:
    cursor.execute(
        "UPDATE sidedishmedias SET media_type=?, side_dish=? WHERE id=?",
        (item.media_type, item.side_dish, item_id),
    )
    conn.commit()
    return cursor.rowcount > 0


def delete_sidedishmedia(item_id: int) -> bool:
    cursor.execute("DELETE FROM sidedishmedias WHERE id=?", (item_id,))
    conn.commit()
    return cursor.rowcount > 0


# --- DrinkStyle CRUD ---
def create_drinkstyle(item: DrinkStyle) -> DrinkStyle:
    cursor.execute(
        "INSERT INTO drinkstyles (style, drink) VALUES (?, ?)", (item.style, item.drink)
    )
    conn.commit()
    item.id = cursor.lastrowid
    return item


def get_drinkstyle(item_id: int) -> Optional[DrinkStyle]:
    cursor.execute("SELECT id, style, drink FROM drinkstyles WHERE id=?", (item_id,))
    row = cursor.fetchone()
    if row:
        return DrinkStyle(id=row[0], style=row[1], drink=row[2])
    return None


def update_drinkstyle(item_id: int, item: DrinkStyle) -> bool:
    cursor.execute(
        "UPDATE drinkstyles SET style=?, drink=? WHERE id=?",
        (item.style, item.drink, item_id),
    )
    conn.commit()
    return cursor.rowcount > 0


def delete_drinkstyle(item_id: int) -> bool:
    cursor.execute("DELETE FROM drinkstyles WHERE id=?", (item_id,))
    conn.commit()
    return cursor.rowcount > 0


# --- TextVariant CRUD ---
def create_textvariant(item: TextVariant) -> TextVariant:
    cursor.execute(
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
    conn.commit()
    item.id = cursor.lastrowid
    return item


def get_textvariant(item_id: int) -> Optional[TextVariant]:
    cursor.execute(
        "SELECT id, main_dish_text_id, side_dish_media_id, drink_style_id, content, variant_index, length, approved, created_at, print_count FROM textvariants WHERE id=?",
        (item_id,),
    )
    row = cursor.fetchone()
    if row:
        return TextVariant(
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


def update_textvariant(item_id: int, item: TextVariant) -> bool:
    cursor.execute(
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
    conn.commit()
    return cursor.rowcount > 0


def delete_textvariant(item_id: int) -> bool:
    cursor.execute("DELETE FROM textvariants WHERE id=?", (item_id,))
    conn.commit()
    return cursor.rowcount > 0


# --- PrintJob CRUD ---
def create_printjob(item: PrintJob) -> PrintJob:
    cursor.execute(
        "INSERT INTO printjobs (text_variant_id, status, created_at, printed_at) VALUES (?, ?, ?, ?)",
        (
            item.text_variant_id,
            item.status.value,
            item.created_at.isoformat(),
            item.printed_at.isoformat() if item.printed_at else None,
        ),
    )
    conn.commit()
    item.id = cursor.lastrowid
    return item


def get_printjob(item_id: int) -> Optional[PrintJob]:
    cursor.execute(
        "SELECT id, text_variant_id, status, created_at, printed_at FROM printjobs WHERE id=?",
        (item_id,),
    )
    row = cursor.fetchone()
    if row:
        return PrintJob(
            id=row[0],
            text_variant_id=row[1],
            status=PrintJobStatus(row[2]),
            created_at=datetime.fromisoformat(row[3]) if row[3] else datetime.now(),
            printed_at=datetime.fromisoformat(row[4]) if row[4] else None,
        )
    return None


def update_printjob(item_id: int, item: PrintJob) -> bool:
    cursor.execute(
        "UPDATE printjobs SET text_variant_id=?, status=?, created_at=?, printed_at=? WHERE id=?",
        (
            item.text_variant_id,
            item.status.value,
            item.created_at.isoformat(),
            item.printed_at.isoformat() if item.printed_at else None,
            item_id,
        ),
    )
    conn.commit()
    return cursor.rowcount > 0


def delete_printjob(item_id: int) -> bool:
    cursor.execute("DELETE FROM printjobs WHERE id=?", (item_id,))
    conn.commit()
    return cursor.rowcount > 0


# --- BarcodeMapping CRUD ---
def create_barcodemapping(item: BarcodeMapping) -> BarcodeMapping:
    cursor.execute(
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
    conn.commit()
    item.id = cursor.lastrowid
    return item


def get_barcodemapping(item_id: int) -> Optional[BarcodeMapping]:
    cursor.execute(
        "SELECT id, barcode, main_dish_text_id, side_dish_media_id, drink_style_id, description, created_at FROM barcodemappings WHERE id=?",
        (item_id,),
    )
    row = cursor.fetchone()
    if row:
        return BarcodeMapping(
            id=row[0],
            barcode=row[1],
            main_dish_text_id=row[2],
            side_dish_media_id=row[3],
            drink_style_id=row[4],
            description=row[5] or "",
            created_at=datetime.fromisoformat(row[6]) if row[6] else datetime.now(),
        )
    return None


def update_barcodemapping(item_id: int, item: BarcodeMapping) -> bool:
    cursor.execute(
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
    conn.commit()
    return cursor.rowcount > 0


def delete_barcodemapping(item_id: int) -> bool:
    cursor.execute("DELETE FROM barcodemappings WHERE id=?", (item_id,))
    conn.commit()
    return cursor.rowcount > 0
