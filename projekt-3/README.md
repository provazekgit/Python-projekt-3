# Election Scraper výsledků voleb z roku 2017

## Python projekt 3 Engeto Akademie

Tento projekt je Election scraper, který stahuje výsledky voleb z roku 2017 z webu volby.cz. Odkaz [ZDE](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)

Ukázka výběru lokality Odkaz [ZDE](https://www.volby.cz/pls/ps2017nss/ps31?xjazyk=CZ&xkraj=4&xnumnuts=3203)

Ukázka výběru lokality 2 Odkaz [ZDE](https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xnumnuts=3204)

Data se stahují a ukládají do souboru CSV.

## Instalace a požadavky

Nejprve vytvořte virtuální prostředí a nainstalujte potřebné knihovny:

```bash
cd /cesta_k_projektu
python -m venv venv
source venv/bin/activate   # Pro Linux/Mac
venv\Scripts\activate      # Pro Windows
pip install -r requirements.txt
```

`````markdown
## Spuštění projektu

Spuštění souboru election-scraper.py

Skript vyžaduje dva argumenty: URL stránky s výsledky a název výstupního souboru CSV.

## Příklad spuštění:

Výsledky hlasování Plzeň město

1. argument: https://www.volby.cz/pls/ps2017nss/ps31?xjazyk=CZ&xkraj=4&xnumnuts=3203
2. argument: vysledky-plzen.csv

Kompletní příklad
python election-scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xnumnuts=3204" plzen-jih1.csv



````bash
python election-scraper.py "https://www.volby.cz/pls/ps2017nss/ps31?xjazyk=CZ&xkraj=4&xnumnuts=3203" vysledky-plzen.csv

python election-scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=4&xnumnuts=3204" plzen-jih1.csv



## Ukázka scriptu:

```python # Ukázka kódu ze skriptu:
# Funkce pro načtení obsahu stránky
def get_page_content(link):
    response = requests.get(link)
    if response.status_code != 200:
        print(f"Chyba: Stránku {link} se nepodařilo načíst")
        return None
    return BeautifulSoup(response.text, 'html.parser')

# Funkce pro načtení základních informací (voliči, obálky, hlasy)
def get_basic_info(soup):
    table = soup.find('table', {'id': 'ps311_t1'})
    if not table:
        print(f"Chyba: Tabulka s ID 'ps311_t1' nenalezena.")
        return None, None, None

    rows = table.find_all('tr')
    try:
        registered = format_number(rows[2].find_all('td')[3].text.strip())
        envelopes = format_number(rows[2].find_all('td')[4].text.strip())
        valid_votes = format_number(rows[2].find_all('td')[7].text.strip())
        return registered, envelopes, valid_votes
    except (IndexError, AttributeError):
        return None, None, None

````
