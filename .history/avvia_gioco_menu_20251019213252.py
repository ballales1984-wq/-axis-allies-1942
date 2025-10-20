"""
LAUNCHER - Avvia gioco con menu modalità
"""

import subprocess
import sys
from menu_principale import show_main_menu
import pygame

def main():
    # Mostra menu
    mode = show_main_menu()
    pygame.quit()
    
    if mode == "quit":
        print("Uscita...")
        sys.exit(0)
    
    elif mode == "singleplayer":
        print("\n[AVVIO] Modalita Singleplayer vs IA")
        # Avvia gioco normale
        subprocess.run([sys.executable, "gioco_avanzato.py"])
    
    elif mode == "server":
        print("\n[AVVIO] Creazione server...")
        print("1. Avvio server in background")
        print("2. Avvio gioco come host\n")
        
        # Avvia server in processo separato
        server_process = subprocess.Popen(
            [sys.executable, "server_multiplayer.py"],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        
        # Aspetta 1 secondo che server si avvii
        import time
        time.sleep(1)
        
        # Avvia gioco in modalità client (connetti a localhost)
        subprocess.run([sys.executable, "gioco_multiplayer.py", "--host"])
    
    elif mode == "client":
        server_ip = input("\nIP del server (Enter = localhost): ").strip() or "localhost"
        print(f"\n[CONNESSIONE] {server_ip}:5555...")
        
        # Avvia gioco in modalità client
        subprocess.run([sys.executable, "gioco_multiplayer.py", "--client", server_ip])


if __name__ == "__main__":
    main()

