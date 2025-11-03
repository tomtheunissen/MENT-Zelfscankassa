import sqlite3 # voor database

import sqlite3

def get_product(code: str):
    conn = sqlite3.connect("data/products.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            code,
            categorie,
            naam,
            prijs,
            COALESCE(co2_uitstoot, 0) AS co2_uitstoot,   -- kg per stuk
            COALESCE(afbeelding_url, '') AS afbeelding_url
        FROM producten
        WHERE code = ?
        LIMIT 1
        """,
        (code,),
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    return dict(row)  # bevat nu co2_uitstoot