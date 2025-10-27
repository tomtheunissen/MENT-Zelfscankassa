from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import get_product


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


@app.route("/", methods=["GET"])
def home():
    totaal = calculate_total(scanned)
    producten = aggregate_cart(scanned)
    return render_template("index.html", producten=producten, totaal=totaal, fout=None)


@app.route("/scan", methods=["POST"])
def scan():
    code = request.form.get("code", "").strip()
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
