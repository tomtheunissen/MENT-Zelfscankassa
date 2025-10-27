from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import get_product

app = Flask(__name__)

# Tijdelijk winkelmandje in geheugen
scanned = []


def calculate_total(items):
    """Som van prijzen van alle losse gescande items"""
    return sum(p["prijs"] for p in items)


def aggregate_cart(items):
    """Maak geaggregeerde regels met aantal en subtotaal per product."""
    agg = {}
    for p in items:
        key = p.get("code") or p.get("id") or p["naam"]
        if key in agg:
            agg[key]["aantal"] += 1
            agg[key]["subtotaal"] = agg[key]["aantal"] * agg[key]["prijs"]
        else:
            agg[key] = {
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


if __name__ == "__main__":
    app.run(debug=True)
