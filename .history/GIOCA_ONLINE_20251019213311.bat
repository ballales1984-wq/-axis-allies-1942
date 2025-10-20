@echo off
echo ============================================
echo AXIS ^& ALLIES 1942 - MULTIPLAYER
echo ============================================
echo.
echo Scegli modalita:
echo.
echo 1 = Gioca SOLO (vs IA)
echo 2 = CREA partita online (tu sei l'host)
echo 3 = UNISCITI a partita
echo.
set /p choice="Scelta (1/2/3): "

if "%choice%"=="1" (
    echo.
    echo Avvio modalita SINGLEPLAYER...
    python gioco_avanzato.py
    goto end
)

if "%choice%"=="2" (
    echo.
    echo ============================================
    echo CREAZIONE SERVER
    echo ============================================
    echo.
    echo 1. Apro SERVER in nuova finestra
    echo 2. Apro GIOCO per te come HOST
    echo.
    echo Gli altri giocatori dovranno connettersi a:
    ipconfig | findstr /i "IPv4"
    echo Porta: 5555
    echo.
    echo Premi un tasto per continuare...
    pause > nul
    
    start "Server Axis & Allies" cmd /k python server_multiplayer.py
    timeout /t 2 /nobreak > nul
    
    echo.
    echo Avvio gioco...
    python gioco_avanzato.py
    goto end
)

if "%choice%"=="3" (
    echo.
    echo ============================================
    echo CONNESSIONE A PARTITA
    echo ============================================
    echo.
    set /p server_ip="IP del server (Enter = localhost): "
    if "%server_ip%"=="" set server_ip=localhost
    
    echo.
    echo Connessione a %server_ip%:5555...
    echo.
    echo [IN SVILUPPO]
    echo Per ora gioca in modalita SINGLEPLAYER!
    timeout /t 3 > nul
    python gioco_avanzato.py
    goto end
)

echo Scelta non valida!
timeout /t 2 > nul

:end
pause

