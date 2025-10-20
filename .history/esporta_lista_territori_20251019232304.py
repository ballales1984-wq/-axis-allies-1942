"""
Esporta la lista dei territori in un file di testo
per facilitare l'inserimento dei nomi reali
"""
import json
import sys
import os

def resource_path(relative_path):
    """Trova il percorso corretto per le risorse"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Carica territori
with open(resource_path("centri.json"), 'r', encoding='utf-8') as f:
    territories = json.load(f)

# Crea file di testo
output_file = "LISTA_TERRITORI_DA_COMPILARE.txt"

with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=" * 70 + "\n")
    f.write("LISTA TERRITORI - AXIS & ALLIES 1942\n")
    f.write("=" * 70 + "\n\n")
    f.write("Istruzioni:\n")
    f.write("-----------\n")
    f.write("1. Apri 'visualizza_mappa_numeri.py' per vedere la mappa con i numeri\n")
    f.write("2. Per ogni territorio, scrivi il nome reale dopo il '->'\n")
    f.write("3. Salva questo file e mandalo indietro\n\n")
    f.write("Formato: ID | Nome Attuale -> NOME_REALE\n\n")
    f.write("=" * 70 + "\n\n")
    
    for t in territories:
        line = f"{t['id']:3d} | {t['name']:20s} -> ___________________________\n"
        f.write(line)
    
    f.write("\n" + "=" * 70 + "\n")
    f.write(f"TOTALE: {len(territories)} territori\n")
    f.write("=" * 70 + "\n")

print(f"\n✅ File creato: {output_file}")
print(f"📝 {len(territories)} territori da compilare")
print("\nOra:")
print("1. Apri 'visualizza_mappa_numeri.py' per vedere i numeri sulla mappa")
print("2. Compila il file TXT con i nomi reali")
print("3. Mandami il file compilato!\n")

