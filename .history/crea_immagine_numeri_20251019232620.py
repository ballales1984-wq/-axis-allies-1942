"""
Crea un'immagine PNG della mappa con tutti i numeri
così l'utente può guardarla senza far girare Python
"""
import pygame
import json
import sys
import os

def resource_path(relative_path):
    """Trova il percorso corretto per le risorse"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Inizializza Pygame
pygame.init()

# Carica la mappa
try:
    mappa = pygame.image.load(resource_path("mappa_hd.jpg"))
except:
    print("[ERRORE] mappa_hd.jpg non trovata!")
    sys.exit(1)

# Ridimensiona
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
mappa = pygame.transform.scale(mappa, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Crea surface
surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
surface.blit(mappa, (0, 0))

# Carica territori
with open(resource_path("centri.json"), 'r', encoding='utf-8') as f:
    territories = json.load(f)

# Font
font_big = pygame.font.Font(None, 32)
font_small = pygame.font.Font(None, 18)

# Colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

print("\n[INFO] Creazione immagine con numeri...")
print(f"[INFO] Territori totali: {len(territories)}")

# Overlay scuro per leggibilità
overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
overlay.fill((0, 0, 0, 120))
surface.blit(overlay, (0, 0))

# Disegna tutti i territori
for i, t in enumerate(territories):
    x, y = t['x'], t['y']
    id_num = t['id']
    name = t['name']
    
    # Cerchio giallo più grande
    pygame.draw.circle(surface, YELLOW, (x, y), 12)
    pygame.draw.circle(surface, WHITE, (x, y), 12, 2)
    
    # Numero grande e NERO per contrasto
    num_text = font_big.render(str(id_num), True, BLACK)
    num_rect = num_text.get_rect(center=(x, y))
    surface.blit(num_text, num_rect)
    
    # Nome sotto (più grande e con sfondo)
    name_text = font_small.render(f"{id_num}:{name}", True, WHITE)
    name_rect = name_text.get_rect(center=(x, y + 20))
    
    # Sfondo per nome
    name_bg = name_rect.inflate(8, 4)
    pygame.draw.rect(surface, (0, 0, 0, 220), name_bg)
    pygame.draw.rect(surface, YELLOW, name_bg, 1)
    surface.blit(name_text, name_rect)
    
    if (i + 1) % 10 == 0:
        print(f"[INFO] Disegnati {i + 1}/{len(territories)} territori...")

# Titolo in alto
title_font = pygame.font.Font(None, 48)
title_text = title_font.render("MAPPA CON NUMERI TERRITORI", True, WHITE)
title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 30))

# Sfondo per titolo
title_bg = title_rect.inflate(40, 20)
pygame.draw.rect(surface, (0, 0, 0, 230), title_bg)
pygame.draw.rect(surface, YELLOW, title_bg, 3)
surface.blit(title_text, title_rect)

# Info in basso
info_font = pygame.font.Font(None, 28)
info_text = info_font.render(f"Totale: {len(territories)} territori - Compila LISTA_TERRITORI_DA_COMPILARE.txt", True, WHITE)
info_rect = info_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))

info_bg = info_rect.inflate(30, 15)
pygame.draw.rect(surface, (0, 0, 0, 230), info_bg)
pygame.draw.rect(surface, YELLOW, info_bg, 2)
surface.blit(info_text, info_rect)

# Salva immagine
output_file = "MAPPA_CON_NUMERI.png"
pygame.image.save(surface, output_file)

print(f"\n[OK] Immagine creata: {output_file}")
print(f"[INFO] Apri l'immagine per vedere tutti i {len(territories)} territori numerati!")
print("\nOra compila il file: LISTA_TERRITORI_DA_COMPILARE.txt")
print("(Si trova sul DESKTOP)\n")

pygame.quit()

