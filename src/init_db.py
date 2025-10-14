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
        ("1002", "Warme dranken", "Cappuccino", 2.20, 4),
        ("1003", "Warme dranken", "Espresso", 1.50, 3),
        ("1004", "Warme dranken", "Latte macchiato", 2.40, 5),
        ("1005", "Warme dranken", "Thee", 1.20, 8),
        ("1006", "Warme dranken", "Verse muntthee", 1.80, 9),
        ("1007", "Warme dranken", "Warme chocomel", 1.20, 6),
        ("1008", "Warme dranken", "Warme chocomel met slagroom", 1.80, 5),

        ("2001", "Koude dranken", "Spa blauw", 1.50, 7),
        ("2002", "Koude dranken", "Spa rood", 1.50, 7),
        ("2003", "Koude dranken", "Cola", 2.00, 5),
        ("2004", "Koude dranken", "Sprite", 2.00, 5),
        ("2005", "Koude dranken", "Fanta", 2.00, 5),
        ("2006", "Koude dranken", "Ice tea", 2.00, 5),

        ("5001", "Broodjes", "Broodje kaas", 2.50, 6),
        ("5002", "Broodjes", "Broodje ham", 2.50, 5),
        ("5003", "Broodjes", "Broodje gezond", 3.00, 4),
        ("5004", "Broodjes", "Broodje gehaktbal", 2.90, 5),
        ("5005", "Broodjes", "Broodje carpaccio", 3.20, 4),
        ("5006", "Broodjes", "Broodje kipfilet", 2.90, 5),
        ("5007", "Broodjes", "Broodje tonijnsalade", 3.10, 4),
        ("5101", "Broodjes", "Panini ham & kaas", 3.20, 4),
        ("5102", "Broodjes", "Panini tomaat mozarella", 3.40, 4),
        ("5103", "Broodjes", "Panini big mac", 3.60, 4),

        ("6001", "Snacks koud", "Appel", 0.70, 8),
        ("6002", "Snacks koud", "Peer", 0.70, 8),
        ("6003", "Snacks koud", "Banaan", 0.70, 8),
        ("6004", "Snacks koud", "Yoghurt aardbei", 1.20, 6),
        ("6005", "Snacks koud", "Yoghurt bosbes", 1.20, 6),
        ("6006", "Snacks koud", "Yoghurt perzik", 1.20, 6),

        ("7001", "Snacks warm", "Frikandel", 1.00, 4),
        ("7002", "Snacks warm", "Kroket", 1.20, 4),
        ("7003", "Snacks warm", "Frikandelbroodje", 1.90, 4),
        ("7004", "Snacks warm", "Saucijzenbroodje", 1.80, 4),
        ("7005", "Snacks warm", "Kaasbroodje", 1.90, 6),
        ("7006", "Snacks warm", "Kaassoufflé", 1.50, 5),


        ("8001", "Maaltijden", "Tomatensoep", 2.90, 5),
        ("8002", "Maaltijden", "Groentesoep", 2.90, 5),
        ("8003", "Maaltijden", "Pompoensoep", 2.90, 5),
        ("8004", "Maaltijden", "Kippensoep", 2.90, 5),

        ("9001", "Zoet & gebak", "Muffin chocolade", 1.60, 4),
        ("9002", "Zoet & gebak", "Muffin aardbei", 1.60, 6),
        ("9003", "Zoet & gebak", "Brownie", 2.40, 4),
        ("9004", "Zoet & gebak", "Koekje wit", 1.60, 3),
        ("9005", "Zoet & gebak", "Koekje puur", 1.60, 3),
        ("9006", "Zoet & gebak", "Appeltaart", 3.20, 6)
    ]
    cursor.executemany("INSERT OR IGNORE INTO producten VALUES (?, ?, ?, ?, ?)", producten)

    conn.commit()

    for row in cursor.execute("SELECT * FROM producten"):
        print(row)

    conn.close()
    print("Database aangemaakt en gevuld!")

if __name__ == "__main__":
    init_db()