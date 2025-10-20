"""
Axis & Allies 1942 - Versione SEMPLICE
Mappa come sfondo + Territori come cerchi + Unità come icone
"""

import pygame
import sys
import os

# Configurazione
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

# Colori
COLOR_ALLIES = (50, 100, 255)
COLOR_AXIS = (255, 50, 50)
COLOR_NEUTRAL = (150, 150, 150)
COLOR_SELECTED = (255, 215, 0)

class Territory:
    """Territorio = un CERCHIO sulla mappa"""
    def __init__(self, name, x, y, territory_id):
        self.id = territory_id
        self.name = name
        self.x = x
        self.y = y
        self.owner = None  # None, "allies", "axis"
        self.units = 0  # Numero unità (carri armati)
        self.neighbors = []
        self.selected = False
        self.radius = 25  # Raggio cerchio
    
    def contains_point(self, px, py):
        """Check se un punto è dentro il cerchio"""
        dist_sq = (px - self.x)**2 + (py - self.y)**2
        return dist_sq <= self.radius**2
    
    def draw(self, surface, font, font_small):
        """Disegna territorio"""
        # Colore
        if self.owner == "allies":
            color = COLOR_ALLIES
        elif self.owner == "axis":
            color = COLOR_AXIS
        else:
            color = COLOR_NEUTRAL
        
        # Bordo oro se selezionato
        if self.selected:
            pygame.draw.circle(surface, COLOR_SELECTED, (self.x, self.y), self.radius + 3, 3)
        
        # Cerchio principale
        pygame.draw.circle(surface, color, (self.x, self.y), self.radius)
        pygame.draw.circle(surface, (0, 0, 0), (self.x, self.y), self.radius, 2)
        
        # Nome (piccolo, sopra)
        name_text = font_small.render(self.name, True, (255, 255, 255))
        name_rect = name_text.get_rect(center=(self.x, self.y - self.radius - 10))
        # Sfondo nero
        bg = pygame.Surface((name_rect.width + 6, name_rect.height + 4))
        bg.set_alpha(180)
        bg.fill((0, 0, 0))
        surface.blit(bg, (name_rect.x - 3, name_rect.y - 2))
        surface.blit(name_text, name_rect)
        
        # Unità (numero grande al centro)
        if self.units > 0:
            unit_text = font.render(str(self.units), True, (255, 255, 255))
            unit_rect = unit_text.get_rect(center=(self.x, self.y))
            surface.blit(unit_text, unit_rect)

class Game:
    """Gioco principale"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Axis & Allies 1942")
        self.clock = pygame.time.Clock()
        
        # Font
        self.font = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 16)
        self.font_large = pygame.font.Font(None, 36)
        
        # Carica mappa di sfondo
        self.background = self.load_background()
        
        # Crea territori (POSIZIONI MANUALI sui paesi nella mappa)
        self.territories = self.create_territories()
        
        # Giocatori
        self.players = [
            {"name": "Alleati", "faction": "allies", "color": COLOR_ALLIES, "money": 100},
            {"name": "Axis", "faction": "axis", "color": COLOR_AXIS, "money": 100}
        ]
        self.current_player = 0
        
        # Stato
        self.selected_territory = None
        self.turn = 1
        
        # Setup iniziale
        self.setup_initial()
        
        print("="*70)
        print("AXIS & ALLIES 1942 - Gioco Avviato")
        print("="*70)
        print("Approccio: Mappa sfondo + Cerchi territori + Icone unità")
        print("="*70)
    
    def load_background(self):
        """Carica mappa di sfondo"""
        maps = ["mappa_hd.jpg", "mappa_semplice.jpg", "mappa_axis_allies.png"]
        
        for filename in maps:
            if os.path.exists(filename):
                try:
                    bg = pygame.image.load(filename)
                    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    print(f"[OK] Mappa caricata: {filename}")
                    return bg
                except:
                    pass
        
        print("[INFO] Nessuna mappa, uso sfondo blu")
        return None
    
    def create_territories(self):
        """Crea territori posizionati sulla mappa"""
        # Posizioni approssimate dei centri degli stati sulla mappa 1400x800
        territories_data = [
            # Europa
            (0, "UK", 280, 550),
            (1, "Francia", 360, 480),
            (2, "Spagna", 300, 420),
            (3, "Germania", 450, 520),
            (4, "Italia", 480, 450),
            (5, "Polonia", 540, 530),
            (6, "Russia", 750, 550),
            (7, "Scandinavia", 480, 620),
            (8, "Balcani", 560, 460),
            (9, "Turchia", 660, 430),
            
            # Africa
            (10, "Nord Africa", 380, 360),
            (11, "Egitto", 620, 350),
            (12, "Africa Est", 650, 250),
            
            # Asia
            (13, "Medio Oriente", 780, 400),
            (14, "India", 900, 380),
            (15, "Cina", 1050, 450),
            (16, "Giappone", 1250, 470),
        ]
        
        territories = []
        for tid, name, x, y in territories_data:
            territories.append(Territory(name, x, y, tid))
        
        # Connessioni base
        connections = [
            (0, 1), (1, 2), (1, 3), (1, 4), (3, 5), (5, 6),
            (3, 7), (4, 8), (8, 9), (2, 10), (10, 11), (11, 12),
            (9, 13), (13, 14), (14, 15), (15, 16)
        ]
        
        for t1, t2 in connections:
            territories[t1].neighbors.append(t2)
            territories[t2].neighbors.append(t1)
        
        return territories
    
    def setup_initial(self):
        """Setup iniziale"""
        # Alleati
        for tid in [0, 1, 6, 7, 11, 14, 15]:
            self.territories[tid].owner = "allies"
            self.territories[tid].units = 3
        
        # Axis
        for tid in [3, 4, 5, 10, 16]:
            self.territories[tid].owner = "axis"
            self.territories[tid].units = 3
        
        # Neutrali
        for tid in [2, 8, 9, 12, 13]:
            self.territories[tid].owner = None
            self.territories[tid].units = 2
    
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
                        self.end_turn()
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
                if self.selected_territory:
                    self.selected_territory.selected = False
                self.selected_territory = terr
                terr.selected = True
                print(f"Selezionato: {terr.name} ({terr.owner}) - {terr.units} unità")
                break
    
    def end_turn(self):
        """Fine turno"""
        self.current_player = 1 - self.current_player
        self.turn += 1
        print(f"\nTurno {self.turn} - {self.players[self.current_player]['name']}")
    
    def draw(self):
        """Disegna tutto"""
        # Sfondo (mappa politica)
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((40, 60, 90))
        
        # Territori (cerchi sopra la mappa)
        for terr in self.territories:
            terr.draw(self.screen, self.font, self.font_small)
        
        # UI
        self.draw_ui()
    
    def draw_ui(self):
        """Disegna interfaccia"""
        # Pannello superiore
        panel = pygame.Surface((SCREEN_WIDTH, 70))
        panel.set_alpha(220)
        panel.fill((30, 30, 60))
        self.screen.blit(panel, (0, 0))
        
        # Info giocatore
        player = self.players[self.current_player]
        text = self.font_large.render(f"{player['name']}", True, player['color'])
        self.screen.blit(text, (20, 15))
        
        money_text = self.font.render(f"Soldi: ${player['money']}", True, (100, 255, 100))
        self.screen.blit(money_text, (20, 50))
        
        turn_text = self.font.render(f"Turno: {self.turn}", True, (255, 255, 255))
        self.screen.blit(turn_text, (600, 25))

if __name__ == "__main__":
    game = Game()
    game.run()

