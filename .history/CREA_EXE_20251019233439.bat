@echo off
echo ============================================
echo CREAZIONE EXE - AXIS ^& ALLIES 1942
echo ============================================
echo.

echo [1/4] Installazione PyInstaller...
pip install pyinstaller

echo.
echo [2/4] Pulizia build precedenti...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "Axis_And_Allies_1942.spec" del "Axis_And_Allies_1942.spec"

echo.
echo [3/4] Creazione EXE (questo richiede qualche minuto)...
pyinstaller --onefile --noconsole --name "Axis_And_Allies_1942" --icon=NONE --add-data "centri.json;." --add-data "mappa_bn.jpg;." --add-data "mappa_hd.jpg;." gioco_avanzato.py

echo.
echo [4/4] Pulizia file temporanei...
if exist build rmdir /s /q build
if exist "Axis_And_Allies_1942.spec" del "Axis_And_Allies_1942.spec"

echo.
echo ============================================
echo COMPLETATO!
echo ============================================
echo.
echo Il file EXE si trova in: dist\Axis_And_Allies_1942.exe
echo.
echo Puoi distribuire il file EXE insieme a:
echo  - centri.json
echo  - mappa_bn.jpg
echo  - mappa_hd.jpg
echo.
echo Oppure usa CREA_PACCHETTO.bat per creare un ZIP completo!
echo.
pause

