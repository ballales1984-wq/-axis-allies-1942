"""
AXIS & ALLIES 1942 - VERSIONE GLOBO 3D
Mappa mondiale su globo terrestre rotante!
"""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectButton import DirectButton
import json
import random
import math

class Unit:
    """Unità militare"""
    def __init__(self, unit_type, durability=100):
        self.type = unit_type
        self.durability = durability

class Territory:
    """Territorio 3D"""
    def __init__(self, id, name, lat, lon):
        self.id = id
        self.name = name
        self.lat = lat  # Latitudine
        self.lon = lon  # Longitudine
        self.owner = None
        self.units = []
        
        # Risorse
        self.money = random.randint(100, 500)
        self.oil = random.randint(100, 300)
        self.tech_points = random.randint(10, 50)
        
        # Sviluppo
        self.development_level = 0
        self.turns_held = 0
        
        # Difese
        self.bunkers = 0
        self.towers = 0
        self.fortress = 0
        
        # Node 3D
        self.marker_node = None

class GlobeGame(ShowBase):
    """Gioco su globo 3D"""
    
    def __init__(self):
        ShowBase.__init__(self)
        
        # Setup camera
        self.disable_mouse()
        self.camera.setPos(0, -15, 0)
        self.camera.lookAt(0, 0, 0)
        
        # Variabili rotazione
        self.globe_rotation = 0
        self.mouse_x = 0
        self.dragging = False
        
        # Colori fazioni
        self.faction_colors = {
            "usa": (0, 0.4, 0.8, 1),
            "europa": (0.8, 0, 0, 1),
            "russia": (0.6, 0, 0.6, 1),
            "cina": (1, 0.8, 0, 1),
            "africa": (0, 0.6, 0, 1)
        }
        
        # Setup gioco
        self.factions = ["usa", "europa", "russia", "cina", "africa"]
        self.current_faction_idx = 0
        self.current_turn = 1
        
        self.faction_resources = {
            faction: {"money": 5000, "oil": 2000, "tech": 0, "tech_level": 0}
            for faction in self.factions
        }
        
        # Crea scena
        self.create_globe()
        self.load_territories()
        self.create_markers()
        self.create_ui()
        
        # Picker per click su oggetti
        self.picker = CollisionTraverser()
        self.pq = CollisionHandlerQueue()
        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = self.camera.attachNewNode(self.pickerNode)
        self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)
        self.picker.addCollider(self.pickerNP, self.pq)
        
        # Input
        self.accept("mouse1", self.on_mouse_click)
        self.accept("mouse1-up", self.on_mouse_release)
        self.accept("space", self.next_turn)
        self.accept("escape", self.exit_game)
        self.accept("wheel_up", self.zoom_in)
        self.accept("wheel_down", self.zoom_out)
        
        # Task
        self.taskMgr.add(self.update_task, "update")
        
        print("=" * 60)
        print("AXIS & ALLIES 1942 - GLOBO 3D")
        print("=" * 60)
        print("CONTROLLI:")
        print("  Mouse drag = Ruota globo")
        print("  Click marker = Seleziona territorio")
        print("  SPAZIO = Fine turno")
        print("  ESC = Esci")
        print("=" * 60)
    
    def create_globe(self):
        """Crea globo terrestre"""
        # Crea sfera
        self.globe = self.loader.loadModel("models/misc/sphere")
        self.globe.reparentTo(self.render)
        self.globe.setScale(5)
        
        # Carica texture mappa
        try:
            tex = self.loader.loadTexture("mappa_hd.jpg")
            self.globe.setTexture(tex, 1)
        except:
            # Se non trova texture, usa colore
            self.globe.setColor(0.3, 0.5, 0.8, 1)
        
        # Abilita rotazione
        self.globe.setHpr(0, 0, 0)
        
        # Luce
        dlight = DirectionalLight('dlight')
        dlight.setColor((1, 1, 1, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        self.render.setLight(dlnp)
        
        # Luce ambientale
        alight = AmbientLight('alight')
        alight.setColor((0.3, 0.3, 0.3, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)
    
    def load_territories(self):
        """Carica territori e converti in coordinate sferiche"""
        try:
            with open("centri.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.territories = []
            
            # Dimensioni mappa
            map_width = 1400
            map_height = 800
            
            for t in data:
                # Converti coordinate 2D in lat/lon
                # X -> Longitudine (-180 a +180)
                # Y -> Latitudine (-90 a +90)
                lon = ((t["x"] / map_width) * 360) - 180
                lat = 90 - ((t["y"] / map_height) * 180)
                
                territory = Territory(t["id"], t["name"], lat, lon)
                
                # Assegna fazione casuale
                territory.owner = self.factions[t["id"] % len(self.factions)]
                
                # Unità iniziali
                for _ in range(random.randint(1, 3)):
                    territory.units.append(Unit("fanteria"))
                
                self.territories.append(territory)
            
            print(f"[OK] Caricati {len(self.territories)} territori")
        except Exception as e:
            print(f"[ERRORE] {e}")
            self.territories = []
    
    def latlon_to_xyz(self, lat, lon, radius=5):
        """Converti lat/lon in coordinate 3D sulla sfera"""
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        
        x = radius * math.cos(lat_rad) * math.cos(lon_rad)
        y = radius * math.cos(lat_rad) * math.sin(lon_rad)
        z = radius * math.sin(lat_rad)
        
        return (x, y, z)
    
    def create_markers(self):
        """Crea marker 3D per territori"""
        for territory in self.territories:
            # Posizione 3D
            x, y, z = self.latlon_to_xyz(territory.lat, territory.lon, 5.1)
            
            # Crea sfera piccola come marker
            marker = self.loader.loadModel("models/misc/sphere")
            marker.reparentTo(self.render)
            marker.setPos(x, y, z)
            marker.setScale(0.1)
            
            # Colore fazione
            color = self.faction_colors.get(territory.owner, (0.5, 0.5, 0.5, 1))
            marker.setColor(*color)
            
            # Salva riferimento
            territory.marker_node = marker
            
            # Tag per click detection
            marker.setTag("territory_id", str(territory.id))
    
    def create_ui(self):
        """Crea interfaccia utente"""
        # Titolo
        self.title = OnscreenText(
            text="AXIS & ALLIES 1942 - GLOBO 3D",
            pos=(0, 0.9),
            scale=0.07,
            fg=(1, 1, 0, 1),
            shadow=(0, 0, 0, 1)
        )
        
        # Info turno
        self.turn_text = OnscreenText(
            text=f"TURNO {self.current_turn} - {self.factions[self.current_faction_idx].upper()}",
            pos=(-1.3, 0.85),
            scale=0.05,
            fg=(1, 1, 1, 1),
            align=TextNode.ALeft
        )
        
        # Risorse
        faction = self.factions[self.current_faction_idx]
        res = self.faction_resources[faction]
        self.resources_text = OnscreenText(
            text=f"[$] {res['money']:,} | [P] {res['oil']:,} | [T] {res['tech']}",
            pos=(-1.3, 0.75),
            scale=0.04,
            fg=(0.8, 0.8, 0.8, 1),
            align=TextNode.ALeft
        )
        
        # Istruzioni
        self.help_text = OnscreenText(
            text="Drag mouse = Ruota | Click marker = Territorio | SPAZIO = Fine turno",
            pos=(0, -0.95),
            scale=0.04,
            fg=(0.6, 0.6, 0.6, 1)
        )
    
    def update_ui(self):
        """Aggiorna UI"""
        faction = self.factions[self.current_faction_idx]
        res = self.faction_resources[faction]
        
        self.turn_text.setText(f"TURNO {self.current_turn} - {faction.upper()}")
        self.resources_text.setText(f"[$] {res['money']:,} | [P] {res['oil']:,} | [T] {res['tech']}")
        
        # Colora testo con colore fazione
        color = self.faction_colors[faction]
        self.turn_text.setFg(color)
    
    def on_mouse_click(self):
        """Mouse premuto"""
        self.dragging = True
        if self.mouseWatcherNode.hasMouse():
            self.mouse_x = self.mouseWatcherNode.getMouseX()
    
    def on_mouse_release(self):
        """Mouse rilasciato"""
        if not self.dragging:
            return
        
        # Check se click su marker
        if self.mouseWatcherNode.hasMouse():
            mpos = self.mouseWatcherNode.getMouse()
            
            # Ray picking
            self.pickerRay.setFromLens(self.camNode, mpos.getX(), mpos.getY())
            
            self.picker.traverse(self.render)
            if self.picker.getNumEntries() > 0:
                self.picker.sortEntries()
                picked = self.picker.getEntry(0).getIntoNodePath()
                
                # Check se ha tag
                if picked.hasTag("territory_id"):
                    territory_id = int(picked.getTag("territory_id"))
                    self.select_territory(territory_id)
        
        self.dragging = False
    
    def select_territory(self, territory_id):
        """Seleziona territorio"""
        territory = next((t for t in self.territories if t.id == territory_id), None)
        if territory:
            print(f"[INFO] {territory.name}")
            print(f"  Owner: {territory.owner}")
            print(f"  Units: {len(territory.units)}")
            print(f"  Money: ${territory.money} | Oil: {territory.oil}P | Tech: {territory.tech_points}T")
    
    def next_turn(self):
        """Prossimo turno"""
        # Produzione risorse
        faction = self.factions[self.current_faction_idx]
        territories = [t for t in self.territories if t.owner == faction]
        
        for t in territories:
            t.turns_held += 1
            t.development_level = min(10, t.turns_held // 3)
        
        money_prod = sum(t.money * (1 + t.development_level * 0.1) for t in territories)
        oil_prod = sum(t.oil * (1 + t.development_level * 0.1) for t in territories)
        tech_prod = sum(t.tech_points * (1 + t.development_level * 0.1) for t in territories)
        
        self.faction_resources[faction]["money"] += int(money_prod)
        self.faction_resources[faction]["oil"] += int(oil_prod)
        self.faction_resources[faction]["tech"] += int(tech_prod)
        
        # Prossima fazione
        self.current_faction_idx = (self.current_faction_idx + 1) % len(self.factions)
        if self.current_faction_idx == 0:
            self.current_turn += 1
        
        self.update_ui()
        print(f"\n[TURNO] {self.factions[self.current_faction_idx].upper()}")
    
    def exit_game(self):
        """Esci"""
        print("\n[INFO] Chiusura...")
        import sys
        sys.exit()
    
    def update_task(self, task):
        """Update loop"""
        # Rotazione globo con mouse drag
        if self.dragging and self.mouseWatcherNode.hasMouse():
            mouse_x = self.mouseWatcherNode.getMouseX()
            delta = mouse_x - self.mouse_x
            self.globe_rotation += delta * 100
            self.globe.setH(self.globe_rotation)
            self.mouse_x = mouse_x
            
            # Ruota anche i marker con il globo
            for territory in self.territories:
                if territory.marker_node:
                    territory.marker_node.setH(self.globe_rotation)
        
        # Auto-rotazione lenta se non dragging
        elif not self.dragging:
            self.globe_rotation += 0.1
            self.globe.setH(self.globe_rotation)
            for territory in self.territories:
                if territory.marker_node:
                    territory.marker_node.setH(self.globe_rotation)
        
        return Task.cont


# Avvia gioco
if __name__ == "__main__":
    # Check se Panda3D è installato
    try:
        app = GlobeGame()
        app.run()
    except Exception as e:
        print(f"[ERRORE] {e}")
        print("\nPer giocare in 3D serve installare Panda3D:")
        print("  pip install panda3d")
        input("\nPremi ENTER per chiudere...")

