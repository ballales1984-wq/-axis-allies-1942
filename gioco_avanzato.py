"""
GreatWar3 - Sistema Armamenti Avanzato
Con Carri Armati, Aerei, Fanteria e sistema durabilità
"""

import pygame
import sys
import json
import os
import random
import math
from console_comando import CommandConsole
from grafica_migliorata import GraphicsEnhancer, UnitIcon, create_territory_sprite
from effetti_visivi import ParticleSystem, BattleAnimation, MissileAnimation
from voce_commenti import VoiceAnnouncer

# Fix per PyInstaller - trova i file anche nell'EXE
def resource_path(relative_path):
    """Ottieni path assoluto per file, funziona anche con PyInstaller"""
    try:
        # PyInstaller crea una cartella temporanea _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Se non è un EXE, usa la directory corrente
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

# 5 ALLEANZE GEOGRAFICHE - COLORI OTTIMIZZATI PER MASSIMA DISTINZIONE
FACTIONS = {
    "usa": {"name": "USA", "color": (0, 120, 255), "money": 5000, "oil": 1000, "tech": 0},  # BLU BRILLANTE
    "europa": {"name": "EUROPA", "color": (255, 0, 0), "money": 5000, "oil": 1000, "tech": 0},  # ROSSO PURO
    "russia": {"name": "RUSSIA", "color": (180, 0, 255), "money": 5000, "oil": 1000, "tech": 0},  # VIOLA/MAGENTA
    "cina": {"name": "CINA", "color": (255, 255, 0), "money": 5000, "oil": 1000, "tech": 0},  # GIALLO PURO
    "africa": {"name": "AFRICA", "color": (0, 220, 0), "money": 5000, "oil": 1000, "tech": 0}  # VERDE BRILLANTE
}

COLOR_SELECTED = (255, 215, 0)

# LIVELLI TECNOLOGIA ESPANSI - 10 LIVELLI!
TECH_LEVELS = [
    {"points": 0, "name": "Era Primitiva", "bonus_attack": 0, "bonus_defense": 0, "unlocks": []},
    {"points": 50, "name": "Industriale", "bonus_attack": 1, "bonus_defense": 1, "unlocks": ["scienziato"]},
    {"points": 150, "name": "Prima Guerra", "bonus_attack": 2, "bonus_defense": 1, "unlocks": ["artiglieria"]},
    {"points": 300, "name": "Seconda Guerra", "bonus_attack": 3, "bonus_defense": 2, "unlocks": ["carro"]},
    {"points": 500, "name": "Guerra Fredda", "bonus_attack": 5, "bonus_defense": 3, "unlocks": ["aereo"]},
    {"points": 800, "name": "Era Moderna", "bonus_attack": 7, "bonus_defense": 4, "unlocks": ["bombardiere", "drone"]},
    {"points": 1200, "name": "Era Digitale", "bonus_attack": 10, "bonus_defense": 6, "unlocks": ["hacker"]},
    {"points": 1700, "name": "Era Robotica", "bonus_attack": 13, "bonus_defense": 8, "unlocks": ["robot"]},
    {"points": 2500, "name": "Era Nucleare", "bonus_attack": 17, "bonus_defense": 10, "unlocks": ["nuke"]},
    {"points": 3500, "name": "Era Futuristica", "bonus_attack": 25, "bonus_defense": 15, "unlocks": ["supersoldato"]}
]

# TIPI UNITÀ
class UnitType:
    FANTERIA = "fanteria"
    CARRO = "carro"
    AEREO = "aereo"
    NUKE = "nuke"
    SCIENZIATO = "scienziato"
    ARTIGLIERIA = "artiglieria"
    DRONE = "drone"
    HACKER = "hacker"
    ROBOT = "robot"
    SUPERSOLDATO = "supersoldato"

