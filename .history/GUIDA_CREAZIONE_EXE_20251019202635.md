# 🎮 GUIDA CREAZIONE EXE

## 📦 **METODO FACILE (AUTOMATICO)**

### **Passo 1: Crea EXE**
```
Doppio click su: CREA_EXE.bat
```

Cosa fa:
- ✅ Installa PyInstaller
- ✅ Crea file EXE unico
- ✅ Include tutte le dipendenze
- ⏱️ Richiede 2-5 minuti

### **Passo 2: Crea Pacchetto Completo**
```
Doppio click su: CREA_PACCHETTO.bat
```

Cosa fa:
- ✅ Crea cartella `Axis_And_Allies_1942_Package`
- ✅ Copia EXE + tutti i file necessari
- ✅ Aggiunge documentazione
- ✅ Pronto per distribuire!

---

## 🛠️ **METODO MANUALE (AVANZATO)**

### **Requisiti:**
```bash
pip install pyinstaller
```

### **Crea EXE:**
```bash
pyinstaller --onefile --noconsole --name "Axis_And_Allies_1942" ^
    --add-data "centri.json;." ^
    --add-data "mappa_bn.jpg;." ^
    --add-data "mappa_hd.jpg;." ^
    gioco_avanzato.py
```

### **Parametri Spiegati:**
- `--onefile` = Un solo file EXE (più facile da distribuire)
- `--noconsole` = Nessuna finestra console nera
- `--name` = Nome del file EXE
- `--add-data` = Include file necessari (JSON, immagini)

### **File Creati:**
```
dist/
  └── Axis_And_Allies_1942.exe  ← Questo è l'EXE!

build/  (cartella temporanea, puoi cancellare)
Axis_And_Allies_1942.spec  (file configurazione)
```

---

## 📁 **COSA DISTRIBUIRE**

### **Opzione 1: Solo EXE (NON FUNZIONA)**
❌ L'EXE da solo NON basta!
- Mancano centri.json e immagini

### **Opzione 2: Pacchetto Completo (RACCOMANDATO)**
✅ Usa `CREA_PACCHETTO.bat` che crea:
```
Axis_And_Allies_1942_Package/
  ├── Axis_And_Allies_1942.exe
  ├── centri.json
  ├── mappa_bn.jpg
  ├── mappa_hd.jpg
  ├── README.md
  ├── GIOCO_FINALE.md
  ├── SISTEMA_ESPANSIONE_E_MISSILI.md
  ├── PORTATA_UNITA.md
  └── LEGGIMI.txt
```

### **Opzione 3: ZIP per Distribuzione**
```bash
1. Esegui CREA_PACCHETTO.bat
2. Click destro su "Axis_And_Allies_1942_Package"
3. Invia a → Cartella compressa
4. Invia il file ZIP!
```

---

## ⚠️ **PROBLEMI COMUNI**

### **Errore: PyInstaller non trovato**
```bash
# Soluzione:
pip install pyinstaller
# Oppure:
python -m pip install pyinstaller
```

### **Errore: File non trovati**
```
FileNotFoundError: centri.json
```
**Soluzione:** Assicurati che questi file siano nella stessa cartella dell'EXE:
- centri.json
- mappa_bn.jpg  
- mappa_hd.jpg

### **EXE troppo grande (>100MB)**
È normale! Include:
- Python
- Pygame
- Tutte le librerie
- Immagini

Per ridurre:
```bash
# Usa --onefile invece di --onedir
# Già fatto nello script!
```

### **Antivirus blocca l'EXE**
È normale per EXE creati con PyInstaller.

**Soluzioni:**
1. Aggiungi eccezione nell'antivirus
2. Usa `--onedir` invece di `--onefile` (crea cartella invece di singolo file)
3. Firma digitalmente l'EXE (richiede certificato)

---

## 🎯 **DISTRIBUZIONE**

### **Per Amici/Test:**
1. Crea pacchetto completo
2. Comprimi in ZIP
3. Invia via email/drive/dropbox

### **Per Pubblicazione:**
1. Crea pacchetto completo
2. Carica su:
   - itch.io (ideale per giochi indie)
   - GitHub Releases
   - Google Drive
   - Dropbox

### **Include nella Descrizione:**
```
REQUISITI:
- Windows 10/11
- 200 MB spazio libero
- Schermo 1400x800 o superiore

INSTALLAZIONE:
1. Scarica e estrai il ZIP
2. Doppio click su Axis_And_Allies_1942.exe
3. Divertiti!

NOTA: Potrebbe essere segnalato dall'antivirus
(è un falso positivo, l'EXE è sicuro)
```

---

## 🚀 **OTTIMIZZAZIONI AVANZATE**

### **EXE Più Piccolo:**
```bash
pyinstaller --onefile --noconsole ^
    --exclude-module matplotlib ^
    --exclude-module numpy ^
    --name "Axis_And_Allies_1942" ^
    gioco_avanzato.py
```

### **EXE con Icona Personalizzata:**
```bash
# Prima crea un file icon.ico
pyinstaller --onefile --noconsole ^
    --icon=icon.ico ^
    --name "Axis_And_Allies_1942" ^
    gioco_avanzato.py
```

### **Debug (con Console):**
```bash
# Toglie --noconsole per vedere errori
pyinstaller --onefile ^
    --name "Axis_And_Allies_1942" ^
    gioco_avanzato.py
```

---

## 📊 **DIMENSIONI FINALI**

### **Tipiche:**
- **EXE:** ~80-120 MB
- **centri.json:** ~50 KB
- **mappa_bn.jpg:** ~2-5 MB
- **mappa_hd.jpg:** ~2-5 MB
- **Totale:** ~90-130 MB

### **Compressa (ZIP):**
- **Totale:** ~40-60 MB

---

## ✅ **CHECKLIST FINALE**

Prima di distribuire, verifica:

- [ ] EXE creato con successo
- [ ] EXE si avvia senza errori
- [ ] Tutti i file inclusi nel pacchetto
- [ ] README incluso
- [ ] Testato su computer pulito (senza Python)
- [ ] Comprimi in ZIP
- [ ] Nome file chiaro (es: `Axis_And_Allies_1942_v1.0.zip`)

---

## 🎮 **PRONTO!**

Ora hai:
- ✅ EXE funzionante
- ✅ Pacchetto completo
- ✅ Documentazione
- ✅ Pronto per distribuire!

**Buona distribuzione! 🚀**

