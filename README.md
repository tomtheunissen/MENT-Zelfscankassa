# Zelfscankassa – Project BITEWISE

Een innovatief Python-project voor een digitale zelfscankassa met productdatabase en milieuscore. Gericht op het verminderen van wachtrijen en stimuleren van duurzame keuzes in de kantine.

---

## Aanleiding & Doelstelling
- Lange wachtrijen in de kantine van Hogeschool Zuyd, vooral tijdens piekuren.
- Verhoogde werkdruk en verminderde klanttevredenheid.
- Groeiend belang van duurzaamheid en bewustwording van CO₂-impact.
- Opdracht: een proof-of-concept zelfscankassa ontwikkelen die:
  - Het afrekenproces versnelt.
  - Inzicht geeft in milieubelasting van producten.
- Doel: een efficiëntere, duurzamere en klantvriendelijkere kantineomgeving.

---

## Projectresultaat
- Werkende zelfscankassa-applicatie met eenvoudige scaninterface.
- Producten automatisch toegevoegd aan digitaal mandje.
- Realtime bijwerken van totaalprijs en CO₂-impact per product.
- Productinformatie met categorieën en milieuscores in gekoppelde database.
- Backend gebouwd met Flask, verzorgt API-routes voor product- en mandjebeheer.
- Geen daadwerkelijke betalingen in deze fase, maar voorbereid op toekomstige integratie.
- Gehost op Azure voor schaalbaarheid en betrouwbaarheid.
- Prototype ontwikkeld binnen 10 weken.

---

## Team & Rollen
| Naam             | Rol                            |
|------------------|--------------------------------|
| Roy Geerkens     | Teamleider                     |
| Tom Theunissen   | Hoofdontwikkelaar & Scrummaster|
| Winston Dang     | Notulist                       |
| Niels Theunissen | Teamlid                        |

---

## Projectstructuur
- Agile aanpak met wekelijkse Scrum-sprints en scrummomenten.
- Gebruik van Trello voor taakbeheer en sprintplanning.
- Go/No-Go momenten voor beslissingen en voortgangsevaluatie.
- Heldere communicatie en efficiënte taakverdeling binnen het team.

---

## Technologie & Architectuur
- **Backend:** Flask-webframework met API-routes voor product- en mandjebeheer.
- **Database:** Productdatabase met categorieën en milieuscores; lokaal met optie tot Azure SQL.
- **Mappenstructuur:**  
  - `src/`: hoofdcode en business logic  
  - `templates/`: HTML-frontend  
  - `static/`: CSS, JavaScript, afbeeldingen  
  - `database/`: datasets en scripts  
- **Hosting:** Azure cloudplatform met automatische scaling en monitoring.
- **Frontend:** eenvoudige, gebruiksvriendelijke interface met realtime updates.
- **Uitbreidingen:** toekomstige integratie van Azure SQL, betaalmodules en rapportages.

---

## Kwaliteit & Risico’s
- **Kwaliteit:**  
  - Intuïtieve interface voor snel leren en gebruik.  
  - Bescherming van gebruikersdata en veilige communicatie.  
  - Snelle respons en minimale laadtijden, ook bij veel producten.  
- **Risico’s:**  
  - Afhankelijkheid van stabiele internetverbinding.  
  - Mogelijke inconsistenties tussen database en frontend.  
  - Fouten bij scannen of onduidelijke feedback kunnen frustreren.  
- **Mitigatie:**  
  - Strakke planning en duidelijke communicatie.  
  - Regelmatige code reviews en uitgebreide tests.  
  - Gebruik van bewezen technologieën.

---

## Installatie & Gebruik
1. Virtuele omgeving aanmaken en activeren:  
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
2. Packages installeren:  
   ```bash
   pip install -r requirements.txt
   ```
3. Applicatie starten:  
   ```bash
   python -m src.main
   ```


---

# Self-Checkout System – Project BITEWISE

An innovative Python project for a digital self-checkout system with a product database and environmental score.  
Focused on reducing queues and promoting sustainable choices in the cafeteria.

---

## Background & Objectives
- Long queues in the Zuyd University cafeteria, especially during peak hours  
- Increased workload and reduced customer satisfaction  
- Growing importance of sustainability and CO₂ awareness  
- Assignment: develop a proof-of-concept self-checkout system that:  
  - Speeds up the checkout process  
  - Provides insight into the environmental impact of products  
- Goal: create a more efficient, sustainable, and customer-friendly cafeteria environment

---

## Project Outcome
- Functional self-checkout application with a simple scan interface  
- Products automatically added to a digital basket  
- Real-time updates of total price and CO₂ impact per product  
- Product information with categories and environmental scores stored in a linked database  
- Backend built with Flask, providing API routes for product and basket management  
- No actual payment processing in this phase, but architecture supports future integration  
- Hosted on Azure for scalability and reliability  
- Prototype developed within 10 weeks

---

## Team & Roles
| Name             | Role                         |
|------------------|------------------------------|
| Roy Geerkens     | Team Leader                  |
| Tom Theunissen   | Lead Developer & Scrum Master|
| Winston Dang     | Secretary                    |
| Niels Theunissen | Timekeeper                   |

---

## Project Structure
- Agile approach with weekly Scrum sprints and stand-up meetings  
- Trello used for task management and sprint planning  
- Go/No-Go moments for key decisions and progress evaluations  
- Clear communication and efficient task distribution within the team

---

## Technology & Architecture
- **Backend:** Flask web framework with API routes for product and basket management  
- **Database:** Product database containing categories and environmental scores; local setup with an option for Azure SQL  
- **Directory structure:**  
  - `src/`: main application code and business logic  
  - `templates/`: HTML frontend  
  - `static/`: CSS, JavaScript, and image files  
  - `database/`: datasets and database scripts  
- **Hosting:** Azure cloud platform with automatic scaling and monitoring  
- **Frontend:** simple, user-friendly interface with real-time updates  
- **Future expansions:** integration with Azure SQL, payment modules, and reporting features

---

## Quality & Risks
- **Quality:**  
  - Intuitive interface for quick learning and easy use  
  - Protection of user data and secure backend communication  
  - Fast response times and minimal load times, even with large product lists  
- **Risks:**  
  - Dependency on a stable internet connection  
  - Possible inconsistencies between database and frontend display  
  - Scanning errors or unclear feedback may cause frustration  
- **Mitigation:**  
  - Tight planning and clear communication  
  - Regular code reviews and thorough testing  
  - Use of proven, reliable technologies

---

## Installation & Usage
1. Create and activate a virtual environment:  
   - **Mac/Linux:**  
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```  
   - **Windows (PowerShell):**  
     ```bash
     python -m venv venv
     venv\Scripts\Activate.ps1
     ```  
   - **Windows (CMD):**  
     ```bash
     python -m venv venv
     venv\Scripts\activate.bat
     ```
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

3. Start the application:  
    ```bash
    python -m src.main
    ```