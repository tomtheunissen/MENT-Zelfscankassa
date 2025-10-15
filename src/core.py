def scan_product(product):
    """retourneert het gescande product"""
    return product

def calculate_total(products):
    """berekent het totaalbedrag van alle producten in de winkelmand"""
    return sum(p["prijs"] for p in products)