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
        ("1001", "Warme dranken", "Koffie", 1.20, 2),
        ("1002", "Warme dranken", "Thee", 1.20, 8),
        ("2001", "Koude dranken", "Cola", 2.00, 5),
        ("2002", "Koude dranken", "Spa blauw", 1.50, 7),
        ("2003", "Koude dranken", "Cola", 2.00, 5),
        ("2004", "Koude dranken", "Ice Tea", 2.00, 5),
        ("3001", "Broodjes", "Broodje kaas", 2.50, 4),
        ("3002", "Broodjes", "Broodje Ham", 2.50, 4),
        ("3003", "Broodjes", "Broodje Gezond", 3.00, 4),
        ("3004", "Broodjes", "Broodje Gehaktbal", 2.90, 4),
        ("4001", "Warme gerechten", "Panini Ham & Kaas", 3.20, 4)
    ]
    cursor.executemany("INSERT OR IGNORE INTO producten VALUES (?, ?, ?, ?, ?)", producten)

    conn.commit()

    for row in cursor.execute("SELECT * FROM producten"):
        print(row)

    conn.close()
    print("Database aangemaakt en gevuld!")

if __name__ == "__main__":
    init_db()