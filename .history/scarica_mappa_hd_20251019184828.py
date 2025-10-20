"""
Scarica mappa HD massima precisione
"""

import urllib.request

url = "https://as2.ftcdn.net/v2/jpg/00/66/78/17/1000_F_66781727_OK9gzibT7H8EK732ICkuqvEHHX6Rithw.jpg"

print("Scarico mappa HD massima precisione...")
print("Fonte: Adobe Stock - Mappa politica HD")

try:
    urllib.request.urlretrieve(url, "mappa_hd.jpg")
    print("[OK] Mappa HD scaricata: mappa_hd.jpg")
    print()
    print("MASSIMA DEFINIZIONE!")
except Exception as e:
    print(f"[ERRORE] {e}")

