"""
Axis & Allies 1942 - Sistema Armamenti Avanzato
Con Carri Armati, Aerei, Fanteria e sistema durabilità
"""

import pygame
import sys
import json
import os
import random

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

# 5 SQUADRE
FACTIONS = {
    "rossi": {"name": "ROSSI", "color": (220, 50, 50), "money": 5000},
    "blu": {"name": "BLU", "color": (50, 100, 255), "money": 5000},
    "verdi": {"name": "VERDI", "color": (50, 200, 50), "money": 5000},
    "gialli": {"name": "GIALLI", "color": (255, 220, 50), "money": 5000},
    "viola": {"name": "VIOLA", "color": (180, 50, 200), "money": 5000}
}

COLOR_SELECTED = (255, 215, 0)

# TIPI UNITÀ
class UnitType:
    FANTERIA = "fanteria"
    CARRO = "carro"
    AEREO = "aereo"

# STATISTICHE UNITÀ
UNIT_STATS = {
    "fanteria": {
        "name": "Fanteria",
        "cost": 50,
        "repair_cost": 20,
        "attack": 2,
        "defense": 2,
        "hp": 10,
        "durability": 10,  # turni prima di rompersi
        "icon": "F"
    },
    "carro": {
        "name": "Carro Armato",
        "cost": 500,
        "repair_cost": 200,
        "attack": 8,
        "defense": 6,
        "hp": 50,
        "durability": 8,
        "icon": "C"
    },
    "aereo": {
        "name": "Aereo",
        "cost": 1500,
        "repair_cost": 600,
        "attack": 15,
        "defense": 5,
        "hp": 30,
        "durability": 6,
        "icon": "A"
    }
}

class Unit:
    """Singola unità militare"""
    def __init__(self, unit_type, turn_created):
        self.type = unit_type
        stats = UNIT_STATS[unit_type]
        self.name = stats["name"]
        self.attack = stats["attack"]
        self.defense = stats["defense"]
        self.hp = stats["hp"]
        self.max_hp = stats["hp"]
        self.durability = stats["durability"]
        self.age = 0  # turni di vita
        self.turn_created = turn_created
        self.needs_repair = False
    
    def age_unit(self):
        """Invecchia l'unità di 1 turno"""
        self.age += 1
        if self.age >= self.durability:
            self.needs_repair = True
    
    def repair(self):
        """Ripara l'unità"""
        self.hp = self.max_hp
        self.age = 0
        self.needs_repair = False
    
    def take_damage(self, damage):
        """Riceve danno"""
        self.hp -= damage
        if self.hp <= 0:
            return True  # Distrutto
        return False

class Territory:
    """Territorio con unità dettagliate"""
    def __init__(self, data):
        self.id = data['id']
        self.name = data.get('name', f"Stato_{self.id}")
        self.x = data['x']
        self.y = data['y']
        self.original_color = tuple(data.get('color', [150, 150, 150]))
        
        # Proprietà
        self.owner = None
        self.units = []  # Lista di Unit
        self.selected = False
        self.radius = 4
        self.income = random.randint(100, 500)  # Reddito più alto
    
    def add_unit(self, unit_type, turn):
        """Aggiungi unità"""
        self.units.append(Unit(unit_type, turn))
    
    def get_color(self):
        """Colore squadra"""
        if self.owner and self.owner in FACTIONS:
            return FACTIONS[self.owner]["color"]
        return (150, 150, 150)
    
    def contains_point(self, px, py):
        """Check click"""
        dist_sq = (px - self.x)**2 + (py - self.y)**2
        return dist_sq <= 100
    
    def get_total_attack(self):
        """Potenza attacco totale"""
        return sum(u.attack for u in self.units if not u.needs_repair)
    
    def get_total_defense(self):
        """Potenza difesa totale"""
        return sum(u.defense for u in self.units if not u.needs_repair)
    
    def count_units_by_type(self):
        """Conta unità per tipo"""
        counts = {"fanteria": 0, "carro": 0, "aereo": 0}
        for u in self.units:
            counts[u.type] += 1
        return counts
    
    def age_all_units(self):
        """Invecchia tutte le unità"""
        for u in self.units:
            u.age_unit()
    
    def draw(self, surface, font_small):
        """Disegna territorio"""
        color = self.get_color()
        
        if self.selected:
            pygame.draw.circle(surface, COLOR_SELECTED, (self.x, self.y), 16, 3)
        
        pygame.draw.circle(surface, color, (self.x, self.y), self.radius)
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.radius, 1)
        
        # Numero totale unità
        total = len(self.units)
        if total > 0:
            text = font_small.render(str(total), True, (255, 255, 255))
            rect = text.get_rect(center=(self.x + 12, self.y))
            bg = pygame.Surface((rect.width + 6, rect.height + 4))
            bg.set_alpha(200)
            bg.fill((0, 0, 0))
            surface.blit(bg, (rect.x - 3, rect.y - 2))
            surface.blit(text, rect)

