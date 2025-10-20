@echo off
echo ============================================
echo CREAZIONE EXE PER DISTRIBUZIONE GUMROAD
echo ============================================
echo.
echo Questo script crea un pacchetto completo per Gumroad:
echo - EXE del gioco
echo - File necessari
echo - README
echo - Licenza
echo.
echo Premi un tasto per iniziare...
pause > nul

echo.
echo [1/5] Installazione PyInstaller...
pip install pyinstaller

echo.
echo [2/5] Creazione EXE...
pyinstaller --onefile --windowed --icon=NONE ^
    --add-data "mappa_bn.jpg;." ^
    --add-data "mappa_hd.jpg;." ^
    --add-data "centri.json;." ^
    --name "AxisAllies1942" ^
    gioco_avanzato.py

echo.
echo [3/5] Creazione cartella distribuzione...
if not exist "DISTRIBUZIONE_GUMROAD" mkdir DISTRIBUZIONE_GUMROAD
if not exist "DISTRIBUZIONE_GUMROAD\AxisAllies1942" mkdir DISTRIBUZIONE_GUMROAD\AxisAllies1942

echo.
echo [4/5] Copia file...
copy "dist\AxisAllies1942.exe" "DISTRIBUZIONE_GUMROAD\AxisAllies1942\"
copy "mappa_bn.jpg" "DISTRIBUZIONE_GUMROAD\AxisAllies1942\"
copy "mappa_hd.jpg" "DISTRIBUZIONE_GUMROAD\AxisAllies1942\"
copy "centri.json" "DISTRIBUZIONE_GUMROAD\AxisAllies1942\"
copy "README_GUMROAD.txt" "DISTRIBUZIONE_GUMROAD\AxisAllies1942\"
copy "LICENZA.txt" "DISTRIBUZIONE_GUMROAD\AxisAllies1942\"
copy "GUIDA_GIOCO.txt" "DISTRIBUZIONE_GUMROAD\AxisAllies1942\"

echo.
echo [5/5] Creazione ZIP per Gumroad...
cd DISTRIBUZIONE_GUMROAD
powershell Compress-Archive -Path "AxisAllies1942" -DestinationPath "AxisAllies1942_v1.0.zip" -Force
cd ..

echo.
echo ============================================
echo [OK] PACCHETTO PRONTO!
echo ============================================
echo.
echo File creato: DISTRIBUZIONE_GUMROAD\AxisAllies1942_v1.0.zip
echo.
echo Dimensione: 
dir "DISTRIBUZIONE_GUMROAD\AxisAllies1942_v1.0.zip"
echo.
echo PROSSIMO PASSO:
echo 1. Carica su Gumroad: AxisAllies1942_v1.0.zip
echo 2. Prezzo: 1 EUR
echo 3. Usa descrizione in: DESCRIZIONE_GUMROAD.txt
echo.
pause

