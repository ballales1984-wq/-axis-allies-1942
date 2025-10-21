@echo off
chcp 65001 >nul
echo ============================================
echo GREATWAR3 - CLIENT MULTIPLAYER
echo ============================================
echo.
echo CONNESSIONE AL SERVER...
echo.
echo Per connetterti serve:
echo 1. L'IP del server (es: 192.168.1.100)
echo 2. Il server deve essere avviato
echo 3. La porta 5555 deve essere aperta
echo.
echo ============================================
echo.

set /p NOME="Il tuo nome giocatore: "
set /p SERVER_IP="IP del server (Enter = localhost): "

if "%SERVER_IP%"=="" set SERVER_IP=localhost

echo.
echo Connessione a %SERVER_IP%:5555 come %NOME%...
echo.

python -c "from client_multiplayer import MultiplayerClient; import time; client = MultiplayerClient('%SERVER_IP%'); client.connect('%NOME%') if client.connect('%NOME%') else print('Errore connessione'); time.sleep(1)"

echo.
echo ============================================
echo.
pause

