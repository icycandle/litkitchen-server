import os
import sqlite3
import pytest
from pathlib import Path


@pytest.mark.e2e
def test_cli_import_textvariant(tmp_path):
    # 準備乾淨的 DB 與 fixture
    test_db = tmp_path / "test.sqlite3"
    test_csv = Path(__file__).parent / "fixtures" / "example_textvariant.csv"
    # 複製 schema.sql 並初始化
    schema_sql = Path(__file__).parent.parent / "sql" / "schema.sql"
    db_path = str(test_db)
    os.environ["LITKITCHEN_DB_PATH"] = db_path
    conn = sqlite3.connect(db_path)
    with open(schema_sql, "r", encoding="utf-8") as f:
        sql_script = f.read()
    for stmt in sql_script.split(";"):
        if stmt.strip():
            conn.execute(stmt)
    conn.commit()
    conn.close()

    # 執行 CLI（用 subprocess 以便 debug）
    import subprocess

    result = subprocess.run(
        [
            "poetry",
            "run",
            "python",
            "-m",
            "litkitchen_server.cli_textvariant",
            str(test_csv),
        ],
        capture_output=True,
        text=True,
    )
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    assert result.returncode == 0

    # 驗證資料寫入
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT main_dish_text_id,side_dish_media_id,drink_style_id,content,variant_index,length,approved,print_count FROM textvariants ORDER BY id"
    )
    rows = cursor.fetchall()
    assert len(rows) == 3
    assert rows[0][0:4] == (1, 10, 100, "示例內容一")
    assert rows[1][0:4] == (2, 20, 200, "示例內容二")
    assert rows[2][0:4] == (3, 30, 300, "Another Example")
    assert rows[0][6] == 1  # approved True
    assert rows[1][6] == 0  # approved False
    assert rows[2][6] == 1
    conn.close()
