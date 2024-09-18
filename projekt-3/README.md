# Election Scraper výsledků voleb z roku 2017

## Python projekt 3 Engeto Akademie

Tento projekt je Election scraper, který stahuje výsledky voleb z roku 2017 z webu volby.cz. Odkaz [ZDE](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)
Ukázka výběru lokality Odkaz [ZDE](https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=4&xnumnuts=3203)

Data se stahují a ukládají do souboru CSV.

## Instalace a požadavky

Nejprve vytvořte virtuální prostředí a nainstalujte potřebné knihovny:

```bash
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

1. argument: https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=4&xnumnuts=3203
2. argument: vysledky-plzen.csv

````bash
python election-scraper.py "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=4&xnumnuts=3203" vysledky-plzen.csv

## Ukázka scriptu:

```python # Ukázka kódu ze skriptu:
import requests
from bs4 import BeautifulSoup

url = "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=4&xnumnuts=3203"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

print(soup.title.string)

print(soup.title.string)
python election-scraper.py "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=4&xnumnuts=3203" vysledky-plzen.csv
````
`````

```

```
