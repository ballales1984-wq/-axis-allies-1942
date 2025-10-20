"""
CORREGGI NOMI GEOGRAFICI
Assegna nomi di città che corrispondono alla posizione geografica reale
"""

import json
import random

# Database città per regione geografica
# Basato su mappa 1400x800 circa
CITTA_PER_REGIONE = {
    # EUROPA OCCIDENTALE (x < 250, y < 300)
    "europa_ovest": [
        "Londra", "Parigi", "Madrid", "Lisbona", "Amsterdam", "Bruxelles",
        "Dublino", "Edimburgo", "Glasgow", "Manchester", "Liverpool", 
        "Marsiglia", "Lione", "Bordeaux", "Nantes", "Porto"
    ],
    
    # EUROPA CENTRALE (250 < x < 400, y < 300)
    "europa_centrale": [
        "Berlino", "Vienna", "Praga", "Budapest", "Monaco", "Zurigo",
        "Brno", "Cracovia", "Dresda", "Stoccarda", "Francoforte",
        "Amburgo", "Hannover", "Lipsia", "Salisburgo", "Graz"
    ],
    
    # EUROPA ORIENTALE / RUSSIA OVEST (400 < x < 600, y < 300)
    "europa_est": [
        "Varsavia", "Kiev", "Minsk", "Riga", "Vilnius", "Tallin",
        "Mosca", "San Pietroburgo", "Volgograd", "Kazan", "Rostov",
        "Smolensk", "Tver", "Yaroslavl", "Nizhny Novgorod"
    ],
    
    # SCANDINAVIA (x < 400, y < 150)
    "scandinavia": [
        "Oslo", "Stoccolma", "Copenhagen", "Helsinki", "Bergen",
        "Göteborg", "Malmö", "Turku", "Tampere", "Trondheim",
        "Stavanger", "Uppsala", "Umeå", "Oulu"
    ],
    
    # EUROPA SUD / BALCANI (200 < x < 400, 300 < y < 450)
    "balcani": [
        "Roma", "Atene", "Istanbul", "Sofia", "Bucarest", "Belgrado",
        "Sarajevo", "Zagabria", "Lubiana", "Skopje", "Tirana",
        "Napoli", "Milano", "Torino", "Genova", "Bologna", "Firenze"
    ],
    
    # MEDIO ORIENTE (400 < x < 600, 300 < y < 500)
    "medio_oriente": [
        "Istanbul", "Tehran", "Baghdad", "Damasco", "Beirut", "Gerusalemme",
        "Amman", "Kuwait", "Riad", "Dubai", "Abu Dhabi", "Doha",
        "Muscat", "Sana'a", "Ankara", "Izmir", "Erevan", "Tbilisi"
    ],
    
    # AFRICA NORD (x < 400, y > 450)
    "africa_nord": [
        "Il Cairo", "Algeri", "Tunisi", "Casablanca", "Tripoli", "Rabat",
        "Alessandria", "Fès", "Marrakech", "Tangeri", "Orano",
        "Bengasi", "Khartum", "Addis Abeba"
    ],
    
    # AFRICA CENTRALE/SUD (x < 400, y > 550)
    "africa_sud": [
        "Kinshasa", "Lagos", "Nairobi", "Johannesburg", "Città del Capo",
        "Luanda", "Dar es Salaam", "Pretoria", "Durban", "Accra",
        "Abidjan", "Dakar", "Maputo", "Kampala", "Lusaka"
    ],
    
    # ASIA CENTRALE (600 < x < 800, 200 < y < 400)
    "asia_centrale": [
        "Tashkent", "Almaty", "Bishkek", "Dushanbe", "Ashgabat",
        "Astana", "Kabul", "Islamabad", "Karachi", "Lahore",
        "Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata"
    ],
    
    # ASIA EST (800 < x < 1000, 200 < y < 450)
    "asia_est": [
        "Pechino", "Shanghai", "Tokyo", "Seoul", "Pyongyang", "Hong Kong",
        "Taipei", "Bangkok", "Hanoi", "Singapore", "Manila",
        "Giacarta", "Kuala Lumpur", "Phnom Penh", "Vientiane",
        "Ulaanbaatar", "Chongqing", "Guangzhou", "Shenzhen"
    ],
    
    # RUSSIA EST / SIBERIA (x > 600, y < 200)
    "siberia": [
        "Novosibirsk", "Yekaterinburg", "Omsk", "Krasnoyarsk", "Irkutsk",
        "Vladivostok", "Khabarovsk", "Tomsk", "Tyumen", "Barnaul",
        "Chelyabinsk", "Ufa", "Perm", "Yakutsk"
    ],
    
    # OCEANIA (900 < x < 1100, y > 500)
    "oceania": [
        "Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide",
        "Auckland", "Wellington", "Christchurch", "Canberra",
        "Hobart", "Darwin", "Gold Coast", "Newcastle"
    ],
    
    # NORD AMERICA (x > 1100, y < 400)
    "nord_america": [
        "New York", "Los Angeles", "Chicago", "Houston", "Toronto",
        "Montreal", "Vancouver", "San Francisco", "Boston", "Miami",
        "Seattle", "Washington", "Philadelphia", "Detroit", "Dallas",
        "Atlanta", "Phoenix", "Las Vegas", "San Diego", "Denver"
    ],
    
    # CENTRO/SUD AMERICA (x > 1100, y > 400)
    "sud_america": [
        "Città del Messico", "San Paolo", "Rio de Janeiro", "Buenos Aires",
        "Lima", "Bogotà", "Santiago", "Caracas", "L'Avana", "Brasilia",
        "Monterrey", "Guadalajara", "Medellín", "Quito", "Montevideo",
        "Asunción", "La Paz", "Panama", "San José", "Managua"
    ]
}

