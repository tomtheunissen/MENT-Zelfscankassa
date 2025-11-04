from order import init_orders_schema, save_order
from uitstoot import km_equiv_from_scanned

# Eenvoudige eco-score op basis van CO₂ in kilogram per stuk (5 = groenst)
def eco_score_from_kg(kg: float) -> int:
    try:
        v = float(kg)
    except (TypeError, ValueError):
        return 3
    if v <= 0.20:
        return 5
    if v <= 0.50:
        return 4
    if v <= 0.80:
        return 3
    if v <= 1.20:
        return 2
    return 1

# Helper: render volledige kassa-pagina zodat HTMX `.cart` kan selecteren
def render_kassa_page(fout=None):
    producten, totaal = aggregate_cart_ordered(scanned)
    # CO2 → km via uitstoot.py
    km_equiv = km_equiv_from_scanned(scanned)
    conn = sqlite3.connect("data/products.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT code, categorie, naam, prijs, COALESCE(afbeelding_url, '') AS afbeelding_url, COALESCE(co2_uitstoot, 0) AS co2_uitstoot FROM producten WHERE categorie = 'Broodjes'")
    broodjes = [dict(row) for row in cursor.fetchall()]
    for d in broodjes:
        d["eco_score"] = eco_score_from_kg(d.get("co2_uitstoot"))

    cursor.execute("SELECT code, categorie, naam, prijs, COALESCE(afbeelding_url, '') AS afbeelding_url, COALESCE(co2_uitstoot, 0) AS co2_uitstoot FROM producten WHERE categorie IN ('Warme dranken', 'Koude dranken')")
    dranken = [dict(row) for row in cursor.fetchall()]
    for d in dranken:
        d["eco_score"] = eco_score_from_kg(d.get("co2_uitstoot"))

    cursor.execute("SELECT code, categorie, naam, prijs, COALESCE(afbeelding_url, '') AS afbeelding_url, COALESCE(co2_uitstoot, 0) AS co2_uitstoot FROM producten WHERE categorie IN ('Snacks warm', 'Snacks koud')")
    snacks = [dict(row) for row in cursor.fetchall()]
    for d in snacks:
        d["eco_score"] = eco_score_from_kg(d.get("co2_uitstoot"))

    cursor.execute("SELECT code, categorie, naam, prijs, COALESCE(afbeelding_url, '') AS afbeelding_url, COALESCE(co2_uitstoot, 0) AS co2_uitstoot FROM producten WHERE categorie NOT IN ('Broodjes', 'Warme dranken', 'Koude dranken', 'Snacks warm', 'Snacks koud')")
    overige = [dict(row) for row in cursor.fetchall()]
    for d in overige:
        d["eco_score"] = eco_score_from_kg(d.get("co2_uitstoot"))
    conn.close()
    return render_template(
        "kassa.html",
        producten=producten,
        totaal=totaal,
        fout=fout,
        broodjes=broodjes,
        dranken=dranken,
        snacks=snacks,
        overige=overige,
        km_equiv=km_equiv  # <-- toegevoegd
    )
from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import get_product
import sqlite3

conn = sqlite3.connect("data/products.db")
cursor = conn.cursor()
app = Flask(__name__)
init_orders_schema()

# Tijdelijk winkelmandje in geheugen
scanned = []

# Stabiele volgorde van regels: volgorde van eerste toevoeging bewaren
cart_order = []  # unieke keys in volgorde van eerste scan

def _code_str(p: dict) -> str:
    # Bepaal stabiele key als string
    return str(key_of(p))

