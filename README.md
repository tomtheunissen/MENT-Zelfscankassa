# Zelfscankassa – Project BITEWISE

Een Python-project waarin een digitale zelfscankassa wordt ontwikkeld met een productdatabase en milieuscore.  
Dit project is onderdeel van de opleiding **HBO-ICT** (Blok 1) en wordt uitgevoerd door **Het G-Team**.

---

## Beschrijving
Het doel van dit project is om een proof-of-concept te maken van een zelfscansysteem dat:
- producten kan scannen en prijzen optelt  
- de CO₂-impact of productcategorie toont om duurzame keuzes te stimuleren  
- wachtrijen in de cafetaria verkort en werkdruk voor personeel verlaagt  


## Team

Ons projectteam bestaat uit de volgende leden:

| Naam                 | Rol                         |
|----------------------|-----------------------------|
| **Roy Geerkens**     | Teamleider                  |
| **Tom Theunissen**   | Tijdsbewaker & Scrummaster  |
| **Winston Dang**     | Notulist                    |
| **Niels Theunissen** | Teamlid                     |


## Categorieën in de productendatabase

Om de producten in de zelfscankassa overzichtelijk en herkenbaar te maken, zijn ze onderverdeeld in vaste categorieën.  
Dit maakt het eenvoudiger voor gebruikers én zorgt ervoor dat we per categorie ook een gemiddelde milieuscore kunnen tonen.

### Eten
- **Broodjes & Beleg** – broodje kaas, broodje gezond, etc.
- **Snacks warm** – frikandel, kroket, kaassoufflé
- **Snacks koud** – salades, fruit, yoghurt
- **Maaltijden** – soep, pasta, rijstgerechten
- **Zoet & Gebak** – koek, muffins, repen

### Dranken
- **Warme dranken** – koffie, thee, chocomel
- **Frisdranken** – cola, fanta, icetea
- **Water & sap** – flesjes water, smoothies, fruitsap
- **Zuivel & alternatieven** – melk, chocolademelk, havermelk

### Overig
- **Overige producten** – kauwgom, snacks verpakt, etc.

<br><br>

## Project starten

**Virtuele omgeving aanmaken en activeren**

Maak eerst een virtuele omgeving aan om de afhankelijkheden gescheiden te houden, en activeer deze vervolgens:

**Mac/Linux**
```bash
python -m venv venv
source venv/bin/activate
```
**Windows (Powershell)**
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```
**Windows (CMD)**
```bash
python -m venv venv
venv\Scripts\activate.bat
```
<br>

**Benodigde packages installeren**
```bash
pip install -r requirements.txt
```

<br>

**Programma starten**

```bash
python -m src.main
```
