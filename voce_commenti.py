"""
COMMENTI VOCALI - Sistema Text-to-Speech per il gioco
Annuncia eventi importanti con voce sintetica!
"""

import pyttsx3
import threading

class VoiceAnnouncer:
    """Annuncia eventi del gioco con voce sintetica"""
    
    def __init__(self):
        try:
            self.engine = pyttsx3.init()
            
            # Configurazione voce
            self.engine.setProperty('rate', 150)  # Velocità (parole/min)
            self.engine.setProperty('volume', 0.9)  # Volume (0-1)
            
            # Prova a impostare voce italiana (se disponibile)
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if 'italian' in voice.name.lower() or 'it' in voice.languages:
                    self.engine.setProperty('voice', voice.id)
                    break
            
            self.enabled = True
            print("[OK] Sistema vocale attivato")
        except Exception as e:
            print(f"[WARN] Sistema vocale non disponibile: {e}")
            self.enabled = False
    
    def speak(self, text):
        """Pronuncia testo in thread separato (non blocca il gioco)"""
        if not self.enabled:
            return
        
        def _speak():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except:
                pass
        
        # Thread per non bloccare il gioco
        thread = threading.Thread(target=_speak, daemon=True)
        thread.start()
    
    def announce_turn(self, faction_name):
        """Annuncia inizio turno"""
        self.speak(f"Turno di {faction_name}")
    
    def announce_attack(self, attacker_name, defender_name):
        """Annuncia attacco"""
        self.speak(f"{attacker_name} attacca {defender_name}")
    
    def announce_conquest(self, territory_name):
        """Annuncia conquista"""
        self.speak(f"{territory_name} viene conquistata!")
    
    def announce_defense(self, territory_name):
        """Annuncia difesa riuscita"""
        self.speak(f"{territory_name} resiste all'attacco!")
    
    def announce_tech_upgrade(self, faction_name, level_name):
        """Annuncia upgrade tecnologico"""
        self.speak(f"{faction_name} raggiunge il livello {level_name}!")
    
    def announce_nuke(self, territory_name):
        """Annuncia lancio atomico"""
        self.speak(f"Attenzione! Bomba atomica su {territory_name}!")
    
    def announce_victory(self, faction_name):
        """Annuncia vittoria"""
        self.speak(f"{faction_name} ha vinto la guerra mondiale!")
    
    def announce_resources(self, money, oil, tech):
        """Annuncia risorse"""
        self.speak(f"Risorse: {money} dollari, {oil} petrolio, {tech} tecnologia")
    
    def announce_purchase(self, unit_name, territory_name):
        """Annuncia acquisto"""
        self.speak(f"{unit_name} acquistato a {territory_name}")
    
    def toggle(self):
        """Abilita/Disabilita voce"""
        self.enabled = not self.enabled
        status = "attivati" if self.enabled else "disattivati"
        print(f"[INFO] Commenti vocali {status}")
        return self.enabled
    
    def cleanup(self):
        """Pulizia risorse"""
        if self.enabled:
            try:
                self.engine.stop()
            except:
                pass