def aggregate_cart_ordered(items):
    """Aggregateer items naar regels in de volgorde van cart_order.
    Retourneert (regels, totaal)
    """
    counts = {}
    info = {}
    for p in items:
        k = _code_str(p)
        counts[k] = counts.get(k, 0) + 1
        info[k] = p
    regels = []
    totaal = 0.0
    for k in cart_order:
        qty = counts.get(k, 0)
        if qty <= 0:
            continue
        p = info.get(k, {})
        prijs = float(p.get("prijs", 0) or 0)
        subt = prijs * qty
        regels.append({
            "key": k,
            "code": p.get("code"),
            "naam": p.get("naam", ""),
            "prijs": prijs,
            "aantal": qty,
            "subtotaal": subt,
            "afbeelding_url": p.get("afbeelding_url", "")
        })
        totaal += subt
    return regels, totaal


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

    return render_template("kassa.html", dranken=dranken)


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

    # Als aantal 0 is, verwijder uit cart_order
    remaining = sum(1 for p in scanned if str(key_of(p)) == code or str(p.get("code")) == code)
    # Bepaal de exacte key zoals wij renderen
    key_render = None
    if idx is not None:
        key_render = code
    if remaining == 0 and key_render in cart_order:
        try:
            cart_order.remove(key_render)
        except ValueError:
            pass

    # 3) Redirect terug naar de home zodat agg/totaal opnieuw worden berekend
    return render_kassa_page()


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
            return render_kassa_page("Product niet gevonden")
        proto = product

    # 4) +1 toevoegen door een instantie toe te voegen aan `scanned`
    scanned.append(proto)
    k = str(key_of(proto))
    if k and k not in cart_order:
        cart_order.append(k)
    return render_kassa_page()


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

    # Ook uit de vaste volgorde verwijderen
    try:
        cart_order.remove(code)
    except ValueError:
        pass

    return render_kassa_page()

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
    producten, totaal = aggregate_cart_ordered(scanned)

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


# Kassa-route voor kassascherm met huidige winkelwagen
@app.route("/kassa", methods=["GET"])
def kassa():
    # Haal winkelwagen en totaal op
    producten, totaal = aggregate_cart_ordered(scanned)
    km_equiv = km_equiv_from_scanned(scanned)
    # Laad opnieuw producten voor de categorieën
    conn = sqlite3.connect("data/products.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT code, categorie, naam, prijs, COALESCE(afbeelding_url, '') AS afbeelding_url, COALESCE(co2_uitstoot, 0) AS co2_uitstoot FROM producten WHERE categorie = 'Broodjes'")
    broodjes = [dict(row) for row in cursor.fetchall()]
    for d in broodjes:
        d["eco_score"] = eco_score_from_kg(d.get("co2_uitstoot"))

    cursor.execute("SELECT code, categorie, naam, prijs, COALESCE(afbeelding_url, '') AS afbeelding_url, COALESCE(co2_uitstoot, 0) AS co2_uitstoot FROM producten WHERE categorie IN ('Warme dranken', 'Koude dranken')")
    dranken = [dict(row) for row in cursor.fetchall()]
    for d in dranken:
        d["eco_score"] = eco_score_from_kg(d.get("co2_uitstoot"))

    cursor.execute("SELECT code, categorie, naam, prijs, COALESCE(afbeelding_url, '') AS afbeelding_url, COALESCE(co2_uitstoot, 0) AS co2_uitstoot FROM producten WHERE categorie IN ('Snacks warm', 'Snacks koud')")
    snacks = [dict(row) for row in cursor.fetchall()]
    for d in snacks:
        d["eco_score"] = eco_score_from_kg(d.get("co2_uitstoot"))

    cursor.execute("SELECT code, categorie, naam, prijs, COALESCE(afbeelding_url, '') AS afbeelding_url, COALESCE(co2_uitstoot, 0) AS co2_uitstoot FROM producten WHERE categorie NOT IN ('Broodjes', 'Warme dranken', 'Koude dranken', 'Snacks warm', 'Snacks koud')")
    overige = [dict(row) for row in cursor.fetchall()]
    for d in overige:
        d["eco_score"] = eco_score_from_kg(d.get("co2_uitstoot"))
    conn.close()

    return render_template(
        "kassa.html",
        producten=producten,
        totaal=totaal,
        fout=None,
        broodjes=broodjes,
        dranken=dranken,
        snacks=snacks,
        overige=overige,
        km_equiv=km_equiv
    )

@app.route("/betalen", methods=["GET"])
def betalen():
    # Maak geaggregeerde regels en totaalbedrag aan uit het huidige mandje
    producten, totaal = aggregate_cart_ordered(scanned)
    km_equiv = km_equiv_from_scanned(scanned)

    # Proof-of-concept: sla direct op (stil) bij binnenkomst van /betalen
    try:
        simple_items = [{"naam": p["naam"], "aantal": int(p.get("aantal", 0) or 0)} for p in producten]
        save_order(simple_items, totaal)
    except Exception:
        # Stil falen zodat de UI niet breekt (optioneel: loggen)
        pass

    return render_template("betalen.html", producten=producten, totaal=totaal, km_equiv=km_equiv)

