"""
Visualizza centri con i colori degli stati dalla mappa
"""

import pygame
import sys
import json
import os

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Centri Stati con Colori Reali")
    
    # Carica mappa
    maps = ["mappa_hd.jpg", "sfondo_classico.png", "mappa_semplice.jpg"]
    background = None
    for filename in maps:
        if os.path.exists(filename):
            try:
                background = pygame.image.load(filename)
                background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
                print(f"[OK] Mappa: {filename}")
                break
            except:
                pass
    
    # Carica centri
    with open("centri.json", "r") as f:
        centri = json.load(f)
    
    print(f"[OK] Caricati {len(centri)} centri con colori")
    print("="*70)
    
    font = pygame.font.Font(None, 16)
    clock = pygame.time.Clock()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Draw
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((40, 70, 100))
        
        # Disegna ogni centro CON IL SUO COLORE
        for centro in centri:
            x, y = centro['x'], centro['y']
            
            # Colore dello stato
            if 'color' in centro:
                r, g, b = centro['color']
                stato_color = (r, g, b)
            else:
                stato_color = (150, 150, 150)
            
            # Cerchio grande con colore stato (semi-trasparente)
            s = pygame.Surface((70, 70), pygame.SRCALPHA)
            pygame.draw.circle(s, (*stato_color, 150), (35, 35), 33)
            screen.blit(s, (x - 35, y - 35))
            
            # Bordo
            pygame.draw.circle(screen, (0, 0, 0), (x, y), 33, 2)
            
            # Punto centro
            pygame.draw.circle(screen, (255, 255, 255), (x, y), 4)
            
            # ID
            id_text = font.render(str(centro['id']), True, (255, 255, 255))
            id_rect = id_text.get_rect(center=(x, y))
            # Sfondo nero per leggibilità
            bg = pygame.Surface((id_rect.width + 6, id_rect.height + 4))
            bg.set_alpha(200)
            bg.fill((0, 0, 0))
            screen.blit(bg, (id_rect.x - 3, id_rect.y - 2))
            screen.blit(id_text, id_rect)
        
        # Info
        info_text = font.render(f"{len(centri)} stati con colori | ESC=Esci", True, (255, 255, 255))
        bg_info = pygame.Surface((info_text.get_width() + 20, info_text.get_height() + 10))
        bg_info.set_alpha(220)
        bg_info.fill((0, 0, 60))
        screen.blit(bg_info, (10, 10))
        screen.blit(info_text, (20, 15))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()

