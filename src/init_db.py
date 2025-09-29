import sqlite3

def init_db():
    conn = sqlite3.connect("data/products.db")
    cursor = conn.cursor()

    # Verwijder oude tabel als die nog bestaat
    cursor.execute("DROP TABLE IF EXISTS producten")

    # Maak tabel
    cursor.execute("""
    CREATE TABLE producten (
        code TEXT PRIMARY KEY,
        categorie TEXT NOT NULL,
        naam TEXT NOT NULL,
        prijs REAL NOT NULL,
        co2_score REAL
    )
    """)

    # Voeg testproducten toe
    producten = [
        ("1001", "Broodjes", "Broodje kaas", 2.50, 0.35),
        ("1002", "Warme dranken", "Koffie", 1.80, 0.10),
        ("1003", "Frisranken", "Cola", 2.00, 0.50)
    ]
    cursor.executemany("INSERT OR IGNORE INTO producten VALUES (?, ?, ?, ?, ?)", producten)

    conn.commit()

    for row in cursor.execute("SELECT * FROM producten"):
        print(row)

    conn.close()
    print("Database aangemaakt en gevuld!")

if __name__ == "__main__":
    init_db()