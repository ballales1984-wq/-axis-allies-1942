"""
Sistema Grafico Migliorato
Effetti visivi professionali per il gioco
"""

import pygame
import math
import random

class GraphicsEnhancer:
    """Migliora la grafica del gioco"""
    
    @staticmethod
    def draw_glowing_circle(surface, center, radius, color, glow_intensity=3):
        """Disegna cerchio con effetto GLOW"""
        x, y = center
        
        # Cerchi concentrici per effetto glow
        for i in range(glow_intensity, 0, -1):
            alpha = 80 // i
            glow_radius = radius + i * 2
            
            s = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            glow_color = (*color[:3], alpha)
            pygame.draw.circle(s, glow_color, (glow_radius, glow_radius), glow_radius)
            surface.blit(s, (x - glow_radius, y - glow_radius))
        
        # Cerchio principale
        pygame.draw.circle(surface, color, center, radius)
    
    @staticmethod
    def draw_gradient_circle(surface, center, radius, color_inner, color_outer):
        """Cerchio con gradiente radiale"""
        x, y = center
        
        # Crea superficie temporanea
        s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        
        # Disegna cerchi concentrici con gradiente
        steps = 10
        for i in range(steps, 0, -1):
            # Interpola colori
            t = i / steps
            r = int(color_inner[0] * t + color_outer[0] * (1 - t))
            g = int(color_inner[1] * t + color_outer[1] * (1 - t))
            b = int(color_inner[2] * t + color_outer[2] * (1 - t))
            
            current_radius = int(radius * i / steps)
            pygame.draw.circle(s, (r, g, b), (radius, radius), current_radius)
        
        surface.blit(s, (x - radius, y - radius))
    
    @staticmethod
    def draw_pulsing_circle(surface, center, radius, color, time_offset=0):
        """Cerchio pulsante (respira)"""
        # Calcola pulsazione
        pulse = math.sin(pygame.time.get_ticks() / 500 + time_offset) * 0.2 + 1
        pulsed_radius = int(radius * pulse)
        
        # Glow pulsante
        GraphicsEnhancer.draw_glowing_circle(surface, center, pulsed_radius, color, 4)
    
    @staticmethod
    def draw_shiny_button(surface, rect, color, is_hover=False, text="", font=None):
        """Pulsante con effetto shiny"""
        x, y, w, h = rect
        
        # Sfondo con gradiente
        for i in range(h):
            # Gradiente verticale
            t = i / h
            if is_hover:
                brightness = 1.3 - t * 0.3
            else:
                brightness = 1.0 - t * 0.3
            
            r = min(255, int(color[0] * brightness))
            g = min(255, int(color[1] * brightness))
            b = min(255, int(color[2] * brightness))
            
            pygame.draw.line(surface, (r, g, b), (x, y + i), (x + w, y + i))
        
        # Highlight superiore
        highlight = pygame.Surface((w - 20, 3), pygame.SRCALPHA)
        highlight.fill((255, 255, 255, 100))
        surface.blit(highlight, (x + 10, y + 5))
        
        # Bordo
        border_color = (255, 255, 255) if is_hover else (150, 150, 150)
        pygame.draw.rect(surface, border_color, (x, y, w, h), 3)
        
        # Testo centrato
        if text and font:
            text_surf = font.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(x + w//2, y + h//2))
            surface.blit(text_surf, text_rect)
    
    @staticmethod
    def create_particle_explosion(x, y, color, particle_count=20):
        """Crea particelle per esplosione"""
        particles = []
        for _ in range(particle_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            lifetime = random.randint(30, 60)
            
            particles.append({
                "x": x,
                "y": y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "color": color,
                "lifetime": lifetime,
                "max_lifetime": lifetime
            })
        return particles
    
    @staticmethod
    def update_particles(particles):
        """Aggiorna particelle"""
        to_remove = []
        
        for i, p in enumerate(particles):
            # Movimento
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            
            # Gravità
            p["vy"] += 0.3
            
            # Friction
            p["vx"] *= 0.98
            p["vy"] *= 0.98
            
            # Lifetime
            p["lifetime"] -= 1
            if p["lifetime"] <= 0:
                to_remove.append(i)
        
        # Rimuovi morte
        for i in reversed(to_remove):
            particles.pop(i)
    
    @staticmethod
    def draw_particles(surface, particles):
        """Disegna particelle"""
        for p in particles:
            # Alpha basato su lifetime
            alpha = int(255 * (p["lifetime"] / p["max_lifetime"]))
            size = max(1, int(3 * (p["lifetime"] / p["max_lifetime"])))
            
            # Disegna
            s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*p["color"], alpha), (size, size), size)
            surface.blit(s, (int(p["x"]) - size, int(p["y"]) - size))

