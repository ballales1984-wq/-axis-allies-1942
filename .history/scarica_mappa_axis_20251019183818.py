"""
Scarica la mappa vera di Axis & Allies
"""

import urllib.request

def scarica_mappa():
    url = "https://static.wikia.nocookie.net/axisandallies/images/6/69/War_of_Nations_3_0_Final.png/revision/latest/scale-to-width-down/1200"
    
    print("Scarico mappa Axis & Allies War of Nations...")
    print(f"URL: {url}")
    
    try:
        urllib.request.urlretrieve(url, "mappa_axis_allies.png")
        print("[OK] Mappa scaricata: mappa_axis_allies.png")
        return True
    except Exception as e:
        print(f"[ERRORE] {e}")
        return False

if __name__ == "__main__":
    scarica_mappa()

