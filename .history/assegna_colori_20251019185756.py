"""
Assegna ad ogni centro il colore dello stato dalla mappa
"""

from PIL import Image
import json
import os

def main():
    print("="*70)
    print("ASSEGNAZIONE COLORI AI CENTRI")
    print("="*70)
    print()
    
    # Carica centri
    with open("centri.json", "r") as f:
        centri = json.load(f)
    
    print(f"[OK] Caricati {len(centri)} centri")
    
    # Carica mappa
    maps = ["mappa_hd.jpg", "sfondo_classico.png", "mappa_semplice.jpg", "mappa.png"]
    img = None
    
    for filename in maps:
        if os.path.exists(filename):
            try:
                img = Image.open(filename)
                img = img.resize((1400, 800))  # Dimensioni gioco
                print(f"[OK] Mappa caricata: {filename}")
                break
            except:
                pass
    
    if not img:
        print("[ERRORE] Nessuna mappa trovata!")
        return
    
    # Converti in array
    import numpy as np
    img_array = np.array(img)
    
    # Campiona colore per ogni centro
    print("\nCampionamento colori...")
    print("-"*70)
    
    for centro in centri:
        x, y = centro['x'], centro['y']
        
        # Assicura che le coordinate siano valide
        if 0 <= x < 1400 and 0 <= y < 800:
            # Campiona colore dal punto
            try:
                r, g, b = img_array[y, x, :3]
                centro['color'] = [int(r), int(g), int(b)]
                
                print(f"  {centro['id']:2d}. {centro['name']:20s} -> RGB({r:3d}, {g:3d}, {b:3d})")
            except:
                centro['color'] = [150, 150, 150]  # Grigio default
                print(f"  {centro['id']:2d}. {centro['name']:20s} -> ERRORE, uso grigio")
        else:
            centro['color'] = [150, 150, 150]
            print(f"  {centro['id']:2d}. {centro['name']:20s} -> coordinate invalide")
    
    # Salva centri con colori
    with open("centri.json", "w") as f:
        json.dump(centri, f, indent=2)
    
    print()
    print("="*70)
    print("COMPLETATO!")
    print("="*70)
    print(f"Salvati {len(centri)} centri con i loro colori in centri.json")
    print()
    print("Ora visualizza con:")
    print("  python visualizza_centri_colorati.py")

if __name__ == "__main__":
    main()

