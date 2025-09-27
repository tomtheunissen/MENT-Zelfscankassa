from .core import scan_product, calculate_total
from .database import get_product

def main():
    print("Welkom bij de Zelfscankassa")

    scanned = []
    while True:
        code = input("Scan productcode (of 'stop'): ")
        if code == "stop":
            totaal = calculate_total(scanned)
            namen = [p['naam'] for p in scanned]  # lijst met alleen namen
            print(f"Totaalbedrag: €{totaal:.2f}. Je winkelmandje bestaat uit: {', '.join(namen)}")
            break
        product = get_product(code)
        if product:
            scanned.append(product)
            print(f"Toegevoegd: {product['naam']} - €{product['prijs']}")
        else:
            print("Product niet gevonden")



if __name__ == "__main__":
    main()