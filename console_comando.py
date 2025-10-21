"""
CONSOLE DI COMANDO - Dashboard completo per il giocatore
Si apre all'inizio di ogni turno
"""

import pygame

class CommandConsole:
    """Console di controllo strategico"""
    
    def __init__(self, faction, territories, factions_data, turn, tech_levels):
        self.faction = faction
        self.territories = territories
        self.factions_data = factions_data
        self.turn = turn
        self.tech_levels = tech_levels
        
        # Dimensioni - SCHERMO 1400x800
        self.width = 1000
        self.height = 700
        self.x = 200
        self.y = 50
        
        self.active = True
        
        # DRAG & DROP - Finestra mobile
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        
        # Calcola statistiche
        self.calculate_stats()
    
    def calculate_stats(self):
        """Calcola tutte le statistiche del giocatore"""
        self.my_territories = [t for t in self.territories if t.owner == self.faction]
        
        # Conta territori
        self.territory_count = len(self.my_territories)
        
        # Conta unità totali - TUTTE LE NUOVE UNITÀ
        self.total_infantry = 0
        self.total_tanks = 0
        self.total_planes = 0
        self.total_bombers = 0
        self.total_scientists = 0
        self.total_artillery = 0
        self.total_drones = 0
        self.total_hackers = 0
        self.total_robots = 0
        self.total_super = 0
        
        for t in self.my_territories:
            counts = t.count_units_by_type()
            self.total_infantry += counts["fanteria"]
            self.total_tanks += counts["carro"]
            self.total_planes += counts["aereo"]
            self.total_bombers += counts["bombardiere"]
            self.total_scientists += counts["scienziato"]
            self.total_artillery += counts["artiglieria"]
            self.total_drones += counts["drone"]
            self.total_hackers += counts["hacker"]
            self.total_robots += counts["robot"]
            self.total_super += counts["supersoldato"]
        
        # Risorse totali
        self.money = self.factions_data[self.faction]["money"]
        self.oil = self.factions_data[self.faction]["oil"]
        self.tech = self.factions_data[self.faction]["tech"]
        
        # Produzione totale
        self.income_total = sum(t.income for t in self.my_territories)
        self.oil_total = sum(t.oil_production for t in self.my_territories)
        self.tech_total = sum(t.tech_points for t in self.my_territories)
        
        # PRODUZIONE TECH DA SCIENZIATI!
        self.tech_from_scientists = self.total_scientists * 10
        
        # Livello tech
        tech_level_idx = 0
        for i, lvl in enumerate(self.tech_levels):
            if self.tech >= lvl["points"]:
                tech_level_idx = i
        self.tech_level = self.tech_levels[tech_level_idx]
        
        # Potenza militare totale
        self.total_attack = self.total_infantry * 2 + self.total_tanks * 8 + self.total_planes * 15
        self.total_defense = self.total_infantry * 2 + self.total_tanks * 6 + self.total_planes * 5
        
        # Top 5 territori più redditizi
        self.my_territories.sort(key=lambda t: t.income, reverse=True)
        self.top_territories = self.my_territories[:5]
        
        # Conta territori sviluppati
        self.developed = sum(1 for t in self.my_territories if t.development_level >= 5)
    
    def draw(self, surface, font, font_small, font_large, font_title):
        """Disegna console con GRAFICA PROFESSIONALE"""
        
        # ===== SFONDO SFOCATO =====
        overlay = pygame.Surface((1400, 800))
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))
        surface.blit(overlay, (0, 0))
        
        # ===== PANNELLO CON GRADIENTE =====
        main_panel = pygame.Surface((self.width, self.height))
        
        # Gradiente verticale
        for i in range(self.height):
            t = i / self.height
            r = int(15 + 10 * t)
            g = int(20 + 15 * t)
            b = int(35 + 20 * t)
            pygame.draw.line(main_panel, (r, g, b), (0, i), (self.width, i))
        
        surface.blit(main_panel, (self.x, self.y))
        
        # OMBRA pannello (dietro)
        shadow = pygame.Surface((self.width + 20, self.height + 20), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 100), (10, 10, self.width, self.height))
        surface.blit(shadow, (self.x - 10, self.y - 10))
        
        # Bordo doppio elegante con glow - COLORE CAMBIA SE TRASCINAMENTO ATTIVO
        if self.dragging:
            pygame.draw.rect(surface, (100, 255, 150), (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 6)
            pygame.draw.rect(surface, (50, 200, 100), (self.x, self.y, self.width, self.height), 4)
            pygame.draw.rect(surface, (25, 150, 75), (self.x + 4, self.y + 4, self.width - 8, self.height - 8), 2)
        else:
            pygame.draw.rect(surface, (150, 200, 255), (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 6)
            pygame.draw.rect(surface, (100, 150, 255), (self.x, self.y, self.width, self.height), 4)
            pygame.draw.rect(surface, (50, 100, 200), (self.x + 4, self.y + 4, self.width - 8, self.height - 8), 2)
        
        # ===== HEADER CON GRADIENTE =====
        header_height = 80
        header = pygame.Surface((self.width, header_height))
        
        # Gradiente header (blu scuro -> blu chiaro)
        for i in range(header_height):
            t = i / header_height
            r = int(30 + 40 * t)
            g = int(50 + 60 * t)
            b = int(100 + 50 * t)
            pygame.draw.line(header, (r, g, b), (0, i), (self.width, i))
        
        surface.blit(header, (self.x, self.y))
        
        # Linea separatore brillante
        pygame.draw.line(surface, (150, 200, 255), 
                        (self.x, self.y + header_height), 
                        (self.x + self.width, self.y + header_height), 3)
        
        # Titolo con GLOW - VERSIONE v2.3 TRASCINABILE
        title = font_title.render("CONSOLE v2.3 TRASCINABILE", True, (255, 255, 100))
        title_rect = title.get_rect(center=(self.x + self.width // 2, self.y + 25))
        
        # Glow dietro titolo
        for offset in range(3, 0, -1):
            glow_title = font_title.render("CONSOLE v2.3 TRASCINABILE", True, (255, 200, 0, 100 // offset))
            glow_rect = glow_title.get_rect(center=(title_rect.centerx + offset, title_rect.centery + offset))
            surface.blit(glow_title, glow_rect)
        
        surface.blit(title, title_rect)
        
        # Indicatore DRAG - mostra solo se non sta trascinando
        if not self.dragging:
            drag_hint = font_small.render("🖐️ Trascina per spostare", True, (200, 200, 200))
            drag_rect = drag_hint.get_rect(center=(self.x + self.width // 2, self.y + 10))
            surface.blit(drag_hint, drag_rect)
        else:
            drag_active = font_small.render("✋ Trascinamento attivo", True, (100, 255, 150))
            drag_rect = drag_active.get_rect(center=(self.x + self.width // 2, self.y + 10))
            surface.blit(drag_active, drag_rect)
        
        # Sottotitolo con colore fazione
        subtitle = font_large.render(f"{self.factions_data[self.faction]['name']} - TURNO {self.turn}", 
                                     True, self.factions_data[self.faction]["color"])
        subtitle_rect = subtitle.get_rect(center=(self.x + self.width // 2, self.y + 55))
        surface.blit(subtitle, subtitle_rect)
        
        # ===== COLONNA SINISTRA - RISORSE =====
        self.draw_resources_panel(surface, font, font_small, self.x + 20, self.y + 100)
        
        # ===== COLONNA CENTRO - MILITARE =====
        self.draw_military_panel(surface, font, font_small, self.x + 350, self.y + 100)
        
        # ===== COLONNA DESTRA - TERRITORI =====
        self.draw_territory_panel(surface, font, font_small, self.x + 680, self.y + 100)
        
        # ===== FOOTER - PULSANTE INIZIA =====
        self.draw_footer(surface, font, font_small, font_large, self.y + self.height - 80)
    
    def draw_resources_panel(self, surface, font, font_small, x, y):
        """Pannello risorse con GRADIENTE"""
        # Box con gradiente
        panel = pygame.Surface((310, 500))
        for i in range(500):
            t = i / 500
            r = int(25 + 15 * t)
            g = int(35 + 25 * t)
            b = int(50 + 30 * t)
            pygame.draw.line(panel, (r, g, b), (0, i), (310, i))
        
        surface.blit(panel, (x, y))
        
        # Bordo con glow
        pygame.draw.rect(surface, (150, 200, 255), (x - 2, y - 2, 314, 504), 3)
        pygame.draw.rect(surface, (100, 150, 200), (x, y, 310, 500), 2)
        
        # Titolo
        title = font.render("[$] ECONOMIA", True, (100, 255, 100))
        surface.blit(title, (x + 10, y + 10))
        
        y_offset = y + 45
        
        # Risorse attuali
        current = font_small.render("RISORSE DISPONIBILI:", True, (200, 200, 200))
        surface.blit(current, (x + 15, y_offset))
        y_offset += 25
        
        money_text = font.render(f"$ {self.money:,}", True, (100, 255, 100))
        surface.blit(money_text, (x + 20, y_offset))
        y_offset += 30
        
        oil_text = font.render(f"[P] {self.oil:,} P", True, (255, 200, 100))
        surface.blit(oil_text, (x + 20, y_offset))
        y_offset += 30
        
        tech_text = font.render(f"[T] {self.tech:,} T", True, (150, 150, 255))
        surface.blit(tech_text, (x + 20, y_offset))
        y_offset += 40
        
        # Separatore
        pygame.draw.line(surface, (100, 100, 150), (x + 15, y_offset), (x + 295, y_offset), 1)
        y_offset += 15
        
        # Produzione prossimo turno
        prod = font_small.render("PRODUZIONE/TURNO:", True, (200, 200, 200))
        surface.blit(prod, (x + 15, y_offset))
        y_offset += 25
        
        inc = font_small.render(f"+$ {self.income_total:,}", True, (150, 255, 150))
        surface.blit(inc, (x + 20, y_offset))
        y_offset += 20
        
        oil_inc = font_small.render(f"+[P] {self.oil_total:,} P", True, (255, 220, 150))
        surface.blit(oil_inc, (x + 20, y_offset))
        y_offset += 20
        
        tech_inc = font_small.render(f"+[T] {self.tech_total:,} T (territori)", True, (180, 180, 255))
        surface.blit(tech_inc, (x + 20, y_offset))
        y_offset += 20
        
        # SCIENZIATI - PRODUZIONE TECH!
        if self.total_scientists > 0:
            sci_tech = font_small.render(f"+[T] {self.tech_from_scientists:,} T (🔬x{self.total_scientists})", True, (100, 255, 255))
            surface.blit(sci_tech, (x + 20, y_offset))
            y_offset += 20
            
            # Totale tech
            total_tech_prod = self.tech_total + self.tech_from_scientists
            total_text = font.render(f"TOTALE: +{total_tech_prod:,} T/turno", True, (255, 255, 100))
            surface.blit(total_text, (x + 20, y_offset))
            y_offset += 30
        else:
            # Suggerimento per comprare scienziati
            no_sci = font_small.render("💡 Compra Scienziati (Q) per +tech!", True, (255, 200, 100))
            surface.blit(no_sci, (x + 20, y_offset))
            y_offset += 30
        
        y_offset += 10
        
        # Livello tecnologia
        pygame.draw.line(surface, (100, 100, 150), (x + 15, y_offset), (x + 295, y_offset), 1)
        y_offset += 15
        
        tech_title = font_small.render("LIVELLO TECNOLOGIA:", True, (200, 200, 200))
        surface.blit(tech_title, (x + 15, y_offset))
        y_offset += 25
        
        tech_level_text = font.render(f"[TECH] {self.tech_level['name']}", True, (255, 255, 100))
        surface.blit(tech_level_text, (x + 20, y_offset))
        y_offset += 30
        
        bonus_text = font_small.render(
            f"Bonus: +{self.tech_level['bonus_attack']} ATT, +{self.tech_level['bonus_defense']} DEF",
            True, (200, 255, 200)
        )
        surface.blit(bonus_text, (x + 20, y_offset))
        y_offset += 25
        
        # BARRA DI PROGRESSO TECNOLOGICO
        next_lvl = None
        for lvl in self.tech_levels:
            if lvl["points"] > self.tech:
                next_lvl = lvl
                break
        
        if next_lvl:
            # Calcola progresso
            current_lvl_points = self.tech_level["points"]
            next_lvl_points = next_lvl["points"]
            progress = (self.tech - current_lvl_points) / (next_lvl_points - current_lvl_points)
            progress = max(0, min(1, progress))
            
            # Disegna barra
            bar_width = 270
            bar_height = 20
            bar_x = x + 20
            bar_y = y_offset
            
            # Sfondo barra
            pygame.draw.rect(surface, (40, 40, 60), (bar_x, bar_y, bar_width, bar_height))
            
            # Riempimento barra
            fill_width = int(bar_width * progress)
            for i in range(bar_height):
                t = i / bar_height
                r = int(100 + 155 * progress)
                g = int(100 + 155 * t)
                b = int(255 - 100 * t)
                pygame.draw.line(surface, (r, g, b), (bar_x, bar_y + i), (bar_x + fill_width, bar_y + i))
            
            # Bordo barra
            pygame.draw.rect(surface, (150, 150, 200), (bar_x, bar_y, bar_width, bar_height), 2)
            
            # Testo progresso
            needed = next_lvl["points"] - self.tech
            progress_text = font_small.render(f"{int(progress * 100)}% - {needed}T al prossimo livello", True, (255, 255, 255))
            surface.blit(progress_text, (bar_x + 5, bar_y + 2))
            y_offset += 25
            
            # Prossimo livello
            next_text = font_small.render(
                f"➜ {next_lvl['name']}",
                True, (150, 200, 255)
            )
            surface.blit(next_text, (x + 20, y_offset))
            
            # Unità sbloccabili
            if len(next_lvl.get("unlocks", [])) > 0:
                unlocks = ", ".join(next_lvl["unlocks"])
                unlock_text = font_small.render(f"Sblocca: {unlocks}", True, (200, 255, 200))
                surface.blit(unlock_text, (x + 25, y_offset + 15))
        else:
            max_text = font.render("⭐ LIVELLO MASSIMO! ⭐", True, (255, 215, 0))
            surface.blit(max_text, (x + 20, y_offset))
    
    def draw_military_panel(self, surface, font, font_small, x, y):
        """Pannello militare con GRADIENTE"""
        # Box con gradiente rosso
        panel = pygame.Surface((310, 500))
        for i in range(500):
            t = i / 500
            r = int(50 + 20 * t)
            g = int(25 + 15 * t)
            b = int(25 + 15 * t)
            pygame.draw.line(panel, (r, g, b), (0, i), (310, i))
        
        surface.blit(panel, (x, y))
        
        # Bordo con glow
        pygame.draw.rect(surface, (255, 150, 150), (x - 2, y - 2, 314, 504), 3)
        pygame.draw.rect(surface, (200, 100, 100), (x, y, 310, 500), 2)
        
        # Titolo
        title = font.render("[WAR] FORZE ARMATE", True, (255, 100, 100))
        surface.blit(title, (x + 10, y + 10))
        
        y_offset = y + 45
        
        # Totale unità - DIVISO IN SEZIONI
        total = font_small.render("🎖️ UNITÀ BASE:", True, (200, 200, 200))
        surface.blit(total, (x + 15, y_offset))
        y_offset += 20
        
        inf = font_small.render(f"  👥 {self.total_infantry} Fanterie", True, (200, 255, 200))
        surface.blit(inf, (x + 20, y_offset))
        y_offset += 18
        
        tank = font_small.render(f"  🚜 {self.total_tanks} Carri", True, (255, 200, 150))
        surface.blit(tank, (x + 20, y_offset))
        y_offset += 18
        
        plane = font_small.render(f"  ✈️  {self.total_planes} Aerei", True, (150, 200, 255))
        surface.blit(plane, (x + 20, y_offset))
        y_offset += 18
        
        bomber = font_small.render(f"  💣 {self.total_bombers} Bombardieri", True, (255, 150, 150))
        surface.blit(bomber, (x + 20, y_offset))
        y_offset += 25
        
        # UNITÀ SPECIALI
        has_special = (self.total_scientists + self.total_artillery + self.total_drones + 
                      self.total_hackers + self.total_robots + self.total_super) > 0
        
        if has_special:
            special = font_small.render("⭐ UNITÀ SPECIALI:", True, (255, 255, 100))
            surface.blit(special, (x + 15, y_offset))
            y_offset += 20
            
            if self.total_scientists > 0:
                sci = font_small.render(f"  🔬 {self.total_scientists} Scienziati (+{self.total_scientists * 10}T/turno)", True, (100, 255, 255))
                surface.blit(sci, (x + 20, y_offset))
                y_offset += 18
            
            if self.total_artillery > 0:
                art = font_small.render(f"  🎯 {self.total_artillery} Artiglieria", True, (255, 200, 100))
                surface.blit(art, (x + 20, y_offset))
                y_offset += 18
            
            if self.total_drones > 0:
                drone = font_small.render(f"  🛸 {self.total_drones} Droni", True, (200, 150, 255))
                surface.blit(drone, (x + 20, y_offset))
                y_offset += 18
            
            if self.total_hackers > 0:
                hack = font_small.render(f"  💻 {self.total_hackers} Hacker (range globale!)", True, (150, 255, 255))
                surface.blit(hack, (x + 20, y_offset))
                y_offset += 18
            
            if self.total_robots > 0:
                robot = font_small.render(f"  🤖 {self.total_robots} Robot", True, (255, 150, 255))
                surface.blit(robot, (x + 20, y_offset))
                y_offset += 18
            
            if self.total_super > 0:
                superunit = font.render(f"  ⚡ {self.total_super} SUPER SOLDATI!", True, (255, 255, 0))
                surface.blit(superunit, (x + 20, y_offset))
                y_offset += 20
            
            y_offset += 10
        else:
            y_offset += 15
        
        # Separatore
        pygame.draw.line(surface, (150, 100, 100), (x + 15, y_offset), (x + 295, y_offset), 1)
        y_offset += 15
        
        # Potenza militare
        power = font_small.render("POTENZA TOTALE:", True, (200, 200, 200))
        surface.blit(power, (x + 15, y_offset))
        y_offset += 25
        
        att = font.render(f"[ATT] Attacco: {self.total_attack}", True, (255, 100, 100))
        surface.blit(att, (x + 20, y_offset))
        y_offset += 30
        
        deff = font.render(f"[DEF] Difesa: {self.total_defense}", True, (100, 100, 255))
        surface.blit(deff, (x + 20, y_offset))
        y_offset += 40
        
        # Capacità offensive
        pygame.draw.line(surface, (150, 100, 100), (x + 15, y_offset), (x + 295, y_offset), 1)
        y_offset += 15
        
        cap_title = font_small.render("CAPACITÀ OPERATIVE:", True, (200, 200, 200))
        surface.blit(cap_title, (x + 15, y_offset))
        y_offset += 25
        
        # Attacchi possibili con petrolio attuale
        total_units = self.total_infantry + self.total_tanks + self.total_planes
        if total_units > 0:
            attacks_possible = self.oil // (20 * total_units)
            att_pos = font_small.render(f"Attacchi possibili: {attacks_possible}", True, (255, 255, 150))
            surface.blit(att_pos, (x + 20, y_offset))
            y_offset += 20
        
        # Unità acquistabili
        units_buyable = self.money // 50
        buy_pos = font_small.render(f"Fanterie acquistabili: {units_buyable}", True, (200, 255, 200))
        surface.blit(buy_pos, (x + 20, y_offset))
        y_offset += 20
        
        tanks_buyable = self.money // 500
        buy_tank = font_small.render(f"Carri acquistabili: {tanks_buyable}", True, (255, 200, 150))
        surface.blit(buy_tank, (x + 20, y_offset))
        y_offset += 20
        
        planes_buyable = self.money // 1500
        buy_plane = font_small.render(f"Aerei acquistabili: {planes_buyable}", True, (150, 200, 255))
        surface.blit(buy_plane, (x + 20, y_offset))
        y_offset += 25
        
        # Nuke
        if self.money >= 10000:
            nuke_text = font_small.render("[!] BOMBA ATOMICA disponibile!", True, (255, 0, 0))
            surface.blit(nuke_text, (x + 20, y_offset))
    
    def draw_territory_panel(self, surface, font, font_small, x, y):
        """Pannello territori con GRADIENTE"""
        # Box con gradiente verde
        panel = pygame.Surface((300, 500))
        for i in range(500):
            t = i / 500
            r = int(25 + 15 * t)
            g = int(50 + 30 * t)
            b = int(25 + 15 * t)
            pygame.draw.line(panel, (r, g, b), (0, i), (300, i))
        
        surface.blit(panel, (x, y))
        
        # Bordo con glow
        pygame.draw.rect(surface, (150, 255, 150), (x - 2, y - 2, 304, 504), 3)
        pygame.draw.rect(surface, (100, 200, 100), (x, y, 300, 500), 2)
        
        # Titolo
        title = font.render("[MAP] TERRITORI", True, (100, 255, 100))
        surface.blit(title, (x + 10, y + 10))
        
        y_offset = y + 45
        
        # Statistiche
        stats = font_small.render(f"Controlli: {self.territory_count} territori", True, (200, 200, 200))
        surface.blit(stats, (x + 15, y_offset))
        y_offset += 20
        
        dev_stat = font_small.render(f"Sviluppati (5+): {self.developed}", True, (255, 215, 0))
        surface.blit(dev_stat, (x + 15, y_offset))
        y_offset += 30
        
        # Separatore
        pygame.draw.line(surface, (100, 150, 100), (x + 15, y_offset), (x + 285, y_offset), 1)
        y_offset += 15
        
        # Top 5 territori
        top_title = font_small.render("TOP 5 TERRITORI PIÙ REDDITIZI:", True, (200, 200, 200))
        surface.blit(top_title, (x + 15, y_offset))
        y_offset += 25
        
        for i, terr in enumerate(self.top_territories):
            # Nome
            name = font_small.render(f"{i+1}. {terr.name}", True, (255, 255, 255))
            surface.blit(name, (x + 20, y_offset))
            y_offset += 18
            
            # Risorse
            res = font_small.render(
                f"   ${terr.income} {terr.oil_production}P {terr.tech_points}T *{terr.development_level}",
                True, (200, 255, 200)
            )
            surface.blit(res, (x + 25, y_offset))
            y_offset += 20
            
            # Unità
            counts = terr.count_units_by_type()
            units = font_small.render(
                f"   F:{counts['fanteria']} C:{counts['carro']} A:{counts['aereo']}",
                True, (180, 180, 180)
            )
            surface.blit(units, (x + 25, y_offset))
            y_offset += 25
        
        # Suggerimento
        y_offset += 20
        pygame.draw.line(surface, (100, 150, 100), (x + 15, y_offset), (x + 285, y_offset), 1)
        y_offset += 15
        
        suggestion = font_small.render("💡 SUGGERIMENTO:", True, (255, 255, 100))
        surface.blit(suggestion, (x + 15, y_offset))
        y_offset += 20
        
        # SUGGERIMENTI INTELLIGENTI BASATI SULLE STATISTICHE
        if self.total_scientists == 0:
            sug = font_small.render("🔬 Compra SCIENZIATI!", True, (100, 255, 255))
            surface.blit(sug, (x + 20, y_offset))
            y_offset += 15
            sug2 = font_small.render("Accelerano la ricerca tech", True, (150, 200, 255))
            surface.blit(sug2, (x + 20, y_offset))
        elif self.total_scientists < 5 and self.tech < 1000:
            sug = font_small.render("Serve più ricerca!", True, (255, 255, 100))
            surface.blit(sug, (x + 20, y_offset))
            y_offset += 15
            sug2 = font_small.render(f"Compra altri scienziati (hai {self.total_scientists})", True, (200, 255, 200))
            surface.blit(sug2, (x + 20, y_offset))
        elif self.oil < 500:
            sug = font_small.render("⚠️ Poco petrolio!", True, (255, 200, 150))
            surface.blit(sug, (x + 20, y_offset))
            y_offset += 15
            sug2 = font_small.render("Conquista territori petroliferi", True, (255, 200, 150))
            surface.blit(sug2, (x + 20, y_offset))
        elif self.tech >= 1200 and self.total_hackers == 0:
            sug = font_small.render("💻 Sblocca HACKER!", True, (150, 255, 255))
            surface.blit(sug, (x + 20, y_offset))
            y_offset += 15
            sug2 = font_small.render("Range globale - attacca ovunque!", True, (200, 255, 200))
            surface.blit(sug2, (x + 20, y_offset))
        elif self.tech >= 3500 and self.total_super == 0:
            sug = font_small.render("⚡ SUPER SOLDATI disponibili!", True, (255, 255, 0))
            surface.blit(sug, (x + 20, y_offset))
            y_offset += 15
            sug2 = font_small.render("Le unità più potenti del gioco!", True, (255, 215, 0))
            surface.blit(sug2, (x + 20, y_offset))
        else:
            sug = font_small.render("✅ Ottima strategia!", True, (150, 255, 150))
            surface.blit(sug, (x + 20, y_offset))
            y_offset += 15
            sug2 = font_small.render("Continua a espandere l'impero!", True, (150, 255, 150))
            surface.blit(sug2, (x + 20, y_offset))
    
    def draw_footer(self, surface, font, font_small, font_large, y):
        """Footer con pulsante"""
        footer_x = self.x
        footer_y = y
        
        # Pulsante grande INIZIA
        button_width = 400
        button_height = 60
        button_x = self.x + (self.width - button_width) // 2
        
        # Check hover
        mouse_pos = pygame.mouse.get_pos()
        self.start_button = pygame.Rect(button_x, footer_y, button_width, button_height)
        is_hover = self.start_button.collidepoint(mouse_pos)
        
        # Gradiente pulsante (verde brillante)
        button_surf = pygame.Surface((button_width, button_height))
        for i in range(button_height):
            t = i / button_height
            if is_hover:
                r = int(100 - 30 * t)
                g = int(255 - 80 * t)
                b = int(100 - 30 * t)
            else:
                r = int(50 - 20 * t)
                g = int(200 - 70 * t)
                b = int(50 - 20 * t)
            pygame.draw.line(button_surf, (r, g, b), (0, i), (button_width, i))
        
        surface.blit(button_surf, (button_x, footer_y))
        
        # Highlight superiore
        highlight = pygame.Surface((button_width - 20, 4), pygame.SRCALPHA)
        highlight.fill((255, 255, 255, 150))
        surface.blit(highlight, (button_x + 10, footer_y + 8))
        
        # Bordo brillante
        pygame.draw.rect(surface, (150, 255, 150), (button_x - 2, footer_y - 2, button_width + 4, button_height + 4), 3)
        pygame.draw.rect(surface, (100, 255, 100), (button_x, footer_y, button_width, button_height), 4)
        
        # Testo
        start_text = font_large.render("INIZIA TURNO", True, (255, 255, 255))
        text_rect = start_text.get_rect(center=(button_x + button_width // 2, footer_y + button_height // 2))
        surface.blit(start_text, text_rect)
        
        # Helper
        helper = font_small.render("Premi SPAZIO o Click qui", True, (200, 200, 200))
        helper_rect = helper.get_rect(center=(self.x + self.width // 2, footer_y - 15))
        surface.blit(helper, helper_rect)
    
    def handle_mouse_down(self, pos):
        """Gestisce mouse down per drag & drop"""
        # Area di drag = header (primi 80px)
        header_rect = pygame.Rect(self.x, self.y, self.width, 80)
        
        if header_rect.collidepoint(pos):
            self.dragging = True
            self.drag_offset_x = pos[0] - self.x
            self.drag_offset_y = pos[1] - self.y
            return True
        return False
    
    def handle_mouse_up(self, pos):
        """Gestisce mouse up"""
        if self.dragging:
            self.dragging = False
            return True
        return False
    
    def handle_mouse_motion(self, pos):
        """Gestisce movimento mouse durante drag"""
        if self.dragging:
            # Calcola nuova posizione
            new_x = pos[0] - self.drag_offset_x
            new_y = pos[1] - self.drag_offset_y
            
            # Limita ai bordi dello schermo (1400x800)
            new_x = max(0, min(new_x, 1400 - self.width))
            new_y = max(0, min(new_y, 800 - self.height))
            
            self.x = new_x
            self.y = new_y
            return True
        return False
    
    def handle_click(self, pos):
        """Gestisce click sul bottone"""
        if hasattr(self, 'start_button') and self.start_button.collidepoint(pos):
            self.active = False
            return True
        return False

