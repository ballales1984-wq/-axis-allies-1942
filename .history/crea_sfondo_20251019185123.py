"""
Crea sfondo personalizzato con colori modificabili
"""

from PIL import Image, ImageDraw
import numpy as np

# COLORI PERSONALIZZABILI
COLOR_MARE = (45, 85, 125)      # Blu mare
COLOR_TERRA = (120, 140, 100)   # Verde terra
COLOR_CONFINI = (0, 0, 0)       # Nero confini

WIDTH = 1400
HEIGHT = 800

def crea_sfondo_base():
    """Crea uno sfondo semplice mare + continenti"""
    
    print("Creazione sfondo personalizzato...")
    
    # Immagine base
    img = Image.new('RGB', (WIDTH, HEIGHT), COLOR_MARE)
    draw = ImageDraw.Draw(img)
    
    print("Disegno continenti...")
    
    # EUROPA (approssimata)
    europa_points = [
        (250, 450), (300, 550), (350, 600), (450, 620),
        (550, 600), (650, 550), (750, 500), (850, 550),
        (900, 600), (850, 650), (750, 650), (650, 620),
        (550, 650), (450, 680), (350, 650), (280, 600),
        (240, 520)
    ]
    draw.polygon(europa_points, fill=COLOR_TERRA, outline=COLOR_CONFINI, width=3)
    
    # AFRICA
    africa_points = [
        (280, 450), (400, 400), (550, 380), (650, 350),
        (680, 280), (650, 200), (550, 150), (450, 140),
        (350, 160), (280, 220), (250, 300), (240, 380)
    ]
    draw.polygon(africa_points, fill=COLOR_TERRA, outline=COLOR_CONFINI, width=3)
    
    # ASIA (grande)
    asia_points = [
        (850, 550), (950, 520), (1050, 500), (1150, 480),
        (1250, 450), (1300, 500), (1280, 580), (1200, 620),
        (1100, 640), (1000, 620), (920, 580)
    ]
    draw.polygon(asia_points, fill=COLOR_TERRA, outline=COLOR_CONFINI, width=3)
    
    # AMERICA (sinistra)
    america_nord = [
        (50, 600), (150, 650), (200, 680), (180, 580),
        (130, 520), (80, 500), (40, 540)
    ]
    draw.polygon(america_nord, fill=COLOR_TERRA, outline=COLOR_CONFINI, width=3)
    
    america_sud = [
        (150, 450), (220, 400), (250, 320), (230, 250),
        (180, 200), (130, 180), (100, 220), (90, 300),
        (110, 380)
    ]
    draw.polygon(america_sud, fill=COLOR_TERRA, outline=COLOR_CONFINI, width=3)
    
    # AUSTRALIA
    australia = [
        (1150, 300), (1250, 280), (1300, 250), (1320, 200),
        (1280, 160), (1200, 150), (1130, 180), (1100, 240)
    ]
    draw.polygon(australia, fill=COLOR_TERRA, outline=COLOR_CONFINI, width=3)
    
    img.save("sfondo_gioco.png")
    print("[OK] Sfondo salvato: sfondo_gioco.png")
    
    return img

def crea_varianti_colore():
    """Crea varianti con colori diversi"""
    
    print("\nCreo varianti colore...")
    
    # Variante 1: Classica (terra beige, mare blu scuro)
    img1 = Image.new('RGB', (WIDTH, HEIGHT), (30, 60, 100))
    draw1 = ImageDraw.Draw(img1)
    terra_beige = (200, 180, 140)
    
    # Disegna continenti
    for points in [europa_points, africa_points, asia_points]:
        draw1.polygon(points, fill=terra_beige, outline=(20, 20, 20), width=3)
    
    img1.save("sfondo_classico.png")
    print("[OK] Variante classica salvata")
    
    # Variante 2: Moderna (colori vivaci)
    img2 = Image.new('RGB', (WIDTH, HEIGHT), (60, 120, 180))
    draw2 = ImageDraw.Draw(img2)
    terra_verde = (100, 180, 80)
    
    for points in [europa_points, africa_points, asia_points]:
        draw2.polygon(points, fill=terra_verde, outline=(0, 0, 0), width=2)
    
    img2.save("sfondo_moderno.png")
    print("[OK] Variante moderna salvata")

# Definisco i punti globalmente per le varianti
europa_points = [(250, 450), (300, 550), (350, 600), (450, 620),
                 (550, 600), (650, 550), (750, 500), (850, 550),
                 (900, 600), (850, 650), (750, 650), (650, 620),
                 (550, 650), (450, 680), (350, 650), (280, 600), (240, 520)]

africa_points = [(280, 450), (400, 400), (550, 380), (650, 350),
                 (680, 280), (650, 200), (550, 150), (450, 140),
                 (350, 160), (280, 220), (250, 300), (240, 380)]

asia_points = [(850, 550), (950, 520), (1050, 500), (1150, 480),
               (1250, 450), (1300, 500), (1280, 580), (1200, 620),
               (1100, 640), (1000, 620), (920, 580)]

if __name__ == "__main__":
    print("="*70)
    print("CREAZIONE SFONDI PERSONALIZZATI")
    print("="*70)
    print()
    
    crea_sfondo_base()
    crea_varianti_colore()
    
    print()
    print("="*70)
    print("Sfondi creati:")
    print("  - sfondo_gioco.png (base)")
    print("  - sfondo_classico.png (beige/blu)")
    print("  - sfondo_moderno.png (verde/azzurro)")
    print("="*70)

