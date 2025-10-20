@echo off
cls
echo ============================================
echo AXIS ^& ALLIES 1942 - SCEGLI MODALITA
echo ============================================
echo.
echo 1 = SINGLEPLAYER (Tu vs IA)
echo     - Controlli USA
echo     - 4 IA nemiche
echo     - Gioca da solo
echo.
echo 2 = HOT SEAT (Passare PC tra amici)
echo     - 5 giocatori umani
echo     - Tutti sullo stesso PC
echo     - A turno!
echo.
echo 3 = MULTIPLAYER ONLINE [IN SVILUPPO]
echo     - Server/Client
echo     - Giocare in rete
echo.
echo Q = Esci
echo.
set /p choice="Scelta (1/2/3/Q): "

if "%choice%"=="1" goto singleplayer
if "%choice%"=="2" goto hotseat
if "%choice%"=="3" goto multiplayer
if /i "%choice%"=="Q" goto end

echo Scelta non valida!
timeout /t 2 > nul
goto start

:singleplayer
cls
echo.
echo ============================================
echo AVVIO SINGLEPLAYER...
echo ============================================
echo.
python gioco_avanzato.py
goto end

:hotseat
cls
echo.
echo ============================================
echo AVVIO HOT SEAT...
echo ============================================
echo.
echo Tutti i giocatori sullo stesso PC!
echo Passatevi il computer a turno.
echo.
timeout /t 2 > nul
python gioco_hotseat.py
goto end

:multiplayer
cls
echo.
echo ============================================
echo MULTIPLAYER ONLINE
echo ============================================
echo.
echo [IN SVILUPPO]
echo.
echo Per ora usa:
echo - SINGLEPLAYER (vs IA)
echo - HOT SEAT (passare PC)
echo.
timeout /t 3 > nul
goto start

:end

