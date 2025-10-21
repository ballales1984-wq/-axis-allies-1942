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
            self.rate = 150  # Velocità (parole/min)
            self.volume = 0.5  # Volume iniziale (0-1) - Medio
            
            self.engine.setProperty('rate', self.rate)
            self.engine.setProperty('volume', self.volume)
            
            # Prova a impostare voce italiana (se disponibile)
            voices = self.engine.getProperty('voices')
            for voice in voices:
                if 'italian' in voice.name.lower() or 'it' in voice.languages:
                    self.engine.setProperty('voice', voice.id)
                    break
            
            self.enabled = True
            print(f"[OK] Sistema vocale attivato - Volume: {int(self.volume * 100)}%")
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
    
    def volume_up(self):
        """Aumenta volume di 10%"""
        if not hasattr(self, 'engine'):
            return "Voce non disponibile"
        
        self.volume = min(1.0, self.volume + 0.1)
        self.engine.setProperty('volume', self.volume)
        percentage = int(self.volume * 100)
        print(f"[VOCE] Volume: {percentage}%")
        return f"Volume Voce: {percentage}%"
    
    def volume_down(self):
        """Diminuisce volume di 10%"""
        if not hasattr(self, 'engine'):
            return "Voce non disponibile"
        
        self.volume = max(0.0, self.volume - 0.1)
        self.engine.setProperty('volume', self.volume)
        percentage = int(self.volume * 100)
        print(f"[VOCE] Volume: {percentage}%")
        return f"Volume Voce: {percentage}%"
    
    def speed_up(self):
        """Aumenta velocità di 20 parole/min"""
        if not hasattr(self, 'engine'):
            return "Voce non disponibile"
        
        self.rate = min(250, self.rate + 20)
        self.engine.setProperty('rate', self.rate)
        print(f"[VOCE] Velocità: {self.rate} parole/min")
        return f"Velocità Voce: {self.rate} wpm"
    
    def speed_down(self):
        """Diminuisce velocità di 20 parole/min"""
        if not hasattr(self, 'engine'):
            return "Voce non disponibile"
        
        self.rate = max(80, self.rate - 20)
        self.engine.setProperty('rate', self.rate)
        print(f"[VOCE] Velocità: {self.rate} parole/min")
        return f"Velocità Voce: {self.rate} wpm"
    
    def get_volume(self):
        """Ottieni volume corrente in percentuale"""
        return int(self.volume * 100)
    
    def get_rate(self):
        """Ottieni velocità corrente"""
        return self.rate
    
    def cleanup(self):
        """Pulizia risorse"""
        if self.enabled:
            try:
                self.engine.stop()
            except:
                pass


