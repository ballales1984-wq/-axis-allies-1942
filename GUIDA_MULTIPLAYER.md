# 🌐 GUIDA MULTIPLAYER - GreatWar3

## 🎮 GIOCARE ONLINE CON GLI AMICI!

GreatWar3 supporta partite **multiplayer online** fino a **5 giocatori** contemporanei!

---

## 🚀 SETUP RAPIDO (LAN/Stessa Rete)

### **🖥️ GIOCATORE 1 - HOST (Server)**

1. **Avvia il server**:
   - Doppio click su `AVVIA_SERVER.bat`
   - Vedrai il tuo **IP locale** (es: 192.168.1.100)
   - **Lascia la finestra aperta!**

2. **Condividi il tuo IP**:
   - Manda l'IP agli altri giocatori
   - Esempio: "Il mio IP è 192.168.1.100"

3. **Aspetta** che tutti si connettano

4. **Gioca**:
   - Quando tutti sono pronti, la partita inizia automaticamente!

---

### **👥 GIOCATORI 2-5 - CLIENT**

1. **Avvia il client**:
   - Doppio click su `AVVIA_CLIENT_MULTIPLAYER.bat`

2. **Inserisci**:
   - **Nome**: Il tuo nome (es: "Mario")
   - **IP Server**: L'IP dell'host (es: 192.168.1.100)

3. **Connetti**:
   - Il client si connette al server
   - Ti viene assegnata una fazione automaticamente

4. **Gioca**:
   - Aspetta il tuo turno
   - Gioca normalmente come in singolo

---

## 🌍 SETUP INTERNET (Giocare da Case Diverse)

### **Opzione 1: Hamachi/VPN** (Consigliato)

1. **Tutti scaricano** LogMeIn Hamachi (gratuito)
2. **Host crea** una rete Hamachi
3. **Altri si uniscono** alla rete
4. **Usate l'IP Hamachi** invece dell'IP locale
5. **Procedete** come LAN

### **Opzione 2: Port Forwarding**

**Solo per utenti avanzati:**

1. **Host** apre la porta 5555 sul router:
   - Accedi al router (192.168.1.1)
   - Trova "Port Forwarding"
   - Aggiungi regola: Porta 5555 → IP del tuo PC
   
2. **Host trova** il suo IP pubblico:
   - Vai su whatismyip.com
   - Condividi questo IP con gli amici

3. **Client** usano l'IP pubblico dell'host

⚠️ **Attenzione**: Aprire porte può essere un rischio di sicurezza!

---

## 🎮 COME FUNZIONA

### **Fazioni Assegnate Automaticamente**

I giocatori vengono assegnati in ordine:
1. **Primo** → USA (Blu)
2. **Secondo** → EUROPA (Rosso)
3. **Terzo** → RUSSIA (Viola)
4. **Quarto** → CINA (Giallo)
5. **Quinto** → AFRICA (Verde)

### **Sistema Turni**

- Ogni giocatore gioca **a turno**
- Solo il giocatore corrente può fare azioni
- Gli altri vedono le azioni in tempo reale
- Premi SPAZIO per passare al prossimo

### **Sincronizzazione**

Il server sincronizza:
- ✅ Acquisti unità
- ✅ Attacchi
- ✅ Movimenti
- ✅ Conquiste
- ✅ Turni
- ✅ Chat (se implementata)

---

## 📋 REQUISITI

### **Hardware:**
- Connessione internet stabile
- Almeno 1 Mbps di banda (multiplayer è leggero)

### **Software:**
- Python 3.7+ installato su TUTTE le macchine
- Dipendenze installate: `pip install -r requirements.txt`
- Firewall configurato per permettere porta 5555

### **Rete:**
- **LAN**: Stesso Wi-Fi o cavo Ethernet
- **Internet**: VPN (Hamachi) o Port Forwarding

---

## 🔧 RISOLUZIONE PROBLEMI

### **"Impossibile connettersi al server"**

**Cause possibili:**
1. Server non avviato → L'host deve avviare `AVVIA_SERVER.bat`
2. IP sbagliato → Verifica l'IP del server
3. Firewall blocca → Disabilita temporaneamente o aggiungi eccezione
4. Porta 5555 occupata → Chiudi altri programmi