class BuyMenu:
    """Menu acquisto unità"""
    def __init__(self, territory, faction, turn):
        self.territory = territory
        self.faction = faction
        self.turn = turn
        self.active = True
        self.selected_item = None
        
        # Posizione menu - OCEANO ATLANTICO (sinistra)
        self.x = 20  # Molto a sinistra
        self.y = 120  # Sotto il pannello info
        self.width = 350  # Un po' più stretto
        self.height = 480
    
    def draw(self, surface, font, font_small):
        """Disegna menu"""
        # Sfondo
        bg = pygame.Surface((self.width, self.height))
        bg.set_alpha(240)
        bg.fill((30, 30, 50))
        surface.blit(bg, (self.x, self.y))
        
        # Bordo
        pygame.draw.rect(surface, (255, 215, 0), (self.x, self.y, self.width, self.height), 3)
        
        # Titolo
        title = font.render(f"ARMERIA - {self.territory.name}", True, (255, 255, 100))
        surface.blit(title, (self.x + 20, self.y + 15))
        
        # Soldi disponibili
        money = FACTIONS[self.faction]["money"]
        money_text = font_small.render(f"Soldi: ${money}", True, (100, 255, 100))
        surface.blit(money_text, (self.x + 20, self.y + 50))
        
        # Lista unità
        y_offset = 90
        for unit_type in ["fanteria", "carro", "aereo"]:
            stats = UNIT_STATS[unit_type]
            self.draw_unit_card(surface, font, font_small, unit_type, stats, 
                              self.x + 20, self.y + y_offset)
            y_offset += 110
        
        # Istruzioni
        inst1 = font_small.render("1=Fanteria | 2=Carro", True, (200, 200, 200))
        inst2 = font_small.render("3=Aereo | R=Ripara", True, (200, 200, 200))
        inst3 = font_small.render("ESC=Chiudi", True, (255, 255, 100))
        surface.blit(inst1, (self.x + 10, self.y + self.height - 50))
        surface.blit(inst2, (self.x + 10, self.y + self.height - 35))
        surface.blit(inst3, (self.x + 10, self.y + self.height - 18))
    
    def draw_unit_card(self, surface, font, font_small, unit_type, stats, x, y):
        """Disegna carta unità"""
        # Box unità
        pygame.draw.rect(surface, (50, 50, 80), (x, y, 360, 100))
        pygame.draw.rect(surface, (100, 100, 150), (x, y, 360, 100), 2)
        
        # Nome e icona
        name_text = font.render(f"{stats['icon']} {stats['name']}", True, (255, 255, 255))
        surface.blit(name_text, (x + 10, y + 10))
        
        # Costo
        cost_text = font_small.render(f"Costo: ${stats['cost']}", True, (255, 255, 100))
        surface.blit(cost_text, (x + 10, y + 35))
        
        # Statistiche
        attack_text = font_small.render(f"Attacco: {stats['attack']}", True, (255, 100, 100))
        surface.blit(attack_text, (x + 10, y + 55))
        
        defense_text = font_small.render(f"Difesa: {stats['defense']}", True, (100, 100, 255))
        surface.blit(defense_text, (x + 140, y + 55))
        
        hp_text = font_small.render(f"HP: {stats['hp']}", True, (100, 255, 100))
        surface.blit(hp_text, (x + 250, y + 55))
        
        # Durabilità
        dur_text = font_small.render(f"Durabilita: {stats['durability']} turni", True, (200, 200, 200))
        surface.blit(dur_text, (x + 10, y + 75))
    
    def handle_key(self, key):
        """Gestisce input"""
        if key == pygame.K_1:
            return self.buy_unit("fanteria")
        elif key == pygame.K_2:
            return self.buy_unit("carro")
        elif key == pygame.K_3:
            return self.buy_unit("aereo")
        elif key == pygame.K_r:
            return self.repair_units()
        elif key == pygame.K_ESCAPE:
            self.active = False
        return None
    
    def buy_unit(self, unit_type):
        """Compra unità"""
        cost = UNIT_STATS[unit_type]["cost"]
        if FACTIONS[self.faction]["money"] >= cost:
            FACTIONS[self.faction]["money"] -= cost
            self.territory.add_unit(unit_type, self.turn)
            return f"Comprato: {UNIT_STATS[unit_type]['name']}"
        return "Soldi insufficienti!"
    
    def repair_units(self):
        """Ripara unità danneggiate"""
        repaired = 0
        total_cost = 0
        for unit in self.territory.units:
            if unit.needs_repair:
                cost = UNIT_STATS[unit.type]["repair_cost"]
                if FACTIONS[self.faction]["money"] >= cost:
                    FACTIONS[self.faction]["money"] -= cost
                    unit.repair()
                    repaired += 1
                    total_cost += cost
        
        if repaired > 0:
            return f"Riparate {repaired} unita (${total_cost})"
        return "Nessuna unita da riparare"

