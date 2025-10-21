# 🔊 CONTROLLO VOLUME VOCE - GreatWar3 v2.5

## 🎵 NUOVO SISTEMA AUDIO INTERATTIVO

Ora puoi regolare il **volume** e la **velocità** della voce in tempo reale durante il gioco!

---

## 🎮 CONTROLLI AUDIO

### **Volume**
| Tasto | Funzione | Incremento |
|--------|----------|------------|
| **+** o **=** | Volume SU | +10% |
| **-** | Volume GIÙ | -10% |

**Range**: 0% - 100%  
**Default**: 50%  
**Passo**: 10% per pressione

### **Velocità Voce**
| Tasto | Funzione | Incremento |
|--------|----------|------------|
| **[** | Velocità GIÙ | -20 parole/min |
| **]** | Velocità SU | +20 parole/min |

**Range**: 80 - 250 parole/min  
**Default**: 150 parole/min  
**Passo**: 20 parole/min per pressione

### **On/Off**
| Tasto | Funzione |
|--------|----------|
| **V** | Toggle voce On/Off |

---

## 📊 INDICATORE VISIVO

### **Angolo Alto Destra**

**Quando voce è ATTIVA:**
```
🔊 [██████████░░] 50%
      +/- Volume
```

**Quando voce è DISATTIVA:**
```
🔇 
```

### **Elementi:**
- **Icona**: 🔊 (attiva) o 🔇 (disattiva)
- **Barra**: Barra verde che si riempie con il volume
- **Percentuale**: Numero da 0% a 100%
- **Help**: Testo "+/- Volume" sotto la barra

---

## 🎨 BARRA VOLUME VISUALE

### **Design:**
```
┌─────────────────────┐
│ 🔊 [████████░░] 50% │ ← Voce attiva, volume 50%
│       +/- Volume    │
└─────────────────────┘
```

### **Colori:**
- Sfondo barra: Grigio scuro (40, 40, 60)
- Riempimento: Verde brillante (100, 255, 100)
- Bordo: Grigio chiaro (150, 150, 200)
- Testo: Bianco

### **Dimensioni:**
- Larghezza barra: 120px
- Altezza barra: 12px
- Posizione: 180px dal bordo destro, 10px dall'alto

---

## 🎯 ESEMPI D'USO

### **Scenario 1: Volume Troppo Alto**
```
1. Senti la voce troppo forte
2. Premi [-] 3 volte
3. Volume: 50% → 40% → 30% → 20%
4. Vedi messaggio: "Volume Voce: 20%"
5. Barra si accorcia in tempo reale
```

### **Scenario 2: Volume Troppo Basso**
```
1. Non senti bene la voce
2. Premi [+] 5 volte
3. Volume: 50% → 60% → 70% → 80% → 90% → 100%
4. Vedi messaggio: "Volume Voce: 100%"
5. Barra diventa completamente piena
```

### **Scenario 3: Voce Troppo Veloce**
```
1. La voce parla troppo velocemente
2. Premi [[] 2 volte
3. Velocità: 150 → 130 → 110 parole/min
4. Vedi messaggio: "Velocità Voce: 110 wpm"
5. La voce rallenta
```

### **Scenario 4: Voce Troppo Lenta**
```
1. La voce è troppo lenta
2. Premi []] 3 volte
3. Velocità: 150 → 170 → 190 → 210 parole/min
4. Vedi messaggio: "Velocità Voce: 210 wpm"
5. La voce accelera
```

### **Scenario 5: Silenziare Completamente**
```
Opzione 1: Premi [V] per disattivare
  → Icona diventa 🔇
  → Barra scompare
  → Nessun commento vocale

Opzione 2: Premi [-] fino a 0%
  → Volume: 0%
  → Voce rimane attiva ma silenziosa
```

---

## 🔧 FUNZIONALITÀ

### **Regolazione in Tempo Reale**
- Volume e velocità cambiano **immediatamente**
- Non serve riavviare il gioco
- Modifiche valide per tutta la sessione

### **Feedback Visivo**
- **Barra verde** mostra livello volume
- **Percentuale** numerica sempre visibile
- **Icona** cambia con stato on/off
- **Messaggio** conferma ogni modifica

### **Feedback Audio**
- Non c'è beep o suono di conferma
- Il volume cambia e sentirai la differenza al prossimo annuncio
- La velocità cambia al prossimo annuncio

---

## 📱 INTERFACCIA UTENTE

### **Posizione Indicatore:**
```
┌──────────────────────────────────────────────────────────┐
│ TURNO 5: USA                    🔊 [████████] 80%       │
│ $5000 | 1200P | 350T                +/- Volume          │
└──────────────────────────────────────────────────────────┘
                                      ↑
                              Angolo in alto a destra
```

### **Stati Possibili:**

**Volume 0% (Muto):**
```
🔊 [░░░░░░░░░░] 0%
```

**Volume 50% (Medio - Default):**
```
🔊 [█████░░░░░] 50%
```

