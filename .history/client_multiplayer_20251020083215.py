"""
CLIENT MULTIPLAYER - Connessione al server
Da integrare in gioco_avanzato.py
"""

import socket
import threading
import pickle
import queue

class MultiplayerClient:
    """Client per connessione multiplayer"""
    
    def __init__(self, server_ip='localhost', server_port=5555):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = None
        self.connected = False
        
        self.my_faction = None
        self.game_id = None
        self.player_name = None
        
        # Coda messaggi ricevuti
        self.message_queue = queue.Queue()
        
        # Thread ricezione
        self.receive_thread = None
    
    def connect(self, player_name):
        """Connetti al server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_ip, self.server_port))
            
            self.player_name = player_name
            
            # Invia richiesta join
            self.send_data({
                "type": "join",
                "name": player_name
            })
            
            # Ricevi conferma
            response = self.receive_data()
            if response and response.get("type") == "joined":
                self.connected = True
                self.my_faction = response.get("faction")
                self.game_id = response.get("game_id")
                
                print(f"[CLIENT] Connesso! Sei {self.my_faction.upper()}")
                print(f"[CLIENT] Partita #{self.game_id}")
                
                # Avvia thread ricezione
                self.receive_thread = threading.Thread(target=self.receive_loop)
                self.receive_thread.daemon = True
                self.receive_thread.start()
                
                return True
            else:
                print("[CLIENT] Connessione fallita")
                return False
                
        except Exception as e:
            print(f"[CLIENT] Errore connessione: {e}")
            return False
    
    def disconnect(self):
        """Disconnetti dal server"""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        self.connected = False
        print("[CLIENT] Disconnesso")
    
    def send_data(self, data):
        """Invia dati al server"""
        if not self.socket:
            return False
        
        try:
            msg = pickle.dumps(data)
            msg_len = len(msg).to_bytes(4, 'big')
            self.socket.sendall(msg_len + msg)
            return True
        except:
            self.connected = False
            return False
    
    def receive_data(self):
        """Ricevi dati dal server"""
        try:
            # Lunghezza
            msg_len_bytes = self.socket.recv(4)
            if not msg_len_bytes:
                return None
            
            msg_len = int.from_bytes(msg_len_bytes, 'big')
            
            # Messaggio
            msg = b''
            while len(msg) < msg_len:
                chunk = self.socket.recv(min(msg_len - len(msg), 4096))
                if not chunk:
                    return None
                msg += chunk
            
            return pickle.loads(msg)
        except:
            return None
    
    def receive_loop(self):
        """Loop ricezione messaggi (thread separato)"""
        while self.connected:
            data = self.receive_data()
            if data:
                self.message_queue.put(data)
            else:
                self.connected = False
                break
        
        print("[CLIENT] Thread ricezione terminato")
    
    def get_messages(self):
        """Ottieni tutti i messaggi ricevuti"""
        messages = []
        while not self.message_queue.empty():
            try:
                messages.append(self.message_queue.get_nowait())
            except queue.Empty:
                break
        return messages
    
    # ===== COMANDI DI GIOCO =====
    
    def buy_unit(self, territory_id, unit_type):
        """Compra unità"""
        return self.send_data({
            "type": "buy_unit",
            "territory_id": territory_id,
            "unit_type": unit_type
        })
    
    def attack(self, from_id, to_id, result):
        """Attacco"""
        return self.send_data({
            "type": "attack",
            "from_id": from_id,
            "to_id": to_id,
            "result": result
        })
    
    def end_turn(self):
        """Fine turno"""
        return self.send_data({
            "type": "end_turn"
        })
    
    def chat_message(self, msg):
        """Messaggio chat"""
        return self.send_data({
            "type": "chat",
            "msg": msg
        })


# Test client standalone
if __name__ == "__main__":
    import time
    
    print("=" * 60)
    print("AXIS & ALLIES 1942 - CLIENT MULTIPLAYER TEST")
    print("=" * 60)
    
    name = input("Nome giocatore: ")
    server_ip = input("IP server (Enter = localhost): ").strip() or "localhost"
    
    client = MultiplayerClient(server_ip)
    
    if client.connect(name):
        print(f"\n[OK] Connesso come {client.my_faction.upper()}!")
        print("Comandi:")
        print("  q = Disconnetti")
        print("  c <msg> = Chat")
        print()
        
        try:
            while client.connected:
                # Controlla messaggi ricevuti
                messages = client.get_messages()
                for msg in messages:
                    print(f"[<-] {msg}")
                
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\n[CLIENT] Disconnessione...")
        finally:
            client.disconnect()
    else:
        print("[ERRORE] Impossibile connettersi al server")