# Route voor bevestiging (bevestiging.html) met totaalbedrag
@app.route("/bevestiging", methods=["GET"])
def bevestiging():
    producten, totaal = aggregate_cart_ordered(scanned)
    return render_template("bevestiging.html", producten=producten, totaal=totaal)

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
        print("DEBUG CO2 laatst toegevoegd:", product.get("co2_uitstoot"))
        k = str(key_of(product))
        if k and k not in cart_order:
            cart_order.append(k)
        return render_kassa_page()
    else:
        return render_kassa_page("Product niet gevonden")


@app.route("/reset", methods=["POST"])
def reset():
    scanned.clear()
    cart_order.clear()
    # Als verzoek vanuit HTMX komt, forceer een volledige redirect naar index
    if request.headers.get("HX-Request"):
        return ("", 204, {"HX-Redirect": url_for("home")})
    # Anders normale server-side redirect
    return redirect(url_for("home"))


@app.route("/scan-json", methods=["POST"])
def scan_json():
    code = (request.json or {}).get("code", "").strip()
    items, total = aggregate_cart_ordered(scanned)
    if not code:
        return jsonify({"error": "Geen code ingevoerd", "producten": items, "totaal": total})

    product = get_product(code)
    if product:
        scanned.append(product)
        k = str(key_of(product))
        if k and k not in cart_order:
            cart_order.append(k)
        items, total = aggregate_cart_ordered(scanned)
        return jsonify({
            "success": True,
            "producten": items,
            "totaal": total,
        })
    else:
        return jsonify({
            "error": "Product niet gevonden",
            "producten": items,
            "totaal": total,
        })



# Nieuwe routes voor +/- en verwijderen zonder refresh
@app.route("/update-json", methods=["POST"])
def update_json():
    """Pas het aantal van een product aan met delta (+1 of -1)."""
    data = request.get_json() or {}
    key = str(data.get("key", "")).strip()
    delta = int(data.get("delta", 0))

    items, total = aggregate_cart_ordered(scanned)

    if not key or delta == 0:
        return jsonify({
            "error": "Ongeldige update",
            "producten": items,
            "totaal": total,
        })

    if delta > 0:
        # +1: voeg één exemplaar toe (zoek representatief product in huidige lijst)
        proto = next((p for p in scanned if key_of(p) == key), None)
        if not proto:
            return jsonify({
                "error": "Product niet in mandje",
                "producten": items,
                "totaal": total,
            })
        scanned.append(proto)
        k = str(key_of(proto))
        if k and k not in cart_order:
            cart_order.append(k)
    else:
        # -1: verwijder één exemplaar als die er is
        idx = next((i for i, p in enumerate(scanned) if key_of(p) == key), None)
        if idx is None:
            return jsonify({
                "error": "Product niet in mandje",
                "producten": items,
                "totaal": total,
            })
        scanned.pop(idx)
        # Als aantal 0 is, verwijder uit cart_order
        remaining = sum(1 for p in scanned if str(key_of(p)) == key)
        if remaining == 0 and key in cart_order:
            try:
                cart_order.remove(key)
            except ValueError:
                pass

    items, total = aggregate_cart_ordered(scanned)

    return jsonify({
        "producten": items,
        "totaal": total,
    })


@app.route("/remove-json", methods=["POST"])
def remove_json():
    """Verwijder de volledige regel (alle exemplaren) van een product uit het mandje."""
    global scanned  # <-- verplaatst naar bovenaan

    data = request.get_json() or {}
    key = str(data.get("key", "")).strip()

    items, total = aggregate_cart_ordered(scanned)

    if not key:
        return jsonify({
            "error": "Geen key ontvangen",
            "producten": items,
            "totaal": total,
        })

    scanned = [p for p in scanned if key_of(p) != key]
    # Ook uit de vaste volgorde verwijderen
    if key in cart_order:
        try:
            cart_order.remove(key)
        except ValueError:
            pass

    items, total = aggregate_cart_ordered(scanned)

    return jsonify({
        "producten": items,
        "totaal": total,
    })


if __name__ == "__main__":
    app.run(debug=True)
