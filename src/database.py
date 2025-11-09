import sqlite3 # voor database

# Dit bestand wordt gebruikt om met de database 'products.db' te communiceren.
# Producten worden opgehaald op basis van hun unieke code.

def get_product(code: str):
    # Verbind met de SQLite database 'products.db'
    conn = sqlite3.connect("data/products.db")
    # Zorgt dat rijen als dictionaries worden teruggegeven
    conn.row_factory = sqlite3.Row
    # Cursor aanmaken voor SQL-query
    cur = conn.cursor()
    # Query uitvoeren om product op te halen op basis van code
    cur.execute(
        """
        SELECT
            code,
            categorie,
            naam,
            prijs,
            COALESCE(co2_uitstoot, 0) AS co2_uitstoot,   -- kg per stuk, vul 0 in bij NULL
            COALESCE(afbeelding_url, '') AS afbeelding_url  -- vul lege string in bij NULL
        FROM producten
        WHERE code = ?
        LIMIT 1
        """,
        (code,),
    )
    # Haal de eerste rij uit het resultaat (of None als niet gevonden)
    row = cur.fetchone()
    # Sluit de database verbinding
    conn.close()
    # Als er geen product is gevonden, geef None terug
    if not row:
        return None
    # Zet de rij om naar een dictionary en geef terug
    return dict(row)