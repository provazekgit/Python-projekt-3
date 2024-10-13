"""
election-scraper.py: Projekt do Engeto Online Python Akademie
author: Karel Provázek
email: provazek@24s.cz
discord: provazek24s.cz_84357
"""

import sys
import csv
import requests
from bs4 import BeautifulSoup

# Funkce pro přidání mezer do čísel (např. "123456" -> "123 456")
def format_number(value):
    try:
        clean_value = value.replace(" ", "")  # Odstraníme mezery, pokud už tam jsou
        return f"{int(clean_value):,}".replace(",", " ")  # Přidáme mezery po třech číslicích
    except (ValueError, AttributeError):
        return value  # Pokud není hodnota číslem, vrátíme ji tak, jak je

# Seznam politických stran
party_names = [
    "Občanská demokratická strana",
    "Řád národa - Vlastenecká unie",
    "CESTA ODPOVĚDNÉ SPOLEČNOSTI",
    "Česká str.sociálně demokrat.",
    "Radostné Česko",
    "STAROSTOVÉ A NEZÁVISLÍ",
    "Komunistická str.Čech a Moravy",
    "Strana zelených",
    "ROZUMNÍ-stop migraci,diktát.EU",
    "Strana svobodných občanů",
    "Blok proti islam.-Obran.domova",
    "Občanská demokratická aliance",
    "Česká pirátská strana",
    "OBČANÉ 2011-SPRAVEDL. PRO LIDI",
    "Referendum o Evropské unii",
    "TOP 09",
    "ANO 2011",
    "SPR-Republ.str.Čsl. M.Sládka",
    "Křesť.demokr.unie-Čs.str.lid.",
    "Česká strana národně sociální",
    "REALISTÉ",
    "SPORTOVCI",
    "Dělnic.str.sociální spravedl.",
    "Svob.a př.dem.-T.Okamura (SPD)",
    "Strana Práv Občanů"
]

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

# Funkce pro načtení hlasů pro strany z tabulek
def get_party_votes(soup, table_id):
    table = soup.find('th', {'id': table_id}).find_parent('table')
    if not table:
        print(f"Chyba: Tabulka s ID '{table_id}' nenalezena.")
        return []

    party_votes = []
    for row in table.find_all('tr')[2:]:
        cells = row.find_all('td')
        if len(cells) > 1:
            party_votes.append(format_number(cells[2].text.strip()))
    return party_votes

# Funkce pro zpracování dat z jednotlivých obcí
def process_obec(link):
    soup = get_page_content(link)
    if soup is None:
        return None, None, None, []

    # Načteme základní informace
    registered, envelopes, valid_votes = get_basic_info(soup)

    # Načteme hlasy pro strany z obou tabulek
    party_votes_1 = get_party_votes(soup, 't1sb3')
    party_votes_2 = get_party_votes(soup, 't2sb3')
    party_votes = party_votes_1 + party_votes_2

    # Přidáme prázdné hodnoty, pokud je málo hlasů
    while len(party_votes) < len(party_names):
        party_votes.append('')

    return registered, envelopes, valid_votes, party_votes

# Funkce pro zpracování všech obcí na stránce
def process_all_tables(soup):
    data = []
    tables = soup.find_all('table')

    for table in tables:
        for row in table.find_all('tr')[2:]:
            cells = row.find_all('td')
            if len(cells) >= 2:
                number = cells[0].text.strip()
                name = cells[1].text.strip()
                link_tag = cells[0].find('a')
                if link_tag and 'href' in link_tag.attrs:
                    link = 'https://www.volby.cz/pls/ps2017nss/' + link_tag['href']
                    registered, envelopes, valid_votes, party_votes = process_obec(link)
                    data.append([number, name, registered, envelopes, valid_votes] + party_votes)
    return data

# Funkce pro vytvoření CSV souboru
def create_csv(output_file, data):
    header = ['Kód obce (code)', 'Název obce (location)', 'Počet voličů (registered)', 'Vydané obálky (envelop)', 'Platné hlasy (valid)'] + party_names

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(data)

    print(f"Soubor {output_file} byl úspěšně vytvořen.")

# Hlavní funkce
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Použití: python election-scraper.py <URL> <název_souboru.csv>")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]

    soup = get_page_content(url)
    if soup is None:
        sys.exit(1)

    data = process_all_tables(soup)
    create_csv(output_file, data)
