"""
Effetti Visivi Avanzati
Particelle, transizioni, animazioni
"""

import pygame
import math
import random

class ParticleSystem:
    """Sistema particellare completo"""
    
    def __init__(self):
        self.particles = []
    
    def add_conquest_effect(self, x, y, color):
        """Effetto conquista territorio"""
        # Esplosione stelle
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 10)
            
            self.particles.append({
                "type": "star",
                "x": x,
                "y": y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "color": color,
                "size": random.randint(2, 5),
                "lifetime": random.randint(40, 80),
                "max_lifetime": 80,
                "rotation": random.uniform(0, 360)
            })
    
    def add_upgrade_effect(self, x, y):
        """Effetto upgrade tecnologia"""
        # Particelle dorate che salgono
        for _ in range(15):
            self.particles.append({
                "type": "tech",
                "x": x + random.randint(-20, 20),
                "y": y,
                "vx": random.uniform(-1, 1),
                "vy": -random.uniform(2, 5),
                "color": (255, 215, 0),
                "size": random.randint(2, 4),
                "lifetime": random.randint(50, 100),
                "max_lifetime": 100
            })
    
    def add_money_effect(self, x, y, amount):
        """Effetto guadagno soldi"""
        # Simboli $ che salgono
        self.particles.append({
            "type": "money",
            "x": x,
            "y": y,
            "vx": random.uniform(-0.5, 0.5),
            "vy": -3,
            "color": (100, 255, 100),
            "text": f"+${amount}",
            "lifetime": 60,
            "max_lifetime": 60
        })
    
    def update(self):
        """Aggiorna tutte le particelle"""
        to_remove = []
        
        for i, p in enumerate(self.particles):
            # Movimento
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            
            # Fisica
            if p["type"] == "star":
                p["vy"] += 0.4  # Gravità
                p["vx"] *= 0.98  # Friction
                p["vy"] *= 0.98
                p["rotation"] += 10
            elif p["type"] == "tech":
                p["vx"] *= 0.95
            
            # Lifetime
            p["lifetime"] -= 1
            if p["lifetime"] <= 0:
                to_remove.append(i)
        
        # Rimuovi
        for i in reversed(to_remove):
            self.particles.pop(i)
    
    def draw(self, surface, font_small=None):
        """Disegna tutte le particelle"""
        for p in self.particles:
            alpha = int(255 * (p["lifetime"] / p["max_lifetime"]))
            
            if p["type"] == "star":
                # Stella rotante
                size = p["size"]
                s = pygame.Surface((size * 3, size * 3), pygame.SRCALPHA)
                
                # Disegna stella
                center = size * 1.5
                points = []
                for i in range(5):
                    angle = math.radians(p["rotation"] + i * 72)
                    px = center + math.cos(angle) * size * 1.5
                    py = center + math.sin(angle) * size * 1.5
                    points.append((px, py))
                    
                    # Punti interni
                    angle_inner = math.radians(p["rotation"] + i * 72 + 36)
                    px_inner = center + math.cos(angle_inner) * size * 0.6
                    py_inner = center + math.sin(angle_inner) * size * 0.6
                    points.append((px_inner, py_inner))
                
                if len(points) >= 3:
                    pygame.draw.polygon(s, (*p["color"], alpha), points)
                
                surface.blit(s, (int(p["x"]) - size * 1.5, int(p["y"]) - size * 1.5))
            
            elif p["type"] == "tech":
                # Cerchietto tech
                pygame.draw.circle(surface, (*p["color"], alpha), 
                                 (int(p["x"]), int(p["y"])), p["size"])
                pygame.draw.circle(surface, (255, 255, 255, alpha), 
                                 (int(p["x"]), int(p["y"])), p["size"], 1)
            
            elif p["type"] == "money" and font_small:
                # Testo
                text = font_small.render(p["text"], True, (*p["color"], alpha))
                surface.blit(text, (int(p["x"]), int(p["y"])))

class ScreenTransition:
    """Transizioni schermo"""
    
    @staticmethod
    def fade_in(surface, alpha_start=255):
        """Fade in schermo"""
        fade = pygame.Surface((1400, 800))
        fade.fill((0, 0, 0))
        fade.set_alpha(alpha_start)
        surface.blit(fade, (0, 0))
    
    @staticmethod
    def slide_panel(surface, panel_surface, target_x, current_x, speed=30):
        """Pannello che scivola"""
        new_x = current_x
        if current_x < target_x:
            new_x = min(target_x, current_x + speed)
        elif current_x > target_x:
            new_x = max(target_x, current_x - speed)
        
        return new_x

