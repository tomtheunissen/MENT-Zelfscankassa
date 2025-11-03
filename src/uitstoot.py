# uitstoot.py
# Eenvoudige helper om CO2-uitstoot van gescande producten om te rekenen naar autokilometers.

CO2_PER_KM_GRAM = 170.0  # Gemiddelde gram CO₂ per kilometer van een auto

def km_equiv_from_scanned(scanned, field="co2_uitstoot"):
    """
    scanned = lijst met producten zoals in je winkelwagen.
    Elk product zou een veld 'co2_uitstoot' in kilogram (kg) moeten bevatten.
    Deze functie rekent dat om naar autokilometers.
    """
    totaal_gram = 0.0
    for p in scanned:
        try:
            kg = float(p.get(field) or 0)   # CO2 per product in kg
        except:
            kg = 0.0
        totaal_gram += kg * 1000.0          # kg → gram

    if CO2_PER_KM_GRAM > 0:
        return totaal_gram / CO2_PER_KM_GRAM
    return 0.0