# STATISTICHE UNITÀ
UNIT_STATS = {
    "fanteria": {
        "name": "Fanteria",
        "cost": 50,
        "repair_cost": 20,
        "attack": 2,
        "defense": 2,
        "hp": 10,
        "durability": 10,
        "range": 100,  # CORTO RAGGIO - solo vicinissimi
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
        "range": 200,  # MEDIO RAGGIO - stati confinanti
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
        "range": 500,  # LUNGO RAGGIO - proiezione globale
        "icon": "A"
    },
    "bombardiere": {
        "name": "Bombardiere",
        "cost": 3000,
        "repair_cost": 1200,
        "attack": 25,  # MOLTO POTENTE
        "defense": 3,  # DEBOLE in difesa
        "hp": 40,
        "durability": 5,
        "range": 700,  # RAGGIO SUPERIORE all'aereo
        "icon": "B"
    },
    "nuke": {
        "name": "BOMBA ATOMICA",
        "cost": 10000,
        "range": 9999,  # ILLIMITATO
        "attack": 999,
        "defense": 0,
        "icon": "☢",
        "repair_cost": 0,
        "hp": 1,
        "durability": 1
    },
    "scienziato": {
        "name": "Scienziato",
        "cost": 300,
        "repair_cost": 100,
        "attack": 0,  # NON COMBATTE
        "defense": 1,  # MOLTO DEBOLE
        "hp": 5,
        "durability": 99,  # VIVE A LUNGO
        "range": 0,  # NON ATTACCA
        "icon": "🔬",
        "tech_production": 10  # Produce 10 tech/turno
    },
    "artiglieria": {
        "name": "Artiglieria",
        "cost": 800,
        "repair_cost": 300,
        "attack": 12,
        "defense": 4,
        "hp": 35,
        "durability": 7,
        "range": 350,  # LUNGO RAGGIO ma meno dell'aereo
        "icon": "🎯"
    },
    "drone": {
        "name": "Drone",
        "cost": 2000,
        "repair_cost": 800,
        "attack": 18,
        "defense": 3,
        "hp": 20,
        "durability": 5,
        "range": 600,  # MOLTO LUNGO RAGGIO
        "icon": "🛸"
    },
    "hacker": {
        "name": "Hacker",
        "cost": 1200,
        "repair_cost": 500,
        "attack": 10,  # ATTACCO CYBER
        "defense": 2,
        "hp": 10,
        "durability": 10,
        "range": 9999,  # ATTACCO GLOBALE via internet
        "icon": "💻",
        "cyber_attack": True  # Può rubare risorse
    },
    "robot": {
        "name": "Robot Militare",
        "cost": 3500,
        "repair_cost": 1500,
        "attack": 30,
        "defense": 20,
        "hp": 80,
        "durability": 8,
        "range": 300,
        "icon": "🤖"
    },
    "supersoldato": {
        "name": "Super Soldato",
        "cost": 5000,
        "repair_cost": 2000,
        "attack": 40,
        "defense": 25,
        "hp": 100,
        "durability": 10,
        "range": 400,
        "icon": "⚡"
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
    """Territorio con 3 RISORSE che CRESCONO nel tempo"""
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
        
        # 3 RISORSE BASE del territorio
        self.base_income = random.randint(100, 500)  # Soldi base
        self.base_oil = random.randint(50, 200)  # Petrolio base
        self.base_tech = random.randint(10, 50)  # Tech base
        
        # BONUS TEMPORALI - crescono ogni turno mantenuto!
        self.turns_held = 0  # Turni sotto stesso proprietario
        self.development_level = 0  # Livello sviluppo (0-10)
        
        # DIFESE ACQUISTABILI (fortificazioni permanenti)
        self.bunkers = 0      # Bunker: +5 difesa ($300)
        self.towers = 0       # Torre: +10 difesa ($800)
        self.fortress = 0     # Fortezza: +30 difesa ($2500)
    
    @property
    def income(self):
        """Reddito aumenta con sviluppo"""
        return self.base_income + (self.development_level * 50)
    
    @property
    def oil_production(self):
        """Petrolio aumenta con sviluppo"""
        return self.base_oil + (self.development_level * 20)
    
    @property
    def tech_points(self):
        """Tech aumenta con sviluppo"""
        return self.base_tech + (self.development_level * 5)
    
    def advance_development(self):
        """Avanza sviluppo ogni turno mantenuto"""
        self.turns_held += 1
        # Ogni 2 turni aumenta development (max 10)
        if self.turns_held % 2 == 0 and self.development_level < 10:
            self.development_level += 1
            return True  # Segnala upgrade
        return False
    
    def reset_development(self):
        """RESET sviluppo quando conquistato"""
        self.turns_held = 0
        self.development_level = 0
    
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
    
    def get_total_attack(self, tech_bonus=0):
        """Potenza attacco totale con BONUS TECNOLOGIA"""
        base_attack = sum(u.attack for u in self.units if not u.needs_repair)
        return base_attack + tech_bonus
    
    def get_total_defense(self, tech_bonus=0):
        """Potenza difesa totale con BONUS TECNOLOGIA + DIFESE STRUTTURALI"""
        base_defense = sum(u.defense for u in self.units if not u.needs_repair)
        defense_with_tech = base_defense + tech_bonus
        
        # AGGIUNGI DIFESE STRUTTURALI
        structural_defense = (self.bunkers * 5) + (self.towers * 10) + (self.fortress * 30)
        
        return defense_with_tech + structural_defense
    
    def count_units_by_type(self):
        """Conta unità per tipo - TUTTE LE NUOVE UNITÀ"""
        counts = {
            "fanteria": 0, "carro": 0, "aereo": 0, "bombardiere": 0,
            "scienziato": 0, "artiglieria": 0, "drone": 0, 
            "hacker": 0, "robot": 0, "supersoldato": 0
        }
        for u in self.units:
            if u.type in counts:
                counts[u.type] += 1
        return counts
    
    def age_all_units(self):
        """Invecchia tutte le unità"""
        for u in self.units:
            u.age_unit()
    
    def get_visual_radius(self):
        """Raggio visivo RIDOTTO - max +2px per evitare sovrapposizioni"""
        return self.radius + min(self.development_level // 5, 2)  # Max +2px
    
    def get_attack_range(self):
        """Raggio attacco aumenta con sviluppo"""
        # Base: 50 pixel (solo vicini)
        # Max sviluppo (10): 300 pixel (lunga distanza!)
        return 50 + (self.development_level * 25)
    
    def has_missiles(self):
        """Ha missili a lungo raggio?"""
        return self.development_level >= 8  # Livello 8+ = missili!
    
    def draw(self, surface, font_small, graphics):
        """Disegna territorio con CRESCITA VISIVA"""
        color = self.get_color()
        visual_radius = self.get_visual_radius()
        
        # CERCHIO DI INFLUENZA RIDOTTO (solo territori molto sviluppati)
        if self.development_level >= 7:
            influence_radius = 15 + (self.development_level - 7)  # Max 18px
            influence_alpha = 20 + (self.development_level * 3)  # Più trasparente
            
            s = pygame.Surface((influence_radius * 2, influence_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*color, influence_alpha), (influence_radius, influence_radius), influence_radius)
            surface.blit(s, (self.x - influence_radius, self.y - influence_radius))
        
        # GLOW RIDOTTO se selezionato
        if self.selected:
            graphics.draw_pulsing_circle(surface, (self.x, self.y), visual_radius + 4, COLOR_SELECTED, self.id)  # +4 invece di +8
        
        # Puntino CRESCE con sviluppo!
        glow_intensity = 2 + self.development_level // 2
        graphics.draw_glowing_circle(surface, (self.x, self.y), visual_radius, color, glow_intensity)
        
        # Bordo brillante
        pygame.draw.circle(surface, (255, 255, 255, 180), (self.x, self.y), visual_radius, 1)
        
        # INDICATORE MISSILI RIDOTTO (se livello 8+)
        if self.has_missiles():
            # Cerchio rosso esterno PICCOLO = raggio missili
            missile_range_visual = 12  # RIDOTTO da 40 a 12!
            s_range = pygame.Surface((missile_range_visual * 2, missile_range_visual * 2), pygame.SRCALPHA)
            pygame.draw.circle(s_range, (255, 0, 0, 40), (missile_range_visual, missile_range_visual), missile_range_visual)
            pygame.draw.circle(s_range, (255, 0, 0, 120), (missile_range_visual, missile_range_visual), missile_range_visual, 1)
            surface.blit(s_range, (self.x - missile_range_visual, self.y - missile_range_visual))
            
            # Icona missile (testo) - più piccola
            missile_icon = font_small.render("M", True, (255, 100, 100))
            surface.blit(missile_icon, (self.x + visual_radius + 2, self.y - 6))
        
        # Stella sviluppo (>= 5)
        if self.development_level >= 5:
            # Stella dorata pulsante
            pulse = math.sin(pygame.time.get_ticks() / 300 + self.id) * 0.2 + 1
            star_size = int(8 * pulse)
            
            dev_text = font_small.render(f"*{self.development_level}", True, (255, 215, 0))
            dev_rect = dev_text.get_rect(center=(self.x, self.y - 14))
            
            # Glow dietro stella
            glow = pygame.Surface((dev_rect.width + 10, dev_rect.height + 6), pygame.SRCALPHA)
            pygame.draw.circle(glow, (255, 215, 0, 100), 
                             (glow.get_width()//2, glow.get_height()//2), star_size)
            surface.blit(glow, (dev_rect.x - 5, dev_rect.y - 3))
            
            # Sfondo testo
            bg_dev = pygame.Surface((dev_rect.width + 6, dev_rect.height + 4))
            bg_dev.set_alpha(230)
            bg_dev.fill((0, 0, 0))
            surface.blit(bg_dev, (dev_rect.x - 3, dev_rect.y - 2))
            surface.blit(dev_text, dev_rect)

class BuyMenu:
    """Menu acquisto unità TRASCINABILE"""
    def __init__(self, territory, faction, turn):
        self.territory = territory
        self.faction = faction
        self.turn = turn
        self.active = True
        self.selected_item = None
        
        # Posizione menu - BARRA ORIZZONTALE IN BASSO - ESTESO PER NUOVE UNITÀ
        self.width = 1360  # Molto largo
        self.height = 240  # Aumentato per 2 righe di bottoni
        self.x = (SCREEN_WIDTH - self.width) // 2  # Centrato
        self.y = SCREEN_HEIGHT - self.height - 10  # In basso
        
        # Drag & drop
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
    
    def draw(self, surface, font, font_small):
        """Disegna menu ORIZZONTALE - Layout a barra in basso"""
        # Reset bottoni per click detection
        self.buttons = []
        
        # Sfondo con gradiente
        bg = pygame.Surface((self.width, self.height))
        bg.set_alpha(240)
        bg.fill((15, 20, 35))
        surface.blit(bg, (self.x, self.y))
        
        # Bordo elegante
        border_color = (100, 255, 150) if self.dragging else (255, 200, 50)
        pygame.draw.rect(surface, border_color, (self.x, self.y, self.width, self.height), 3)
        
        # === LAYOUT ORIZZONTALE - 3 SEZIONI ===
        
        # SEZIONE 1: INFO TERRITORIO (sinistra - 280px)
        x1 = self.x + 15
        
        # Titolo
        title = font_small.render(f"{self.territory.name.upper()}", True, (255, 255, 100))
        surface.blit(title, (x1, self.y + 10))
        
        # Sviluppo
        dev_text = font_small.render(f"Sviluppo: {self.territory.development_level}/10", True, (255, 215, 0))
        surface.blit(dev_text, (x1, self.y + 30))
        
        # Unità presenti - TUTTE LE UNITÀ
        counts = self.territory.count_units_by_type()
        units_line = f"F:{counts['fanteria']} C:{counts['carro']} A:{counts['aereo']} B:{counts['bombardiere']}"
        units_text = font_small.render(units_line, True, (200, 255, 200))
        surface.blit(units_text, (x1, self.y + 50))
        
        # Nuove unità (riga 2)
        units_line2 = f"🔬:{counts['scienziato']} 🎯:{counts['artiglieria']} 🛸:{counts['drone']}"
        units_text2 = font_small.render(units_line2, True, (150, 255, 255))
        surface.blit(units_text2, (x1, self.y + 65))
        
        # Risorse
        money = FACTIONS[self.faction]["money"]
        oil = FACTIONS[self.faction]["oil"]
        tech = FACTIONS[self.faction]["tech"]
        
        res_text1 = font_small.render(f"[$] ${money}", True, (100, 255, 100))
        surface.blit(res_text1, (x1, self.y + 70))
        
        res_text2 = font_small.render(f"[P] {oil}P [T] {tech}T", True, (255, 200, 100))
        surface.blit(res_text2, (x1, self.y + 90))
        
        # Produzione
        prod = font_small.render(f"+${self.territory.income} +{self.territory.oil_production}P +{self.territory.tech_points}T/turno", 
                                True, (150, 200, 255))
        surface.blit(prod, (x1, self.y + 110))
        
        # Difese
        if self.territory.bunkers > 0 or self.territory.towers > 0 or self.territory.fortress > 0:
            def_bonus = (self.territory.bunkers * 5) + (self.territory.towers * 10) + (self.territory.fortress * 30)
            def_text = font_small.render(f"DEF: +{def_bonus}", True, (255, 200, 150))
            surface.blit(def_text, (x1, self.y + 130))
        
        help1 = font_small.render("ESC=Chiudi", True, (150, 150, 180))
        surface.blit(help1, (x1, self.y + 155))
        
        # Separatore verticale 1
        pygame.draw.line(surface, (100, 150, 200), 
                        (self.x + 280, self.y + 10), 
                        (self.x + 280, self.y + self.height - 10), 2)
        
        # SEZIONE 2: ACQUISTA UNITÀ (centro - 680px)
        x2 = self.x + 295
        
        # Titolo sezione
        buy_title = font_small.render("ACQUISTA:", True, (255, 215, 100))
        surface.blit(buy_title, (x2, self.y + 10))
        
        # Bottoni unità in ORIZZONTALE (4 unità + nuke + ripara = 6 bottoni)
        btn_width = 105
        btn_height = 70
        btn_spacing = 112
        btn_y = self.y + 30
        
        # Fanteria
        self.draw_buy_button_compact(surface, font_small, "fanteria", UNIT_STATS["fanteria"], 
                                     x2, btn_y, btn_width, btn_height, 1)
        
        # Carro
        self.draw_buy_button_compact(surface, font_small, "carro", UNIT_STATS["carro"], 
                                     x2 + btn_spacing, btn_y, btn_width, btn_height, 2)
        
        # Aereo
        self.draw_buy_button_compact(surface, font_small, "aereo", UNIT_STATS["aereo"], 
                                     x2 + btn_spacing * 2, btn_y, btn_width, btn_height, 3)
        
        # Bombardiere
        self.draw_buy_button_compact(surface, font_small, "bombardiere", UNIT_STATS["bombardiere"], 
                                     x2 + btn_spacing * 3, btn_y, btn_width, btn_height, 4)
        
        # RIGA 2: NUOVE UNITÀ SPECIALI
        btn_y2 = self.y + 110
        btn_spacing_small = 90  # Bottoni più stretti per inserirne 6
        btn_width_small = 85
        btn_height_small = 55
        
        # Scienziato (Q)
        self.draw_buy_button_compact(surface, font_small, "scienziato", UNIT_STATS["scienziato"], 
                                     x2, btn_y2, btn_width_small, btn_height_small, 'Q')
        
        # Artiglieria (W)
        self.draw_buy_button_compact(surface, font_small, "artiglieria", UNIT_STATS["artiglieria"], 
                                     x2 + btn_spacing_small, btn_y2, btn_width_small, btn_height_small, 'W')
        
        # Drone (E)
        self.draw_buy_button_compact(surface, font_small, "drone", UNIT_STATS["drone"], 
                                     x2 + btn_spacing_small * 2, btn_y2, btn_width_small, btn_height_small, 'E')
        
        # Hacker (T)
        self.draw_buy_button_compact(surface, font_small, "hacker", UNIT_STATS["hacker"], 
                                     x2 + btn_spacing_small * 3, btn_y2, btn_width_small, btn_height_small, 'T')
        
        # Robot (Y)
        self.draw_buy_button_compact(surface, font_small, "robot", UNIT_STATS["robot"], 
                                     x2 + btn_spacing_small * 4, btn_y2, btn_width_small, btn_height_small, 'Y')
        
        # Super Soldato (U)
        self.draw_buy_button_compact(surface, font_small, "supersoldato", UNIT_STATS["supersoldato"], 
                                     x2 + btn_spacing_small * 5, btn_y2, btn_width_small, btn_height_small, 'U')
        
        # RIGA 3: Ripara e Nuke
        btn_y3 = self.y + 175
        self.draw_repair_button_compact(surface, font_small, x2, btn_y3, btn_width, 50)
        self.draw_nuke_button_compact(surface, font_small, x2 + btn_spacing, btn_y3, btn_width * 2, 50)
        
        # Separatore verticale 2
        pygame.draw.line(surface, (100, 150, 200), 
                        (self.x + 980, self.y + 10), 
                        (self.x + 980, self.y + self.height - 10), 2)
        
        # SEZIONE 3: DIFESE (destra - 360px)
        x3 = self.x + 995
        
        # Titolo difese
        def_title = font_small.render("COSTRUISCI DIFESE:", True, (100, 255, 100))
        surface.blit(def_title, (x3, self.y + 10))
        
        # 3 bottoni difese in verticale compatte
        def_y = self.y + 35
        def_spacing = 45
        
        self.draw_defense_button_compact(surface, font_small, "bunker", 2000, 5, x3, def_y, 5)
        self.draw_defense_button_compact(surface, font_small, "tower", 5000, 10, x3, def_y + def_spacing, 6)
        self.draw_defense_button_compact(surface, font_small, "fortress", 15000, 30, x3, def_y + def_spacing * 2, 7)
        
        # Help in basso - AGGIORNATO CON NUOVE UNITÀ
        help_text = font_small.render("1-4:Base | Q:Scienziato W:Artig E:Drone T:Hacker Y:Robot U:Super | 5-7:Difese | R:Ripara N:Nuke", 
                                     True, (150, 150, 200))
        surface.blit(help_text, (self.x + 10, self.y + self.height - 18))
    
    def draw_unit_icon(self, surface, unit_type, x, y, size=40):
        """Disegna icona stilizzata dell'unità"""
        
        if unit_type == "fanteria":
            # SOLDATINO (omino stilizzato)
            # Testa
            pygame.draw.circle(surface, (255, 220, 180), (x + size//2, y + size//4), size//6)
            pygame.draw.circle(surface, (100, 100, 100), (x + size//2, y + size//4), size//6, 1)
            # Corpo
            pygame.draw.rect(surface, (80, 120, 80), 
                           (x + size//3, y + size//2.5, size//3, size//2.2))
            # Braccia
            pygame.draw.line(surface, (80, 120, 80), 
                           (x + size//4, y + size//2), (x + size*3//4, y + size//2), 4)
            # Gambe
            pygame.draw.line(surface, (80, 120, 80), 
                           (x + size//2.5, y + size*3//4), (x + size//3, y + size), 4)
            pygame.draw.line(surface, (80, 120, 80), 
                           (x + size*2//3, y + size*3//4), (x + size*3//4, y + size), 4)
            # Fucile
            pygame.draw.line(surface, (60, 60, 60), 
                           (x + size*3//4, y + size//2.5), (x + size*3//4, y + size//5), 3)
        
        elif unit_type == "carro":
            # CARRO ARMATO
            # Cingoli
            pygame.draw.rect(surface, (100, 100, 100), 
                           (x + size//6, y + size*2//3, size*2//3, size//4))
            # Corpo
            pygame.draw.rect(surface, (120, 100, 70), 
                           (x + size//5, y + size//3, size*3//5, size//2.5))
            # Torretta
            pygame.draw.rect(surface, (140, 120, 80), 
                           (x + size//3, y + size//6, size//3, size//3))
            # Cannone
            pygame.draw.rect(surface, (80, 80, 80), 
                           (x + size*2//3, y + size//4, size//3, size//10))
            # Ruote cingoli
            pygame.draw.circle(surface, (50, 50, 50), (x + size//4, y + size*3//4), size//10)
            pygame.draw.circle(surface, (50, 50, 50), (x + size*3//4, y + size*3//4), size//10)
        
        elif unit_type == "aereo":
            # AEREO (vista dall'alto)
            # Fusoliera
            pygame.draw.polygon(surface, (70, 90, 130), [
                (x + size//2, y + size//6),        # Naso
                (x + size//2.5, y + size*5//6),    # Sinistra
                (x + size*3//5, y + size*5//6)     # Destra
            ])
            # Ali
            pygame.draw.polygon(surface, (100, 120, 160), [
                (x + size//10, y + size//2),       # Ala sx
                (x + size*4//5, y + size//2),      # Ala dx
                (x + size//2, y + size*3//5)       # Centro
            ])
            # Coda
            pygame.draw.polygon(surface, (90, 110, 150), [
                (x + size//3, y + size*4//5),
                (x + size*2//3, y + size*4//5),
                (x + size//2, y + size)
            ])
            # Cockpit
            pygame.draw.circle(surface, (150, 200, 255), (x + size//2, y + size//3), size//8)
        
        elif unit_type == "bombardiere":
            # BOMBARDIERE (più grande e pesante)
            # Fusoliera principale (più larga)
            pygame.draw.rect(surface, (90, 90, 90), 
                           (x + size//3, y + size//6, size//3, size*2//3))
            # Ali larghe
            pygame.draw.polygon(surface, (120, 120, 120), [
                (x, y + size//2),                  # Ala sx
                (x + size, y + size//2),            # Ala dx
                (x + size//2, y + size*3//5)       # Centro
            ])
            # Motori sulle ali
            pygame.draw.circle(surface, (180, 50, 50), (x + size//4, y + size//2), size//8)
            pygame.draw.circle(surface, (180, 50, 50), (x + size*3//4, y + size//2), size//8)
            # Coda a T
            pygame.draw.rect(surface, (100, 100, 100), 
                           (x + size//2.5, y + size*4//5, size//5, size//8))
            # Nose cone
            pygame.draw.polygon(surface, (140, 140, 140), [
                (x + size//2, y),
                (x + size//3, y + size//4),
                (x + size*2//3, y + size//4)
            ])
            # Bombe sotto (distintivo!)
            pygame.draw.ellipse(surface, (200, 50, 50), 
                              (x + size//2.5, y + size//2.2, size//8, size//5))
            pygame.draw.ellipse(surface, (200, 50, 50), 
                              (x + size*3//5, y + size//2.2, size//8, size//5))
        
        elif unit_type == "scienziato":
            # SCIENZIATO - Omino con camice e provetta
            # Testa
            pygame.draw.circle(surface, (255, 220, 180), (x + size//2, y + size//5), size//6)
            # Occhiali
            pygame.draw.circle(surface, (200, 200, 255), (x + size//2 - size//10, y + size//5), size//12, 2)
            pygame.draw.circle(surface, (200, 200, 255), (x + size//2 + size//10, y + size//5), size//12, 2)
            # Camice bianco
            pygame.draw.rect(surface, (240, 240, 255), 
                           (x + size//3, y + int(size/2.5), size//3, size//2))
            # Braccia
            pygame.draw.line(surface, (240, 240, 255), 
                           (x + size//4, y + size//2), (x + size*3//4, y + size//2), 4)
            # Provetta (mano sinistra)
            pygame.draw.rect(surface, (100, 255, 255), 
                           (x + size//5, y + size//2.5, size//8, size//4))
            pygame.draw.circle(surface, (100, 255, 255), (x + size//5 + size//16, y + size//2.5), size//16)
        
        elif unit_type == "artiglieria":
            # ARTIGLIERIA - Cannone con ruote
            # Ruote
            pygame.draw.circle(surface, (100, 80, 60), (x + size//4, y + size*3//4), size//6)
            pygame.draw.circle(surface, (100, 80, 60), (x + size*3//4, y + size*3//4), size//6)
            # Base
            pygame.draw.rect(surface, (120, 100, 80), 
                           (x + size//4, y + size//2, size//2, size//5))
            # Cannone
            pygame.draw.rect(surface, (80, 60, 50), 
                           (x + size//2, y + size//3, size//2, size//8))
            # Bocca fuoco (rosso)
            pygame.draw.circle(surface, (255, 100, 50), (x + size, y + size//3 + size//16), size//12)
        
        elif unit_type == "drone":
            # DRONE - Quadricottero futuristico
            # Corpo centrale
            pygame.draw.circle(surface, (200, 200, 220), (x + size//2, y + size//2), size//5)
            pygame.draw.circle(surface, (255, 50, 50), (x + size//2, y + size//2), size//8)  # LED rosso
            # Bracci
            pygame.draw.line(surface, (150, 150, 170), (x + size//4, y + size//4), (x + size//2, y + size//2), 3)
            pygame.draw.line(surface, (150, 150, 170), (x + size*3//4, y + size//4), (x + size//2, y + size//2), 3)
            pygame.draw.line(surface, (150, 150, 170), (x + size//4, y + size*3//4), (x + size//2, y + size//2), 3)
            pygame.draw.line(surface, (150, 150, 170), (x + size*3//4, y + size*3//4), (x + size//2, y + size//2), 3)
            # Eliche (cerchi ai 4 angoli)
            for pos in [(size//4, size//4), (size*3//4, size//4), (size//4, size*3//4), (size*3//4, size*3//4)]:
                pygame.draw.circle(surface, (100, 150, 200), (x + pos[0], y + pos[1]), size//8)
                pygame.draw.circle(surface, (150, 200, 255), (x + pos[0], y + pos[1]), size//12)
        
        elif unit_type == "hacker":
            # HACKER - Computer portatile
            # Base del laptop
            pygame.draw.rect(surface, (50, 50, 60), 
                           (x + size//6, y + size//2, size*2//3, size//3))
            # Schermo
            pygame.draw.rect(surface, (30, 30, 40), 
                           (x + size//5, y + size//6, size*3//5, size//2.5))
            # Schermo attivo (verde matrix)
            pygame.draw.rect(surface, (0, 255, 100), 
                           (x + size//4, y + size//4, size//2, size//3))
            # Codice (linee verdi)
            for i in range(3):
                pygame.draw.line(surface, (0, 200, 80), 
                               (x + size//3, y + size//3 + i*size//10), 
                               (x + size*2//3, y + size//3 + i*size//10), 1)
            # Warning symbol (skull cyber)
            pygame.draw.circle(surface, (255, 50, 50), (x + size*3//4, y + size//4), size//10)
        
        elif unit_type == "robot":
            # ROBOT MILITARE - Umanoide corazzato
            # Testa robotica
            pygame.draw.rect(surface, (180, 180, 200), 
                           (x + size//3, y + size//8, size//3, size//4))
            # Occhi LED rossi
            pygame.draw.circle(surface, (255, 50, 50), (x + size//2.5, y + size//5), size//12)
            pygame.draw.circle(surface, (255, 50, 50), (x + size*3//5, y + size//5), size//12)
            # Antenna
            pygame.draw.line(surface, (255, 255, 100), 
                           (x + size//2, y + size//8), (x + size//2, y), 2)
            pygame.draw.circle(surface, (255, 255, 100), (x + size//2, y), size//15)
            # Corpo corazzato
            pygame.draw.rect(surface, (150, 150, 180), 
                           (x + size//3, y + size//2.5, size//3, size//2))
            # Braccia (spesse)
            pygame.draw.rect(surface, (130, 130, 160), 
                           (x + size//6, y + size//2, size//8, size//2.5))
            pygame.draw.rect(surface, (130, 130, 160), 
                           (x + size*2//3, y + size//2, size//8, size//2.5))
            # Arma integrata (braccio destro)
            pygame.draw.rect(surface, (255, 100, 50), 
                           (x + size*2//3, y + size*3//5, size//6, size//10))
        
        elif unit_type == "supersoldato":
            # SUPER SOLDATO - Elite con armatura potenziata
            # Casco high-tech
            pygame.draw.circle(surface, (255, 215, 0), (x + size//2, y + size//5), size//5)
            # Visore (cyan brillante)
            pygame.draw.rect(surface, (0, 255, 255), 
                           (x + size//3, y + size//5, size//3, size//12))
            # Armatura dorata
            pygame.draw.rect(surface, (255, 215, 0), 
                           (x + size//3, y + size//2.5, size//3, size//2))
            # Spalle potenziate
            pygame.draw.circle(surface, (255, 200, 0), (x + size//4, y + size//2.5), size//8)
            pygame.draw.circle(surface, (255, 200, 0), (x + size*3//4, y + size//2.5), size//8)
            # Braccia potenti
            pygame.draw.rect(surface, (200, 180, 0), 
                           (x + size//6, y + size//2, size//6, size//2.5))
            pygame.draw.rect(surface, (200, 180, 0), 
                           (x + size*2//3, y + size//2, size//6, size//2.5))
            # Arma al plasma (viola brillante)
            pygame.draw.rect(surface, (200, 50, 255), 
                           (x + size*3//4, y + size*3//5, size//4, size//8))
            pygame.draw.circle(surface, (255, 100, 255), (x + size, y + size*3//5 + size//16), size//12)
            # Effetto energia (cerchi concentrici gialli)
            pygame.draw.circle(surface, (255, 255, 100), (x + size//2, y + size*3//4), size//8, 2)
            pygame.draw.circle(surface, (255, 255, 150), (x + size//2, y + size*3//4), size//12, 1)
        
        else:
            # Fallback - emoji o testo
            pass
    
    def draw_buy_button_compact(self, surface, font_small, unit_type, stats, x, y, w, h, key_num):
        """Bottone COMPATTO con icone MIGLIORATE"""
        # Check mouse hover
        mouse_pos = pygame.mouse.get_pos()
        is_hover = (x <= mouse_pos[0] <= x + w and y <= mouse_pos[1] <= y + h)
        
        # Salva per click
        if not hasattr(self, 'buttons'):
            self.buttons = []
        self.buttons.append({"rect": pygame.Rect(x, y, w, h), "type": unit_type})
        
        # SFONDO COLORATO PER TIPO UNITÀ
        if unit_type == "scienziato":
            bg_color = (40, 80, 100) if is_hover else (30, 60, 80)
            border_color = (100, 255, 255) if is_hover else (80, 200, 200)
        elif unit_type in ["artiglieria", "carro"]:
            bg_color = (80, 60, 40) if is_hover else (60, 45, 30)
            border_color = (255, 200, 100) if is_hover else (200, 150, 80)
        elif unit_type in ["drone", "aereo"]:
            bg_color = (40, 60, 90) if is_hover else (30, 45, 70)
            border_color = (150, 200, 255) if is_hover else (100, 150, 200)
        elif unit_type == "hacker":
            bg_color = (30, 70, 50) if is_hover else (20, 50, 35)
            border_color = (100, 255, 150) if is_hover else (70, 200, 100)
        elif unit_type == "robot":
            bg_color = (70, 50, 80) if is_hover else (50, 35, 60)
            border_color = (200, 150, 255) if is_hover else (150, 100, 200)
        elif unit_type == "supersoldato":
            bg_color = (100, 80, 20) if is_hover else (70, 60, 15)
            border_color = (255, 215, 0) if is_hover else (200, 170, 0)
        else:
            bg_color = (50, 80, 50) if is_hover else (40, 60, 40)
            border_color = (100, 255, 100) if is_hover else (80, 180, 80)
        
        # Gradiente sfondo
        for i in range(h):
            t = i / h
            r = int(bg_color[0] * (1 + 0.3 * t))
            g = int(bg_color[1] * (1 + 0.3 * t))
            b = int(bg_color[2] * (1 + 0.3 * t))
            pygame.draw.line(surface, (r, g, b), (x, y + i), (x + w, y + i))
        
        # Bordo con spessore se hover
        border_width = 3 if is_hover else 2
        pygame.draw.rect(surface, border_color, (x, y, w, h), border_width)
        
        # BOX ICONA con sfondo scuro
        icon_box_size = 35
        icon_box_x = x + 5
        icon_box_y = y + 5
        pygame.draw.rect(surface, (20, 20, 30), (icon_box_x, icon_box_y, icon_box_size, icon_box_size))
        pygame.draw.rect(surface, border_color, (icon_box_x, icon_box_y, icon_box_size, icon_box_size), 1)
        
        # Icona MIGLIORATA - PIÙ GRANDE
        icon_size = 30
        self.draw_unit_icon(surface, unit_type, icon_box_x + 2, icon_box_y + 2, icon_size)
        
        # Nome unità
        name = stats.get('name', unit_type.capitalize())
        name_short = name[:8] if len(name) > 8 else name
        name_text = font_small.render(name_short, True, (255, 255, 255))
        surface.blit(name_text, (x + 45, y + 5))
        
        # Tasto
        key_text = font_small.render(f"[{key_num}]", True, (255, 255, 100))
        surface.blit(key_text, (x + 45, y + 20))
        
        # Costo
        cost_text = font_small.render(f"${stats['cost']}", True, (100, 255, 100))
        surface.blit(cost_text, (x + 5, y + h - 16))
        
        # CONTROLLO TECNOLOGIA - mostra se sbloccata
        tech_points = FACTIONS[self.faction]["tech"]
        is_unlocked = (unit_type == "fanteria")  # Fanteria sempre sbloccata
        required_tech = 0
        
        for level in TECH_LEVELS:
            if unit_type in level.get("unlocks", []):
                required_tech = level["points"]
                if tech_points >= required_tech:
                    is_unlocked = True
                break
        
        # Indicatore LOCK/UNLOCK
        if not is_unlocked:
            # Overlay scuro se bloccato
            lock_overlay = pygame.Surface((w, h))
            lock_overlay.set_alpha(150)
            lock_overlay.fill((0, 0, 0))
            surface.blit(lock_overlay, (x, y))
            
            # Simbolo lucchetto
            lock_text = font_small.render("🔒", True, (255, 100, 100))
            surface.blit(lock_text, (x + w//2 - 10, y + h//2 - 10))
            
            # Tech richiesta
            req_text = font_small.render(f"{required_tech}T", True, (255, 200, 100))
            surface.blit(req_text, (x + w//2 - 15, y + h - 16))
        else:
            # Stats ATT/DEF - con icone (solo se sbloccato)
            if stats['attack'] > 0:
                att_text = font_small.render(f"⚔️{stats['attack']}", True, (255, 150, 150))
                surface.blit(att_text, (x + w - 60, y + h - 30))
            
            def_text = font_small.render(f"🛡️{stats['defense']}", True, (150, 200, 255))
            surface.blit(def_text, (x + w - 60, y + h - 15))
            
            # Badge speciale per scienziato
            if unit_type == "scienziato":
                tech_badge = font_small.render("+10T", True, (100, 255, 255))
                surface.blit(tech_badge, (x + 45, y + 35))
    
    def draw_repair_button_compact(self, surface, font_small, x, y, w, h):
        """Bottone RIPARA compatto"""
        mouse_pos = pygame.mouse.get_pos()
        is_hover = (x <= mouse_pos[0] <= x + w and y <= mouse_pos[1] <= y + h)
        
        if not hasattr(self, 'buttons'):
            self.buttons = []
        self.buttons.append({"rect": pygame.Rect(x, y, w, h), "type": "repair"})
        
        bg_color = (80, 80, 50) if is_hover else (60, 60, 40)
        pygame.draw.rect(surface, bg_color, (x, y, w, h))
        pygame.draw.rect(surface, (255, 200, 100) if is_hover else (200, 150, 80), (x, y, w, h), 2)
        
        repair_text = font_small.render("[R] RIPARA", True, (255, 255, 255))
        surface.blit(repair_text, (x + 8, y + 10))
        
        cost_text = font_small.render("Variabile", True, (255, 200, 100))
        surface.blit(cost_text, (x + 8, y + 28))
    
    def draw_nuke_button_compact(self, surface, font_small, x, y, w, h):
        """Bottone NUKE compatto"""
        mouse_pos = pygame.mouse.get_pos()
        is_hover = (x <= mouse_pos[0] <= x + w and y <= mouse_pos[1] <= y + h)
        
        if not hasattr(self, 'buttons'):
            self.buttons = []
        self.buttons.append({"rect": pygame.Rect(x, y, w, h), "type": "nuke"})
        
        bg_color = (100, 20, 20) if is_hover else (70, 15, 15)
        pygame.draw.rect(surface, bg_color, (x, y, w, h))
        pygame.draw.rect(surface, (255, 50, 50) if is_hover else (200, 50, 50), (x, y, w, h), 2)
        
        nuke_text = font_small.render("[N] BOMBA ATOMICA", True, (255, 100, 100))
        surface.blit(nuke_text, (x + 10, y + 10))
        
        cost_text = font_small.render("$10,000 - DISTRUZIONE AREA", True, (255, 255, 100))
        surface.blit(cost_text, (x + 10, y + 28))
    
    def draw_defense_button_compact(self, surface, font_small, def_type, cost, bonus, x, y, key_num):
        """Bottone DIFESA compatto"""
        mouse_pos = pygame.mouse.get_pos()
        w = 340
        h = 38
        is_hover = (x <= mouse_pos[0] <= x + w and y <= mouse_pos[1] <= y + h)
        
        if not hasattr(self, 'buttons'):
            self.buttons = []
        self.buttons.append({"rect": pygame.Rect(x, y, w, h), "type": def_type})
        
        bg_color = (40, 50, 80) if is_hover else (30, 40, 60)
        pygame.draw.rect(surface, bg_color, (x, y, w, h))
        pygame.draw.rect(surface, (150, 200, 255) if is_hover else (100, 150, 200), (x, y, w, h), 2)
        
        # Nome
        name = def_type.capitalize()
        name_text = font_small.render(f"[{key_num}] {name}", True, (255, 255, 255))
        surface.blit(name_text, (x + 8, y + 5))
        
        # Costo e bonus
        info_text = font_small.render(f"${cost} | +{bonus} DEF", True, (255, 200, 100))
        surface.blit(info_text, (x + 8, y + 20))
        
        # Quantità già costruita
        current_count = 0
        if def_type == "bunker":
            current_count = self.territory.bunkers
        elif def_type == "tower":
            current_count = self.territory.towers
        elif def_type == "fortress":
            current_count = self.territory.fortress
        
        if current_count > 0:
            count_text = font_small.render(f"x{current_count}", True, (100, 255, 100))
            surface.blit(count_text, (x + w - 35, y + 12))
    
    def draw_buy_button(self, surface, font, font_small, unit_type, stats, x, y, number):
        """Disegna PULSANTE acquisto CLICCABILE con ICONA"""
        button_width = 320
        button_height = 85
        
        # Salva rect per click detection
        button_rect = pygame.Rect(x, y, button_width, button_height)
        if not hasattr(self, 'buttons'):
            self.buttons = {}
        self.buttons[unit_type] = button_rect
        
        # Check hover
        mouse_pos = pygame.mouse.get_pos()
        is_hover = button_rect.collidepoint(mouse_pos)
        
        # Sfondo pulsante con colore (più chiaro se hover)
        if unit_type == "fanteria":
            bg_color = (80, 120, 80) if is_hover else (60, 80, 60)
        elif unit_type == "carro":
            bg_color = (120, 100, 70) if is_hover else (80, 70, 50)
        elif unit_type == "aereo":
            bg_color = (70, 90, 130) if is_hover else (50, 60, 90)
        else:  # bombardiere
            bg_color = (100, 100, 100) if is_hover else (70, 70, 70)
        
        pygame.draw.rect(surface, bg_color, (x, y, button_width, button_height))
        
        # Bordo più spesso se hover
        border_width = 3 if is_hover else 2
        pygame.draw.rect(surface, (255, 200, 50), (x, y, button_width, button_height), border_width)
        
        # ICONA UNITÀ (NUOVO!)
        icon_box_x = x + 8
        icon_box_y = y + 8
        icon_size = 50
        # Sfondo icona
        pygame.draw.rect(surface, (30, 30, 30), (icon_box_x, icon_box_y, icon_size, icon_size))
        pygame.draw.rect(surface, (100, 100, 100), (icon_box_x, icon_box_y, icon_size, icon_size), 1)
        # Disegna icona
        self.draw_unit_icon(surface, unit_type, icon_box_x + 5, icon_box_y + 5, icon_size - 10)
        
        # Numero tasto
        key_text = font.render(str(number), True, (255, 255, 100))
        surface.blit(key_text, (x + icon_box_x + 5, y + 65))
        
        # Nome unità GRANDE
        name_text = font.render(f"{stats['name']}", True, (255, 255, 255))
        surface.blit(name_text, (x + 70, y + 8))
        
        # Costo EVIDENTE
        cost_text = font.render(f"${stats['cost']}", True, (100, 255, 100))
        surface.blit(cost_text, (x + 70, y + 35))
        
        # Stats compatte
        stats_text = font_small.render(
            f"ATT:{stats['attack']} DEF:{stats['defense']} HP:{stats['hp']}", 
            True, (200, 200, 200)
        )
        surface.blit(stats_text, (x + 70, y + 62))
    
    def draw_nuke_button(self, surface, font, font_small, x, y):
        """Pulsante BOMBA ATOMICA"""
        button_width = 320
        button_height = 55
        
        # Salva rect
        button_rect = pygame.Rect(x, y, button_width, button_height)
        if not hasattr(self, 'buttons'):
            self.buttons = {}
        self.buttons['nuke'] = button_rect
        
        # Check hover
        mouse_pos = pygame.mouse.get_pos()
        is_hover = button_rect.collidepoint(mouse_pos)
        
        # Sfondo ROSSO lampeggiante
        import time
        flash = int(time.time() * 3) % 2
        if flash:
            bg_color = (180, 20, 20) if is_hover else (150, 0, 0)
        else:
            bg_color = (140, 0, 0) if is_hover else (120, 0, 0)
        
        pygame.draw.rect(surface, bg_color, (x, y, button_width, button_height))
        
        border_width = 4 if is_hover else 3
        pygame.draw.rect(surface, (255, 50, 50), (x, y, button_width, button_height), border_width)
        
        # Icona atomica
        nuke_icon = font.render("[N]", True, (255, 255, 0))
        surface.blit(nuke_icon, (x + 12, y + 12))
        
        # Testo
        name_text = font.render("BOMBA ATOMICA", True, (255, 255, 255))
        surface.blit(name_text, (x + 45, y + 8))
        
        cost_text = font.render("$10,000", True, (255, 255, 100))
        surface.blit(cost_text, (x + 45, y + 30))
    
    def draw_repair_button(self, surface, font, font_small, x, y):
        """Pulsante RIPARA CLICCABILE"""
        button_width = 320
        button_height = 50
        
        # Salva rect per click
        button_rect = pygame.Rect(x, y, button_width, button_height)
        if not hasattr(self, 'buttons'):
            self.buttons = {}
        self.buttons['repair'] = button_rect
        
        # Check hover
        mouse_pos = pygame.mouse.get_pos()
        is_hover = button_rect.collidepoint(mouse_pos)
        
        # Sfondo arancione (più chiaro se hover)
        bg_color = (140, 80, 30) if is_hover else (100, 60, 20)
        pygame.draw.rect(surface, bg_color, (x, y, button_width, button_height))
        
        border_width = 4 if is_hover else 3
        pygame.draw.rect(surface, (255, 150, 50), (x, y, button_width, button_height), border_width)
        
        # Tasto R
        key_circle = pygame.Surface((35, 35), pygame.SRCALPHA)
        pygame.draw.circle(key_circle, (255, 200, 100), (17, 17), 17)
        pygame.draw.circle(key_circle, (0, 0, 0), (17, 17), 17, 2)
        surface.blit(key_circle, (x + 8, y + 7))
        
        key_text = font.render("R", True, (0, 0, 0))
        key_rect = key_text.get_rect(center=(x + 25, y + 24))
        surface.blit(key_text, key_rect)
        
        # Testo
        repair_text = font.render("RIPARA TUTTE LE UNITA'", True, (255, 255, 255))
        surface.blit(repair_text, (x + 55, y + 15))
    
    def draw_defense_buttons(self, surface, font_small, x, y):
        """Pulsanti per acquistare DIFESE strutturali"""
        mouse_pos = pygame.mouse.get_pos()
        button_width = 320
        button_height = 30
        
        defenses = [
            ("bunker", "4 - BUNKER ($300) +5 DEF", 300, self.territory.bunkers, (60, 100, 60)),
            ("tower", "5 - TORRE ($800) +10 DEF", 800, self.territory.towers, (100, 60, 60)),
            ("fortress", "6 - FORTEZZA ($2500) +30 DEF", 2500, self.territory.fortress, (100, 100, 30))
        ]
        
        for def_type, label, cost, count, base_color in defenses:
            button_rect = pygame.Rect(x, y, button_width, button_height)
            if not hasattr(self, 'buttons'):
                self.buttons = {}
            self.buttons[def_type] = button_rect
            
            is_hover = button_rect.collidepoint(mouse_pos)
            
            # Sfondo (più chiaro se hover)
            r, g, b = base_color
            if is_hover:
                bg_color = (min(255, r + 40), min(255, g + 40), min(255, b + 40))
            else:
                bg_color = base_color
            
            pygame.draw.rect(surface, bg_color, button_rect)
            pygame.draw.rect(surface, (200, 200, 200), button_rect, 2)
            
            # Testo
            text_label = f"{label} [Hai: {count}]"
            text = font_small.render(text_label, True, (255, 255, 255))
            surface.blit(text, (x + 5, y + 8))
            
            y += button_height + 3
    
    def contains_point(self, px, py):
        """Check se punto è dentro il menu"""
        return (self.x <= px <= self.x + self.width and 
                self.y <= py <= self.y + self.height)
    
    def in_title_bar(self, px, py):
        """Check se punto è nella barra titolo (per drag)"""
        return (self.x <= px <= self.x + self.width and 
                self.y <= py <= self.y + 40)
    
    def start_drag(self, mouse_x, mouse_y):
        """Inizia trascinamento"""
        self.dragging = True
        self.drag_offset_x = mouse_x - self.x
        self.drag_offset_y = mouse_y - self.y
    
    def stop_drag(self):
        """Fine trascinamento"""
        self.dragging = False
    
    def update_position(self, mouse_x, mouse_y):
        """Aggiorna posizione durante drag"""
        if self.dragging:
            self.x = mouse_x - self.drag_offset_x
            self.y = mouse_y - self.drag_offset_y
            
            # Limiti schermo
            self.x = max(0, min(self.x, 1400 - self.width))
            self.y = max(0, min(self.y, 800 - self.height))
    
    def handle_click_button(self, mouse_pos):
        """Gestisce CLICK sui pulsanti"""
        if not hasattr(self, 'buttons'):
            return None
        
        for button in self.buttons:
            if button["rect"].collidepoint(mouse_pos):
                button_type = button["type"]
                
                if button_type == "fanteria":
                    return self.buy_unit("fanteria")
                elif button_type == "carro":
                    return self.buy_unit("carro")
                elif button_type == "aereo":
                    return self.buy_unit("aereo")
                elif button_type == "bombardiere":
                    return self.buy_unit("bombardiere")
                elif button_type == "nuke":
                    return "nuke_mode"
                elif button_type == "repair":
                    return self.repair_units()
                elif button_type == "bunker":
                    return self.buy_defense("bunker", 2000, 5)
                elif button_type == "tower":
                    return self.buy_defense("tower", 5000, 10)
                elif button_type == "fortress":
                    return self.buy_defense("fortress", 15000, 30)
        return None
    
    def handle_key(self, key):
        """Gestisce input TASTIERA (alternativa ai click)"""
        if key == pygame.K_1:
            return self.buy_unit("fanteria")
        elif key == pygame.K_2:
            return self.buy_unit("carro")
        elif key == pygame.K_3:
            return self.buy_unit("aereo")
        elif key == pygame.K_4:
            return self.buy_unit("bombardiere")
        elif key == pygame.K_q:
            return self.buy_unit("scienziato")
        elif key == pygame.K_w:
            return self.buy_unit("artiglieria")
        elif key == pygame.K_e:
            return self.buy_unit("drone")
        elif key == pygame.K_t:
            return self.buy_unit("hacker")
        elif key == pygame.K_y:
            return self.buy_unit("robot")
        elif key == pygame.K_u:
            return self.buy_unit("supersoldato")
        elif key == pygame.K_n:
            return "nuke_mode"  # Modalità lancio nuke
        elif key == pygame.K_r:
            return self.repair_units()
        elif key == pygame.K_5:
            return self.buy_defense("bunker", 2000, 5)
        elif key == pygame.K_6:
            return self.buy_defense("tower", 5000, 10)
        elif key == pygame.K_7:
            return self.buy_defense("fortress", 15000, 30)
        elif key == pygame.K_ESCAPE:
            self.active = False
        return None
    
    def buy_unit(self, unit_type):
        """Compra unità con controllo TECNOLOGIA"""
        # Controlla se l'unità è sbloccata dal livello tecnologico
        tech_points = FACTIONS[self.faction]["tech"]
        unit_unlocked = False
        required_tech_level = "Era Primitiva"
        
        # Verifica se l'unità è disponibile al livello tech attuale
        for level in TECH_LEVELS:
            if tech_points >= level["points"]:
                if unit_type in level["unlocks"] or unit_type == "fanteria":  # Fanteria sempre disponibile
                    unit_unlocked = True
                    break
                # Aggiorna il nome del livello richiesto
                for future_level in TECH_LEVELS:
                    if unit_type in future_level["unlocks"]:
                        required_tech_level = future_level["name"]
                        break
        
        # Fanteria sempre disponibile
        if unit_type == "fanteria":
            unit_unlocked = True
        
        if not unit_unlocked:
            return f"Tecnologia insufficiente! Serve: {required_tech_level}"
        
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
    
    def buy_defense(self, defense_type, cost, bonus):
        """Acquista DIFESA strutturale"""
        if FACTIONS[self.faction]["money"] >= cost:
            FACTIONS[self.faction]["money"] -= cost
            
            if defense_type == "bunker":
                self.territory.bunkers += 1
                return f"[OK] Bunker (+5 DEF) Tot: {self.territory.bunkers}"
            elif defense_type == "tower":
                self.territory.towers += 1
                return f"[OK] Torre (+10 DEF) Tot: {self.territory.towers}"
            elif defense_type == "fortress":
                self.territory.fortress += 1
                return f"[OK] Fortezza (+30 DEF) Tot: {self.territory.fortress}"
        else:
            return f"Servono ${cost}!"

class Game:
    """Gioco completo"""
    
    def __init__(self):
        pygame.init()
        
        # SCHERMO 1400x800
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("GreatWar3 - Gioco di Guerra Strategico")
        self.clock = pygame.time.Clock()
        self.fullscreen = False
        
        self.font = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 16)
        self.font_large = pygame.font.Font(None, 32)
        self.font_title = pygame.font.Font(None, 48)
        
        self.background = self.load_background()
        self.territories = self.load_territories()
        
        self.faction_order = ["usa", "europa", "russia", "cina", "africa"]
        self.current_faction_idx = 0
        self.current_faction = self.faction_order[0]
        self.turn = 1
        
        # Sistema IA - solo USA è umano (giocatore), gli altri sono PC
        self.human_faction = "usa"
        self.ai_factions = ["europa", "russia", "cina", "africa"]
        
        # DIFFICOLTÀ AUMENTATA - IA inizia con PIÙ RISORSE
        for ai_faction in self.ai_factions:
            FACTIONS[ai_faction]["money"] = 8000   # Era 5000, ora 8000
            FACTIONS[ai_faction]["oil"] = 2000     # Era 1000, ora 2000
            FACTIONS[ai_faction]["tech"] = 50      # Era 0, ora 50 (vantaggio tecnologico)
        
        self.assign_territories()
        
        self.selected = None
        self.mode = "select"
        self.buy_menu = None
        self.message = ""
        self.message_timer = 0
        
        # Sistema NUKE
        self.nuke_mode = False
        self.nuke_animations = []
        
        # Sistema SAVE/LOAD
        self.save_load_menu = None  # "save" o "load" quando attivo
        
        # Sistema VITTORIA
        self.victory_faction = None  # Fazione vincitrice
        self.victory_stats = {}  # Statistiche finali
        
        # TIMER RISORSE - accumulo graduale
        self.resource_timer = 0
        self.seconds_in_turn = 0
        
        # CONSOLE DI COMANDO - Apri subito per il primo turno!
        self.command_console = CommandConsole(
            self.current_faction,
            self.territories,
            FACTIONS,
            self.turn,
            TECH_LEVELS
        )
        
        # SISTEMA PARTICELLE E ANIMAZIONI
        self.particles = ParticleSystem()
        self.battle_animations = []
        self.missile_animations = []
        
        # SISTEMA COMMENTI VOCALI
        self.voice = VoiceAnnouncer()
        
        print("="*70)
        print("GREATWAR3 - GIOCO DI GUERRA STRATEGICO")
        print("="*70)
        print("TU controlli: USA")
        print("PC controlla: EUROPA, RUSSIA, CINA, AFRICA")
        print()
        print("NUOVO! Sistema 3 RISORSE:")
        print("  [+] Conquista territorio -> Prendi TUTTE le risorse!")
        print("  [$] Soldi - Compra armamenti")
        print("  [P] Petrolio - Serve per muovere e attaccare")
        print("  [T] Tecnologia - Upgrade armamenti automatici")
        print()
        print("Armamenti: Fanteria ($50), Carro ($500), Aereo ($1500)")
        print("Controlli:")
        print("  Click territorio = APRE ARMERIA automaticamente")
        print("  A = Attacco")
        print("  I = Info territorio")
        print("  S = SALVA partita (4 slot)")
        print("  L = CARICA partita (4 slot)")
        print("  V = Toggle voce on/off")
        print("  N = Bomba atomica ($10,000)")
        print("  SPAZIO = Fine turno (solo nel TUO turno)")
        print("  Nel menu: Click pulsanti o 1/2/3/R")
        print()
        print("IA gioca automaticamente nei suoi turni!")
        print("="*70)
    
    def load_background(self):
        """Carica mappa - funziona anche con EXE"""
        # Prova prima mappa_bn.jpg
        path_bn = resource_path("mappa_bn.jpg")
        if os.path.exists(path_bn):
            return pygame.image.load(path_bn)
        
        # Se non trova, prova mappa_hd.jpg
        path_hd = resource_path("mappa_hd.jpg")
        if os.path.exists(path_hd):
            return pygame.image.load(path_hd)
        
        print("[WARNING] Nessuna mappa trovata! Usando sfondo blu.")
        return None
    
    def load_territories(self):
        """Carica territori - funziona anche con EXE"""
        path = resource_path("centri.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Territory(item) for item in data]
    
    def assign_territories(self):
        """Assegna territori con unità iniziali - IA PIÙ FORTE"""
        shuffled = list(range(len(self.territories)))
        random.shuffle(shuffled)
        per_faction = len(self.territories) // 5
        
        for i, faction in enumerate(self.faction_order):
            start = i * per_faction
            end = start + per_faction if i < 4 else len(self.territories)
            
            for idx in shuffled[start:end]:
                self.territories[idx].owner = faction
                
                # Unità iniziali - IA ha PIÙ UNITÀ (difficoltà aumentata)
                if faction == self.human_faction:  # Giocatore umano
                    # Giocatore: unità normali
                    for _ in range(random.randint(2, 4)):
                        self.territories[idx].add_unit("fanteria", 0)
                    for _ in range(random.randint(0, 2)):
                        self.territories[idx].add_unit("carro", 0)
                else:  # IA (nemici)
                    # IA: MOLTE PIÙ UNITÀ (difficoltà alta)
                    for _ in range(random.randint(4, 6)):  # Era 2-4, ora 4-6
                        self.territories[idx].add_unit("fanteria", 0)
                    for _ in range(random.randint(1, 3)):  # Era 0-2, ora 1-3
                        self.territories[idx].add_unit("carro", 0)
                    # IA inizia anche con alcuni aerei!
                    if random.random() < 0.3:  # 30% chance di avere un aereo
                        self.territories[idx].add_unit("aereo", 0)
    
    def next_turn(self):
        """Prossimo turno con CRESCITA TERRITORI"""
        # Raccogli TUTTE le risorse E avanza sviluppo
        income = 0
        oil = 0
        tech = 0
        upgraded_count = 0
        scientists_count = 0
        
        for t in self.territories:
            if t.owner == self.current_faction:
                # Raccogli risorse (con bonus sviluppo!)
                income += t.income
                oil += t.oil_production
                tech += t.tech_points
                
                # SCIENZIATI PRODUCONO TECNOLOGIA!
                for unit in t.units:
                    if unit.type == "scienziato":
                        tech += UNIT_STATS["scienziato"].get("tech_production", 10)
                        scientists_count += 1
                
                # Avanza sviluppo territorio
                if t.advance_development():
                    upgraded_count += 1
                
                # Invecchia unità
                t.age_all_units()
        
        FACTIONS[self.current_faction]["money"] += income
        FACTIONS[self.current_faction]["oil"] += oil
        FACTIONS[self.current_faction]["tech"] += tech
        
        msg = f"{FACTIONS[self.current_faction]['name']} +${income} +{oil}P +{tech}T"
        if scientists_count > 0:
            msg += f" | {scientists_count}🔬"
        if upgraded_count > 0:
            msg += f" | {upgraded_count} sviluppati!"
        
        self.show_message(msg)
        
        # Prossima fazione
        self.current_faction_idx = (self.current_faction_idx + 1) % len(self.faction_order)
        self.current_faction = self.faction_order[self.current_faction_idx]
        
        # ANNUNCIO VOCALE TURNO
        faction_name = FACTIONS[self.current_faction]['name']
        self.voice.announce_turn(faction_name)
        
        if self.current_faction_idx == 0:
            self.turn += 1
        
        self.mode = "select"
        if self.selected:
            self.selected.selected = False
        self.selected = None
        
        # RESET timer turno
        self.seconds_in_turn = 0
        self.resource_timer = 0
        
        # APRI CONSOLE se è turno umano
        if self.current_faction == self.human_faction:
            self.command_console = CommandConsole(
                self.current_faction,
                self.territories,
                FACTIONS,
                self.turn,
                TECH_LEVELS
            )
        
        # Se è turno IA, esegui automaticamente
        if self.current_faction in self.ai_factions:
            pygame.time.set_timer(pygame.USEREVENT + 1, 1500)  # IA agisce dopo 1.5s
        
        # CHECK VITTORIA!
        self.check_victory()
    
    def check_victory(self):
        """Verifica se una fazione ha conquistato il mondo!"""
        if self.victory_faction:
            return  # Già vinto
        
        # Conta territori per fazione
        territory_count = {}
        for faction_id in self.faction_order:
            territory_count[faction_id] = 0
        
        for t in self.territories:
            if t.owner in territory_count:
                territory_count[t.owner] += 1
        
        # Check se qualcuno ha TUTTO
        total_territories = len(self.territories)
        for faction_id, count in territory_count.items():
            if count == total_territories:
                # VITTORIA!
                self.victory_faction = faction_id
                self.victory_stats = {
                    "turni": self.turn,
                    "territori": count,
                    "money": FACTIONS[faction_id]["money"],
                    "oil": FACTIONS[faction_id]["oil"],
                    "tech": FACTIONS[faction_id]["tech"],
                    "nome": FACTIONS[faction_id]["name"]
                }
                print(f"\n{'='*70}")
                print(f"VITTORIA! {FACTIONS[faction_id]['name']} HA CONQUISTATO IL MONDO!")
                print(f"Turni totali: {self.turn}")
                print(f"{'='*70}\n")
                
                # Annuncio vocale
                self.voice.announce_conquest(f"IL MONDO - {FACTIONS[faction_id]['name']} VINCE!")
                break
    
    def activate_nuke_mode(self):
        """Attiva modalità lancio nuke"""
        # Check costo
        if FACTIONS[self.current_faction]["money"] < 10000:
            self.show_message("Servono $10,000 per la Bomba Atomica!")
            return
        
        # Paga
        FACTIONS[self.current_faction]["money"] -= 10000
        self.nuke_mode = True
        self.buy_menu = None
        self.show_message("BOMBA ATOMICA PRONTA! Click su bersaglio...")
        print("\n[NUKE] Bomba atomica acquistata! Seleziona bersaglio...")
    
    def save_game(self, slot):
        """Salva la partita nello slot specificato (1-4)"""
        save_data = {
            "turn": self.turn,
            "current_faction_idx": self.current_faction_idx,
            "territories": []
        }
        
        # Salva stato di ogni territorio
        for t in self.territories:
            units_data = [{"type": u.type, "health": u.health} for u in t.units]
            
            territory_data = {
                "id": t.id,
                "owner": t.owner,
                "units": units_data,
                "income": t.income,
                "oil_production": t.oil_production,
                "tech_points": t.tech_points,
                "development_level": t.development_level,
                "bunkers": t.bunkers,
                "towers": t.towers,
                "fortress": t.fortress
            }
            save_data["territories"].append(territory_data)
        
        # Salva risorse fazioni
        save_data["factions"] = {}
        for faction_id, faction_data in FACTIONS.items():
            save_data["factions"][faction_id] = {
                "money": faction_data["money"],
                "oil": faction_data["oil"],
                "tech": faction_data["tech"]
            }
        
        # Salva su file
        filename = f"save_slot_{slot}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2)
        
        self.show_message(f"Partita salvata in SLOT {slot}!")
        print(f"[SAVE] Partita salvata: {filename}")
    
    def load_game(self, slot):
        """Carica la partita dallo slot specificato (1-4)"""
        filename = f"save_slot_{slot}.json"
        
        if not os.path.exists(filename):
            self.show_message(f"SLOT {slot} vuoto!")
            return False
        
        with open(filename, 'r', encoding='utf-8') as f:
            save_data = json.load(f)
        
        # Ripristina turno e fazione
        self.turn = save_data["turn"]
        self.current_faction_idx = save_data["current_faction_idx"]
        self.current_faction = self.faction_order[self.current_faction_idx]
        
        # Ripristina risorse fazioni
        for faction_id, faction_resources in save_data["factions"].items():
            FACTIONS[faction_id]["money"] = faction_resources["money"]
            FACTIONS[faction_id]["oil"] = faction_resources["oil"]
            FACTIONS[faction_id]["tech"] = faction_resources["tech"]
        
        # Ripristina territori
        for territory_data in save_data["territories"]:
            # Trova territorio corrispondente
            territory = self.territories[territory_data["id"]]
            
            # Ripristina owner
            territory.owner = territory_data["owner"]
            
            # Ripristina unità
            territory.units = []
            for unit_data in territory_data["units"]:
                unit = Unit(unit_data["type"])
                unit.health = unit_data["health"]
                territory.units.append(unit)
            
            # Ripristina risorse
            territory.income = territory_data["income"]
            territory.oil_production = territory_data["oil_production"]
            territory.tech_points = territory_data["tech_points"]
            territory.development_level = territory_data["development_level"]
            
            # Ripristina difese
            territory.bunkers = territory_data.get("bunkers", 0)
            territory.towers = territory_data.get("towers", 0)
            territory.fortress = territory_data.get("fortress", 0)
        
        self.show_message(f"Partita caricata da SLOT {slot}!")
        print(f"[LOAD] Partita caricata: {filename}")
        return True
    
    def show_save_menu(self):
        """Mostra menu selezione slot di salvataggio"""
        self.save_load_menu = "save"
        self.show_message("SALVA: Premi 1, 2, 3 o 4 per scegliere slot")
    
    def show_load_menu(self):
        """Mostra menu selezione slot di caricamento"""
        self.save_load_menu = "load"
        self.show_message("CARICA: Premi 1, 2, 3 o 4 per scegliere slot")
    
    def launch_nuke(self, pos):
        """Lancia bomba atomica su posizione"""
        # Trova territorio target
        target = None
        for t in self.territories:
            if t.contains_point(pos[0], pos[1]):
                target = t
                break
        
        if not target:
            self.nuke_mode = False
            return
        
        print(f"\n[NUKE] Lanciata su {target.name}!")
        
        # Trova tutti i territori entro raggio 150 pixel
        nuke_radius = 150
        affected = []
        
        for t in self.territories:
            dist = ((t.x - target.x)**2 + (t.y - target.y)**2) ** 0.5
            if dist <= nuke_radius:
                affected.append(t)
        
        print(f"  [NUKE] {len(affected)} territori colpiti!")
        
        # DISTRUGGE tutto nell'area
        for t in affected:
            # Uccidi tutte le unità
            t.units = []
            
            # RESET sviluppo
            t.reset_development()
            
            # Diventa neutrale
            old_owner = t.owner
            t.owner = None
            
            print(f"    [-] {t.name} DISTRUTTO!")
        
        # Animazione esplosione
        self.nuke_animations.append({
            "x": target.x,
            "y": target.y,
            "radius": 10,
            "max_radius": nuke_radius,
            "alpha": 255
        })
        
        self.nuke_mode = False
        self.show_message(f"[NUKE] {len(affected)} territori distrutti!")
    
    def show_message(self, msg):
        """Mostra messaggio temporaneo"""
        self.message = msg
        self.message_timer = 180
        print(f"[INFO] {msg}")
    
    def get_tech_level(self, faction):
        """Ottieni livello tecnologia"""
        tech_points = FACTIONS[faction]["tech"]
        level = 0
        for i, lvl in enumerate(TECH_LEVELS):
            if tech_points >= lvl["points"]:
                level = i
        return TECH_LEVELS[level]
    
    def show_territory_info(self):
        """Mostra info territorio CON RISORSE"""
        if not self.selected:
            return
        
        t = self.selected
        counts = t.count_units_by_type()
        
        # Bonus tech se è tuo territorio
        tech_bonus_att = 0
        tech_bonus_def = 0
        if t.owner == self.current_faction:
            tech_level = self.get_tech_level(self.current_faction)
            tech_bonus_att = tech_level["bonus_attack"]
            tech_bonus_def = tech_level["bonus_defense"]
        
        att = t.get_total_attack(tech_bonus_att)
        deff = t.get_total_defense(tech_bonus_def)
        
        # Info con sviluppo e portata
        dev_info = f"Sviluppo:{t.development_level}/10" if t.development_level > 0 else "Nuovo"
        range_info = f"Raggio:{t.get_attack_range()}px"
        missile_info = " [MISSILI]" if t.has_missiles() else ""  # Niente emoji!
        msg = f"{t.name}: F:{counts['fanteria']} C:{counts['carro']} A:{counts['aereo']} | ATT:{att} DEF:{deff} | {range_info}{missile_info} | ${t.income} {t.oil_production}P {t.tech_points}T | {dev_info}"
        self.show_message(msg)
    
    def attack(self, attacker, defender):
        """Sistema combattimento con PORTATA PER TIPO UNITÀ"""
        if attacker.owner != self.current_faction:
            self.show_message("Non e' il tuo territorio")
            return
        
        if defender.owner == self.current_faction:
            self.show_message("Non puoi attaccare te stesso")
            return
        
        if len(attacker.units) == 0:
            self.show_message("Nessuna unita per attaccare")
            return
        
        # CALCOLA DISTANZA
        distance = ((attacker.x - defender.x)**2 + (attacker.y - defender.y)**2) ** 0.5
        
        # FILTRA unità per PORTATA - TUTTE LE UNITÀ!
        units_by_range = {
            "fanteria": [],
            "carro": [],
            "aereo": [],
            "bombardiere": [],
            "nuke": [],
            "scienziato": [],
            "artiglieria": [],
            "drone": [],
            "hacker": [],
            "robot": [],
            "supersoldato": []
        }
        
        for unit in attacker.units:
            unit_range = UNIT_STATS.get(unit.type, {}).get("range", 0)
            if distance <= unit_range:
                if unit.type in units_by_range:
                    units_by_range[unit.type].append(unit)
        
        # Conta unità che possono attaccare
        total_units = len(attacker.units)
        attacking_units = sum(len(units) for units in units_by_range.values())
        
        if attacking_units == 0:
            # NESSUNA unità può raggiungere!
            attack_range = attacker.get_attack_range()
            if attacker.has_missiles() and distance > attack_range:
                # Usa missili se disponibili
                self.missile_attack(attacker, defender, distance)
                return
            else:
                self.show_message(f"FUORI PORTATA! Dist:{int(distance)}px (F:100 Art:350 C:200 A:500 D:600 H:∞)")
                return
        
        # Mostra quali unità partecipano
        if attacking_units < total_units:
            excluded = total_units - attacking_units
            msg = f"[!] {excluded} unita FUORI PORTATA! (F:100 Art:350 C:200 A:500 D:600 H:∞)"
            print(f"[INFO] {msg}")
            self.show_message(msg)
        
        # CALCOLA quante unità (di quelle in portata) possono essere rifornite
        oil_per_unit = 20
        oil_available = FACTIONS[attacker.owner]["oil"]
        
        # Unità rifornibili (solo quelle in portata!)
        units_with_fuel = min(attacking_units, oil_available // oil_per_unit)
        
        if units_with_fuel == 0:
            oil_cost = attacking_units * oil_per_unit
            self.show_message(f"Petrolio insufficiente! Servono {oil_cost}P")
            return
        
        # Consuma petrolio per le unità rifornite
        oil_cost = units_with_fuel * oil_per_unit
        oil_used = oil_cost
        FACTIONS[attacker.owner]["oil"] -= oil_used
        
        # Messaggio se attacco parziale per petrolio
        if units_with_fuel < attacking_units:
            print(f"\n[PETROLIO] Solo {units_with_fuel}/{attacking_units} unità in portata rifornite!")
            self.show_message(f"Attacco con {units_with_fuel}/{attacking_units} unità (-{oil_used}P)")
        
        # Salva proprietario originale
        original_defender_owner = defender.owner
        
        # BONUS TECNOLOGIA
        att_tech = self.get_tech_level(attacker.owner)
        def_tech = self.get_tech_level(defender.owner) if defender.owner else TECH_LEVELS[0]
        
        # CALCOLA POTENZA solo dalle unità in portata e rifornite
        attack_power = 0
        units_counted = 0
        
        for unit_type, units in units_by_range.items():
            if units and units_counted < units_with_fuel:
                units_to_add = min(len(units), units_with_fuel - units_counted)
                unit_attack = UNIT_STATS[unit_type]["attack"]
                attack_power += units_to_add * unit_attack * (1 + att_tech["bonus_attack"] / 100)
                units_counted += units_to_add
        
        att_power = int(attack_power)
        def_power = defender.get_total_defense(def_tech["bonus_defense"])
        
        print(f"\n[BATTAGLIA] {attacker.name} vs {defender.name}")
        print(f"  Distanza: {int(distance)}px")
        print(f"  Unità in portata: {attacking_units}/{total_units}")
        print(f"  F:{len(units_by_range['fanteria'])} C:{len(units_by_range['carro'])} A:{len(units_by_range['aereo'])} B:{len(units_by_range.get('bombardiere', []))}")
        print(f"  Unità rifornite: {units_with_fuel}/{attacking_units} (-{oil_used}P)")
        print(f"  Attacco: {att_power} | Difesa: {def_power}")
        
        # ANNUNCIO VOCALE ATTACCO
        self.voice.announce_attack(attacker.name, defender.name)
        
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
            # TERRITORIO CONQUISTATO! PRENDI TUTTE LE RISORSE!
            
            # BONUS immediati dalle risorse del territorio
            money_bonus = defender.income * 3
            oil_bonus = defender.oil_production * 5
            tech_bonus = defender.tech_points * 2
            
            FACTIONS[attacker.owner]["money"] += money_bonus
            FACTIONS[attacker.owner]["oil"] += oil_bonus
            FACTIONS[attacker.owner]["tech"] += tech_bonus
            
            print(f"\n  [CONQUISTA] {defender.name}")
            print(f"  + ${money_bonus} soldi")
            print(f"  + {oil_bonus} petrolio")
            print(f"  + {tech_bonus} punti tech")
            
            # Check upgrade tecnologia
            new_tech_level = self.get_tech_level(attacker.owner)
            if new_tech_level["name"] != TECH_LEVELS[0]["name"]:
                print(f"  [TECH] Livello: {new_tech_level['name']} (+{new_tech_level['bonus_attack']} ATT, +{new_tech_level['bonus_defense']} DEF)")
            
            # Penalità per chi perde
            if original_defender_owner is not None:
                loss = defender.income * 2
                FACTIONS[original_defender_owner]["money"] = max(0, FACTIONS[original_defender_owner]["money"] - loss)
            
            # RESET SVILUPPO quando conquistato!
            old_dev_level = defender.development_level
            defender.reset_development()
            
            if old_dev_level > 0:
                print(f"  [RESET] Sviluppo {old_dev_level} -> 0 (conquistato)")
            
            # Cambia proprietà
            defender.owner = attacker.owner
            
            # ANNUNCIO VOCALE CONQUISTA
            self.voice.announce_conquest(defender.name)
            
            # Sposta metà unità
            half = len(attacker.units) // 2
            for _ in range(half):
                if attacker.units:
                    defender.units.append(attacker.units.pop())
            
            # EFFETTI VISIVI CONQUISTA!
            self.particles.add_conquest_effect(defender.x, defender.y, FACTIONS[attacker.owner]["color"])
            self.particles.add_money_effect(defender.x, defender.y, money_bonus)
            
            # Messaggio
            if attacker.owner == self.human_faction:
                self.show_message(f"[+] {defender.name}! ${money_bonus} {oil_bonus}P {tech_bonus}T")
            else:
                self.show_message(f"[IA] Conquista {defender.name}")
            
            # CHECK VITTORIA dopo conquista!
            self.check_victory()
        else:
            # ANNUNCIO VOCALE DIFESA RIUSCITA
            self.voice.announce_defense(defender.name)
            self.show_message(f"[-{oil_cost}P] Att:-{att_losses} Def:-{def_losses}")
        
        # Animazione battaglia
        self.battle_animations.append(BattleAnimation((attacker.x, attacker.y), (defender.x, defender.y)))
    
    def missile_attack(self, attacker, defender, distance):
        """ATTACCO CON MISSILI a lungo raggio!"""
        print(f"\n[MISSILI] {attacker.name} -> {defender.name} (distanza: {int(distance)})")
        
        # COSTO MAGGIORATO per missili
        total_units = len(attacker.units)
        oil_per_unit = 50  # Missili costano più petrolio!
        oil_available = FACTIONS[attacker.owner]["oil"]
        
        units_with_fuel = min(total_units, oil_available // oil_per_unit)
        
        if units_with_fuel == 0:
            self.show_message("PETROLIO INSUFFICIENTE per missili!")
            return
        
        oil_used = units_with_fuel * oil_per_unit
        FACTIONS[attacker.owner]["oil"] -= oil_used
        
        # POTENZA RIDOTTA a distanza (50% normale)
        att_tech = self.get_tech_level(attacker.owner)
        full_power = attacker.get_total_attack(att_tech["bonus_attack"])
        missile_power = int(full_power * 0.5 * (units_with_fuel / total_units))
        
        def_tech = self.get_tech_level(defender.owner) if defender.owner else TECH_LEVELS[0]
        def_power = defender.get_total_defense(def_tech["bonus_defense"])
        
        print(f"  Potenza missile: {missile_power} vs Difesa: {def_power}")
        
        # Battaglia
        att_losses = max(0, def_power // 10)
        def_losses = max(0, missile_power // 5)
        
        for _ in range(att_losses):
            if attacker.units:
                attacker.units.pop(random.randint(0, len(attacker.units) - 1))
        
        for _ in range(def_losses):
            if defender.units:
                defender.units.pop(random.randint(0, len(defender.units) - 1))
        
        # Conquista se distrutto
        if len(defender.units) == 0:
            old_owner = defender.owner
            defender.owner = attacker.owner
            defender.reset_development()
            
            # Bonus ridotti (attacco a distanza)
            money_bonus = defender.income * 2
            oil_bonus = defender.oil_production * 3
            tech_bonus = defender.tech_points
            
            FACTIONS[attacker.owner]["money"] += money_bonus
            FACTIONS[attacker.owner]["oil"] += oil_bonus
            FACTIONS[attacker.owner]["tech"] += tech_bonus
            
            # Effetti
            self.particles.add_conquest_effect(defender.x, defender.y, FACTIONS[attacker.owner]["color"])
            
            self.show_message(f"[MISSILE] {defender.name} conquistato! +${money_bonus}")
            
            # CHECK VITTORIA dopo conquista missile!
            self.check_victory()
        else:
            self.show_message(f"[MISSILE -{oil_used}P] Att:-{att_losses} Def:-{def_losses}")
        
        # ANIMAZIONE MISSILE
        self.missile_animations.append(MissileAnimation((attacker.x, attacker.y), (defender.x, defender.y)))
    
    def ai_turn(self):
        """Turno dell'IA - DIFFICOLTÀ AUMENTATA"""
        print(f"\n[IA] Turno {FACTIONS[self.current_faction]['name']}")
        
        # 1. BONUS RISORSE IA (più difficile)
        FACTIONS[self.current_faction]["money"] += 500  # Bonus extra
        FACTIONS[self.current_faction]["oil"] += 200    # Petrolio extra
        
        # 2. COMPRA UNITÀ - PIÙ AGGRESSIVO
        my_territories = [t for t in self.territories if t.owner == self.current_faction]
        money = FACTIONS[self.current_faction]["money"]
        
        # Compra in TUTTI i territori principali (non solo 3)
        for terr in my_territories[:7]:  # Primi 7 territori invece di 3
            if money >= 3000:  # Compra bombardiere
                terr.add_unit("bombardiere", self.turn)
                money -= 3000
                self.show_message(f"[IA] {terr.name}: Comprato Bombardiere")
            elif money >= 1500:  # Compra aereo
                terr.add_unit("aereo", self.turn)
                money -= 1500
                self.show_message(f"[IA] {terr.name}: Comprato Aereo")
            elif money >= 500:  # Compra carro
                terr.add_unit("carro", self.turn)
                money -= 500
                self.show_message(f"[IA] {terr.name}: Comprato Carro")
            elif money >= 50:  # Compra fanteria
                terr.add_unit("fanteria", self.turn)
                money -= 50
        
        # Compra anche difese nei territori deboli
        weak_territories = [t for t in my_territories if len(t.units) < 3]
        for terr in weak_territories[:5]:
            if money >= 50:
                terr.add_unit("fanteria", self.turn)
                money -= 50
        
        FACTIONS[self.current_faction]["money"] = money
        
        # 3. ATTACCA MULTIPLI - Più attacchi per turno
        attacks_made = 0
        max_attacks = 3  # Fino a 3 attacchi per turno
        
        for terr in sorted(my_territories, key=lambda t: len(t.units), reverse=True):
            if attacks_made >= max_attacks:
                break
            
            if len(terr.units) < 3:  # Attacca solo se hai almeno 3 unità
                continue
            
            # Trova nemici e ordina per debolezza
            enemies = [t for t in self.territories 
                      if t.owner != self.current_faction and t.owner is not None]
            
            # Priorità: nemici più deboli
            enemies.sort(key=lambda t: len(t.units))
            
            if enemies and random.random() < 0.65:  # 65% chance attacco (era 30%)
                target = enemies[0]  # Attacca il più debole
                
                # Attacca anche se leggermente inferiore (più aggressivo)
                if terr.get_total_attack() > target.get_total_defense() * 0.7:
                    self.show_message(f"[IA] Attacco: {terr.name} -> {target.name}")
                    self.attack(terr, target)
                    attacks_made += 1
        
        # 4. Fine turno automatico dopo 2 secondi
        pygame.time.set_timer(pygame.USEREVENT + 2, 2000)
    
    def run(self):
        """Game loop"""
        running = True
        ai_timer_active = False
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Timer IA
                elif event.type == pygame.USEREVENT + 1:
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Disattiva
                    self.ai_turn()
                
                elif event.type == pygame.USEREVENT + 2:
                    pygame.time.set_timer(pygame.USEREVENT + 2, 0)  # Disattiva
                    self.next_turn()
                
                elif event.type == pygame.KEYDOWN:
                    if self.victory_faction:
                        # Schermo vittoria attivo
                        if event.key == pygame.K_SPACE:
                            # Nuova partita
                            self.__init__()  # Reset completo
                        elif event.key == pygame.K_s:
                            # Salva vittoria
                            self.save_game(1)  # Salva in slot 1
                            self.show_message("Vittoria salvata in SLOT 1!")
                        elif event.key == pygame.K_ESCAPE:
                            running = False
                    elif self.save_load_menu:
                        # Menu SAVE/LOAD attivo - 1,2,3,4 per scegliere slot
                        if event.key == pygame.K_1:
                            if self.save_load_menu == "save":
                                self.save_game(1)
                            else:
                                self.load_game(1)
                            self.save_load_menu = None
                        elif event.key == pygame.K_2:
                            if self.save_load_menu == "save":
                                self.save_game(2)
                            else:
                                self.load_game(2)
                            self.save_load_menu = None
                        elif event.key == pygame.K_3:
                            if self.save_load_menu == "save":
                                self.save_game(3)
                            else:
                                self.load_game(3)
                            self.save_load_menu = None
                        elif event.key == pygame.K_4:
                            if self.save_load_menu == "save":
                                self.save_game(4)
                            else:
                                self.load_game(4)
                            self.save_load_menu = None
                        elif event.key == pygame.K_ESCAPE:
                            self.save_load_menu = None
                            self.show_message("Annullato")
                    elif self.command_console:
                        # Console attiva - SPAZIO o ESC per chiudere, S/L per save/load
                        if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                            self.command_console = None
                        elif event.key == pygame.K_s:
                            # SALVA dalla console
                            self.command_console = None
                            self.show_save_menu()
                        elif event.key == pygame.K_l:
                            # CARICA dalla console
                            self.command_console = None
                            self.show_load_menu()
                    elif self.buy_menu:
                        # Check prima per S/L
                        if event.key == pygame.K_s:
                            self.buy_menu = None
                            self.show_save_menu()
                        elif event.key == pygame.K_l:
                            self.buy_menu = None
                            self.show_load_menu()
                        else:
                            msg = self.buy_menu.handle_key(event.key)
                            if msg == "nuke_mode":
                                self.activate_nuke_mode()
                            elif msg:
                                self.show_message(msg)
                            if not self.buy_menu.active:
                                self.buy_menu = None
                    else:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                        elif event.key == pygame.K_SPACE:
                            # Solo se è turno umano
                            if self.current_faction == self.human_faction:
                                self.next_turn()
                            else:
                                self.show_message("Aspetta il turno dell'IA...")
                        elif event.key == pygame.K_a:
                            self.mode = "attack"
                            self.show_message("Seleziona territorio da attaccare")
                        elif event.key == pygame.K_i:
                            self.show_territory_info()
                        elif event.key == pygame.K_v:
                            # Toggle VOCE
                            status = self.voice.toggle()
                            msg = "Commenti ATTIVI" if status else "Commenti DISATTIVATI"
                            self.show_message(msg)
                        elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:
                            # AUMENTA VOLUME VOCE
                            msg = self.voice.volume_up()
                            self.show_message(msg)
                        elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                            # DIMINUISCI VOLUME VOCE
                            msg = self.voice.volume_down()
                            self.show_message(msg)
                        elif event.key == pygame.K_LEFTBRACKET or event.key == pygame.K_RIGHTBRACKET:
                            # VELOCITÀ VOCE
                            if event.key == pygame.K_LEFTBRACKET:
                                msg = self.voice.speed_down()
                            else:
                                msg = self.voice.speed_up()
                            self.show_message(msg)
                        elif event.key == pygame.K_F11:
                            # Toggle FULLSCREEN
                            self.fullscreen = not self.fullscreen
                            if self.fullscreen:
                                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                                self.show_message("SCHERMO INTERO ATTIVO (F11 per uscire)")
                            else:
                                self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                                self.show_message("FINESTRA NORMALE (F11 per schermo intero)")
                        elif event.key == pygame.K_s:
                            # SALVA PARTITA (chiudi console prima)
                            if self.command_console:
                                self.command_console = None
                            if self.buy_menu:
                                self.buy_menu = None
                            self.show_save_menu()
                        elif event.key == pygame.K_l:
                            # CARICA PARTITA (chiudi console prima)
                            if self.command_console:
                                self.command_console = None
                            if self.buy_menu:
                                self.buy_menu = None
                            self.show_load_menu()
                        elif event.key == pygame.K_n:
                            # Tasto scorciatoia per NUKE
                            if FACTIONS[self.current_faction]["money"] >= 10000:
                                self.activate_nuke_mode()
                            else:
                                self.show_message("Servono $10,000 per Nuke!")
                        
                        elif event.key == pygame.K_ESCAPE:
                            # Chiudi menu/console
                            if self.buy_menu:
                                self.buy_menu = None
                            elif self.command_console:
                                self.command_console = None
                            elif self.nuke_mode:
                                self.nuke_mode = False
                                self.show_message("Nuke cancellata")
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Console comando - check drag o click su pulsante
                        if self.command_console:
                            # Prima controlla se inizia drag
                            if not self.command_console.handle_mouse_down(event.pos):
                                # Se non è drag, controlla click sul bottone
                                if self.command_console.handle_click(event.pos):
                                    self.command_console = None
                        # Solo se è turno umano
                        elif self.current_faction != self.human_faction:
                            self.show_message("Non e' il tuo turno!")
                        elif self.buy_menu:
                            # Check prima se clicco su un PULSANTE del menu
                            msg = self.buy_menu.handle_click_button(event.pos)
                            if msg == "nuke_mode":
                                self.activate_nuke_mode()
                            elif msg:
                                self.show_message(msg)
                            # Altrimenti check se clicco sulla barra titolo per trascinare
                            elif self.buy_menu.in_title_bar(event.pos[0], event.pos[1]):
                                self.buy_menu.start_drag(event.pos[0], event.pos[1])
                        elif self.nuke_mode:
                            # Lancia nuke su target
                            self.launch_nuke(event.pos)
                        else:
                            self.handle_click(event.pos)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        # Console comando - ferma drag
                        if self.command_console:
                            self.command_console.handle_mouse_up(event.pos)
                        # Buy menu - ferma drag
                        if self.buy_menu:
                            self.buy_menu.stop_drag()
                
                elif event.type == pygame.MOUSEMOTION:
                    # Console comando - aggiorna posizione durante drag
                    if self.command_console:
                        self.command_console.handle_mouse_motion(event.pos)
                    # Buy menu - aggiorna posizione durante drag
                    if self.buy_menu and self.buy_menu.dragging:
                        self.buy_menu.update_position(event.pos[0], event.pos[1])
            
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()
    
    def handle_click(self, pos):
        """Click handler - Trova territorio PIÙ VICINO al click"""
        clicked = None
        min_distance = float('inf')
        
        # Trova tutti i territori sotto il click e scegli il più vicino
        for t in self.territories:
            if t.contains_point(pos[0], pos[1]):
                # Calcola distanza dal centro del territorio
                distance = math.hypot(pos[0] - t.x, pos[1] - t.y)
                if distance < min_distance:
                    min_distance = distance
                    clicked = t
        
        if not clicked:
            return
        
        if self.mode == "select":
            if self.selected:
                self.selected.selected = False
            self.selected = clicked
            clicked.selected = True
            self.show_territory_info()
            
            # APRI ARMERIA AUTOMATICAMENTE se è tuo territorio
            if clicked.owner == self.current_faction:
                self.buy_menu = BuyMenu(clicked, self.current_faction, self.turn)
        
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
        
        # Territori con grafica migliorata
        gfx = GraphicsEnhancer()
        for t in self.territories:
            t.draw(self.screen, self.font_small, gfx)
        
        # Animazioni battaglie
        self.draw_battle_animations()
        
        # Animazioni MISSILI
        self.draw_missile_animations()
        
        # Animazioni NUKE
        self.draw_nuke_animations()
        
        # Sistema particelle
        self.particles.update()
        self.particles.draw(self.screen, self.font_small)
        
        # UI
        self.draw_ui()
        
        # Menu acquisto
        if self.buy_menu:
            self.buy_menu.draw(self.screen, self.font, self.font_small)
        
        # CONSOLE DI COMANDO (ma SOTTO menu save/load!)
        if self.command_console and not self.save_load_menu:
            self.command_console.draw(self.screen, self.font, self.font_small, 
                                     self.font_large, self.font_title)
        
        # Cursore NUKE
        if self.nuke_mode and not self.command_console and not self.save_load_menu:
            mouse_pos = pygame.mouse.get_pos()
            # Cerchio rosso lampeggiante
            pygame.draw.circle(self.screen, (255, 0, 0), mouse_pos, 150, 3)
            pygame.draw.circle(self.screen, (255, 255, 0), mouse_pos, 5)
            
            nuke_text = self.font_small.render("ZONA IMPATTO", True, (255, 0, 0))
            self.screen.blit(nuke_text, (mouse_pos[0] - 40, mouse_pos[1] - 170))
        
        # Menu SAVE/LOAD
        if self.save_load_menu:
            # Overlay scuro
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))
            
            # Box centrale
            box_width = 600
            box_height = 400
            box_x = (SCREEN_WIDTH - box_width) // 2
            box_y = (SCREEN_HEIGHT - box_height) // 2
            
            # Sfondo con gradiente
            bg = pygame.Surface((box_width, box_height))
            bg.fill((20, 30, 50))
            self.screen.blit(bg, (box_x, box_y))
            
            # Bordo
            pygame.draw.rect(self.screen, (255, 200, 50), (box_x, box_y, box_width, box_height), 4)
            pygame.draw.rect(self.screen, (100, 150, 255), (box_x+4, box_y+4, box_width-8, box_height-8), 2)
            
            # Titolo
            title = "SALVA PARTITA" if self.save_load_menu == "save" else "CARICA PARTITA"
            title_text = self.font_title.render(title, True, (255, 255, 100))
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, box_y + 50))
            self.screen.blit(title_text, title_rect)
            
            # Slot buttons
            slot_y = box_y + 120
            for i in range(1, 5):
                slot_text = f"SLOT {i}"
                
                # Check se esiste salvataggio
                save_exists = os.path.exists(f"save_slot_{i}.json")
                if save_exists and self.save_load_menu == "load":
                    slot_text += " [OCCUPATO]"
                    color = (100, 255, 100)
                elif save_exists and self.save_load_menu == "save":
                    slot_text += " [SOVRASCRIVI]"
                    color = (255, 200, 100)
                else:
                    slot_text += " [VUOTO]"
                    color = (150, 150, 150)
                
                # Button
                btn_width = 500
                btn_height = 50
                btn_x = (SCREEN_WIDTH - btn_width) // 2
                btn_y = slot_y + (i - 1) * 70
                
                # Sfondo button
                pygame.draw.rect(self.screen, (50, 60, 80), (btn_x, btn_y, btn_width, btn_height))
                pygame.draw.rect(self.screen, color, (btn_x, btn_y, btn_width, btn_height), 3)
                
                # Testo
                text = self.font_large.render(slot_text, True, color)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, btn_y + 25))
                self.screen.blit(text, text_rect)
                
                # Numero tasto
                key_text = self.font.render(f"[{i}]", True, (255, 255, 255))
                self.screen.blit(key_text, (btn_x - 50, btn_y + 15))
            
            # Istruzioni
            help_text = "Premi 1, 2, 3 o 4 per scegliere - ESC per annullare"
            help_surf = self.font.render(help_text, True, (200, 200, 200))
            help_rect = help_surf.get_rect(center=(SCREEN_WIDTH // 2, box_y + box_height - 40))
            self.screen.blit(help_surf, help_rect)
        
        # SCHERMO VITTORIA (sopra TUTTO!)
        if self.victory_faction:
            # Overlay scuro completo
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            self.screen.blit(overlay, (0, 0))
            
            # Box vittoria GRANDE
            box_width = 800
            box_height = 500
            box_x = (SCREEN_WIDTH - box_width) // 2
            box_y = (SCREEN_HEIGHT - box_height) // 2
            
            # Sfondo con colore fazione
            faction_color = FACTIONS[self.victory_faction]["color"]
            bg = pygame.Surface((box_width, box_height))
            bg.fill((20, 25, 35))
            self.screen.blit(bg, (box_x, box_y))
            
            # Bordo colorato con colore fazione
            pygame.draw.rect(self.screen, faction_color, (box_x, box_y, box_width, box_height), 8)
            pygame.draw.rect(self.screen, (255, 255, 100), (box_x+8, box_y+8, box_width-16, box_height-16), 3)
            
            # TITOLO VITTORIA (pulsante)
            pulse = abs(math.sin(pygame.time.get_ticks() / 500)) * 0.3 + 0.7
            title_size = int(56 * pulse)
            title_font = pygame.font.Font(None, title_size)
            title_text = title_font.render("VITTORIA!", True, (255, 255, 100))
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, box_y + 60))
            
            # Glow dietro titolo
            for offset in range(3, 0, -1):
                glow_color = (255, 255, 100, 100 - offset * 30)
                glow_surf = title_font.render("VITTORIA!", True, glow_color[:3])
                glow_rect = glow_surf.get_rect(center=(SCREEN_WIDTH // 2 + offset, box_y + 60 + offset))
                self.screen.blit(glow_surf, glow_rect)
            
            self.screen.blit(title_text, title_rect)
            
            # Nome fazione vincitrice
            winner_text = self.font_title.render(self.victory_stats["nome"], True, faction_color)
            winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, box_y + 120))
            self.screen.blit(winner_text, winner_rect)
            
            # Sottotitolo
            subtitle = self.font_large.render("HA CONQUISTATO IL MONDO!", True, (200, 200, 255))
            subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, box_y + 160))
            self.screen.blit(subtitle, subtitle_rect)
            
            # Separatore
            pygame.draw.line(self.screen, (100, 150, 200), 
                           (box_x + 50, box_y + 200), 
                           (box_x + box_width - 50, box_y + 200), 3)
            
            # STATISTICHE FINALI
            stats_y = box_y + 230
            stats_lines = [
                f"TURNI TOTALI: {self.victory_stats['turni']}",
                f"TERRITORI CONQUISTATI: {self.victory_stats['territori']}/{len(self.territories)}",
                f"DENARO FINALE: ${self.victory_stats['money']:,}",
                f"PETROLIO FINALE: {self.victory_stats['oil']:,}P",
                f"TECNOLOGIA FINALE: {self.victory_stats['tech']:,}T"
            ]
            
            for i, line in enumerate(stats_lines):
                stat_text = self.font.render(line, True, (255, 255, 255))
                stat_rect = stat_text.get_rect(center=(SCREEN_WIDTH // 2, stats_y + i * 35))
                
                # Sfondo per stat
                stat_bg = stat_rect.inflate(20, 10)
                pygame.draw.rect(self.screen, (40, 50, 70), stat_bg)
                pygame.draw.rect(self.screen, faction_color, stat_bg, 2)
                
                self.screen.blit(stat_text, stat_rect)
            
            # Messaggio finale
            congrats = self.font_large.render("COMPLIMENTI!", True, (255, 255, 100))
            congrats_rect = congrats.get_rect(center=(SCREEN_WIDTH // 2, box_y + 420))
            self.screen.blit(congrats, congrats_rect)
            
            # Istruzioni
            help_text = "SPAZIO = Nuova partita | S = Salva vittoria | ESC = Esci"
            help_surf = self.font.render(help_text, True, (200, 200, 200))
            help_rect = help_surf.get_rect(center=(SCREEN_WIDTH // 2, box_y + box_height - 30))
            self.screen.blit(help_surf, help_rect)
        
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
    
    def draw_battle_animations(self):
        """Disegna animazioni battaglie"""
        to_remove = []
        
        for i, anim in enumerate(self.battle_animations):
            anim.update()
            anim.draw(self.screen)
            
            if not anim.active:
                to_remove.append(i)
        
        for i in reversed(to_remove):
            self.battle_animations.pop(i)
    
    def draw_missile_animations(self):
        """Disegna animazioni missili"""
        to_remove = []
        
        for i, anim in enumerate(self.missile_animations):
            anim.update()
            anim.draw(self.screen)
            
            if not anim.active:
                to_remove.append(i)
        
        for i in reversed(to_remove):
            self.missile_animations.pop(i)
    
    def draw_nuke_animations(self):
        """Disegna esplosioni nucleari"""
        to_remove = []
        
        for i, anim in enumerate(self.nuke_animations):
            # Espandi cerchio
            anim["radius"] += 8
            anim["alpha"] -= 8
            
            if anim["alpha"] <= 0 or anim["radius"] > anim["max_radius"]:
                to_remove.append(i)
                continue
            
            # Disegna esplosione
            s = pygame.Surface((anim["radius"] * 2, anim["radius"] * 2), pygame.SRCALPHA)
            
            # Cerchi concentrici rosso-arancio
            pygame.draw.circle(s, (255, 100, 0, min(255, anim["alpha"])), 
                             (anim["radius"], anim["radius"]), anim["radius"])
            pygame.draw.circle(s, (255, 200, 0, min(255, anim["alpha"] // 2)), 
                             (anim["radius"], anim["radius"]), anim["radius"] // 2)
            pygame.draw.circle(s, (255, 255, 255, min(255, anim["alpha"] // 3)), 
                             (anim["radius"], anim["radius"]), anim["radius"] // 4)
            
            self.screen.blit(s, (anim["x"] - anim["radius"], anim["y"] - anim["radius"]))
        
        # Rimuovi finite
        for i in reversed(to_remove):
            self.nuke_animations.pop(i)
    
    def draw_ui(self):
        """UI con TIMER"""
        panel = pygame.Surface((SCREEN_WIDTH, 100))
        panel.set_alpha(230)
        panel.fill((20, 20, 40))
        self.screen.blit(panel, (0, 0))
        
        # Turno con indicatore PC/Umano
        faction_name = FACTIONS[self.current_faction]["name"]
        faction_color = FACTIONS[self.current_faction]["color"]
        
        if self.current_faction == self.human_faction:
            turn_text = self.font_large.render(f"TURNO {self.turn}: {faction_name} (TU)", True, faction_color)
        else:
            turn_text = self.font_large.render(f"TURNO {self.turn}: {faction_name} (PC)", True, faction_color)
        
        self.screen.blit(turn_text, (20, 15))
        
        # Timer turno (conta secondi)
        self.resource_timer += 1
        if self.resource_timer >= 60:
            self.resource_timer = 0
            self.seconds_in_turn += 1
        
        timer_text = self.font_small.render(f"Tempo: {self.seconds_in_turn}s", True, (200, 200, 200))
        self.screen.blit(timer_text, (350, 20))
        
        # 3 RISORSE
        money = FACTIONS[self.current_faction]["money"]
        oil = FACTIONS[self.current_faction]["oil"]
        tech = FACTIONS[self.current_faction]["tech"]
        tech_level = self.get_tech_level(self.current_faction)
        
        res_text = self.font.render(f"${money} | {oil}P | {tech}T ({tech_level['name']})", True, (255, 255, 100))
        self.screen.blit(res_text, (20, 55))
        
        # Indicatore produzione prevista prossimo turno
        income_next = sum(t.income for t in self.territories if t.owner == self.current_faction)
        oil_next = sum(t.oil_production for t in self.territories if t.owner == self.current_faction)
        tech_next = sum(t.tech_points for t in self.territories if t.owner == self.current_faction)
        
        next_text = self.font_small.render(
            f"Prossimo turno: +${income_next} +{oil_next}P +{tech_next}T",
            True, (150, 255, 150)
        )
        self.screen.blit(next_text, (20, 78))
        
        # Territori
        x_offset = 400
        for faction in self.faction_order:
            count = sum(1 for t in self.territories if t.owner == faction)
            color = FACTIONS[faction]["color"]
            text = self.font_small.render(f"{FACTIONS[faction]['name'][:3]}: {count}", True, color)
            self.screen.blit(text, (x_offset, 25))
            x_offset += 80
        
        # Istruzioni
        if self.nuke_mode:
            inst = self.font.render("[!] CLICK per LANCIARE NUKE! [!]", True, (255, 0, 0))
            self.screen.blit(inst, (450, 55))
        else:
            inst = self.font_small.render("Click=Armeria | A=Attacco | N=NUKE | I=Info | SPAZIO=Fine", 
                                         True, (200, 200, 200))
            self.screen.blit(inst, (400, 60))
        
        # INDICATORE VOLUME VOCE (angolo in alto a destra)
        vol_x = SCREEN_WIDTH - 180
        vol_y = 10
        
        # Icona voce
        voice_icon = "🔊" if self.voice.enabled else "🔇"
        voice_text = self.font.render(voice_icon, True, (255, 255, 255))
        self.screen.blit(voice_text, (vol_x, vol_y))
        
        # Barra volume
        if self.voice.enabled:
            bar_x = vol_x + 30
            bar_y = vol_y + 8
            bar_width = 120
            bar_height = 12
            
            # Sfondo barra
            pygame.draw.rect(self.screen, (40, 40, 60), (bar_x, bar_y, bar_width, bar_height))
            
            # Riempimento barra
            fill_width = int(bar_width * self.voice.volume)
            pygame.draw.rect(self.screen, (100, 255, 100), (bar_x, bar_y, fill_width, bar_height))
            
            # Bordo
            pygame.draw.rect(self.screen, (150, 150, 200), (bar_x, bar_y, bar_width, bar_height), 1)
            
            # Percentuale
            perc_text = self.font_small.render(f"{int(self.voice.volume * 100)}%", True, (255, 255, 255))
            self.screen.blit(perc_text, (bar_x + bar_width + 5, bar_y - 2))
            
            # Help tasti
            help_vol = self.font_small.render("+/- Volume", True, (180, 180, 180))
            self.screen.blit(help_vol, (vol_x + 30, vol_y + 25))

if __name__ == "__main__":
    game = Game()
    game.run()

