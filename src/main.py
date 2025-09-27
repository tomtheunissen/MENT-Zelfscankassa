from .core import scan_product, calculate_total
from .database import get_product

def main():
    print("Welkom bij de Zelfscankassa")

    scanned = []
    while True:
        code = input("Scan productcode (of 'stop'): ")
        if code == "stop":
            break
        product = get_product(code)
        if product:
            scanned.append(product)
            print(f"Toegevoegd: {product['naam']} - €{product['prijs']}")
        else:
            print("Product niet gevonden")

    totaal = calculate_total(scanned)
    print(f"Totaalbedrag: €{totaal:.2f}")

if __name__ == "__main__":
    main()