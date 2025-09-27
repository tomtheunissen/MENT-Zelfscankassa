import sqlite3

def get_product(code):
    conn = sqlite3.connect("data/products.db")
    cursor = conn.cursor()
    cursor.execute("SELECT naam, prijs FROM producten WHERE code = ?", (code,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"naam": row[0], "prijs": row[1]}
    return None