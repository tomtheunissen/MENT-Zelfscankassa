# Zelfscankassa – Project BITEWISE

Een innovatief Python-project gericht op het ontwikkelen van een digitale zelfscankassa met een productdatabase en milieuscore, ontworpen om wachtrijen in de kantine te verminderen en duurzame keuzes te stimuleren.

---

## Aanleiding & Doelstelling

In de kantine van Hogeschool Zuyd ontstaan vaak lange wachtrijen, wat leidt tot ontevredenheid onder studenten en personeel. Dit project richt zich op het ontwikkelen van een proof-of-concept zelfscankassa die het afrekenproces versnelt en tegelijkertijd inzicht geeft in de CO₂-impact van producten. Hiermee willen we bijdragen aan een duurzamere en efficiëntere kantineomgeving.

---

## Projectresultaat

Het resultaat is een werkende zelfscankassa-applicatie met de volgende kenmerken:
- Producten scannen en prijzen automatisch optellen
- Tonen van CO₂-impact per product om duurzame keuzes te stimuleren
- Backend gebouwd met Flask en een gekoppelde productdatabase
- Gehost op Azure voor schaalbaarheid en betrouwbaarheid
- Prototype ontwikkeld binnen 10 weken

---

## Team & Rollen

| Naam                 | Rol                         |
|----------------------|-----------------------------|
| Roy Geerkens         | Teamleider                  |
| Tom Theunissen       | Tijdsbewaker & Scrummaster  |
| Winston Dang         | Notulist                    |
| Niels Theunissen     | Teamlid                     |

---

## Projectstructuur

Het project is georganiseerd volgens een agile aanpak met wekelijkse sprints en regelmatige scrummomenten. De samenwerking wordt vastgelegd in een samenwerkingscontract om heldere afspraken te waarborgen.

---

## Technologie & Architectuur

- **Backend:** Flask-webframework voor API en serverlogica  
- **Database:** Productdatabase met categorieën en milieuscores  
- **Hosting:** Azure cloudplatform voor deployment en beheer  
- **Frontend:** Eenvoudige interface voor het scannen en afrekenen  
- **Milieuscore:** CO₂-impact per product inzichtelijk gemaakt  

---

## Installatie & Gebruik

1. Maak een virtuele omgeving aan en activeer deze:
   - Mac/Linux:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
   - Windows (Powershell):
     ```bash
     python -m venv venv
     venv\Scripts\Activate.ps1
     ```
   - Windows (CMD):
     ```bash
     python -m venv venv
     venv\Scripts\activate.bat
     ```
2. Installeer benodigde packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Start de applicatie:
   ```bash
   python -m src.main
   ```

---

## Kwaliteit & Risico’s

- **Kwaliteit:** Regelmatige code reviews en tests waarborgen de stabiliteit.  
- **Risico’s:** Beperkingen in tijd (10 weken) en afhankelijkheden van externe hosting (Azure) kunnen invloed hebben op het eindresultaat.  
- **Mitigatie:** Strakke planning, duidelijke communicatie en het gebruik van bewezen technologieën.

---

## English Summary

# Self-Checkout System – Project BITEWISE

An innovative Python project aimed at developing a digital self-checkout system with a product database and environmental score, designed to reduce queues in the cafeteria and promote sustainable choices.

**Background & Objective:**  
Long queues at the Zuyd University cafeteria cause dissatisfaction. This project creates a proof-of-concept self-checkout system that speeds up payments and provides CO₂ impact insights per product.

**Project Outcome:**  
A working application that scans products, sums prices, shows CO₂ impact, uses a Flask backend, and is deployed on Azure. Developed within 10 weeks.

**Team & Roles:**  
Roy Geerkens (Team Leader), Tom Theunissen (Timekeeper & Scrum Master), Winston Dang (Secretary), Niels Theunissen (Team Member).

**Technology & Architecture:**  
Flask backend, product database with categories and environmental scores, Azure hosting, simple frontend interface.

**Installation & Usage:**  
Create and activate a virtual environment, install dependencies, and run the application.

**Quality & Risks:**  
Code reviews and testing ensure stability; time constraints and hosting dependencies are managed through planning and communication.

This project demonstrates a practical solution to improve efficiency and sustainability in a real-world setting.
