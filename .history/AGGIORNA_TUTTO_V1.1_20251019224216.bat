@echo off
echo ============================================
echo AGGIORNAMENTO COMPLETO VERSIONE 1.1
echo ============================================
echo.
echo NOVITA v1.1:
echo - BOMBARDIERE (nuova unita!)
echo - ICONE GRAFICHE unita
echo - COMMENTI VOCALI
echo - Menu armeria migliorato
echo.
pause

echo.
echo [1/5] Pulizia vecchi file...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "AxisAllies1942.spec" del "AxisAllies1942.spec"

echo.
echo [2/5] Creazione EXE v1.1...
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
echo [4/5] Creazione ZIP per Gumroad...
if exist "TEMP_GUMROAD" rmdir /s /q "TEMP_GUMROAD"
mkdir "TEMP_GUMROAD"

copy "dist\AxisAllies1942.exe" "TEMP_GUMROAD\"
copy "mappa_bn.jpg" "TEMP_GUMROAD\"
copy "mappa_hd.jpg" "TEMP_GUMROAD\"
copy "centri.json" "TEMP_GUMROAD\"

echo @echo off > "TEMP_GUMROAD\GIOCA.bat"
echo start "" "AxisAllies1942.exe" >> "TEMP_GUMROAD\GIOCA.bat"
echo exit >> "TEMP_GUMROAD\GIOCA.bat"

echo. > "TEMP_GUMROAD\LEGGI_PRIMA.txt"
echo AXIS ^& ALLIES 1942 - v1.1 >> "TEMP_GUMROAD\LEGGI_PRIMA.txt"
echo ======================================== >> "TEMP_GUMROAD\LEGGI_PRIMA.txt"
echo. >> "TEMP_GUMROAD\LEGGI_PRIMA.txt"
echo NOVITA VERSIONE 1.1: >> "TEMP_GUMROAD\LEGGI_PRIMA.txt"
echo. >> "TEMP_GUMROAD\LEGGI_PRIMA.txt"
echo - BOMBARDIERE (nuova unita strategica!) >> "TEMP_GUMROAD\LEGGI_PRIMA.txt"
echo - ICONE GRAFICHE per tutte le unita >> "TEMP_GUMROAD\LEGGI_PRIMA.txt"
echo - COMMENTI VOCALI (voce che annuncia eventi!) >> "TEMP_GUMROAD\LEGGI_PRIMA.txt"
echo - Menu armeria piu visivo >> "TEMP_GUMROAD\LEGGI_PRIMA.txt"
echo. >> "TEMP_GUMROAD\LEGGI_PRIMA.txt"
echo CONTROLLI: >> "TEMP_GUMROAD\LEGGI_PRIMA.txt"
echo - V = Attiva/Disattiva voce >> "TEMP_GUMROAD\LEGGI_PRIMA.txt"
echo - 4 = Compra Bombardiere >> "TEMP_GUMROAD\LEGGI_PRIMA.txt"
echo. >> "TEMP_GUMROAD\LEGGI_PRIMA.txt"
echo DIVERTITI! >> "TEMP_GUMROAD\LEGGI_PRIMA.txt"

copy "GUIDA_GIOCO.txt" "TEMP_GUMROAD\"

powershell -Command "Compress-Archive -Path 'TEMP_GUMROAD\*' -DestinationPath 'AxisAllies1942_v1.1.zip' -Force"

copy "AxisAllies1942_v1.1.zip" "C:\Users\user\Desktop\"

rmdir /s /q "TEMP_GUMROAD"

echo.
echo [5/5] Verifica dimensione...
powershell -Command "Get-Item 'C:\Users\user\Desktop\AxisAllies1942_v1.1.zip' | Select-Object Name, @{Name='SizeMB';Expression={[math]::Round($_.Length/1MB,2)}}"

echo.
echo ============================================
echo [OK] VERSIONE 1.1 PRONTA!
echo ============================================
echo.
echo FILE CREATI:
echo.
echo Desktop\AxisAllies1942\AxisAllies1942.exe (AGGIORNATO!)
echo Desktop\AxisAllies1942_v1.1.zip (PER GUMROAD!)
echo.
echo NOVITA v1.1:
echo [+] Bombardiere (ATT:25, PORTATA:700, $3000)
echo [+] Icone grafiche unita
echo [+] Commenti vocali (Tasto V)
echo [+] Menu armeria migliorato
echo.
echo PRONTO PER:
echo 1. Giocare (doppio click icona Desktop)
echo 2. Aggiornare Gumroad (upload nuovo ZIP)
echo.
pause

