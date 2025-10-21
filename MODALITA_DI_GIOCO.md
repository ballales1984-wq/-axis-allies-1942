# 🎮 MODALITÀ DI GIOCO - GreatWar3 v2.5

## 4 MODI PER GIOCARE!

GreatWar3 offre **4 modalità di gioco** diverse per adattarsi a ogni situazione!

---

## 1️⃣ SINGOLO (vs IA)

### **Descrizione:**
Gioca da solo contro **4 IA** controllate dal computer.

### **Caratteristiche:**
- ✅ Tu controlli **USA** (Blu)
- ✅ IA controlla: Europa, Russia, Cina, Africa
- ✅ IA ha bonus risorse iniziali
- ✅ IA attacca automaticamente
- ✅ Perfetto per imparare e praticare

### **Come Avviare:**
```
Doppio click su: GreatWar3 FINALE.lnk (Desktop)
Oppure: LAUNCHER.bat → Opzione [1]
```

### **Difficoltà:**
- IA inizia con più risorse (8000$ vs 5000$)
- IA ha vantaggio tecnologico (+50 tech)
- IA attacca in modo intelligente
- **Sfida**: Sconfiggere tutte le 4 IA!

### **Ideale Per:**
- 🎯 Giocatori singoli
- 📚 Imparare il gioco
- 🏆 Sfide personali
- ⏱️ Partite veloci (30-45 min)

---

## 2️⃣ HOT SEAT (Stesso PC)

### **Descrizione:**
Più giocatori sullo **stesso computer** si passano il mouse a turno.

### **Caratteristiche:**
- ✅ Fino a 5 giocatori
- ✅ Ogni giocatore controlla una fazione
- ✅ Nessuna IA, tutti umani
- ✅ Si gioca a turno sulla stessa macchina

### **Come Avviare:**
```
Doppio click su: GIOCA_HOT_SEAT.bat
Oppure: LAUNCHER.bat → Opzione [2]
```

### **Regole:**
1. Giocatore 1 (USA) fa il suo turno
2. Passa il mouse al Giocatore 2 (EUROPA)
3. Giocatore 2 fa il suo turno
4. E così via...
5. **Onore**: Non guardare territori/risorse altrui! 😄

### **Ideale Per:**
- 👨‍👩‍👧‍👦 Serate in famiglia
- 🎉 Feste con amici
- 🏠 Un solo PC disponibile
- 🎲 Atmosfera da gioco da tavolo

---

## 3️⃣ MULTIPLAYER LAN (Rete Locale)

### **Descrizione:**
Giocare su **PC diversi** ma sulla **stessa rete** (stesso Wi-Fi).

### **Caratteristiche:**
- ✅ Fino a 5 giocatori su PC diversi
- ✅ Ogni giocatore vede solo il proprio schermo
- ✅ Azioni sincronizzate in tempo reale
- ✅ Veloce e stabile (LAN)

### **Setup:**

**Host (Giocatore 1):**
```
1. Doppio click su: AVVIA_SERVER.bat
2. Trova il tuo IP (mostrato nella finestra)
   Esempio: 192.168.1.100
3. Condividi l'IP con gli altri giocatori
4. Lascia la finestra aperta!
```

**Altri Giocatori (2-5):**
```
1. Doppio click su: AVVIA_CLIENT_MULTIPLAYER.bat
2. Inserisci nome
3. Inserisci IP dell'host (es: 192.168.1.100)
4. Premi Enter
5. Aspetta che tutti si connettano
```

**Quando tutti sono connessi:**
```
[GAME 1] PARTITA INIZIATA!
→ Ogni giocatore gioca col proprio PC
→ Il server sincronizza tutto
```

### **Requisiti:**
- Tutti sulla stessa rete Wi-Fi o LAN
- Firewall non blocca porta 5555
- Python installato su tutti i PC

### **Ideale Per:**
- 🏠 LAN Party
- 👥 Amici nella stessa casa
- 🎮 Gaming serio con schermi separati
- ⚡ Connessione veloce e stabile

---

## 4️⃣ MULTIPLAYER ONLINE (Internet)

### **Descrizione:**
Giocare con amici **da case diverse** via Internet.

### **Caratteristiche:**
- ✅ Gioca con chiunque nel mondo
- ✅ Serve VPN (Hamachi) o Port Forwarding
- ✅ Tutte le funzionalità di LAN
- ⚠️ Più complesso da configurare

### **Setup con Hamachi (Facile):**

**Tutti i giocatori:**
```
1. Scarica LogMeIn Hamachi (gratis)
2. Installa e crea account
```

**Host:**
```
1. Crea una rete in Hamachi
2. Condividi nome rete e password
3. Avvia AVVIA_SERVER.bat
4. Usa l'IP Hamachi (es: 25.xxx.xxx.xxx)
```

**Altri Giocatori:**
```
1. Unisciti alla rete Hamachi dell'host
2. Avvia AVVIA_CLIENT_MULTIPLAYER.bat
3. Inserisci l'IP Hamachi dell'host
4. Gioca!
```

### **Setup con Port Forwarding (Avanzato):**

⚠️ **Solo per utenti esperti!**

