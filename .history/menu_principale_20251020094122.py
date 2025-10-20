"""
MENU PRINCIPALE - Scegli modalità di gioco
"""

import pygame
import sys

def show_main_menu():
    """Mostra menu e ritorna scelta"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("GreatWar3 - Menu")
    clock = pygame.time.Clock()
    
    font_title = pygame.font.Font(None, 72)
    font_menu = pygame.font.Font(None, 48)
    font_small = pygame.font.Font(None, 24)
    
    # Opzioni
    options = [
        {"text": "1 - GIOCA SOLO (vs IA)", "mode": "singleplayer"},
        {"text": "2 - CREA PARTITA ONLINE (Server)", "mode": "server"},
        {"text": "3 - UNISCITI A PARTITA (Client)", "mode": "client"},
        {"text": "ESC - Esci", "mode": "quit"}
    ]
    
    selected = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                elif event.key == pygame.K_1:
                    return "singleplayer"
                elif event.key == pygame.K_2:
                    return "server"
                elif event.key == pygame.K_3:
                    return "client"
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected]["mode"]
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check click su opzioni
                for i, opt in enumerate(options):
                    y = 200 + i * 80
                    rect = pygame.Rect(150, y, 500, 60)
                    if rect.collidepoint(mouse_pos):
                        return opt["mode"]
        
        # Disegna
        screen.fill((20, 30, 50))
        
        # Titolo
        title = font_title.render("AXIS & ALLIES 1942", True, (255, 255, 100))
        title_rect = title.get_rect(center=(400, 80))
        screen.blit(title, title_rect)
        
        subtitle = font_small.render("Alleanze Mondiali", True, (200, 200, 200))
        subtitle_rect = subtitle.get_rect(center=(400, 140))
        screen.blit(subtitle, subtitle_rect)
        
        # Opzioni
        mouse_pos = pygame.mouse.get_pos()
        for i, opt in enumerate(options):
            y = 200 + i * 80
            rect = pygame.Rect(150, y, 500, 60)
            
            # Check hover
            is_hover = rect.collidepoint(mouse_pos) or i == selected
            
            # Sfondo
            if is_hover:
                pygame.draw.rect(screen, (80, 100, 150), rect)
            else:
                pygame.draw.rect(screen, (40, 50, 80), rect)
            
            pygame.draw.rect(screen, (150, 200, 255), rect, 3)
            
            # Testo
            color = (255, 255, 255) if is_hover else (200, 200, 200)
            text = font_menu.render(opt["text"], True, color)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        
        # Footer
        footer = font_small.render("Usa frecce o click per selezionare", True, (150, 150, 150))
        footer_rect = footer.get_rect(center=(400, 550))
        screen.blit(footer, footer_rect)
        
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    mode = show_main_menu()
    print(f"Modalita selezionata: {mode}")
    pygame.quit()


