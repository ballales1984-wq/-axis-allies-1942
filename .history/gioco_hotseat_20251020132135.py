"""
MODALITÀ HOT SEAT - Tutti i giocatori sullo stesso PC
Ogni giocatore fa il suo turno, poi passa il PC al prossimo
"""

import sys
import os

# Copia tutto da gioco_avanzato.py ma SENZA IA
# Ogni fazione è controllata da un giocatore reale

def resource_path(relative_path):
    """Ottieni path assoluto per risorse (compatibile con PyInstaller)"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

import pygame
import random
import json
import math

# ===== CONFIGURAZIONE =====
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

# Colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 50, 50)
BLUE = (50, 50, 255)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 50)
ORANGE = (255, 165, 0)

# Colori fazioni
FACTION_COLORS = {
    "usa": (0, 100, 200),      # Blu
    "europa": (200, 0, 0),      # Rosso
    "russia": (150, 0, 150),    # Viola
    "cina": (255, 200, 0),      # Giallo
    "africa": (0, 150, 0)       # Verde
}

# Statistiche unità
UNIT_STATS = {
    "fanteria": {"attack": 2, "defense": 2, "cost": 50, "range": 100},
    "carro": {"attack": 6, "defense": 4, "cost": 500, "range": 200},
    "aereo": {"attack": 12, "defense": 6, "cost": 1500, "range": 500}
}

# Livelli tecnologici
TECH_LEVELS = {
    0: {"name": "Antica", "attack_bonus": 0, "defense_bonus": 0, "threshold": 0},
    1: {"name": "Moderno", "attack_bonus": 5, "defense_bonus": 3, "threshold": 100},
    2: {"name": "Futuro", "attack_bonus": 10, "defense_bonus": 5, "threshold": 200}
}


class Unit:
    """Unità militare"""
    def __init__(self, unit_type, durability=100):
        self.type = unit_type
        self.durability = durability  # 0-100


class Territory:
    """Territorio sulla mappa"""
    def __init__(self, id, name, x, y, color):
        self.id = id
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.owner = None
        self.units = []
        
        # Risorse
        self.money = random.randint(100, 500)
        self.oil = random.randint(100, 300)
        self.tech_points = random.randint(10, 50)
        
        # Sviluppo territorio
        self.development_level = 0
        self.turns_held = 0
        
        # Difese strutturali
        self.bunkers = 0
        self.towers = 0
        self.fortress = 0
        
        self.radius = 8
    
    def get_total_attack(self, tech_level=0):
        """Calcola attacco totale"""
        bonus = TECH_LEVELS.get(tech_level, {}).get("attack_bonus", 0)
        total = bonus
        for unit in self.units:
            if unit.type in UNIT_STATS:
                base = UNIT_STATS[unit.type]["attack"]
                total += int(base * (unit.durability / 100.0))
        return total
    
    def get_total_defense(self, tech_level=0):
        """Calcola difesa totale"""
        bonus = TECH_LEVELS.get(tech_level, {}).get("defense_bonus", 0)
        structural_defense = (self.bunkers * 5) + (self.towers * 10) + (self.fortress * 30)
        total = bonus + structural_defense
        for unit in self.units:
            if unit.type in UNIT_STATS:
                base = UNIT_STATS[unit.type]["defense"]
                total += int(base * (unit.durability / 100.0))
        return total
    
    def get_visual_radius(self):
        """Raggio visivo (aumenta con sviluppo)"""
        return self.radius + (self.development_level * 10)
    
    def get_attack_range(self):
        """Raggio d'attacco (aumenta con sviluppo)"""
        return 50 + (self.development_level * 25)
    
    def draw(self, surface, font_small):
        """Disegna territorio"""
        # Cerchio base
        color = FACTION_COLORS.get(self.owner, GRAY) if self.owner else GRAY
        pygame.draw.circle(surface, color, (self.x, self.y), self.radius)
        
        # Bordo
        pygame.draw.circle(surface, WHITE, (self.x, self.y), self.radius, 2)
        
        # Cerchio di influenza (se sviluppato)
        if self.development_level > 0:
            influence_radius = self.get_visual_radius()
            pygame.draw.circle(surface, (*color, 50), (self.x, self.y), influence_radius, 1)
        
        # Conta unità per tipo
        unit_counts = {"fanteria": 0, "carro": 0, "aereo": 0}
        for unit in self.units:
            if unit.type in unit_counts:
                unit_counts[unit.type] += 1
        
        # Mostra unità come testo piccolo sopra
        y_offset = -15
        for unit_type, count in unit_counts.items():
            if count > 0:
                symbol = "F" if unit_type == "fanteria" else ("C" if unit_type == "carro" else "A")
                text = font_small.render(f"{symbol}:{count}", True, WHITE)
                surface.blit(text, (self.x - 15, self.y + y_offset))
                y_offset += 12


