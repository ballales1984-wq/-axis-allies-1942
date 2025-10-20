"""
Editor Centri - Posiziona i centri/capitali per ogni stato
Click sulla mappa per aggiungere un centro
"""

import pygame
import sys
import json
import os

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

class CentroEditor:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Editor Centri Stati - Click per aggiungere")
        self.clock = pygame.time.Clock()
        
        # Font
        self.font = pygame.font.Font(None, 20)
        self.font_large = pygame.font.Font(None, 24)
        
        # Carica mappa
        self.background = self.load_map()
        
        # Lista centri
        self.centri = []  # Lista di {id, name, x, y}
        self.carica_centri()
        
        # Editing
        self.counter = len(self.centri)
        
        print("="*70)
        print("EDITOR CENTRI STATI")
        print("="*70)
        print("Controlli:")
        print("  Click SINISTRO = Aggiungi centro")
        print("  Click DESTRO = Rimuovi centro")
        print("  S = Salva centri")
        print("  ESC = Esci")
        print("="*70)
    
    def load_map(self):
        """Carica la mappa di sfondo"""
        maps = ["mappa_hd.jpg", "sfondo_classico.png", "sfondo_gioco.png", 
                "mappa_semplice.jpg", "mappa.png"]
        
        for filename in maps:
            if os.path.exists(filename):
                try:
                    bg = pygame.image.load(filename)
                    bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    print(f"[OK] Mappa caricata: {filename}")
                    return bg
                except:
                    pass
        
        # Crea sfondo semplice se nessuna mappa
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg.fill((40, 70, 100))
        return bg
    
    def carica_centri(self):
        """Carica centri salvati se esistono"""
        if os.path.exists("centri.json"):
            with open("centri.json", "r") as f:
                self.centri = json.load(f)
            print(f"[OK] Caricati {len(self.centri)} centri esistenti")
    
    def salva_centri(self):
        """Salva i centri in file JSON"""
        with open("centri.json", "w") as f:
            json.dump(self.centri, f, indent=2)
        print(f"[OK] Salvati {len(self.centri)} centri in centri.json")
    
    def aggiungi_centro(self, x, y):
        """Aggiungi un nuovo centro"""
        centro = {
            "id": self.counter,
            "name": f"Stato_{self.counter}",
            "x": x,
            "y": y
        }
        self.centri.append(centro)
        self.counter += 1
        print(f"[+] Centro aggiunto: {centro['name']} a ({x}, {y})")
    
    def rimuovi_centro(self, x, y):
        """Rimuovi il centro più vicino"""
        if not self.centri:
            return
        
        # Trova il più vicino
        min_dist = float('inf')
        closest = None
        
        for centro in self.centri:
            dist = (centro['x'] - x)**2 + (centro['y'] - y)**2
            if dist < min_dist:
                min_dist = dist
                closest = centro
        
        # Rimuovi se abbastanza vicino (< 30 pixel)
        if closest and min_dist < 900:
            self.centri.remove(closest)
            print(f"[-] Centro rimosso: {closest['name']}")
    
    def run(self):
        """Loop principale"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_s:
                        self.salva_centri()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if event.button == 1:  # Sinistro = aggiungi
                        self.aggiungi_centro(x, y)
                    elif event.button == 3:  # Destro = rimuovi
                        self.rimuovi_centro(x, y)
            
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        
        # Salva prima di uscire
        self.salva_centri()
        pygame.quit()
        sys.exit()
    
    def draw(self):
        """Disegna tutto"""
        # Sfondo (mappa)
        self.screen.blit(self.background, (0, 0))
        
        # Disegna tutti i centri
        for centro in self.centri:
            x, y = centro['x'], centro['y']
            
            # Cerchio grande semi-trasparente
            s = pygame.Surface((60, 60), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 255, 100, 100), (30, 30), 28)
            self.screen.blit(s, (x - 30, y - 30))
            
            # Punto rosso al centro
            pygame.draw.circle(self.screen, (255, 0, 0), (x, y), 5)
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 5, 1)
            
            # ID
            id_text = self.font.render(str(centro['id']), True, (255, 255, 255))
            id_rect = id_text.get_rect(center=(x, y - 20))
            bg = pygame.Surface((id_rect.width + 4, id_rect.height + 2))
            bg.set_alpha(200)
            bg.fill((0, 0, 0))
            self.screen.blit(bg, (id_rect.x - 2, id_rect.y - 1))
            self.screen.blit(id_text, id_rect)
        
        # UI Info
        self.draw_ui()
    
    def draw_ui(self):
        """Disegna UI"""
        # Pannello superiore
        panel = pygame.Surface((SCREEN_WIDTH, 60))
        panel.set_alpha(220)
        panel.fill((30, 30, 60))
        self.screen.blit(panel, (0, 0))
        
        # Testo
        info = self.font_large.render(f"Centri: {len(self.centri)} | Click=Aggiungi | Destro=Rimuovi | S=Salva | ESC=Esci", 
                                      True, (255, 255, 100))
        self.screen.blit(info, (20, 18))

if __name__ == "__main__":
    editor = CentroEditor()
    editor.run()

