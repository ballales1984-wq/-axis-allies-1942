"""
Axis & Allies 1942 - Sistema a Griglia MASSIMA
Griglia fine adattata a mappa politica SENZA scritte
"""

import pygame
import sys
import json

# GRIGLIA MASSIMA possibile
GRID_WIDTH = 280   # Massimo quadrati orizzontali
GRID_HEIGHT = 160  # Massimo quadrati verticali
# Totale: 44,800 quadrati!

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

def carica_griglia_pulita():
    """Carica la griglia pulita o la crea"""
    try:
        with open("griglia_pulita.json", "r") as f:
            griglia_str = json.load(f)
        griglia = {}
        for key, value in griglia_str.items():
            x, y = map(int, key.split(','))
            griglia[(x, y)] = value
        print(f"[OK] Griglia caricata: {len(griglia)} celle")
        return griglia
    except:
        print("[INFO] Griglia non trovata, la creo ora...")
        return crea_griglia_da_mappa()

def crea_griglia_da_mappa():
    """Crea griglia campionando la mappa senza scritte"""
    from PIL import Image
    import numpy as np
    
    # Usa mappa SEMPLIFICATA (SOLO CONFINI!)
    try:
        img = Image.open("mappa_semplice.jpg")
        print(f"[OK] Uso MAPPA SEMPLIFICATA (SOLO confini, ZERO scritte)!")
    except:
        try:
            img = Image.open("mappa_confini_completi.png")
            print(f"[OK] Uso mappa confini completi")
        except:
            try:
                img = Image.open("mappa_axis_allies.png")
                print(f"[OK] Uso mappa Axis & Allies")
            except:
                print("[ERRORE] Nessuna mappa trovata!")
                return {}
    
    # Ridimensiona a dimensioni schermo
    img = img.resize((SCREEN_WIDTH, SCREEN_HEIGHT))
    img_array = np.array(img)
    
    griglia = {}
    
    print(f"Campionamento griglia {GRID_WIDTH}x{GRID_HEIGHT}...")
    
    cell_w = SCREEN_WIDTH / GRID_WIDTH
    cell_h = SCREEN_HEIGHT / GRID_HEIGHT
    
    for gx in range(GRID_WIDTH):
        for gy in range(GRID_HEIGHT):
            px = int(gx * cell_w + cell_w/2)
            py = int(gy * cell_h + cell_h/2)
            
            try:
                r, g, b = img_array[py, px, :3]
                
                # Mare = blu, Terra = altri colori
                is_sea = b > r + 20 and b > g + 20
                
                griglia[(gx, gy)] = {
                    "color": [int(r), int(g), int(b)],
                    "type": "sea" if is_sea else "land"
                }
            except:
                griglia[(gx, gy)] = {"color": [100, 100, 100], "type": "unknown"}
    
    print(f"[OK] Griglia creata: {len(griglia)} celle")
    return griglia

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(f"Griglia {GRID_WIDTH}x{GRID_HEIGHT} = {GRID_WIDTH*GRID_HEIGHT} quadrati")
    
    griglia = carica_griglia_pulita()
    
    # Dimensione celle in pixel
    cell_w = SCREEN_WIDTH / GRID_WIDTH
    cell_h = SCREEN_HEIGHT / GRID_HEIGHT
    
    print("="*70)
    print(f"GRIGLIA MASSIMA: {GRID_WIDTH} x {GRID_HEIGHT} = {GRID_WIDTH*GRID_HEIGHT} quadrati")
    print(f"Dimensione quadrato: {cell_w:.2f} x {cell_h:.2f} pixel")
    print("="*70)
    
    # Pre-renderizza
    grid_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    for gx in range(GRID_WIDTH):
        for gy in range(GRID_HEIGHT):
            if (gx, gy) in griglia:
                r, g, b = griglia[(gx, gy)]["color"]
                px = gx * cell_w
                py = gy * cell_h
                rect = pygame.Rect(px, py, cell_w + 1, cell_h + 1)
                pygame.draw.rect(grid_surface, (r, g, b), rect)
    
    print("[OK] Griglia renderizzata")
    
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 20)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        screen.fill((0, 0, 0))
        screen.blit(grid_surface, (0, 0))
        
        # Info
        mx, my = pygame.mouse.get_pos()
        gx = int(mx / cell_w)
        gy = int(my / cell_h)
        
        if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
            if (gx, gy) in griglia:
                tipo = griglia[(gx, gy)]["type"]
                text = font.render(f"[{gx},{gy}] {tipo}", True, (255, 255, 0))
                screen.blit(text, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