**Host:**
```
1. Apri porta 5555 sul router
2. Trova IP pubblico (whatismyip.com)
3. Condividi IP pubblico
4. Avvia server
```

**Altri Giocatori:**
```
1. Usa IP pubblico dell'host
2. Connetti normalmente
```

### **Ideale Per:**
- 🌍 Giocare con amici lontani
- 🌐 Comunità online
- 📱 Discord/TeamSpeak party
- 🏆 Tornei online

---

## 📊 CONFRONTO MODALITÀ

| Feature | Singolo | Hot Seat | LAN | Online |
|---------|---------|----------|-----|--------|
| **Giocatori** | 1 | 2-5 | 2-5 | 2-5 |
| **PC necessari** | 1 | 1 | 2-5 | 2-5 |
| **Rete** | No | No | Wi-Fi | Internet |
| **Setup** | ⚡ Istantaneo | ⚡ Istantaneo | 🔧 Facile | 🔧 Medio |
| **Latency** | 0ms | 0ms | 10-50ms | 50-300ms |
| **IA** | 4 IA | No IA | No IA | No IA |
| **Difficoltà** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Divertimento** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🎯 QUALE SCEGLIERE?

### **Vuoi Imparare?**
→ **SINGOLO** (vs IA)
- Pratica senza pressione
- Impara meccaniche
- Testa strategie

### **Serata con Amici a Casa?**
→ **HOT SEAT** (stesso PC)
- Facile e veloce
- Nessuna configurazione
- Atmosfera conviviale

### **LAN Party?**
→ **MULTIPLAYER LAN**
- Ognuno col suo PC
- Esperienza competitiva
- Connessione perfetta

### **Amici Lontani?**
→ **MULTIPLAYER ONLINE**
- Gioca via Internet
- Usa Hamachi
- Discord per parlare

---

## 🏆 REGOLE MULTIPLAYER

### **Assegnazione Fazioni:**
Automatica in ordine di connessione:
1. **USA** (Blu) - Primo connesso
2. **EUROPA** (Rosso) - Secondo connesso
3. **RUSSIA** (Viola) - Terzo connesso
4. **CINA** (Giallo) - Quarto connesso
5. **AFRICA** (Verde) - Quinto connesso

### **Turni:**
- I giocatori giocano in ordine
- Solo il giocatore corrente può fare azioni
- Gli altri vedono le azioni in tempo reale
- Premi SPAZIO per passare al prossimo

### **Vittoria:**
- Conquista tutti gli 82 territori
- Elimina tutte le altre fazioni
- O domina con superiorità tecnologica

---

## 💡 CONSIGLI MULTIPLAYER

### **Per l'Host:**
- ✅ Usa connessione cablata (non Wi-Fi)
- ✅ Non chiudere la finestra del server
- ✅ Condividi chiaramente il tuo IP
- ✅ Testa prima in LAN

### **Per i Client:**
- ✅ Verifica l'IP dell'host
- ✅ Assicurati che il firewall non blocchi
- ✅ Connessione stabile (evita download)
- ✅ Pazienza durante la connessione

### **Per Tutti:**
- 🎤 Usa Discord/TeamSpeak per parlare
- 💾 Salva spesso (tasto S)
- ⏱️ Stabilisci tempo massimo per turno
- 🤝 Divertiti e gioca fair!

---

## 🔧 FILE LAUNCHER

Il **LAUNCHER.bat** è il modo più facile per scegliere:

```
╔════════════════════════════════════════╗
║     GREATWAR3 - LAUNCHER               ║
╠════════════════════════════════════════╣
║  [1] Singolo (vs IA)                   ║
║  [2] Hot Seat (stesso PC)              ║
║  [3] Multiplayer - CREA SERVER         ║
║  [4] Multiplayer - UNISCITI            ║
║  [5] Leggi Guida                       ║
║  [0] Esci                              ║
╚════════════════════════════════════════╝
```

**Doppio click** su `LAUNCHER GreatWar3.lnk` sul Desktop!

---

## 📝 NOTE IMPORTANTI

### **Porte di Rete:**
- Server usa porta: **5555**
- Assicurati sia aperta nel firewall

### **Compatibilità:**
- Tutti i giocatori devono avere la **stessa versione**
- Usa `GreatWar3_FINALE.exe` (v2.5)

### **Salvataggi:**
- Multiplayer: Salvato sul server
- Client vedono stato sincronizzato
- Se server chiude, partita finisce

---

## 🎯 FEATURE MULTIPLAYER

### **Attualmente Supportato:**
- ✅ Fino a 5 giocatori
- ✅ Sincronizzazione azioni
- ✅ Turni gestiti dal server
- ✅ Notifiche connessioni/disconnessioni
- ✅ Acquisto unità sincronizzato
- ✅ Combattimenti sincronizzati

### **In Sviluppo:**
- ⏳ Chat integrata nel gioco
- ⏳ Lobby grafica
- ⏳ Spettatori
- ⏳ Replay partite
- ⏳ Classifica online

---

**Scegli la modalità che preferisci e inizia a giocare!** 🎮🌍

*"La guerra è meglio con gli amici. Anche se li stai conquistando."* - GreatWar3 Multiplayer

