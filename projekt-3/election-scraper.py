"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Karel Provázek
email: provazek@24s.cz
discord: provazek24s.cz_84357
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv

# Kontrola, zda byly zadány argumenty
if len(sys.argv) != 3:
    print("Použití: python projekt_3.py <url> <výstupní soubor>")
    sys.exit(1)

url = sys.argv[1]
output_file = sys.argv[2]

# Stažení obsahu stránky s hlavičkou User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
response = requests.get(url, headers=headers)

# Kontrola, zda požadavek proběhl úspěšně
if response.status_code != 200:
    print(f"Chyba při načítání stránky: {response.status_code}")
    sys.exit(1)

# Předání HTML obsahu do BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Pro ukázku si vypíšeme HTML titulek stránky
print(f"Titulní stránka: {soup.title.string}")

# Najdeme všechny tabulky na stránce, bez ohledu na třídu
tables = soup.find_all('table')

# Seznam pro uložení dat
data = []

# Funkce pro zpracování sloučených buněk
def expand_row(row):
    expanded_row = []
    for cell in row:
        colspan = int(cell.get('colspan', 1))  # Pokud má buňka atribut colspan, použije se jeho hodnota, jinak 1
        rowspan = int(cell.get('rowspan', 1))  # Totéž pro rowspan
        text = cell.get_text(separator=' ').strip()

        # Pokud je to buňka záhlaví (th), zvýrazníme ji
        if cell.name == 'th':
            text = f"***{text}***"

        # Přidáme buňku i se zohledněným colspan
        expanded_row.extend([text] * colspan)
    return expanded_row

# Zpracujeme všechny nalezené tabulky
for table_index, table in enumerate(tables):
    print(f"Zpracovávám tabulku číslo {table_index + 1}")
    
    # Najdeme všechny řádky v tabulce (včetně hlavičky)
    rows = table.find_all('tr')

    # Zpracujeme každý řádek
    for row in rows:
        cells = row.find_all(['th', 'td'])
        
        if len(cells) > 0:
            expanded_row = expand_row(cells)
            # Přidáme data do seznamu
            data.append(expanded_row)

    # Po každé tabulce přidáme prázdný řádek pro oddělení tabulek
    data.append([])

# Uložení dat do CSV souboru
if data:
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Zapsání všech získaných dat
        writer.writerows(data)
    print(f"Data byla úspěšně uložena do souboru {output_file}")
else:
    print("Nenašla se žádná data pro uložení.")