def determina_regione(x, y):
    """Determina la regione geografica in base alle coordinate"""
    
    # Mappa circa 1400x800
    
    # SCANDINAVIA (nord europa)
    if y < 150 and x < 400:
        return "scandinavia"
    
    # SIBERIA / RUSSIA EST (nord asia)
    if y < 200 and x > 600:
        return "siberia"
    
    # NORD AMERICA (ovest, nord)
    if x > 1100 and y < 400:
        return "nord_america"
    
    # SUD AMERICA (ovest, sud)
    if x > 1100 and y >= 400:
        return "sud_america"
    
    # OCEANIA (est-sud asia)
    if x > 900 and y > 500:
        return "oceania"
    
    # EUROPA OCCIDENTALE
    if x < 250 and 150 <= y < 300:
        return "europa_ovest"
    
    # EUROPA CENTRALE
    if 250 <= x < 400 and y < 300:
        return "europa_centrale"
    
    # EUROPA ORIENTALE / RUSSIA OVEST
    if 400 <= x < 600 and y < 300:
        return "europa_est"
    
    # BALCANI / SUD EUROPA
    if 200 <= x < 400 and 300 <= y < 450:
        return "balcani"
    
    # MEDIO ORIENTE
    if 400 <= x < 650 and 300 <= y < 500:
        return "medio_oriente"
    
    # AFRICA NORD
    if x < 400 and 450 <= y < 550:
        return "africa_nord"
    
    # AFRICA SUD
    if x < 400 and y >= 550:
        return "africa_sud"
    
    # ASIA CENTRALE
    if 600 <= x < 800 and 200 <= y < 500:
        return "asia_centrale"
    
    # ASIA EST
    if 800 <= x <= 1000 and 200 <= y < 500:
        return "asia_est"
    
    # Default: Europa centrale
    return "europa_centrale"

def correggi_nomi():
    """Corregge i nomi delle città in base alla posizione geografica"""
    
    print("="*60)
    print("CORREZIONE NOMI GEOGRAFICI")
    print("="*60)
    print()
    
    # Carica territori
    with open("centri.json", "r", encoding="utf-8") as f:
        territories = json.load(f)
    
    print(f"[OK] Caricati {len(territories)} territori")
    print()
    
    # Conta regioni
    regioni_count = {}
    nomi_usati = set()
    
    # Prima passa: conta quanti territori per regione
    for terr in territories:
        regione = determina_regione(terr["x"], terr["y"])
        regioni_count[regione] = regioni_count.get(regione, 0) + 1
    
    print("DISTRIBUZIONE REGIONI:")
    for reg, count in sorted(regioni_count.items()):
        print(f"  {reg:20s}: {count:3d} territori")
    print()
    
    # Seconda passa: assegna nomi
    backup_cities = []
    
    for terr in territories:
        x, y = terr["x"], terr["y"]
        regione = determina_regione(x, y)
        
        # Prendi città disponibili per quella regione
        citta_disponibili = [
            c for c in CITTA_PER_REGIONE[regione] 
            if c not in nomi_usati
        ]
        
        # Se non ci sono più città disponibili, usa da altre regioni vicine
        if not citta_disponibili:
            print(f"[!] Regione {regione} esaurita! Uso città generiche...")
            
            # Regioni vicine
            regioni_vicine = {
                "europa_ovest": ["europa_centrale", "balcani", "scandinavia"],
                "europa_centrale": ["europa_ovest", "europa_est", "balcani"],
                "europa_est": ["europa_centrale", "siberia", "asia_centrale"],
                "scandinavia": ["europa_ovest", "europa_centrale", "siberia"],
                "balcani": ["europa_centrale", "medio_oriente", "africa_nord"],
                "medio_oriente": ["balcani", "asia_centrale", "africa_nord"],
                "africa_nord": ["balcani", "medio_oriente", "africa_sud"],
                "africa_sud": ["africa_nord"],
                "asia_centrale": ["europa_est", "medio_oriente", "asia_est", "siberia"],
                "asia_est": ["asia_centrale", "siberia", "oceania"],
                "siberia": ["europa_est", "asia_centrale", "asia_est"],
                "oceania": ["asia_est"],
                "nord_america": ["sud_america"],
                "sud_america": ["nord_america"]
            }
            
            # Prova regioni vicine
            for reg_vicina in regioni_vicine.get(regione, []):
                citta_disponibili = [
                    c for c in CITTA_PER_REGIONE[reg_vicina]
                    if c not in nomi_usati
                ]
                if citta_disponibili:
                    break
            
            # Se ancora nessuna, usa backup
            if not citta_disponibili:
                citta_disponibili = [f"Città-{len(nomi_usati)+1}"]
        
        # Scegli nome
        nome = citta_disponibili[0]
        terr["name"] = nome
        nomi_usati.add(nome)
        
        print(f"  [{terr['id']:3d}] {nome:20s} @ ({x:4d}, {y:3d}) -> {regione}")
    
    # Salva
    with open("centri.json", "w", encoding="utf-8") as f:
        json.dump(territories, f, indent=2, ensure_ascii=False)
    
    print()
    print("="*60)
    print(f"[OK] Salvati {len(territories)} territori con nomi corretti!")
    print("="*60)
    print()
    print("FATTO! Ora i nomi corrispondono alle posizioni geografiche reali!")

if __name__ == "__main__":
    correggi_nomi()

