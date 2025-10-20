@echo off
echo ============================================
echo AXIS ^& ALLIES 1942 - GLOBO 3D
echo ============================================
echo.
echo Mappa mondiale su globo terrestre rotante!
echo.
echo CONTROLLI:
echo - Drag mouse = Ruota globo
echo - Click territorio = Seleziona
echo - SPAZIO = Fine turno
echo - ESC = Esci
echo.
echo Premi un tasto per iniziare...
pause > nul
echo.

python gioco_globo3d.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ============================================
    echo [INFO] Panda3D non installato!
    echo ============================================
    echo.
    echo Per giocare in 3D serve Panda3D.
    echo.
    set /p install="Installare ora? (S/N): "
    if /i "%install%"=="S" (
        echo.
        echo Installazione Panda3D...
        pip install panda3d
        echo.
        echo [OK] Prova di nuovo!
        timeout /t 3 > nul
        python gioco_globo3d.py
    )
)

pause

