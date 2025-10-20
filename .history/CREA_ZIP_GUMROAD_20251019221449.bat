@echo off
echo ============================================
echo CREAZIONE ZIP PER GUMROAD
echo ============================================
echo.
echo Questo crea il file ZIP corretto da 29 MB
echo da caricare su Gumroad!
echo.
pause

echo.
echo [1/5] Creazione cartella temporanea...
if exist "TEMP_GUMROAD" rmdir /s /q "TEMP_GUMROAD"
mkdir "TEMP_GUMROAD"

echo.
echo [2/5] Copia files necessari...
copy "dist\AxisAllies1942.exe" "TEMP_GUMROAD\"
copy "mappa_bn.jpg" "TEMP_GUMROAD\"
copy "mappa_hd.jpg" "TEMP_GUMROAD\"
copy "centri.json" "TEMP_GUMROAD\"
copy "README_GUMROAD.txt" "TEMP_GUMROAD\LEGGI_PRIMA.txt"
copy "GUIDA_GIOCO.txt" "TEMP_GUMROAD\"

echo.
echo [3/5] Creazione file AVVIA.bat...
echo @echo off > "TEMP_GUMROAD\GIOCA.bat"
echo start "" "AxisAllies1942.exe" >> "TEMP_GUMROAD\GIOCA.bat"
echo exit >> "TEMP_GUMROAD\GIOCA.bat"

echo.
echo [4/5] Compressione in ZIP...
powershell -Command "Compress-Archive -Path 'TEMP_GUMROAD\*' -DestinationPath 'AxisAllies1942_v1.0.zip' -Force"

echo.
echo [5/5] Copia su Desktop...
copy "AxisAllies1942_v1.0.zip" "C:\Users\user\Desktop\"

echo.
echo [6/5] Verifica dimensione...
powershell -Command "Get-Item 'C:\Users\user\Desktop\AxisAllies1942_v1.0.zip' | Select-Object Name, @{Name='SizeMB';Expression={[math]::Round($_.Length/1MB,2)}}"

echo.
echo [7/5] Pulizia...
rmdir /s /q "TEMP_GUMROAD"

echo.
echo ============================================
echo [OK] ZIP CREATO SUL DESKTOP!
echo ============================================
echo.
echo File: AxisAllies1942_v1.0.zip
echo Dimensione: circa 29 MB
echo.
echo ORA:
echo 1. Vai su https://app.gumroad.com/products
echo 2. Modifica "wargames3"
echo 3. Elimina file vecchio (853 Bytes)
echo 4. Carica AxisAllies1942_v1.0.zip dal Desktop
echo 5. Salva!
echo.
pause

