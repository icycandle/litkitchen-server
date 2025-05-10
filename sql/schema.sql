-- LitKitchen SQLite Schema (auto-generated)

CREATE TABLE IF NOT EXISTS maindishtexts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_name TEXT,
    work_title TEXT,
    main_dish TEXT,
    publisher TEXT,
    genre TEXT,
    description TEXT
);

CREATE TABLE IF NOT EXISTS sidedishmedias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    media_type TEXT,
    side_dish TEXT
);

CREATE TABLE IF NOT EXISTS drinkstyles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    style TEXT,
    drink TEXT
);

CREATE TABLE IF NOT EXISTS textvariants (
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
);

CREATE TABLE IF NOT EXISTS printjobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text_variant_id INTEGER,
    status TEXT,
    created_at TEXT,
    printed_at TEXT
);

CREATE TABLE IF NOT EXISTS barcodemappings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    barcode TEXT,
    main_dish_text_id INTEGER,
    side_dish_media_id INTEGER,
    drink_style_id INTEGER,
    description TEXT,
    created_at TEXT
);

-- Indexes for query optimization
CREATE INDEX IF NOT EXISTS idx_textvariant_keys ON textvariants (main_dish_text_id, side_dish_media_id, drink_style_id);
CREATE INDEX IF NOT EXISTS idx_printjob_text_variant_id ON printjobs (text_variant_id);
CREATE UNIQUE INDEX IF NOT EXISTS idx_barcode_unique ON barcodemappings (barcode);
