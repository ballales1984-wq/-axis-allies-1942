@echo off
echo ============================================
echo INSTALLAZIONE SISTEMA COMMENTI VOCALI
echo ============================================
echo.
echo Questo installa pyttsx3 per i commenti vocali!
echo.
echo La voce annuncera:
echo - Turni
echo - Attacchi
echo - Conquiste
echo - Difese
echo.
pause

echo.
echo [1/2] Installazione pyttsx3...
pip install pyttsx3

echo.
echo [2/2] Test voce...
python -c "import pyttsx3; engine = pyttsx3.init(); engine.say('Sistema vocale installato!'); engine.runAndWait(); print('[OK] Voce funzionante!')"

echo.
echo ============================================
echo [OK] SISTEMA VOCALE PRONTO!
echo ============================================
echo.
echo Ora avvia il gioco e sentirai i commenti!
echo.
echo CONTROLLI VOCE NEL GIOCO:
echo - V = Attiva/Disattiva voce
echo.
pause

