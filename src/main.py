from core import calculate_total
from database import get_product

def main():
    """de hoofdfunctie, zorgt dat gebruikers kunenn scannen, en geeft dit vervolgens allemaal weer in het winkelmandje"""

    def winkelmandje():
        """functie om het winkelmandje te maken en printen"""
        overzicht = {} # dictionary om gescande producten en aantallen bij te houden
        # Ga alle gescande producten langs om aantal per product te tellen
        for product in scanned: 
            naam = product['naam'] 
            prijs = product['prijs']
            if naam in overzicht:
                overzicht[naam]['aantal'] += 1
            else:
                overzicht[naam] = {'prijs': prijs, 'aantal': 1}

        regels = []
        # bereken totaalprijs per product en voeg regels samen voor weergave
        for naam, info in overzicht.items():
            totaal_prijs = info['prijs'] * info['aantal']
            regels.append(f"{info['aantal']}x {naam} - €{totaal_prijs:.2f}")

        # print statement met alle producten en totaalprijs
        print(
            f"\n----------------------------------------------\n\n"
            f"**Winkelmandje**\n\nJe winkelmandje bestaat uit:\n"
            + "\n".join(regels)
            + f"\n\nTotaal: €{totaal:.2f}\n\n----------------------------------------------"
    )


    # loop voor het scannen van producten (voor nu handmatig code invoeren)
    scanned = []
    while True:
        code = input("Scan productcode (of 'stop'): ") # vraag productcode of "stop"
        if code == "stop":
            totaal = calculate_total(scanned) # bereken totaalprijs
            winkelmandje()
            break
        product = get_product(code) # zoek product in database
        if product:
            scanned.append(product) # voegt product toe aan lijst gescande items 
            print(f"Toegevoegd: {product['naam']} - €{product['prijs']}")
        else:
            print("Product niet gevonden") # foutmelding bij onbekende code



if __name__ == "__main__":
    main()