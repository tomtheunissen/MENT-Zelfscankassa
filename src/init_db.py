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
        co2_uitstoot REAL,
        afbeelding_url TEXT 
    )
    """)

    producten = [
        # Warme dranken — CO2 in kg CO2e per portie
        ("1001", "Warme dranken", "Koffie", 1.20, 0.25, "src/static/img/products/warme_dranken/koffie.webp"),
        ("1002", "Warme dranken", "Cappuccino", 2.20, 0.55, "src/static/img/products/warme_dranken/cappuccino.webp"),
        ("1003", "Warme dranken", "Espresso", 1.50, 0.18, "src/static/img/products/warme_dranken/espresso.webp"),
        ("1004", "Warme dranken", "Latte macchiato", 2.40, 0.60, "src/static/img/products/warme_dranken/latte_macchiato.webp"),
        ("1005", "Warme dranken", "Thee", 1.20, 0.03, "src/static/img/products/warme_dranken/thee.webp"),
        ("1006", "Warme dranken", "Verse muntthee", 1.80, 0.05, "src/static/img/products/warme_dranken/verse_muntthee.webp"),
        ("1007", "Warme dranken", "Warme chocomel", 1.20, 0.45, "src/static/img/products/warme_dranken/warme_chocomel.webp"),
        ("1008", "Warme dranken", "Warme chocomel met slagroom", 1.80, 0.55, "src/static/img/products/warme_dranken/warme_chocomel_slagroom.webp"),

        # Koude dranken — fles/blikje 330–500 ml
        ("2001", "Koude dranken", "Spa blauw", 1.50, 0.20, "src/static/img/products/koude_dranken/spa_blauw.webp"),
        ("2002", "Koude dranken", "Spa rood", 1.50, 0.20, "src/static/img/products/koude_dranken/spa_rood.webp"),
        ("2003", "Koude dranken", "Cola", 2.00, 0.25, "src/static/img/products/koude_dranken/cola.webp"),
        ("2004", "Koude dranken", "Sprite", 2.00, 0.25, "src/static/img/products/koude_dranken/sprite.webp"),
        ("2005", "Koude dranken", "Fanta", 2.00, 0.25, "src/static/img/products/koude_dranken/fanta.webp"),
        ("2006", "Koude dranken", "Ice tea", 2.00, 0.30, "src/static/img/products/koude_dranken/ice_tea.webp"),

        # Broodjes — standaard belegde broodjes
        ("5001", "Broodjes", "Broodje kaas", 3.50, 0.60, "src/static/img/products/broodjes/broodje_kaas.webp"),
        ("5002", "Broodjes", "Broodje ham", 3.50, 0.70, "src/static/img/products/broodjes/broodje_ham.webp"),
        ("5003", "Broodjes", "Broodje ham en kaas", 3.70, 0.80, "src/static/img/products/broodjes/broodje_ham_kaas.webp"),
        ("5004", "Broodjes", "Broodje gezond", 4.00, 0.50, "src/static/img/products/broodjes/broodje_gezond.webp"),
        ("5005", "Broodjes", "Broodje gehaktbal", 3.90, 1.40, "src/static/img/products/broodjes/broodje_gehaktbal.webp"),
        ("5006", "Broodjes", "Broodje carpaccio", 4.20, 1.80, "src/static/img/products/broodjes/broodje_carpaccio.webp"),
        ("5007", "Broodjes", "Broodje kipfilet", 3.90, 0.90, "src/static/img/products/broodjes/broodje_kipfilet.webp"),
        ("5008", "Broodjes", "Broodje tonijn", 4.10, 1.30, "src/static/img/products/broodjes/broodje_tonijn.webp"),
        ("5009", "Broodjes", "Broodje kip krokant", 4.00, 1.10,"src/static/img/products/broodjes/broodje_kip_krokant.webp"),
        ("5010", "Broodjes", "Broodje blt", 4.50, 1.20, "src/static/img/products/broodjes/broodje_blt.webp"),
        ("5011", "Broodjes", "Broodje eiersalade", 3.60, 0.60, "src/static/img/products/broodjes/broodje_eiersalade.webp"),
        ("5101", "Broodjes", "Panini ham & kaas", 3.90, 1.00, "src/static/img/products/broodjes/panini_ham_kaas.webp"),
        ("5102", "Broodjes", "Panini tomaat mozarella", 3.90, 0.80, "src/static/img/products/broodjes/panini_tomaat_mozarella.webp"),
        ("5103", "Broodjes", "Panini big mac", 3.90, 1.50, "src/static/img/products/broodjes/panini_big_mac.webp"),

        # Snacks warm
        ("6001", "Snacks warm", "Frikandel", 1.00, 0.70, "src/static/img/products/snacks_warm/frikandel.webp"),
        ("6002", "Snacks warm", "Kroket", 1.20, 0.70, "src/static/img/products/snacks_warm/kroket.webp"),
        ("6003", "Snacks warm", "Kaassoufflé", 1.50, 0.70, "src/static/img/products/snacks_warm/kaassouffle.webp"),
        ("6004", "Snacks warm", "Frikandelbroodje", 1.90, 0.90, "src/static/img/products/snacks_warm/frikandelbroodje.webp"),
        ("6005", "Snacks warm", "Saucijzenbroodje", 1.80, 1.00, "src/static/img/products/snacks_warm/saucijzenbroodje.webp"),
        ("6006", "Snacks warm", "Kaasbroodje", 1.90, 0.80, "src/static/img/products/snacks_warm/kaasbroodje.webp"),

        # Snacks koud
        ("7001", "Snacks koud", "Appel", 0.70, 0.05, "src/static/img/products/snacks_koud/appel.webp"),
        ("7002", "Snacks koud", "Peer", 0.70, 0.05, "src/static/img/products/snacks_koud/peer.webp"),
        ("7003", "Snacks koud", "Banaan", 0.70, 0.08, "src/static/img/products/snacks_koud/banaan.webp"),
        ("7004", "Snacks koud", "Yoghurt aardbei", 1.20, 0.40, "src/static/img/products/snacks_koud/yoghurt_aardbei.webp"),
        ("7005", "Snacks koud", "Yoghurt bosbes", 1.20, 0.40, "src/static/img/products/snacks_koud/yoghurt_bosbes.webp"),
        ("7006", "Snacks koud", "Yoghurt perzik", 1.20, 0.40, "src/static/img/products/snacks_koud/yoghurt_perzik.webp"),

        # Maaltijden — soep per kom
        ("8001", "Maaltijden", "Tomatensoep", 2.90, 0.30, "src/static/img/products/maaltijden/tomatensoep.webp"),
        ("8002", "Maaltijden", "Groentesoep", 2.90, 0.30, "src/static/img/products/maaltijden/groentesoep.webp"),
        ("8003", "Maaltijden", "Pompoensoep", 2.90, 0.35, "src/static/img/products/maaltijden/pompoensoep.webp"),
        ("8004", "Maaltijden", "Kippensoep", 2.90, 0.50, "src/static/img/products/maaltijden/kippensoep.webp"),

        # Zoet & gebak — per stuk
        ("9001", "Zoet & gebak", "Muffin chocolade", 1.60, 0.50, "src/static/img/products/zoet_gebak/muffin_chocolade.webp"),
        ("9002", "Zoet & gebak", "Muffin aardbei", 1.60, 0.45, "src/static/img/products/zoet_gebak/muffin_aardbei.webp"),
        ("9003", "Zoet & gebak", "Brownie", 2.40, 0.60, "src/static/img/products/zoet_gebak/brownie.webp"),
        ("9004", "Zoet & gebak", "Koekje wit", 1.60, 0.25, "src/static/img/products/zoet_gebak/koekje_wit.webp"),
        ("9005", "Zoet & gebak", "Koekje puur", 1.60, 0.25, "src/static/img/products/zoet_gebak/koekje_puur.webp"),
        ("9006", "Zoet & gebak", "Appeltaart", 3.20, 0.60, "src/static/img/products/zoet_gebak/appeltaart.webp"),
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