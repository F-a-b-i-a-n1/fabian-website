# Dieses Python Programm erstellt mir eine json Datei, die den gesamten Text in meinen HTML-Dateien enthält.
# Diese json Datei ist wichtig, damit ich mit der Such-Funktion (in der Navigationsleiste) über alle Seiten hinweg (Also "indexübergreifend") suchen kann.

import os
import json
from bs4 import BeautifulSoup

# Ordner, in dem die HTML-Dateien liegen
ROOT_DIR = '.'  # oder z. B. 'website'

# Index, der am Ende gespeichert wird
search_index = []

# Alle .html-Dateien durchgehen
for root, dirs, files in os.walk(ROOT_DIR):
    for file in files:
        if file.endswith('.html'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                text = soup.get_text(separator=' ', strip=True)
                rel_path = os.path.relpath(file_path, ROOT_DIR)
                search_index.append({
                    'url': rel_path.replace('\\', '/'),
                    'text': text
                })

# Ergebnis als JSON speichern
with open('search-index.json', 'w', encoding='utf-8') as out_file:
    json.dump(search_index, out_file, ensure_ascii=False, indent=2)

print("✅ search-index.json wurde erstellt.")