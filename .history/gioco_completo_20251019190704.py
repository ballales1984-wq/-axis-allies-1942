"""
Axis & Allies 1942 - Gioco Completo a 5 Squadre
"""

import pygame
import sys
import json
import os
import random

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

# 5 SQUADRE CON COLORI
FACTIONS = {
    "rossi": {"name": "ROSSI", "color": (220, 50, 50), "money": 50},
    "blu": {"name": "BLU", "color": (50, 100, 255), "money": 50},
    "verdi": {"name": "VERDI", "color": (50, 200, 50), "money": 50},
    "gialli": {"name": "GIALLI", "color": (255, 220, 50), "money": 50},
    "viola": {"name": "VIOLA", "color": (180, 50, 200), "money": 50}
}

COLOR_SELECTED = (255, 215, 0)  # Oro

class Territory:
    """Territorio = stato con puntino colorabile"""
    def __init__(self, data):
        self.id = data['id']
        self.name = data.get('name', f"Stato_{self.id}")
        self.x = data['x']
        self.y = data['y']
        self.original_color = tuple(data.get('color', [150, 150, 150]))
        
        # Proprietà di gioco
        self.owner = None  # rossi, blu, verdi, gialli, viola
        self.units = 0
        self.selected = False
        self.radius = 4
        self.income = random.randint(2, 8)  # Reddito
    
    def get_color(self):
        """Colore basato sulla squadra proprietaria"""
        if self.owner and self.owner in FACTIONS:
            return FACTIONS[self.owner]["color"]
        else:
            return (150, 150, 150)  # Grigio neutrale
    
    def contains_point(self, px, py):
        """Check se punto è dentro"""
        dist_sq = (px - self.x)**2 + (py - self.y)**2
        return dist_sq <= 100
    
    def draw(self, surface, font_small):
        """Disegna territorio"""
        color = self.get_color()
        
        # Bordo oro se selezionato
        if self.selected:
            pygame.draw.circle(surface, COLOR_SELECTED, (self.x, self.y), 16, 3)
        
        # PUNTINO colorato
        pygame.draw.circle(surface, color, (self.x, self.y), self.radius)
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.radius, 1)
        
        # Nome SOLO se selezionato
        if self.selected:
            name_text = font_small.render(self.name, True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(self.x, self.y - 25))
            bg = pygame.Surface((name_rect.width + 8, name_rect.height + 4))
            bg.set_alpha(220)
            bg.fill((0, 0, 0))
            surface.blit(bg, (name_rect.x - 4, name_rect.y - 2))
            surface.blit(name_text, name_rect)
        
        # Unità
        if self.units > 0:
            unit_text = font_small.render(str(self.units), True, (255, 255, 255))
            unit_rect = unit_text.get_rect(center=(self.x + 12, self.y))
            bg = pygame.Surface((unit_rect.width + 6, unit_rect.height + 4))
            bg.set_alpha(200)
            bg.fill((0, 0, 0))
            surface.blit(bg, (unit_rect.x - 3, unit_rect.y - 2))
            surface.blit(unit_text, unit_rect)