class UnitIcon:
    """Icone belle per unità"""
    
    @staticmethod
    def draw_infantry_icon(surface, x, y, size=12, color=(255, 255, 255)):
        """Icona fanteria stilizzata"""
        # Corpo (rettangolo)
        body_rect = pygame.Rect(x - size//4, y - size//3, size//2, size//2)
        pygame.draw.rect(surface, color, body_rect)
        
        # Testa (cerchio)
        pygame.draw.circle(surface, color, (x, y - size//2), size//4)
        
        # Fucile (linea)
        pygame.draw.line(surface, color, (x, y), (x + size//2, y - size//4), 2)
    
    @staticmethod
    def draw_tank_icon(surface, x, y, size=14, color=(255, 255, 255)):
        """Icona carro armato stilizzato"""
        # Corpo carro
        body = pygame.Rect(x - size//2, y - size//4, size, size//2)
        pygame.draw.rect(surface, color, body)
        
        # Torre
        turret = pygame.Rect(x - size//4, y - size//2, size//2, size//3)
        pygame.draw.rect(surface, color, turret)
        
        # Cannone
        pygame.draw.rect(surface, color, (x + size//4, y - size//3, size//2, 3))
    
    @staticmethod
    def draw_plane_icon(surface, x, y, size=14, color=(255, 255, 255)):
        """Icona aereo stilizzato"""
        # Fusoliera
        points = [
            (x + size//2, y),  # Punta
            (x - size//2, y - size//6),  # Ala su
            (x - size//2, y + size//6),  # Ala giù
        ]
        pygame.draw.polygon(surface, color, points)
        
        # Ali
        pygame.draw.line(surface, color, (x - size//4, y - size//3), (x - size//4, y + size//3), 3)

class BattleAnimation:
    """Animazioni per battaglie"""
    
    def __init__(self, attacker_pos, defender_pos):
        self.start_x, self.start_y = attacker_pos
        self.end_x, self.end_y = defender_pos
        self.progress = 0
        self.max_progress = 30
        self.active = True
        
        # Proiettili
        self.projectiles = []
        for _ in range(5):
            self.projectiles.append({
                "delay": random.randint(0, 15),
                "fired": False
            })
    
    def update(self):
        """Aggiorna animazione"""
        self.progress += 1
        if self.progress >= self.max_progress:
            self.active = False
    
    def draw(self, surface):
        """Disegna animazione battaglia"""
        if not self.active:
            return
        
        # Linea tratteggiata tra territori
        segments = 10
        for i in range(segments):
            if i % 2 == 0:
                start_x = self.start_x + (self.end_x - self.start_x) * i / segments
                start_y = self.start_y + (self.end_y - self.start_y) * i / segments
                end_x = self.start_x + (self.end_x - self.start_x) * (i + 1) / segments
                end_y = self.start_y + (self.end_y - self.start_y) * (i + 1) / segments
                
                pygame.draw.line(surface, (255, 100, 100), 
                               (int(start_x), int(start_y)), 
                               (int(end_x), int(end_y)), 3)
        
        # Proiettili
        for proj in self.projectiles:
            if self.progress > proj["delay"] and not proj["fired"]:
                proj["fired"] = True
                proj["t"] = 0
            
            if proj.get("fired"):
                proj["t"] += 0.05
                if proj["t"] <= 1:
                    # Posizione interpolata
                    px = self.start_x + (self.end_x - self.start_x) * proj["t"]
                    py = self.start_y + (self.end_y - self.start_y) * proj["t"]
                    
                    # Disegna proiettile
                    pygame.draw.circle(surface, (255, 255, 0), (int(px), int(py)), 4)
                    pygame.draw.circle(surface, (255, 100, 0), (int(px), int(py)), 2)

def create_territory_sprite(radius, color, development_level=0):
    """Crea sprite migliorato per territorio"""
    size = radius * 4
    sprite = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    
    # Glow esterno (più grande se sviluppato)
    glow_layers = 3 + development_level // 3
    for i in range(glow_layers, 0, -1):
        alpha = 40 // i
        glow_radius = radius + i * 2
        glow_color = (*color, alpha)
        pygame.draw.circle(sprite, glow_color, (center, center), glow_radius)
    
    # Gradiente radiale
    for i in range(radius, 0, -1):
        t = i / radius
        # Colore più chiaro al centro
        r = min(255, int(color[0] + (255 - color[0]) * (1 - t) * 0.3))
        g = min(255, int(color[1] + (255 - color[1]) * (1 - t) * 0.3))
        b = min(255, int(color[2] + (255 - color[2]) * (1 - t) * 0.3))
        
        pygame.draw.circle(sprite, (r, g, b), (center, center), i)
    
    # Bordo brillante
    pygame.draw.circle(sprite, (255, 255, 255, 200), (center, center), radius, 1)
    
    # Highlight (riflesso luce)
    highlight_pos = (center - radius//3, center - radius//3)
    pygame.draw.circle(sprite, (255, 255, 255, 100), highlight_pos, radius//3)
    
    return sprite

