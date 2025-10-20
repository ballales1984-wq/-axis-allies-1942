"""
Visualizza la mappa con i NUMERI dei territori
per permettere all'utente di associare i nomi reali
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
    print("Errore: mappa_hd.jpg non trovata!")
    sys.exit(1)

# Ridimensiona se troppo grande
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800
mappa = pygame.transform.scale(mappa, (SCREEN_WIDTH, SCREEN_HEIGHT))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("MAPPA CON NUMERI - Dimmi i nomi reali!")

# Carica territori
with open(resource_path("centri.json"), 'r', encoding='utf-8') as f:
    territories = json.load(f)

# Font
font_big = pygame.font.Font(None, 28)
font_small = pygame.font.Font(None, 16)

# Colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Stato
current_page = 0
territories_per_page = 20
total_pages = (len(territories) + territories_per_page - 1) // territories_per_page

running = True
clock = pygame.time.Clock()

print("\n" + "="*50)
print("MAPPA VISUALIZZATA!")
print("="*50)
print("\nCONTROLLI:")
print("  FRECCIA DESTRA/SINISTRA: Cambia pagina")
print("  ESC: Esci")
print("  MOUSE: Passa sopra un numero per vedere info")
print("\nOra dimmi i nomi delle città!")
print("="*50 + "\n")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RIGHT:
                current_page = min(current_page + 1, total_pages - 1)
            elif event.key == pygame.K_LEFT:
                current_page = max(current_page - 1, 0)
    
    # Disegna mappa
    screen.blit(mappa, (0, 0))
    
    # Overlay scuro per leggibilità
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    screen.blit(overlay, (0, 0))
    
    # Mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    hovered_territory = None
    
    # Disegna territori della pagina corrente
    start_idx = current_page * territories_per_page
    end_idx = min(start_idx + territories_per_page, len(territories))
    
    for i in range(start_idx, end_idx):
        t = territories[i]
        x, y = t['x'], t['y']
        id_num = t['id']
        name = t['name']
        
        # Cerchio giallo
        pygame.draw.circle(screen, YELLOW, (x, y), 8)
        pygame.draw.circle(screen, WHITE, (x, y), 8, 2)
        
        # Numero grande
        num_text = font_big.render(str(id_num), True, WHITE)
        num_rect = num_text.get_rect(center=(x, y))
        
        # Sfondo scuro per il numero
        bg_rect = num_rect.inflate(8, 4)
        pygame.draw.rect(screen, (0, 0, 0, 200), bg_rect)
        pygame.draw.rect(screen, YELLOW, bg_rect, 2)
        
        screen.blit(num_text, num_rect)
        
        # Nome sotto (piccolo)
        name_text = font_small.render(name, True, WHITE)
        name_rect = name_text.get_rect(center=(x, y + 15))
        
        # Sfondo per nome
        name_bg = name_rect.inflate(6, 2)
        pygame.draw.rect(screen, (0, 0, 0, 180), name_bg)
        screen.blit(name_text, name_rect)
        
        # Check hover
        dist = ((mouse_x - x) ** 2 + (mouse_y - y) ** 2) ** 0.5
        if dist < 15:
            hovered_territory = t
    
    # Info pagina in alto
    page_info = f"Pagina {current_page + 1}/{total_pages} - Territori {start_idx + 1}-{end_idx}/{len(territories)}"
    page_text = font_big.render(page_info, True, WHITE)
    page_bg = pygame.Rect(10, 10, page_text.get_width() + 20, 40)
    pygame.draw.rect(screen, (0, 0, 0, 200), page_bg)
    pygame.draw.rect(screen, YELLOW, page_bg, 2)
    screen.blit(page_text, (20, 20))
    
    # Istruzioni in basso
    help_text = "FRECCE: Cambia pagina | ESC: Esci | HOVER: Info territorio"
    help_surf = font_small.render(help_text, True, WHITE)
    help_bg = pygame.Rect(10, SCREEN_HEIGHT - 40, help_surf.get_width() + 20, 30)
    pygame.draw.rect(screen, (0, 0, 0, 200), help_bg)
    pygame.draw.rect(screen, YELLOW, help_bg, 2)
    screen.blit(help_surf, (20, SCREEN_HEIGHT - 30))
    
    # Info territorio hover
    if hovered_territory:
        info_lines = [
            f"ID: {hovered_territory['id']}",
            f"Nome attuale: {hovered_territory['name']}",
            f"Posizione: ({hovered_territory['x']}, {hovered_territory['y']})",
            f"Colore: RGB{tuple(hovered_territory['color'])}"
        ]
        
        # Box info
        info_y = 60
        for line in info_lines:
            info_text = font_small.render(line, True, WHITE)
            info_bg = pygame.Rect(10, info_y, info_text.get_width() + 20, 25)
            pygame.draw.rect(screen, (0, 0, 0, 220), info_bg)
            pygame.draw.rect(screen, RED, info_bg, 2)
            screen.blit(info_text, (20, info_y + 5))
            info_y += 28
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()

print("\n" + "="*50)
print("Programma terminato!")
print("="*50)