class Game:
    """Gioco completo"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Axis & Allies 1942 - 5 Squadre")
        self.clock = pygame.time.Clock()
        
        # Font
        self.font = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 16)
        self.font_large = pygame.font.Font(None, 36)
        
        # Mappa
        self.background = self.load_background()
        
        # Territori
        self.territories = self.load_territories()
        
        # Gioco
        self.faction_order = ["rossi", "blu", "verdi", "gialli", "viola"]
        self.current_faction_idx = 0
        self.current_faction = self.faction_order[0]
        self.turn = 1
        
        # Assegna stati alle squadre
        self.assign_territories()
        
        # Selezione
        self.selected = None
        self.selected_for_attack = None
        
        # Modalità
        self.mode = "select"  # select, attack, move
        
        print("="*70)
        print("AXIS & ALLIES 1942 - GIOCO COMPLETO A 5 SQUADRE")
        print("="*70)
        print(f"Territori: {len(self.territories)}")
        print(f"Squadre: {', '.join([FACTIONS[f]['name'] for f in self.faction_order])}")
        print()
        print("Controlli:")
        print("  Click = Seleziona territorio")
        print("  A = Modalita ATTACCO")
        print("  M = Modalita MOVIMENTO")
        print("  B = Compra unita (+1 unita, -5 soldi)")
        print("  SPAZIO = Fine turno")
        print("  ESC = Esci")
        print("="*70)
    
    def load_background(self):
        """Carica mappa B/N"""
        if os.path.exists("mappa_bn.jpg"):
            try:
                bg = pygame.image.load("mappa_bn.jpg")
                return bg
            except:
                pass
        return None
    
    def load_territories(self):
        """Carica territori"""
        with open("centri.json", "r") as f:
            data = json.load(f)
        return [Territory(item) for item in data]
    
    def assign_territories(self):
        """Assegna territori alle 5 squadre"""
        # Mescola territori
        shuffled = list(range(len(self.territories)))
        random.shuffle(shuffled)
        
        # Dividi tra le 5 squadre
        per_faction = len(self.territories) // 5
        
        for i, faction in enumerate(self.faction_order):
            start = i * per_faction
            end = start + per_faction if i < 4 else len(self.territories)
            
            count = 0
            for idx in shuffled[start:end]:
                self.territories[idx].owner = faction
                self.territories[idx].units = random.randint(2, 5)
                count += 1
            
            print(f"[OK] {FACTIONS[faction]['name']}: {count} territori")
    
    def next_turn(self):
        """Passa al prossimo turno"""
        # Raccogli reddito
        income = self.collect_income()
        FACTIONS[self.current_faction]["money"] += income
        
        print(f"\n[TURNO {self.turn}] {FACTIONS[self.current_faction]['name']} raccolto: {income} soldi")
        
        # Prossima fazione
        self.current_faction_idx = (self.current_faction_idx + 1) % len(self.faction_order)
        self.current_faction = self.faction_order[self.current_faction_idx]
        
        if self.current_faction_idx == 0:
            self.turn += 1
        
        self.mode = "select"
        if self.selected:
            self.selected.selected = False
        self.selected = None
        self.selected_for_attack = None
    
    def collect_income(self):
        """Raccogli reddito dai territori"""
        income = 0
        for terr in self.territories:
            if terr.owner == self.current_faction:
                income += terr.income
        return income
    
    def buy_unit(self):
        """Compra un'unità"""
        if not self.selected or self.selected.owner != self.current_faction:
            print("[!] Seleziona un tuo territorio")
            return
        
        if FACTIONS[self.current_faction]["money"] >= 5:
            FACTIONS[self.current_faction]["money"] -= 5
            self.selected.units += 1
            print(f"[+] Unita comprata in {self.selected.name}")
        else:
            print("[!] Soldi insufficienti (servono 5)")
    
    def attack(self, attacker, defender):
        """Attacco tra due territori"""
        if attacker.owner != self.current_faction:
            print("[!] Non e' il tuo territorio")
            return
        
        if defender.owner == self.current_faction:
            print("[!] Non puoi attaccare te stesso")
            return
        
        if attacker.units < 2:
            print("[!] Servono almeno 2 unita per attaccare")
            return
        
        # Combattimento semplice con dadi
        print(f"\n[BATTAGLIA] {attacker.name} ({attacker.units}) -> {defender.name} ({defender.units})")
        
        att_losses = 0
        def_losses = 0
        
        # Ogni unità ha 50% di colpire
        for _ in range(attacker.units - 1):  # -1 per lasciare difesa
            if random.random() < 0.5:
                def_losses += 1
        
        for _ in range(defender.units):
            if random.random() < 0.4:  # Difesa leggermente più debole
                att_losses += 1
        
        # Applica perdite
        attacker.units = max(1, attacker.units - att_losses)
        defender.units = max(0, defender.units - def_losses)
        
        print(f"  Attaccante perde: {att_losses}, Difensore perde: {def_losses}")
        
        # Se difensore a 0, conquistato!
        if defender.units == 0:
            defender.owner = attacker.owner
            defender.units = attacker.units - 1
            attacker.units = 1
            print(f"[CONQUISTATO] {defender.name} dai {FACTIONS[attacker.owner]['name']}!")
        else:
            print(f"[DIFESA] {defender.name} resiste!")
    
    def move_units(self, from_terr, to_terr, amount):
        """Muovi unità"""
        if from_terr.owner != self.current_faction:
            return
        if to_terr.owner != self.current_faction:
            return
        if from_terr.units <= amount:
            return
        
        from_terr.units -= amount
        to_terr.units += amount
        print(f"[MOVIMENTO] {amount} unita: {from_terr.name} -> {to_terr.name}")
    
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
                        self.next_turn()
                    
                    elif event.key == pygame.K_a:
                        self.mode = "attack"
                        print("[MODE] Attacco - seleziona territorio da attaccare")
                    
                    elif event.key == pygame.K_m:
                        self.mode = "move"
                        print("[MODE] Movimento")
                    
                    elif event.key == pygame.K_b:
                        self.buy_unit()
                
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
        clicked = None
        for terr in self.territories:
            if terr.contains_point(pos[0], pos[1]):
                clicked = terr
                break
        
        if not clicked:
            return
        
        if self.mode == "select":
            # Deseleziona precedente
            if self.selected:
                self.selected.selected = False
            
            # Seleziona nuovo
            self.selected = clicked
            clicked.selected = True
            
            owner_str = FACTIONS[clicked.owner]["name"] if clicked.owner else "Neutrale"
            print(f"Selezionato: {clicked.name} ({owner_str}) - {clicked.units} unita, +{clicked.income}/turno")
        
        elif self.mode == "attack":
            if not self.selected:
                print("[!] Seleziona prima un territorio attaccante")
                return
            
            # Attacca
            self.attack(self.selected, clicked)
            self.mode = "select"
        
        elif self.mode == "move":
            if not self.selected:
                self.selected = clicked
                clicked.selected = True
            else:
                # Muovi 1 unità
                self.move_units(self.selected, clicked, 1)
                self.selected.selected = False
                self.selected = None
                self.mode = "select"
    
    def draw(self):
        """Disegna tutto"""
        # Sfondo
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((40, 70, 100))
        
        # Territori
        for terr in self.territories:
            terr.draw(self.screen, self.font_small)
        
        # UI
        self.draw_ui()
    
    def draw_ui(self):
        """UI completa"""
        # Pannello superiore
        panel = pygame.Surface((SCREEN_WIDTH, 100))
        panel.set_alpha(230)
        panel.fill((20, 20, 40))
        self.screen.blit(panel, (0, 0))
        
        # Turno attuale
        faction_name = FACTIONS[self.current_faction]["name"]
        faction_color = FACTIONS[self.current_faction]["color"]
        
        turn_text = self.font_large.render(f"TURNO {self.turn}: {faction_name}", True, faction_color)
        self.screen.blit(turn_text, (20, 15))
        
        # Soldi
        money = FACTIONS[self.current_faction]["money"]
        money_text = self.font.render(f"Soldi: {money}", True, (255, 255, 100))
        self.screen.blit(money_text, (20, 55))
        
        # Conta territori per squadra
        x_offset = 400
        for faction in self.faction_order:
            count = sum(1 for t in self.territories if t.owner == faction)
            color = FACTIONS[faction]["color"]
            name = FACTIONS[faction]["name"][:3]
            
            text = self.font_small.render(f"{name}: {count}", True, color)
            self.screen.blit(text, (x_offset, 25))
            x_offset += 80
        
        # Modalità
        mode_text = f"Modo: {self.mode.upper()}"
        if self.selected:
            mode_text += f" | {self.selected.name}"
        
        mode_display = self.font_small.render(mode_text, True, (255, 255, 255))
        self.screen.blit(mode_display, (400, 60))
        
        # Istruzioni
        instructions = self.font_small.render(
            "A=Attacco | M=Movimento | B=Compra(5$) | SPAZIO=Fine turno",
            True, (200, 200, 200)
        )
        self.screen.blit(instructions, (20, 78))

if __name__ == "__main__":
    game = Game()
    game.run()

