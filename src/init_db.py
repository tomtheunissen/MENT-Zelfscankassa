import sqlite3
from pathlib import Path

def init_db():
    """functie om de database te creëeren"""
    # maak een pad dat werkt ongeacht waar je het script start
    project_root = Path(__file__).resolve().parents[1]  # .../Zelfscankassa
    db_path = project_root / "data" / "products.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)  # zorg dat /data bestaat

    conn = sqlite3.connect(db_path)  # was: "data/products.db"
    cursor = conn.cursor()
    
    # Verwijder oude tabel als die nog bestaat
    cursor.execute("DROP TABLE IF EXISTS producten")

    # Maakt tabel
    cursor.execute("""
    CREATE TABLE producten (
        code TEXT PRIMARY KEY NOT NULL, 
        categorie TEXT NOT NULL,
        naam TEXT NOT NULL,
        prijs REAL NOT NULL,
        co2_score REAL,
        afbeelding_url TEXT 
    )
    """)

    # De proef database met voorbeeldproducten
    producten = [
        ("1001", "Warme dranken", "Koffie", 1.20, 2, None),
        ("1002", "Warme dranken", "Cappuccino", 2.20, 4, None),
        ("1003", "Warme dranken", "Espresso", 1.50, 3, None),
        ("1004", "Warme dranken", "Latte macchiato", 2.40, 5, None),
        ("1005", "Warme dranken", "Thee", 1.20, 8, None),
        ("1006", "Warme dranken", "Verse muntthee", 1.80, 9, None),
        ("1007", "Warme dranken", "Warme chocomel", 1.20, 6, None),
        ("1008", "Warme dranken", "Warme chocomel met slagroom", 1.80, 5, None),

        ("2001", "Koude dranken", "Spa blauw", 1.50, 7, None),
        ("2002", "Koude dranken", "Spa rood", 1.50, 7, None),
        ("2003", "Koude dranken", "Cola", 2.00, 5, None),
        ("2004", "Koude dranken", "Sprite", 2.00, 5, None),
        ("2005", "Koude dranken", "Fanta", 2.00, 5, None),
        ("2006", "Koude dranken", "Ice tea", 2.00, 5, None),

        ("5001", "Broodjes", "Broodje kaas", 3.50, 6, None),
        ("5002", "Broodjes", "Broodje ham", 3.50, 5, None),
        ("5003", "Broodjes", "Broodje ham en kaas", 3.70, 4, None),
        ("5004", "Broodjes", "Broodje gezond", 4.00, 4, None),
        ("5005", "Broodjes", "Broodje gehaktbal", 3.90, 5, None),
        ("5006", "Broodjes", "Broodje carpaccio", 4.20, 4, None),
        ("5007", "Broodjes", "Broodje kipfilet", 3.90, 5, None),
        ("5008", "Broodjes", "Broodje tonijn", 4.10, 4, None),
        ("5009", "Broodjes", "Broodje kip krokant", 4.00, 3, None),
        ("5010", "Broodjes", "Broodje blt", 4.50, 4, None),
        ("5011", "Broodjes", "Broodje eiersalade", 3.60, 3, None),
        ("5101", "Broodjes", "Panini ham & kaas", 3.90, 4, None),
        ("5102", "Broodjes", "Panini tomaat mozarella", 3.90, 4, None),
        ("5103", "Broodjes", "Panini big mac", 3.90, 4, None),

        ("6001", "Snacks warm", "Frikandel", 1.00, 4, None),
        ("6002", "Snacks warm", "Kroket", 1.20, 4, None),
        ("6003", "Snacks warm", "Frikandelbroodje", 1.90, 4, None),
        ("6004", "Snacks warm", "Saucijzenbroodje", 1.80, 4, None),
        ("6005", "Snacks warm", "Kaasbroodje", 1.90, 6, None),
        ("6006", "Snacks warm", "Kaassoufflé", 1.50, 5, None),

        ("7001", "Snacks koud", "Appel", 0.70, 8, None),
        ("7002", "Snacks koud", "Peer", 0.70, 8, None),
        ("7003", "Snacks koud", "Banaan", 0.70, 8, None),
        ("7004", "Snacks koud", "Yoghurt aardbei", 1.20, 6, None),
        ("7005", "Snacks koud", "Yoghurt bosbes", 1.20, 6, None),
        ("7006", "Snacks koud", "Yoghurt perzik", 1.20, 6, None),


        ("8001", "Maaltijden", "Tomatensoep", 2.90, 5, None),
        ("8002", "Maaltijden", "Groentesoep", 2.90, 5, None),
        ("8003", "Maaltijden", "Pompoensoep", 2.90, 5, None),
        ("8004", "Maaltijden", "Kippensoep", 2.90, 5, None),

        ("9001", "Zoet & gebak", "Muffin chocolade", 1.60, 4, None),
        ("9002", "Zoet & gebak", "Muffin aardbei", 1.60, 6, None),
        ("9003", "Zoet & gebak", "Brownie", 2.40, 4, None),
        ("9004", "Zoet & gebak", "Koekje wit", 1.60, 3, None),
        ("9005", "Zoet & gebak", "Koekje puur", 1.60, 3, None),
        ("9006", "Zoet & gebak", "Appeltaart", 3.20, 6, None)
    ]
    # voegt de producten toe aan de databse
    cursor.executemany("INSERT OR IGNORE INTO producten VALUES (?, ?, ?, ?, ?, ?)", producten)

    conn.commit() # slaat de wijzigingen op

    # print de databse als controle
    for row in cursor.execute("SELECT * FROM producten"):
        print(row)

    # beëindigt verbinding met database
    conn.close()
    print("Database aangemaakt en gevuld!")

if __name__ == "__main__":
    init_db()