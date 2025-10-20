"""
Axis & Allies 1942 - Sistema Conquista
Gli stati cambiano colore quando vengono conquistati
"""

import pygame
import sys
import json
import os

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

# COLORI FAZIONI
COLOR_ALLEATI = (50, 100, 255)      # Blu
COLOR_AXIS = (255, 50, 50)          # Rosso
COLOR_NEUTRALE = (150, 150, 150)    # Grigio
COLOR_SELECTED = (255, 215, 0)      # Oro

class Territory:
    """Territorio = uno stato con centro colorabile"""
    def __init__(self, data):
        self.id = data['id']
        self.name = data.get('name', f"Stato_{self.id}")
        self.x = data['x']
        self.y = data['y']
        self.original_color = tuple(data.get('color', [150, 150, 150]))
        
        # Proprietà di gioco
        self.owner = None  # None, "allies", "axis"
        self.units = 0
        self.selected = False
        self.radius = 20  # Cerchi più piccoli!
    
    def get_color(self):
        """Colore basato su chi controlla"""
        if self.owner == "allies":
            return COLOR_ALLEATI
        elif self.owner == "axis":
            return COLOR_AXIS
        else:
            return COLOR_NEUTRALE
    
    def contains_point(self, px, py):
        """Check se punto è dentro"""
        dist_sq = (px - self.x)**2 + (py - self.y)**2
        return dist_sq <= self.radius**2
    
    def draw(self, surface, font, font_small):
        """Disegna territorio"""
        color = self.get_color()
        
        # Bordo oro se selezionato
        if self.selected:
            pygame.draw.circle(surface, COLOR_SELECTED, (self.x, self.y), self.radius + 4, 4)
        
        # Cerchio principale (colorato per fazione!)
        pygame.draw.circle(surface, color, (self.x, self.y), self.radius)
        pygame.draw.circle(surface, (0, 0, 0), (self.x, self.y), self.radius, 2)
        
        # Nome
        name_text = font_small.render(self.name, True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(self.x, self.y - self.radius - 12))
        bg = pygame.Surface((name_rect.width + 6, name_rect.height + 4))
        bg.set_alpha(200)
        bg.fill((0, 0, 0))
        surface.blit(bg, (name_rect.x - 3, name_rect.y - 2))
        surface.blit(name_text, name_rect)
        
        # Unità (numero al centro)
        if self.units > 0:
            unit_text = font.render(str(self.units), True, (255, 255, 255))
            unit_rect = unit_text.get_rect(center=(self.x, self.y))
            surface.blit(unit_text, unit_rect)

class Game:
    """Gioco principale"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Axis & Allies 1942 - Conquista Stati")
        self.clock = pygame.time.Clock()
        
        # Font
        self.font = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 16)
        self.font_large = pygame.font.Font(None, 36)
        
        # Mappa
        self.background = self.load_background()
        
        # Territori
        self.territories = self.load_territories()
        
        # Giocatori
        self.current_faction = "allies"  # allies o axis
        
        # Setup iniziale
        self.setup_initial()
        
        # Selezione
        self.selected = None
        
        print("="*70)
        print("AXIS & ALLIES 1942 - SISTEMA CONQUISTA")
        print("="*70)
        print(f"Territori: {len(self.territories)}")
        print()
        print("Controlli:")
        print("  Click territorio = Seleziona")
        print("  SPAZIO = Cambia fazione (Alleati <-> Axis)")
        print("  C = Conquista territorio selezionato")
        print("  + = Aggiungi unità")
        print("  - = Rimuovi unità")
        print("  ESC = Esci")
        print("="*70)
    
    def load_background(self):
        """Carica mappa"""
        maps = ["mappa_hd.jpg", "sfondo_classico.png", "mappa_semplice.jpg"]
        for f in maps:
            if os.path.exists(f):
                try:
                    bg = pygame.image.load(f)
                    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    return bg
                except:
                    pass
        return None
    
    def load_territories(self):
        """Carica territori da centri.json"""
        with open("centri.json", "r") as f:
            data = json.load(f)
        
        territories = []
        for item in data:
            territories.append(Territory(item))
        
        return territories
    
    def setup_initial(self):
        """Setup iniziale - assegna alcuni territori"""
        # Alleati (primi 8)
        for i in range(0, 8):
            if i < len(self.territories):
                self.territories[i].owner = "allies"
                self.territories[i].units = 3
        
        # Axis (8-15)
        for i in range(8, 16):
            if i < len(self.territories):
                self.territories[i].owner = "axis"
                self.territories[i].units = 3
        
        # Resto neutrale
        for i in range(16, len(self.territories)):
            self.territories[i].owner = None
            self.territories[i].units = 2
    
    def run(self):
        """Game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    
                    elif event.key == pygame.K_SPACE:
                        # Cambia fazione
                        self.current_faction = "axis" if self.current_faction == "allies" else "allies"
                        print(f"Fazione attiva: {self.current_faction}")
                    
                    elif event.key == pygame.K_c:
                        # Conquista territorio selezionato
                        if self.selected:
                            self.selected.owner = self.current_faction
                            self.selected.units = 3
                            print(f"CONQUISTATO: {self.selected.name} -> {self.current_faction}")
                    
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        # Aggiungi unità
                        if self.selected:
                            self.selected.units += 1
                    
                    elif event.key == pygame.K_MINUS:
                        # Rimuovi unità
                        if self.selected and self.selected.units > 0:
                            self.selected.units -= 1
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_click(event.pos)
            
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()
    
    def handle_click(self, pos):
        """Gestisce click"""
        for terr in self.territories:
            if terr.contains_point(pos[0], pos[1]):
                # Deseleziona precedente
                if self.selected:
                    self.selected.selected = False
                
                # Seleziona nuovo
                self.selected = terr
                terr.selected = True
                
                owner_str = terr.owner if terr.owner else "Neutrale"
                print(f"Selezionato: {terr.name} ({owner_str}) - {terr.units} unità")
                break
    
    def draw(self):
        """Disegna tutto"""
        # Sfondo
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((40, 70, 100))
        
        # Territori (cambiano colore!)
        for terr in self.territories:
            terr.draw(self.screen, self.font, self.font_small)
        
        # UI
        self.draw_ui()
    
    def draw_ui(self):
        """UI"""
        # Pannello
        panel = pygame.Surface((SCREEN_WIDTH, 70))
        panel.set_alpha(220)
        panel.fill((30, 30, 60))
        self.screen.blit(panel, (0, 0))
        
        # Fazione attiva
        faction_name = "ALLEATI" if self.current_faction == "allies" else "AXIS"
        faction_color = COLOR_ALLEATI if self.current_faction == "allies" else COLOR_AXIS
        
        text = self.font_large.render(f"Fazione: {faction_name}", True, faction_color)
        self.screen.blit(text, (20, 15))
        
        # Conta territori
        allies_count = sum(1 for t in self.territories if t.owner == "allies")
        axis_count = sum(1 for t in self.territories if t.owner == "axis")
        neutral_count = sum(1 for t in self.territories if t.owner is None)
        
        stats = self.font.render(
            f"Alleati: {allies_count} | Axis: {axis_count} | Neutrali: {neutral_count}",
            True, (255, 255, 255)
        )
        self.screen.blit(stats, (20, 45))
        
        # Istruzioni
        if self.selected:
            info = self.font_small.render(
                f"Selezionato: {self.selected.name} | C=Conquista | +/-=Unità",
                True, (255, 255, 100)
            )
            self.screen.blit(info, (600, 25))

if __name__ == "__main__":
    game = Game()
    game.run()