class Game:
    """Gioco HOT SEAT - Tutti giocatori umani"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Axis & Allies 1942 - HOT SEAT")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Font
        self.font = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 20)
        self.font_title = pygame.font.Font(None, 48)
        
        # Carica mappa e territori
        self.load_background()
        self.load_territories()
        
        # Setup fazioni (tutte controllate da giocatori)
        self.factions = ["usa", "europa", "russia", "cina", "africa"]
        self.faction_resources = {
            faction: {"money": 5000, "oil": 2000, "tech": 0, "tech_level": 0}
            for faction in self.factions
        }
        
        # Assegna territori casualmente
        self.assign_territories()
        
        # Turni
        self.current_faction_idx = 0
        self.current_turn = 1
        
        # Stato gioco
        self.selected_territory = None
        self.message = ""
        self.message_timer = 0
        
        # Menu acquisto
        self.buy_menu = None
    
    def load_background(self):
        """Carica immagine mappa"""
        try:
            self.background = pygame.image.load(resource_path("mappa_bn.jpg"))
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.background = None
    
    def load_territories(self):
        """Carica territori da JSON"""
        try:
            with open(resource_path("centri.json"), "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.territories = []
            for t in data:
                territory = Territory(
                    t["id"], t["name"], t["x"], t["y"],
                    tuple(t.get("color", [128, 128, 128]))
                )
                self.territories.append(territory)
            
            print(f"[OK] Caricati {len(self.territories)} territori")
        except Exception as e:
            print(f"[ERRORE] Caricamento territori: {e}")
            self.territories = []
    
    def assign_territories(self):
        """Assegna territori casualmente alle fazioni"""
        shuffled = list(self.territories)
        random.shuffle(shuffled)
        
        for i, territory in enumerate(shuffled):
            faction = self.factions[i % len(self.factions)]
            territory.owner = faction
            
            # Assegna unità iniziali
            for _ in range(random.randint(1, 3)):
                territory.units.append(Unit("fanteria"))
    
    def get_current_faction(self):
        """Ottieni fazione corrente"""
        return self.factions[self.current_faction_idx]
    
    def next_turn(self):
        """Passa al turno successivo"""
        # Produzione risorse per fazione corrente
        faction = self.get_current_faction()
        territories = [t for t in self.territories if t.owner == faction]
        
        # Sviluppo territori
        developed_count = 0
        for t in territories:
            t.turns_held += 1
            old_level = t.development_level
            t.development_level = min(10, t.turns_held // 3)
            if t.development_level > old_level:
                developed_count += 1
        
        # Produzione
        money_prod = sum(t.money * (1 + t.development_level * 0.1) for t in territories)
        oil_prod = sum(t.oil * (1 + t.development_level * 0.1) for t in territories)
        tech_prod = sum(t.tech_points * (1 + t.development_level * 0.1) for t in territories)
        
        self.faction_resources[faction]["money"] += int(money_prod)
        self.faction_resources[faction]["oil"] += int(oil_prod)
        self.faction_resources[faction]["tech"] += int(tech_prod)
        
        # Check upgrade tecnologico
        tech = self.faction_resources[faction]["tech"]
        old_level = self.faction_resources[faction]["tech_level"]
        for level, data in sorted(TECH_LEVELS.items(), reverse=True):
            if tech >= data["threshold"]:
                self.faction_resources[faction]["tech_level"] = level
                if level > old_level:
                    self.show_message(f"[TECH] {faction.upper()}: {data['name']}!")
                break
        
        # Passa alla prossima fazione
        self.current_faction_idx = (self.current_faction_idx + 1) % len(self.factions)
        if self.current_faction_idx == 0:
            self.current_turn += 1
        
        next_faction = self.get_current_faction()
        self.show_message(f"TURNO DI {next_faction.upper()}! Passa il PC al giocatore {next_faction.upper()}")
    
    def show_message(self, msg):
        """Mostra messaggio temporaneo"""
        self.message = msg
        self.message_timer = 180  # 3 secondi
        print(f"[INFO] {msg}")
    
    def handle_click(self, pos):
        """Gestisci click mouse - Trova territorio PIÙ VICINO"""
        # Check menu acquisto
        if self.buy_menu:
            if self.buy_menu.handle_click(pos):
                return
            # Chiudi menu se click fuori
            self.buy_menu = None
            return
        
        # Selezione territorio - Trova il più vicino se sovrapposti
        closest_territory = None
        min_distance = float('inf')
        
        for territory in self.territories:
            dist = math.hypot(pos[0] - territory.x, pos[1] - territory.y)
            if dist <= territory.radius:
                if dist < min_distance:
                    min_distance = dist
                    closest_territory = territory
        
        if closest_territory:
            # Click su territorio più vicino
            if closest_territory.owner == self.get_current_faction():
                # Territorio proprio - apri menu
                self.selected_territory = closest_territory
                from gioco_avanzato import BuyMenu
                self.buy_menu = BuyMenu(closest_territory, self.faction_resources[closest_territory.owner])
                self.show_message(f"Territorio: {closest_territory.name}")
            else:
                # Territorio nemico - attacca se possibile
                if self.selected_territory and self.selected_territory.owner == self.get_current_faction():
                    self.attack(self.selected_territory, closest_territory)
    
    def attack(self, attacker, defender):
        """Attacca territorio"""
        # Calcola distanza
        distance = math.hypot(attacker.x - defender.x, attacker.y - defender.y)
        
        # Filtra unità in portata
        units_in_range = []
        for unit in attacker.units:
            unit_range = UNIT_STATS.get(unit.type, {}).get("range", 100)
            if distance <= unit_range:
                units_in_range.append(unit)
        
        if not units_in_range:
            self.show_message("FUORI PORTATA!")
            return
        
        # Check petrolio
        oil_needed = len(units_in_range) * 20
        faction = attacker.owner
        if self.faction_resources[faction]["oil"] < oil_needed:
            units_in_range = units_in_range[:self.faction_resources[faction]["oil"] // 20]
            if not units_in_range:
                self.show_message("Petrolio insufficiente!")
                return
        
        # Consuma petrolio
        oil_used = len(units_in_range) * 20
        self.faction_resources[faction]["oil"] -= oil_used
        
        # Calcola potenze
        att_tech = self.faction_resources[faction]["tech_level"]
        def_tech = self.faction_resources.get(defender.owner, {}).get("tech_level", 0)
        
        att_power = sum(UNIT_STATS[u.type]["attack"] * (u.durability / 100) for u in units_in_range)
        att_power += TECH_LEVELS[att_tech]["attack_bonus"]
        
        def_power = defender.get_total_defense(def_tech)
        
        # Battaglia
        print(f"[BATTAGLIA] {attacker.name} vs {defender.name}")
        print(f"  Attacco: {int(att_power)} | Difesa: {int(def_power)}")
        
        if att_power > def_power:
            # CONQUISTA!
            # Trasferisci risorse
            self.faction_resources[faction]["money"] += defender.money
            self.faction_resources[faction]["oil"] += defender.oil
            self.faction_resources[faction]["tech"] += defender.tech_points
            
            # Cambia proprietario
            defender.owner = faction
            defender.turns_held = 0
            defender.development_level = 0
            
            # Muovi unità
            defender.units = units_in_range
            attacker.units = [u for u in attacker.units if u not in units_in_range]
            
            self.show_message(f"[CONQUISTA] {defender.name}! +{defender.money}$ +{defender.oil}P")
        else:
            # Difesa tiene - danneggia attaccanti
            for unit in units_in_range:
                unit.durability = max(0, unit.durability - random.randint(10, 30))
            
            # Rimuovi unità distrutte
            attacker.units = [u for u in attacker.units if u.durability > 0]
            
            self.show_message(f"Attacco fallito! -{oil_used}P")
    
    def draw(self):
        """Disegna tutto"""
        # Sfondo
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(BLACK)
        
        # Territori
        for territory in self.territories:
            territory.draw(self.screen, self.font_small)
        
        # HUD
        self.draw_hud()
        
        # Menu acquisto
        if self.buy_menu:
            self.buy_menu.draw(self.screen, self.font, self.font_small)
        
        # Messaggio
        if self.message_timer > 0:
            text = self.font.render(self.message, True, YELLOW)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50))
            self.message_timer -= 1
        
        pygame.display.flip()
    
    def draw_hud(self):
        """Disegna HUD"""
        faction = self.get_current_faction()
        resources = self.faction_resources[faction]
        
        # Pannello info
        y = 10
        color = FACTION_COLORS[faction]
        
        # Fazione e turno
        text = self.font.render(f"TURNO {self.current_turn} - {faction.upper()}", True, color)
        self.screen.blit(text, (10, y))
        y += 35
        
        # Risorse
        text = self.font_small.render(f"[$] {resources['money']:,} | [P] {resources['oil']:,} | [T] {resources['tech']}", True, WHITE)
        self.screen.blit(text, (10, y))
        y += 25
        
        # Territori
        territories = len([t for t in self.territories if t.owner == faction])
        text = self.font_small.render(f"Territori: {territories}", True, WHITE)
        self.screen.blit(text, (10, y))
        
        # Controlli
        y = SCREEN_HEIGHT - 80
        controls = [
            "Click territorio tuo = Menu acquisto",
            "Click territorio nemico = Attacca",
            "SPAZIO = Fine turno",
            "ESC = Chiudi menu"
        ]
        for line in controls:
            text = self.font_small.render(line, True, GRAY)
            self.screen.blit(text, (10, y))
            y += 20
    
    def run(self):
        """Loop principale"""
        print("=" * 60)
        print("MODALITÀ HOT SEAT - Passare PC tra giocatori!")
        print("=" * 60)
        print(f"Fazioni: {', '.join(self.factions)}")
        print()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.next_turn()
                    elif event.key == pygame.K_ESCAPE:
                        if self.buy_menu:
                            self.buy_menu = None
                        else:
                            self.running = False
            
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()


if __name__ == "__main__":
    # Importa BuyMenu da gioco_avanzato
    from gioco_avanzato import BuyMenu
    
    game = Game()
    game.run()


