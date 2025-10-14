from core import scan_product, calculate_total
from database import get_product

def main():
    def winkelmandje():
        overzicht = {}
        for product in scanned:
            naam = product['naam']
            prijs = product['prijs']
            if naam in overzicht:
                overzicht[naam]['aantal'] += 1
            else:
                overzicht[naam] = {'prijs': prijs, 'aantal': 1}

        regels = []
        for naam, info in overzicht.items():
            totaal_prijs = info['prijs'] * info['aantal']
            regels.append(f"{info['aantal']}x {naam} - €{totaal_prijs:.2f}")

        # print statement voor de winkelmand
        print(
            f"\n----------------------------------------------\n\n"
            f"**Winkelmandje**\n\nJe winkelmandje bestaat uit:\n"
            + "\n".join(regels)
            + f"\n\nTotaal: €{totaal:.2f}\n\n----------------------------------------------"
    )


    scanned = []
    while True:
        code = input("Scan productcode (of 'stop'): ")
        if code == "stop":
            totaal = calculate_total(scanned)
            namen = [p['naam'] for p in scanned]  # lijst met alleen namen
            winkelmandje()
            break
        product = get_product(code)
        if product:
            scanned.append(product)
            print(f"Toegevoegd: {product['naam']} - €{product['prijs']}")
        else:
            print("Product niet gevonden")



if __name__ == "__main__":
    main()