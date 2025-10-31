from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import get_product
import sqlite3

conn = sqlite3.connect("data/products.db")
cursor = conn.cursor()
app = Flask(__name__)

# Tijdelijk winkelmandje in geheugen
scanned = []


def calculate_total(items):
    """Som van prijzen van alle losse gescande items"""
    return sum(p["prijs"] for p in items)



def key_of(p):
    """Bepaal een stabiele key voor een product (voorkeur: code > id > naam)."""
    return p.get("code") or p.get("id") or p["naam"]

def aggregate_cart(items):
    """Maak geaggregeerde regels met aantal, subtotaal en stabiele key per product."""
    agg = {}
    for p in items:
        k = key_of(p)
        if k in agg:
            agg[k]["aantal"] += 1
            agg[k]["subtotaal"] = agg[k]["aantal"] * agg[k]["prijs"]
        else:
            agg[k] = {
                "key": k,
                "code": p.get("code"),
                "naam": p["naam"],
                "prijs": p["prijs"],
                "aantal": 1,
                "subtotaal": p["prijs"],
            }
    return list(agg.values())


@app.route("/menu_dranken")
def menu_dranken():
    """Toon alle dranken uit de database en geef ze door aan de template."""
    conn = sqlite3.connect("data/products.db")
    conn.row_factory = sqlite3.Row  # maakt rijen toegankelijk als dict
    cursor = conn.cursor()

    cursor.execute("""
        SELECT code, categorie, naam, prijs, COALESCE(afbeelding_url, '') AS afbeelding_url
        FROM producten
        WHERE categorie IN ('Warme dranken', 'Koude dranken')
    """)
    dranken = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return render_template("index.html", dranken=dranken)


# /minus?code=5008 of form POST, or /minus/5008
@app.route("/minus", methods=["GET", "POST"])            # /minus?code=5008 of form POST
@app.route("/minus/<code>", methods=["GET", "POST"])     # /minus/5008
def minus(code=None):
    """Verlaag het aantal van een product met 1 door één instantie uit `scanned` te verwijderen."""
    # 1) Code bepalen uit pad of query/form
    if code is None:
        code = (request.values.get("code") or "").strip()
    else:
        code = str(code).strip()

    if not code:
        return redirect(url_for("home"))

    # 2) Zoek één match in scanned op basis van stabiele key of p['code'] en verwijder die
    idx = next((i for i, p in enumerate(scanned)
                if str(key_of(p)) == code or str(p.get("code")) == code), None)
    if idx is not None:
        scanned.pop(idx)

    # 3) Redirect terug naar de home zodat agg/totaal opnieuw worden berekend
    return redirect(url_for("home"))


# /plus?code=5008 of form POST, or /plus/5008
@app.route("/plus", methods=["GET", "POST"])            # /plus?code=5008 of form POST
@app.route("/plus/<code>", methods=["GET", "POST"])     # /plus/5008
def plus(code=None):
    """Verhoog het aantal van een product (geïdentificeerd via code/key) met 1.
    We muteren de bronlijst `scanned`; `agg` is afgeleid en wordt bij renderen herberekend.
    """
    # 1) Code bepalen uit pad of query/form
    if code is None:
        code = (request.values.get("code") or "").strip()
    else:
        code = str(code).strip()

    if not code:
        return redirect(url_for("home"))

    # 2) Probeer een bestaand item in het mandje te vinden op basis van onze stabiele key
    proto = next((p for p in scanned if str(key_of(p)) == code or str(p.get("code")) == code), None)

    # 3) Als het nog niet in het mandje zit, haal het uit de database
    if proto is None:
        product = get_product(code)
        if not product:
            # Toon dezelfde home met foutmelding
            totaal = calculate_total(scanned)
            producten = aggregate_cart(scanned)
            return render_template(
                "index.html",
                producten=producten,
                totaal=totaal,
                fout="Product niet gevonden",
            )
        proto = product

    # 4) +1 toevoegen door een instantie toe te voegen aan `scanned`
    scanned.append(proto)
    return redirect(url_for("home"))


@app.route("/delete", methods=["GET", "POST"])            # /delete?code=5008 of form POST
@app.route("/delete/<code>", methods=["GET", "POST"])     # /delete/5008
def delete(code=None):
    """Verwijder alle instanties van een product (op basis van key/code) uit het mandje."""
    global scanned
    # Code bepalen uit pad of query/form
    if code is None:
        code = (request.values.get("code") or "").strip()
    else:
        code = str(code).strip()

    if not code:
        return redirect(url_for("home"))

    # Filter alles weg dat matcht op stabiele key of p['code']
    scanned = [p for p in scanned if not (
        str(key_of(p)) == code or str(p.get("code")) == code
    )]

    return redirect(url_for("home"))

