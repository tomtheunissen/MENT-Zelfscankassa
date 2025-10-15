import sqlite3 # voor database

def get_product(code):
    """haalt producten op uit de database"""
    # start verbinding met database
    conn = sqlite3.connect("data/products.db")
    cursor = conn.cursor()

    # zoek product via productcode
    cursor.execute("SELECT naam, prijs FROM producten WHERE code = ?", (code,))
    row = cursor.fetchone()

    # beëindigt verbinding met database
    conn.close()

    # geef product als dict of None wanneer niks gevonden
    if row:
        return {"naam": row[0], "prijs": row[1]}
    return None