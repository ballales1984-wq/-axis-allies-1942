"""
SERVER MULTIPLAYER - Axis & Allies 1942
Gestisce partite online tra giocatori
"""

import socket
import threading
import json
import pickle
from datetime import datetime

class GameServer:
    """Server per partite multiplayer"""
    
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Partite attive
        self.games = {}  # {game_id: GameRoom}
        self.next_game_id = 1
        
        # Client connessi
        self.clients = {}  # {conn: {"name": str, "game_id": int, "faction": str}}
        
        print(f"[SERVER] Avvio su {host}:{port}")
        
    def start(self):
        """Avvia server"""
        self.server.bind((self.host, self.port))
        self.server.listen(10)
        print(f"[SERVER] In ascolto su porta {self.port}")
        print("[SERVER] In attesa di giocatori...")
        
        while True:
            try:
                conn, addr = self.server.accept()
                print(f"[SERVER] Nuova connessione da {addr}")
                
                # Thread per gestire client
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.daemon = True
                thread.start()
                
            except Exception as e:
                print(f"[ERRORE] {e}")
    
    def handle_client(self, conn, addr):
        """Gestisce comunicazione con singolo client"""
        try:
            # Ricevi nome giocatore
            data = self.receive_data(conn)
            if not data or data.get("type") != "join":
                conn.close()
                return
            
            player_name = data.get("name", f"Player_{addr[1]}")
            print(f"[SERVER] {player_name} connesso da {addr}")
            
            # Assegna a una partita
            game_id = self.find_or_create_game()
            game = self.games[game_id]
            
            # Assegna fazione
            faction = game.add_player(conn, player_name, addr)
            if not faction:
                self.send_data(conn, {"type": "error", "msg": "Partita piena"})
                conn.close()
                return
            
            self.clients[conn] = {
                "name": player_name,
                "game_id": game_id,
                "faction": faction
            }
            
            # Conferma connessione
            self.send_data(conn, {
                "type": "joined",
                "game_id": game_id,
                "faction": faction,
                "msg": f"Benvenuto {player_name}! Sei {faction}"
            })
            
            # Notifica altri giocatori
            game.broadcast({
                "type": "player_joined",
                "name": player_name,
                "faction": faction
            }, exclude=conn)
            
            # Loop ricezione comandi
            while True:
                data = self.receive_data(conn)
                if not data:
                    break
                
                self.process_command(conn, data, game)
            
        except Exception as e:
            print(f"[ERRORE] Client {addr}: {e}")
        finally:
            # Disconnessione
            if conn in self.clients:
                client_info = self.clients[conn]
                game_id = client_info["game_id"]
                
                if game_id in self.games:
                    self.games[game_id].remove_player(conn)
                
                del self.clients[conn]
                print(f"[SERVER] {client_info['name']} disconnesso")
            
            conn.close()
    
    def find_or_create_game(self):
        """Trova partita disponibile o creane una nuova"""
        # Cerca partita in attesa
        for game_id, game in self.games.items():
            if not game.is_full():
                return game_id
        
        # Crea nuova partita
        game_id = self.next_game_id
        self.next_game_id += 1
        self.games[game_id] = GameRoom(game_id)
        print(f"[SERVER] Nuova partita creata: #{game_id}")
        return game_id
    
    def process_command(self, conn, data, game):
        """Processa comando da client"""
        cmd_type = data.get("type")
        
        if cmd_type == "buy_unit":
            # Acquisto unità
            game.handle_buy_unit(conn, data)
        
        elif cmd_type == "attack":
            # Attacco
            game.handle_attack(conn, data)
        
        elif cmd_type == "end_turn":
            # Fine turno
            game.handle_end_turn(conn)
        
        elif cmd_type == "chat":
            # Messaggio chat
            game.broadcast({
                "type": "chat",
                "from": self.clients[conn]["name"],
                "msg": data.get("msg", "")
            })
    
    def send_data(self, conn, data):
        """Invia dati serializzati"""
        try:
            msg = pickle.dumps(data)
            msg_len = len(msg).to_bytes(4, 'big')
            conn.sendall(msg_len + msg)
        except:
            pass
    
    def receive_data(self, conn):
        """Ricevi dati serializzati"""
        try:
            # Leggi lunghezza
            msg_len_bytes = conn.recv(4)
            if not msg_len_bytes:
                return None
            
            msg_len = int.from_bytes(msg_len_bytes, 'big')
            
            # Leggi messaggio
            msg = b''
            while len(msg) < msg_len:
                chunk = conn.recv(min(msg_len - len(msg), 4096))
                if not chunk:
                    return None
                msg += chunk
            
            return pickle.loads(msg)
        except:
            return None


