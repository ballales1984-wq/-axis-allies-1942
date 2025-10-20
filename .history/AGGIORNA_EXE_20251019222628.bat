@echo off
echo ============================================
echo AGGIORNAMENTO EXE CON ICONE
echo ============================================
echo.
echo Creo nuovo EXE con le icone delle unita!
echo.
pause

echo.
echo [1/3] Rimozione vecchio EXE...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "AxisAllies1942.spec" del "AxisAllies1942.spec"

echo.
echo [2/3] Creazione nuovo EXE...
pyinstaller --onefile --windowed ^
    --add-data "mappa_bn.jpg;." ^
    --add-data "mappa_hd.jpg;." ^
    --add-data "centri.json;." ^
    --name "AxisAllies1942" ^
    gioco_avanzato.py

echo.
echo [3/3] Aggiornamento Desktop...
copy "dist\AxisAllies1942.exe" "C:\Users\user\Desktop\AxisAllies1942\"

echo.
echo [4/3] Creazione nuovo ZIP...
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

powershell -Command "Compress-Archive -Path 'TEMP_GUMROAD\*' -DestinationPath 'AxisAllies1942_v1.1_ICONE.zip' -Force"
copy "AxisAllies1942_v1.1_ICONE.zip" "C:\Users\user\Desktop\"
rmdir /s /q "TEMP_GUMROAD"

echo.
echo ============================================
echo [OK] EXE AGGIORNATO!
echo ============================================
echo.
echo Nuovo EXE in: C:\Users\user\Desktop\AxisAllies1942\
echo Nuovo ZIP in: C:\Users\user\Desktop\AxisAllies1942_v1.1_ICONE.zip
echo.
echo NOVITA v1.1:
echo - ICONE GRAFICHE per Fanteria, Carro, Aereo
echo - Menu armeria piu visivo
echo - Piu professionale!
echo.
echo Puoi aggiornare su Gumroad con questo nuovo ZIP!
echo.
pause