**Soluzione:**
```
1. Host: Verifica che il server sia avviato
2. Host: Condividi nuovamente l'IP (ipconfig)
3. Client: Prova "localhost" se sei sulla stessa macchina
4. Entrambi: Disabilita firewall temporaneamente
```

### **"Partita piena"**

**Causa**: Già 5 giocatori connessi

**Soluzione**: Aspetta che qualcuno si disconnetta o crea un nuovo server

### **"Lag/Ritardo"**

**Causa**: Connessione lenta o instabile

**Soluzione:**
- Usa connessione cablata invece di Wi-Fi
- Chiudi download/streaming
- Avvicina il PC al router

---

## 🎯 MODALITÀ DI GIOCO

### **1. Hot Seat (Locale - Stesso PC)**
File: `GIOCA_HOT_SEAT.bat`
- Tutti i giocatori sullo stesso computer
- Si passa il mouse a turno
- Non serve rete

### **2. LAN (Rete Locale)**
File: `AVVIA_SERVER.bat` + client
- Giocatori sulla stessa rete
- Veloce e stabile
- Ideale per LAN party

### **3. Online (Internet)**
File: Server + client + Hamachi
- Giocatori da case diverse
- Serve VPN o port forwarding
- Latenza dipende dalla connessione

---

## 📝 COMANDI SERVER

**Durante l'esecuzione del server, puoi:**
- Vedere chi si connette
- Vedere le azioni dei giocatori
- Monitorare la partita
- Premere Ctrl+C per spegnere

**Output server:**
```
[SERVER] In ascolto su porta 5555
[SERVER] Nuova connessione da 192.168.1.101
[SERVER] Mario connesso
[GAME 1] Mario -> USA (1/5)
[SERVER] Luigi connesso
[GAME 1] Luigi -> EUROPA (2/5)
...
[GAME 1] PARTITA INIZIATA!
```

---

## 🎨 CHAT (Feature Futura)

Attualmente il multiplayer supporta:
- ✅ Azioni di gioco sincronizzate
- ✅ Turni sincronizzati
- ✅ Notifiche giocatori
- ⏳ Chat testuale (implementata ma non integrata nel gioco)

**Per usare la chat**: Serve integrare l'interfaccia nel gioco principale.

---

## 🏆 STRATEGIE MULTIPLAYER

### **Differenze vs Singolo:**
- 🤝 **Alleanze temporanee**: Accordati con altri giocatori
- 🎯 **Focus su 1 nemico**: Coordinate gli attacchi
- 💰 **Economia critica**: Proteggi territori redditizi
- 🔬 **Tech race**: Chi raggiunge per primo i Super Soldati vince
- 🛡️ **Difesa**: Costruisci difese pesanti, gli umani sono più imprevedibili dell'IA

### **Tattiche Vincenti:**
1. **Early game**: Compra scienziati, accumula tech velocemente
2. **Mid game**: Espandi territori, bilancia economia e esercito
3. **Late game**: Domina con Super Soldati e Hacker

---

## 📊 SPECIFICHE TECNICHE

**Protocollo**: TCP Socket  
**Porta**: 5555  
**Serializzazione**: Pickle (Python)  
**Max giocatori**: 5 (1 per fazione)  
**Sincronizzazione**: Server autoritativo  
**Latenza tipica**: 10-50ms (LAN), 50-200ms (Internet)  

---

## 🔮 FUTURE FEATURES

Possibili miglioramenti futuri:
- [ ] Chat integrata nel gioco con UI
- [ ] Lobby grafiche per scegliere fazione
- [ ] Spettatori che guardano senza giocare
- [ ] Replay delle partite
- [ ] Classifica online
- [ ] Matchmaking automatico
- [ ] Server dedicati pubblici

---

## 📞 SUPPORTO

**Problemi di connessione?**
- Controlla il firewall
- Verifica l'IP
- Prova prima in LAN

**Server non funziona?**
- Verifica che Python sia installato
- Verifica che le dipendenze siano installate
- Controlla la porta 5555 non sia occupata

**Partita si blocca?**
- Il server deve rimanere sempre attivo
- Se l'host si disconnette, la partita finisce
- Salva spesso (tasto S)

---

**Buone partite multiplayer!** 🎮🌐👥

*"La guerra è meglio con gli amici."* - GreatWar3 Multiplayer

