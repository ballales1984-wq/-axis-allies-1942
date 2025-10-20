"""
Converte la mappa in bianco e nero
"""

from PIL import Image

# Carica mappa
img = Image.open("mappa_hd.jpg")

# Converti in bianco e nero
img_bn = img.convert('L')  # Scala di grigi
img_bn = img_bn.convert('RGB')  # Torna a RGB ma grigio

# Ridimensiona
img_bn = img_bn.resize((1400, 800))

# Salva
img_bn.save("mappa_bn.jpg")

print("[OK] Mappa convertita in bianco e nero: mappa_bn.jpg")

