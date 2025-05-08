# testautomation-ecommerce

Projekt für automatisierten Test

## Testablauf

1. Öffnet die Startseite des Demo-Shops
2. Prüft, ob die Hauptüberschrift "Shop" sichtbar ist
3. Prüft, ob der Warenkorb zu Beginn leer ist
4. Legt den Artikel "Album" in den Warenkorb
5. Öffnet den Warenkorb
6. Ändert die Menge des Artikels auf 2
7. Klickt auf "Update Cart"
8. Überprüft, ob Gesamtpreis 30€ beträgt

## Vorraussetzungen

- Python 3.8+
- pip
- playwright, pip install playwright
- Git Bash / cmd

## Installation

1. Repo klonen
2. Abhänigkeiten installieren (pip install -r requirements.txt)

## Test ausführen

pytest -s tests/test_shop.py