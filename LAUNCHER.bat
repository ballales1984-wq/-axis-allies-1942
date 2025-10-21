@echo off
chcp 65001 >nul
cls
color 0A
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║              🌍 GREATWAR3 - LAUNCHER PRINCIPALE 🌍             ║
echo ║                                                                ║
echo ║               Gioco di Guerra Strategico v2.5                  ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo.
echo ┌────────────────────────────────────────────────────────────────┐
echo │  SCEGLI MODALITÀ DI GIOCO:                                     │
echo └────────────────────────────────────────────────────────────────┘
echo.
echo   [1] 🎮 GIOCA SINGOLO (Tu vs IA)
echo       - Modalità classica
echo       - 4 nemici controllati dal computer
echo       - Tutte le nuove funzionalità
echo.
echo   [2] 🏠 GIOCA HOT SEAT (Stesso PC)
echo       - Tutti i giocatori sullo stesso computer
echo       - Si passa il mouse a turno
echo       - Perfetto per serate con amici
echo.
echo   [3] 🌐 MULTIPLAYER - CREA SERVER
echo       - Ospita una partita online
echo       - Fino a 5 giocatori da PC diversi
echo       - Condividi il tuo IP con gli amici
echo.
echo   [4] 🌐 MULTIPLAYER - UNISCITI A SERVER
echo       - Connettiti a una partita esistente
echo       - Serve l'IP dell'host
echo       - Gioca contro altri giocatori umani
echo.
echo   [5] 📖 LEGGI GUIDA MULTIPLAYER
echo.
echo   [0] ❌ ESCI
echo.
echo ════════════════════════════════════════════════════════════════
echo.

set /p SCELTA="Scelta (0-5): "

if "%SCELTA%"=="1" goto SINGOLO
if "%SCELTA%"=="2" goto HOTSEAT
if "%SCELTA%"=="3" goto SERVER
if "%SCELTA%"=="4" goto CLIENT
if "%SCELTA%"=="5" goto GUIDA
if "%SCELTA%"=="0" goto FINE

echo.
echo ❌ Scelta non valida!
timeout /t 2 >nul
goto :eof

:SINGOLO
cls
echo.
echo 🎮 AVVIO MODALITÀ SINGOLO...
echo.
start "" "dist\GreatWar3_FINALE.exe"
goto FINE

:HOTSEAT
cls
echo.
echo 🏠 AVVIO MODALITÀ HOT SEAT...
echo.
call GIOCA_HOT_SEAT.bat
goto FINE

:SERVER
cls
echo.
echo 🌐 AVVIO SERVER MULTIPLAYER...
echo.
call AVVIA_SERVER.bat
goto FINE

:CLIENT
cls
echo.
echo 🌐 CONNESSIONE A SERVER...
echo.
call AVVIA_CLIENT_MULTIPLAYER.bat
goto FINE

:GUIDA
cls
type GUIDA_MULTIPLAYER.md
echo.
echo.
pause
goto :eof

:FINE
exit