@app.route("/", methods=["GET"])
def home():
    # Maak verbinding met de database
    conn = sqlite3.connect("data/products.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Haal alle broodjes op
    cursor.execute("""
        SELECT code, categorie, naam, prijs, COALESCE(afbeelding_url, '') AS afbeelding_url
        FROM producten
        WHERE categorie = 'Broodjes'
    """)
    broodjes = [dict(row) for row in cursor.fetchall()]

    # Haal alle dranken (warme + koude) op
    cursor.execute("""
        SELECT code, categorie, naam, prijs, COALESCE(afbeelding_url, '') AS afbeelding_url
        FROM producten
        WHERE categorie IN ('Warme dranken', 'Koude dranken')
    """)
    dranken = [dict(row) for row in cursor.fetchall()]

    # Haal alle snacks op
    cursor.execute("""
        SELECT code, categorie, naam, prijs, COALESCE(afbeelding_url, '') AS afbeelding_url
        FROM producten
        WHERE categorie IN ('Snacks warm', 'Snacks koud')
    """)
    snacks = [dict(row) for row in cursor.fetchall()]

    # Haal overige producten op
    cursor.execute("""
        SELECT code, categorie, naam, prijs, COALESCE(afbeelding_url, '') AS afbeelding_url
        FROM producten
        WHERE categorie NOT IN ('Broodjes', 'Warme dranken', 'Koude dranken', 'Snacks warm', 'Snacks koud')
    """)
    overige = [dict(row) for row in cursor.fetchall()]
    conn.close()

    # Winkelwagen en totaal berekenen
    totaal = calculate_total(scanned)
    producten = aggregate_cart(scanned)

    # Geef alles door aan de template
    return render_template(
        "index.html",
        producten=producten,
        totaal=totaal,
        fout=None,
        broodjes=broodjes,
        dranken=dranken,
        snacks=snacks,
        overige=overige
    )

@app.route("/scan", methods=["GET", "POST"]) 
@app.route("/scan/<code>", methods=["GET"]) 
def scan(code=None):
    # Bepaal code uit POST-body of uit de URL-parameter
    if request.method == "POST" and code is None:
        code = request.form.get("code", "").strip()
    elif code is not None:
        code = str(code).strip()

    if not code:
        return redirect(url_for("home"))

    product = get_product(code)
    if product:
        scanned.append(product)
        return redirect(url_for("home"))
    else:
        totaal = calculate_total(scanned)
        producten = aggregate_cart(scanned)
        return render_template(
            "index.html",
            producten=producten,
            totaal=totaal,
            fout="Product niet gevonden",
        )


@app.route("/reset", methods=["POST"])
def reset():
    scanned.clear()
    return redirect(url_for("home"))


@app.route("/scan-json", methods=["POST"])
def scan_json():
    code = (request.json or {}).get("code", "").strip()
    if not code:
        return jsonify({"error": "Geen code ingevoerd", "producten": aggregate_cart(scanned), "totaal": calculate_total(scanned)})

    product = get_product(code)
    if product:
        scanned.append(product)
        return jsonify({
            "success": True,
            "producten": aggregate_cart(scanned),
            "totaal": calculate_total(scanned),
        })
    else:
        return jsonify({
            "error": "Product niet gevonden",
            "producten": aggregate_cart(scanned),
            "totaal": calculate_total(scanned),
        })



# Nieuwe routes voor +/- en verwijderen zonder refresh
@app.route("/update-json", methods=["POST"])
def update_json():
    """Pas het aantal van een product aan met delta (+1 of -1)."""
    data = request.get_json() or {}
    key = str(data.get("key", "")).strip()
    delta = int(data.get("delta", 0))

    if not key or delta == 0:
        return jsonify({
            "error": "Ongeldige update",
            "producten": aggregate_cart(scanned),
            "totaal": calculate_total(scanned),
        })

    if delta > 0:
        # +1: voeg één exemplaar toe (zoek representatief product in huidige lijst)
        proto = next((p for p in scanned if key_of(p) == key), None)
        if not proto:
            return jsonify({
                "error": "Product niet in mandje",
                "producten": aggregate_cart(scanned),
                "totaal": calculate_total(scanned),
            })
        scanned.append(proto)
    else:
        # -1: verwijder één exemplaar als die er is
        idx = next((i for i, p in enumerate(scanned) if key_of(p) == key), None)
        if idx is None:
            return jsonify({
                "error": "Product niet in mandje",
                "producten": aggregate_cart(scanned),
                "totaal": calculate_total(scanned),
            })
        scanned.pop(idx)

    return jsonify({
        "producten": aggregate_cart(scanned),
        "totaal": calculate_total(scanned),
    })


@app.route("/remove-json", methods=["POST"])
def remove_json():
    """Verwijder de volledige regel (alle exemplaren) van een product uit het mandje."""
    global scanned  # <-- verplaatst naar bovenaan

    data = request.get_json() or {}
    key = str(data.get("key", "")).strip()

    if not key:
        return jsonify({
            "error": "Geen key ontvangen",
            "producten": aggregate_cart(scanned),
            "totaal": calculate_total(scanned),
        })

    scanned = [p for p in scanned if key_of(p) != key]

    return jsonify({
        "producten": aggregate_cart(scanned),
        "totaal": calculate_total(scanned),
    })


if __name__ == "__main__":
    app.run(debug=True)
