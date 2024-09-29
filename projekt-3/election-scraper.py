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

# Funkce pro kontrolu argumentů
def check_arguments():
    if len(sys.argv) != 3:
        print("Použití: python projekt_3.py <url> <výstupní soubor>")
        sys.exit(1)
    return sys.argv[1], sys.argv[2]

# Funkce pro načtení stránky
def fetch_page_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Chyba při načítání stránky: {response.status_code}")
        sys.exit(1)
    return BeautifulSoup(response.text, 'html.parser')

# Funkce pro zpracování sloučených buněk
def expand_row(row):
    expanded_row = []
    for cell in row:
        colspan = int(cell.get('colspan', 1))
        rowspan = int(cell.get('rowspan', 1))
        text = cell.get_text(separator=' ').strip()
        if cell.name == 'th':
            text = f"***{text}***"
        expanded_row.extend([text] * colspan)
    return expanded_row

# Funkce pro zpracování všech tabulek
def process_tables(soup):
    tables = soup.find_all('table')
    data = []
    for table_index, table in enumerate(tables):
        print(f"Zpracovávám tabulku číslo {table_index + 1}")
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all(['th', 'td'])
            if len(cells) > 0:
                expanded_row = expand_row(cells)
                data.append(expanded_row)
        data.append([])  # Přidáme prázdný řádek pro oddělení tabulek
    return data

# Funkce pro uložení dat do CSV
def save_to_csv(data, output_file):
    if data:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
        print(f"Data byla úspěšně uložena do souboru {output_file}")
    else:
        print("Nenašla se žádná data pro uložení.")

# Hlavní funkce
def main():
    url, output_file = check_arguments()
    soup = fetch_page_content(url)
    print(f"Titulní stránka: {soup.title.string}")
    data = process_tables(soup)
    save_to_csv(data, output_file)

if __name__ == "__main__":
    main()
