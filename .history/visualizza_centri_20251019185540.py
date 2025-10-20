"""
Visualizza i centri posizionati sulla mappa
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
    pygame.display.set_caption("Centri Stati Posizionati")
    
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
    
    if not background:
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background.fill((40, 70, 100))
    
    # Carica centri
    with open("centri.json", "r") as f:
        centri = json.load(f)
    
    print(f"[OK] Caricati {len(centri)} centri")
    print("="*70)
    for c in centri:
        print(f"  {c['id']:2d}. {c['name']:20s} ({c['x']:4d}, {c['y']:3d})")
    print("="*70)
    
    font = pygame.font.Font(None, 18)
    font_name = pygame.font.Font(None, 16)
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
        screen.blit(background, (0, 0))
        
        # Disegna ogni centro
        for centro in centri:
            x, y = centro['x'], centro['y']
            
            # Cerchio area
            pygame.draw.circle(screen, (255, 200, 0, 100), (x, y), 30, 2)
            
            # Punto centro
            pygame.draw.circle(screen, (255, 0, 0), (x, y), 6)
            pygame.draw.circle(screen, (255, 255, 255), (x, y), 6, 2)
            
            # Nome
            name_text = font_name.render(centro['name'], True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(x, y - 35))
            bg = pygame.Surface((name_rect.width + 6, name_rect.height + 4))
            bg.set_alpha(200)
            bg.fill((0, 0, 0))
            screen.blit(bg, (name_rect.x - 3, name_rect.y - 2))
            screen.blit(name_text, name_rect)
            
            # ID
            id_text = font.render(str(centro['id']), True, (255, 255, 100))
            screen.blit(id_text, (x - 8, y - 8))
        
        # Info
        info = font.render(f"{len(centri)} centri posizionati | ESC=Esci", True, (255, 255, 255))
        bg_info = pygame.Surface((info.get_width() + 20, info.get_height() + 10))
        bg_info.set_alpha(220)
        bg_info.fill((0, 0, 60))
        screen.blit(bg_info, (10, 10))
        screen.blit(info, (20, 15))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()

