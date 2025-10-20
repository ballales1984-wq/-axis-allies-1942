"""
Completa e armonizza i confini degli stati
Rileva bordi tra colori diversi e li rende uniformi
"""

from PIL import Image, ImageDraw, ImageFilter
import numpy as np

def carica_mappa():
    """Carica la mappa Axis & Allies"""
    try:
        img = Image.open("mappa_axis_allies.png")
        print(f"[OK] Mappa caricata: {img.size[0]}x{img.size[1]}")
        return img
    except:
        print("[ERRORE] mappa_axis_allies.png non trovata!")
        return None

def rileva_bordi(img):
    """Rileva i bordi/confini tra stati"""
    from PIL import ImageFilter
    
    print("[1/4] Rilevamento bordi...")
    
    # Converti in scala di grigi
    gray = img.convert('L')
    
    # Rileva bordi con filtro
    edges = gray.filter(ImageFilter.FIND_EDGES)
    
    # Aumenta contrasto bordi
    edges = edges.point(lambda x: 255 if x > 20 else 0)
    
    print("[OK] Bordi rilevati")
    return edges

def rinforza_confini(img, edges):
    """Rinforza e completa i confini"""
    print("[2/4] Rinforzo confini...")
    
    # Converti in array numpy
    img_array = np.array(img)
    edges_array = np.array(edges)
    
    # Dilata i bordi per renderli più spessi
    from scipy.ndimage import binary_dilation
    edges_dilated = binary_dilation(edges_array > 128, iterations=2)
    
    # Applica bordi neri sull'immagine
    img_array[edges_dilated] = [0, 0, 0]  # Nero
    
    result = Image.fromarray(img_array)
    print("[OK] Confini rinforzati")
    
    return result

def armonizza_colori(img):
    """Armonizza i colori degli stati (riduce variazioni)"""
    print("[3/4] Armonizzazione colori...")
    
    # Riduci palette colori
    img_quantized = img.quantize(colors=50)  # Max 50 colori
    img_quantized = img_quantized.convert('RGB')
    
    print("[OK] Colori armonizzati")
    return img_quantized

def salva_risultato(img):
    """Salva la mappa con confini completati"""
    print("[4/4] Salvataggio...")
    
    # Ridimensiona a dimensioni gioco
    img_final = img.resize((1400, 800), Image.Resampling.LANCZOS)
    
    img_final.save("mappa_confini_completi.png")
    print("[OK] Salvata: mappa_confini_completi.png")
    
    return img_final

def main():
    print("="*70)
    print("COMPLETAMENTO E ARMONIZZAZIONE CONFINI")
    print("="*70)
    print()
    
    # Carica
    img = carica_mappa()
    if not img:
        return
    
    # Rileva bordi
    edges = rileva_bordi(img)
    
    # Rinforza confini
    try:
        img_confini = rinforza_confini(img, edges)
    except ImportError:
        print("[INFO] scipy non installato, salto rinforzo automatico")
        img_confini = img
    
    # Armonizza
    img_armonica = armonizza_colori(img_confini)
    
    # Salva
    img_finale = salva_risultato(img_armonica)
    
    print()
    print("="*70)
    print("COMPLETATO!")
    print("="*70)
    print()
    print("Mappa creata:")
    print("  - mappa_confini_completi.png")
    print()
    print("Ora visualizza con:")
    print("  python main.py")
    print("="*70)

if __name__ == "__main__":
    main()

