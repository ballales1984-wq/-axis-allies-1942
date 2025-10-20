@echo off
echo ============================================
echo GREATWAR3 - MODALITA HOT SEAT
echo ============================================
echo.
echo Tutti i giocatori sullo stesso PC!
echo Ogni giocatore fa il suo turno, poi passa il PC.
echo.
echo 5 FAZIONI:
echo   - USA (Blu)
echo   - EUROPA (Rosso)
echo   - RUSSIA (Viola)
echo   - CINA (Giallo)
echo   - AFRICA (Verde)
echo.
echo Premi un tasto per iniziare...
pause > nul
echo.
echo Avvio gioco...
echo.

python gioco_hotseat.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRORE] Il gioco ha avuto un problema!
    pause
)


