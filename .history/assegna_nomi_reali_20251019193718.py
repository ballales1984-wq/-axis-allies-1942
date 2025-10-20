"""
Assegna nomi reali di città/stati agli 82 territori
"""

import json

# 82 NOMI REALI di città/stati/regioni del mondo
NOMI_REALI = [
    # Europa (30)
    "Londra", "Parigi", "Berlino", "Roma", "Madrid", "Amsterdam", "Vienna", "Varsavia",
    "Praga", "Budapest", "Atene", "Istanbul", "Mosca", "San Pietroburgo", "Kiev",
    "Oslo", "Stoccolma", "Copenhagen", "Helsinki", "Dublino", "Lisbona", "Bruxelles",
    "Zurigo", "Monaco", "Belgrado", "Bucarest", "Sofia", "Minsk", "Riga", "Tallin",
    
    # Asia (25)
    "Tokyo", "Pechino", "Shanghai", "Delhi", "Mumbai", "Bangkok", "Singapore", "Manila",
    "Seoul", "Pyongyang", "Hanoi", "Hong Kong", "Taiwan", "Kuala Lumpur", "Jakarta",
    "Islamabad", "Kabul", "Tehran", "Baghdad", "Damasco", "Ankara", "Gerusalemme",
    "Riad", "Dubai", "Doha",
    
    # Americhe (15)
    "New York", "Washington", "Los Angeles", "Chicago", "Toronto", "Vancouver",
    "Città del Messico", "L'Avana", "Caracas", "Lima", "Rio de Janeiro", "San Paolo",
    "Buenos Aires", "Santiago", "Bogotà",
    
    # Africa (10)
    "Il Cairo", "Lagos", "Nairobi", "Johannesburg", "Addis Abeba", "Casablanca",
    "Tunisi", "Algeri", "Luanda", "Kinshasa",
    
    # Oceania (2)
    "Sydney", "Auckland"
]

# Carica centri esistenti
with open("centri.json", "r") as f:
    centri = json.load(f)

print("="*70)
print("ASSEGNAZIONE NOMI REALI AI TERRITORI")
print("="*70)

# Assegna nomi
for i, centro in enumerate(centri):
    if i < len(NOMI_REALI):
        centro["name"] = NOMI_REALI[i]
        print(f"{i:2d}. {NOMI_REALI[i]}")
    else:
        centro["name"] = f"Regione_{i}"

# Salva
with open("centri.json", "w") as f:
    json.dump(centri, f, indent=2)

print("="*70)
print(f"[OK] Assegnati {len(centri)} nomi reali!")
print("="*70)

