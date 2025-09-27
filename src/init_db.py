import sqlite3

def init_db():
    conn = sqlite3.connect("data/products.db")
    cursor = conn.cursor()

    # Maak tabel
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS producten (
        code TEXT PRIMARY KEY,
        naam TEXT NOT NULL,
        prijs REAL NOT NULL,
        co2_score REAL
    )
    """)

    # Voeg testproducten toe
    producten = [
        ("1001", "Broodje kaas", 2.50, 0.35),
        ("1002", "Koffie", 1.80, 0.10),
        ("1003", "Frisdrank", 2.00, 0.50)
    ]
    cursor.executemany("INSERT OR IGNORE INTO producten VALUES (?, ?, ?, ?)", producten)

    conn.commit()
    conn.close()
    print("Database aangemaakt en gevuld!")

if __name__ == "__main__":
    init_db()