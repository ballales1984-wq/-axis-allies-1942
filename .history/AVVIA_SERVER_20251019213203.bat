@echo off
echo ============================================
echo AXIS ^& ALLIES 1942 - SERVER MULTIPLAYER
echo ============================================
echo.
echo Avvio server sulla porta 5555...
echo.
echo IMPORTANTE:
echo - Lascia questa finestra aperta
echo - I giocatori si connetteranno a questo server
echo - Condividi il tuo IP con gli altri giocatori
echo.
echo Il tuo IP locale:
ipconfig | findstr /i "IPv4"
echo.
echo ============================================
echo.

python server_multiplayer.py

pause

