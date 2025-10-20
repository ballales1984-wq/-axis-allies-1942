"""
Scarica mappa mondiale semplificata SOLO CONFINI
"""

import urllib.request

url = "https://thumbs.dreamstime.com/z/cartina-mondiale-dei-confini-semplificata-mappa-schematica-del-mondo-carta-politica-vuota-paesi-con-frontiere-generalizzate-239335130.jpg"

print("Scarico mappa semplificata...")
print("Fonte: Dreamstime - Mappa politica vuota")

try:
    urllib.request.urlretrieve(url, "mappa_semplice.jpg")
    print("[OK] Mappa scaricata: mappa_semplice.jpg")
    print()
    print("Questa mappa ha:")
    print("  - SOLO confini")
    print("  - ZERO scritte")
    print("  - Colori uniformi")
    print("  - PERFETTA per il gioco!")
except Exception as e:
    print(f"[ERRORE] {e}")

