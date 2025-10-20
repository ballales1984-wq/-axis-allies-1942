@echo off
echo ============================================
echo AGGIORNAMENTO CON NOMI GEOGRAFICI CORRETTI
echo ============================================
echo.
echo NOVITA v1.2:
echo - Nomi citta corretti geograficamente!
echo - Bombardiere (nuova unita)
echo - Icone grafiche unita
echo - Commenti vocali
echo.
pause

echo.
echo [1/5] Pulizia vecchi file...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "AxisAllies1942.spec" del "AxisAllies1942.spec"

echo.
echo [2/5] Creazione EXE v1.2...
pyinstaller --onefile --windowed ^
    --add-data "mappa_bn.jpg;." ^
    --add-data "mappa_hd.jpg;." ^
    --add-data "centri.json;." ^
    --name "AxisAllies1942" ^
    gioco_avanzato.py

echo.
echo [3/5] Aggiornamento Desktop...
copy "dist\AxisAllies1942.exe" "C:\Users\user\Desktop\AxisAllies1942\"

echo.
echo [4/5] Creazione ZIP per Gumroad v1.2...
if exist "TEMP_GUMROAD" rmdir /s /q "TEMP_GUMROAD"
mkdir "TEMP_GUMROAD"
copy "dist\AxisAllies1942.exe" "TEMP_GUMROAD\"
copy "mappa_bn.jpg" "TEMP_GUMROAD\"
copy "mappa_hd.jpg" "TEMP_GUMROAD\"
copy "centri.json" "TEMP_GUMROAD\"
copy "README_GUMROAD.txt" "TEMP_GUMROAD\LEGGI_PRIMA.txt"
copy "GUIDA_GIOCO.txt" "TEMP_GUMROAD\"

echo @echo off > "TEMP_GUMROAD\GIOCA.bat"
echo start "" "AxisAllies1942.exe" >> "TEMP_GUMROAD\GIOCA.bat"
echo exit >> "TEMP_GUMROAD\GIOCA.bat"

echo.
echo [5/5] Compressione ZIP...
powershell -command "Compress-Archive -Path 'TEMP_GUMROAD\*' -DestinationPath 'C:\Users\user\Desktop\AxisAllies1942_v1.2.zip' -Force"

if exist "TEMP_GUMROAD" rmdir /s /q "TEMP_GUMROAD"

echo.
echo ============================================
echo [OK] AGGIORNAMENTO COMPLETATO!
echo ============================================
echo.
echo FILE CREATI:
echo - Desktop\AxisAllies1942\AxisAllies1942.exe (aggiornato)
echo - Desktop\AxisAllies1942_v1.2.zip (per Gumroad)
echo.
echo CARICA QUESTO NUOVO ZIP SU GUMROAD!
echo.
pause