class GameRoom:
    """Stanza di gioco per partita multiplayer"""
    
    def __init__(self, game_id):
        self.game_id = game_id
        self.players = {}  # {conn: {"name": str, "faction": str, "ready": bool}}
        self.max_players = 5
        
        self.factions = ["usa", "europa", "russia", "cina", "africa"]
        self.available_factions = list(self.factions)
        
        self.current_turn = 0
        self.current_faction_idx = 0
        
        self.game_state = None  # Stato gioco condiviso
        self.started = False
    
    def is_full(self):
        """Partita piena?"""
        return len(self.players) >= self.max_players
    
    def add_player(self, conn, name, addr):
        """Aggiungi giocatore"""
        if self.is_full():
            return None
        
        # Assegna prima fazione disponibile
        if not self.available_factions:
            return None
        
        faction = self.available_factions.pop(0)
        
        self.players[conn] = {
            "name": name,
            "faction": faction,
            "ready": False,
            "addr": addr
        }
        
        print(f"[GAME {self.game_id}] {name} -> {faction.upper()} ({len(self.players)}/{self.max_players})")
        
        # Se partita piena, inizia!
        if self.is_full():
            self.start_game()
        
        return faction
    
    def remove_player(self, conn):
        """Rimuovi giocatore"""
        if conn in self.players:
            player = self.players[conn]
            faction = player["faction"]
            
            # Restituisci fazione
            if faction not in self.available_factions:
                self.available_factions.append(faction)
            
            del self.players[conn]
            
            # Notifica altri
            self.broadcast({
                "type": "player_left",
                "name": player["name"],
                "faction": faction
            })
    
    def start_game(self):
        """Inizia partita"""
        self.started = True
        print(f"[GAME {self.game_id}] PARTITA INIZIATA!")
        
        # Invia conferma a tutti
        self.broadcast({
            "type": "game_start",
            "players": {p["faction"]: p["name"] for p in self.players.values()},
            "msg": "PARTITA INIZIATA!"
        })
    
    def handle_buy_unit(self, conn, data):
        """Gestisce acquisto unità"""
        # Broadcast a tutti
        player = self.players[conn]
        self.broadcast({
            "type": "unit_bought",
            "faction": player["faction"],
            "unit_type": data.get("unit_type"),
            "territory_id": data.get("territory_id")
        })
    
    def handle_attack(self, conn, data):
        """Gestisce attacco"""
        player = self.players[conn]
        self.broadcast({
            "type": "attack",
            "faction": player["faction"],
            "from_id": data.get("from_id"),
            "to_id": data.get("to_id"),
            "result": data.get("result")
        })
    
    def handle_end_turn(self, conn):
        """Gestisce fine turno"""
        player = self.players[conn]
        
        # Passa al prossimo
        self.current_faction_idx = (self.current_faction_idx + 1) % len(self.factions)
        if self.current_faction_idx == 0:
            self.current_turn += 1
        
        next_faction = self.factions[self.current_faction_idx]
        
        self.broadcast({
            "type": "turn_change",
            "faction": next_faction,
            "turn": self.current_turn,
            "msg": f"Turno di {next_faction.upper()}"
        })
    
    def broadcast(self, data, exclude=None):
        """Invia messaggio a tutti i giocatori"""
        for conn in list(self.players.keys()):
            if conn != exclude:
                try:
                    msg = pickle.dumps(data)
                    msg_len = len(msg).to_bytes(4, 'big')
                    conn.sendall(msg_len + msg)
                except:
                    pass


if __name__ == "__main__":
    print("=" * 60)
    print("AXIS & ALLIES 1942 - SERVER MULTIPLAYER")
    print("=" * 60)
    print()
    
    server = GameServer()
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n[SERVER] Spegnimento...")
    except Exception as e:
        print(f"[ERRORE] {e}")


