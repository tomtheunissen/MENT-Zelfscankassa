# Hulpfunctie om totale CO2-uitstoot om te rekenen naar autokilometers.

# Gemiddelde uitstoot van een personenauto in gram CO2 per kilometer
CO2_PER_KM_GRAM = 170.0  # Gemiddelde gram CO2 per kilometer van een auto

def km_equiv_from_scanned(scanned, field="co2_uitstoot"):
    """
    scanned = lijst met producten zoals in je winkelwagen.
    Elk product zou een veld 'co2_uitstoot' in kilogram (kg) moeten bevatten.
    Deze functie rekent dat om naar autokilometers.
    """
    # Variabele om de totale CO2-uitstoot in gram bij te houden
    totaal_gram = 0.0
    # Loop door elk product in de lijst
    for p in scanned:
        try:
            kg = float(p.get(field) or 0)   # CO2 per product in kg
        except:
            # Bij een fout (bijv. niet-converteerbaar) stel in op 0
            kg = 0.0
        totaal_gram += kg * 1000.0          # kg naar gram

    # Als de gemiddelde uitstoot per km groter dan 0 is, bereken kilometers
    if CO2_PER_KM_GRAM > 0:
        return totaal_gram / CO2_PER_KM_GRAM
    # Anders geef 0 terug (geen uitstoot of geen data)
    return 0.0