**Volume 100% (Massimo):**
```
🔊 [██████████] 100%
```

**Voce Disattivata:**
```
🔇
```

---

## 🎛️ CONFIGURAZIONE AVANZATA

### **Limiti Volume:**
- **Minimo**: 0% (muto ma voce attiva)
- **Massimo**: 100% (volume pieno)
- **Incremento**: 10% per pressione tasto
- **Totale step**: 10 livelli (0, 10, 20, ..., 100)

### **Limiti Velocità:**
- **Minimo**: 80 parole/min (molto lenta)
- **Massimo**: 250 parole/min (velocissima)
- **Incremento**: 20 parole/min per pressione
- **Default**: 150 parole/min (normale)
- **Totale step**: 9 livelli

---

## 💡 CONSIGLI D'USO

### **Per Giocare Concentrato:**
```
Volume: 20-30%
Velocità: 130 wpm
→ Annunci discreti che non distraggono
```

### **Per Giocare Coinvolto:**
```
Volume: 70-80%
Velocità: 150-170 wpm
→ Esperienza immersiva e dinamica
```

### **Per Partite Notturne:**
```
Volume: 10%
Velocità: 110 wpm
→ Voce bassa e lenta per non disturbare
```

### **Per Streaming/Video:**
```
Volume: 60-70%
Velocità: 150 wpm
→ Ottimo per registrazioni e spiegazioni
```

---

## 🎤 ANNUNCI VOCALI

Il gioco annuncia:
- 📢 **Inizio turno**: "Turno di USA"
- ⚔️ **Attacchi**: "USA attacca Russia"
- 🏴 **Conquiste**: "Giappone viene conquistata!"
- 🛡️ **Difese**: "Francia resiste all'attacco!"
- 🔬 **Upgrade tech**: "USA raggiunge il livello Era Digitale!"
- ☢️ **Bombe atomiche**: "Attenzione! Bomba atomica su Cina!"
- 🏆 **Vittoria**: "USA ha vinto la guerra mondiale!"

---

## 🐛 TROUBLESHOOTING

### **Non Sento la Voce**

**Possibili cause:**
1. Volume a 0% → Premi [+] più volte
2. Voce disattivata → Premi [V] per attivarla
3. Sistema TTS non disponibile → Verifica Python pyttsx3

**Soluzione rapida:**
```
1. Premi [V] per attivare
2. Premi [+] 5 volte (volume a 100%)
3. Aspetta un evento (es: passa turno)
4. Dovresti sentire "Turno di..."
```

### **Voce Troppo Veloce/Lenta**

**Troppo veloce (parla incomprensibile):**
- Premi [[] ripetutamente
- Porta a 110-130 wpm

**Troppo lenta (noiosa):**
- Premi []] ripetutamente
- Porta a 170-190 wpm

### **Voce in Lingua Sbagliata**

Il sistema cerca automaticamente voci italiane, ma potrebbe usare inglese.  
**Al momento**: Non c'è controllo manuale lingue (feature futura)

---

## 📊 STATISTICHE

### **Configurazione Default:**
```
Volume: 50%
Velocità: 150 parole/min
Lingua: Italiano (se disponibile)
Stato: Attiva
```

### **Range Completi:**
```
Volume: 0% → 10% → 20% → ... → 100%
Velocità: 80 → 100 → 120 → ... → 250 wpm
```

### **Tasti Totali:**
```
4 tasti: +, -, [, ]
1 toggle: V
```

---

## 🚀 COME TESTARE

1. **Avvia** il gioco: `GreatWar3 FINALE.lnk`
2. **Guarda in alto a destra**: Vedi 🔊 con barra?
3. **Premi +**: Volume sale al 60%, barra si allunga
4. **Premi -**: Volume scende al 40%, barra si accorcia
5. **Passa turno** (SPAZIO): Senti "Turno di..."
6. **Regola** fino al volume perfetto!

---

## 📝 FILE MODIFICATI

- ✅ **voce_commenti.py**:
  - `volume_up()` - Aumenta volume
  - `volume_down()` - Diminuisce volume
  - `speed_up()` - Aumenta velocità
  - `speed_down()` - Diminuisce velocità
  - `get_volume()` - Ottieni volume corrente
  - `get_rate()` - Ottieni velocità corrente

- ✅ **gioco_avanzato.py**:
  - Tasti +/- per volume
  - Tasti [ ] per velocità
  - Indicatore visivo in alto a destra
  - Barra animata in tempo reale

---

## 🎯 VANTAGGI

✨ **Personalizzazione Totale**: Regola come preferisci  
✨ **Tempo Reale**: Cambi istantanei senza riavvio  
✨ **Feedback Visivo**: Vedi cosa stai modificando  
✨ **Messaggi Chiari**: Conferma ogni cambio  
✨ **Persistente**: Impostazioni valide per tutta la partita  

---

**Il controllo audio rende l'esperienza di gioco completamente personalizzabile!** 🎵🎮

*"Il volume perfetto rende perfetta la guerra."* - Audio System v2.5