class Game:
    """Gioco completo"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Axis & Allies 1942 - Sistema Armamenti Avanzato")
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 16)
        self.font_large = pygame.font.Font(None, 32)
        
        self.background = self.load_background()
        self.territories = self.load_territories()
        
        self.faction_order = ["rossi", "blu", "verdi", "gialli", "viola"]
        self.current_faction_idx = 0
        self.current_faction = self.faction_order[0]
        self.turn = 1
        
        self.assign_territories()
        
        self.selected = None
        self.mode = "select"
        self.buy_menu = None
        self.message = ""
        self.message_timer = 0
        
        print("="*70)
        print("AXIS & ALLIES 1942 - SISTEMA ARMAMENTI AVANZATO")
        print("="*70)
        print("Armamenti: Fanteria ($50), Carro ($500), Aereo ($1500)")
        print("Controlli:")
        print("  Click = Seleziona")
        print("  INVIO = Apri Armeria")
        print("  A = Attacco")
        print("  I = Info territorio")
        print("  SPAZIO = Fine turno")
        print("="*70)
    
    def load_background(self):
        if os.path.exists("mappa_bn.jpg"):
            return pygame.image.load("mappa_bn.jpg")
        return None
    
    def load_territories(self):
        with open("centri.json", "r") as f:
            data = json.load(f)
        return [Territory(item) for item in data]
    
    def assign_territories(self):
        """Assegna territori con unità iniziali"""
        shuffled = list(range(len(self.territories)))
        random.shuffle(shuffled)
        per_faction = len(self.territories) // 5
        
        for i, faction in enumerate(self.faction_order):
            start = i * per_faction
            end = start + per_faction if i < 4 else len(self.territories)
            
            for idx in shuffled[start:end]:
                self.territories[idx].owner = faction
                # Unità iniziali casuali
                for _ in range(random.randint(2, 4)):
                    self.territories[idx].add_unit("fanteria", 0)
                for _ in range(random.randint(0, 2)):
                    self.territories[idx].add_unit("carro", 0)
    
    def next_turn(self):
        """Prossimo turno"""
        # Raccogli reddito
        income = sum(t.income for t in self.territories if t.owner == self.current_faction)
        FACTIONS[self.current_faction]["money"] += income
        
        # Invecchia unità
        for t in self.territories:
            if t.owner == self.current_faction:
                t.age_all_units()
        
        self.show_message(f"Raccolto: ${income}")
        
        # Prossima fazione
        self.current_faction_idx = (self.current_faction_idx + 1) % len(self.faction_order)
        self.current_faction = self.faction_order[self.current_faction_idx]
        
        if self.current_faction_idx == 0:
            self.turn += 1
        
        self.mode = "select"
        if self.selected:
            self.selected.selected = False
        self.selected = None
    
    def show_message(self, msg):
        """Mostra messaggio temporaneo"""
        self.message = msg
        self.message_timer = 180
        print(f"[INFO] {msg}")
    
    def show_territory_info(self):
        """Mostra info territorio"""
        if not self.selected:
            return
        
        t = self.selected
        counts = t.count_units_by_type()
        att = t.get_total_attack()
        deff = t.get_total_defense()
        
        msg = f"{t.name}: F:{counts['fanteria']} C:{counts['carro']} A:{counts['aereo']} | ATT:{att} DEF:{deff}"
        self.show_message(msg)
    
    def attack(self, attacker, defender):
        """Sistema combattimento avanzato"""
        if attacker.owner != self.current_faction:
            self.show_message("Non e' il tuo territorio")
            return
        
        if defender.owner == self.current_faction:
            self.show_message("Non puoi attaccare te stesso")
            return
        
        if len(attacker.units) == 0:
            self.show_message("Nessuna unita per attaccare")
            return
        
        # Combattimento
        att_power = attacker.get_total_attack()
        def_power = defender.get_total_defense()
        
        print(f"\n[BATTAGLIA] {attacker.name} vs {defender.name}")
        print(f"  Attacco: {att_power} | Difesa: {def_power}")
        
        # Perdite basate su potenza
        att_losses = max(0, def_power // 5)
        def_losses = max(0, att_power // 5)
        
        # Rimuovi unità casuali
        for _ in range(att_losses):
            if attacker.units:
                attacker.units.pop(random.randint(0, len(attacker.units) - 1))
        
        for _ in range(def_losses):
            if defender.units:
                defender.units.pop(random.randint(0, len(defender.units) - 1))
        
        # Conquista?
        if len(defender.units) == 0:
            defender.owner = attacker.owner
            # Sposta metà unità
            half = len(attacker.units) // 2
            for _ in range(half):
                if attacker.units:
                    defender.units.append(attacker.units.pop())
            
            self.show_message(f"CONQUISTATO {defender.name}!")
        else:
            self.show_message(f"Att:-{att_losses} Def:-{def_losses}")
    
    def run(self):
        """Game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if self.buy_menu:
                        msg = self.buy_menu.handle_key(event.key)
                        if msg:
                            self.show_message(msg)
                        if not self.buy_menu.active:
                            self.buy_menu = None
                    else:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                        elif event.key == pygame.K_SPACE:
                            self.next_turn()
                        elif event.key == pygame.K_RETURN:
                            if self.selected and self.selected.owner == self.current_faction:
                                self.buy_menu = BuyMenu(self.selected, self.current_faction, self.turn)
                        elif event.key == pygame.K_a:
                            self.mode = "attack"
                            self.show_message("Seleziona territorio da attaccare")
                        elif event.key == pygame.K_i:
                            self.show_territory_info()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not self.buy_menu:
                        self.handle_click(event.pos)
            
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()
    
    def handle_click(self, pos):
        """Click handler"""
        clicked = None
        for t in self.territories:
            if t.contains_point(pos[0], pos[1]):
                clicked = t
                break
        
        if not clicked:
            return
        
        if self.mode == "select":
            if self.selected:
                self.selected.selected = False
            self.selected = clicked
            clicked.selected = True
            self.show_territory_info()
        
        elif self.mode == "attack":
            if self.selected:
                self.attack(self.selected, clicked)
            self.mode = "select"
    
    def draw(self):
        """Disegna tutto"""
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill((40, 70, 100))
        
        # Territori
        for t in self.territories:
            t.draw(self.screen, self.font_small)
        
        # UI
        self.draw_ui()
        
        # Menu acquisto
        if self.buy_menu:
            self.buy_menu.draw(self.screen, self.font, self.font_small)
        
        # Messaggio
        if self.message_timer > 0:
            msg = self.font.render(self.message, True, (255, 255, 100))
            rect = msg.get_rect(center=(SCREEN_WIDTH // 2, 120))
            bg = pygame.Surface((rect.width + 20, rect.height + 10))
            bg.set_alpha(220)
            bg.fill((0, 0, 0))
            self.screen.blit(bg, (rect.x - 10, rect.y - 5))
            self.screen.blit(msg, rect)
            self.message_timer -= 1
    
    def draw_ui(self):
        """UI"""
        panel = pygame.Surface((SCREEN_WIDTH, 100))
        panel.set_alpha(230)
        panel.fill((20, 20, 40))
        self.screen.blit(panel, (0, 0))
        
        # Turno
        faction_name = FACTIONS[self.current_faction]["name"]
        faction_color = FACTIONS[self.current_faction]["color"]
        turn_text = self.font_large.render(f"TURNO {self.turn}: {faction_name}", True, faction_color)
        self.screen.blit(turn_text, (20, 15))
        
        # Soldi
        money = FACTIONS[self.current_faction]["money"]
        money_text = self.font.render(f"Soldi: ${money}", True, (100, 255, 100))
        self.screen.blit(money_text, (20, 55))
        
        # Territori
        x_offset = 400
        for faction in self.faction_order:
            count = sum(1 for t in self.territories if t.owner == faction)
            color = FACTIONS[faction]["color"]
            text = self.font_small.render(f"{FACTIONS[faction]['name'][:3]}: {count}", True, color)
            self.screen.blit(text, (x_offset, 25))
            x_offset += 80
        
        # Istruzioni
        inst = self.font_small.render("INVIO=Armeria | A=Attacco | I=Info | SPAZIO=Fine", 
                                     True, (200, 200, 200))
        self.screen.blit(inst, (400, 60))

if __name__ == "__main__":
    game = Game()
    game.run()

