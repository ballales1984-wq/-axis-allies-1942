@echo off
echo ============================================
echo INSTALLAZIONE PANDA3D per GLOBO 3D
echo ============================================
echo.
echo Questo installerà Panda3D per il gioco 3D!
echo.
pause

echo.
echo [1/2] Installazione Panda3D...
pip install panda3d

echo.
echo [2/2] Test installazione...
python -c "from panda3d.core import *; print('[OK] Panda3D installato!')"

echo.
echo ============================================
echo [OK] PRONTO PER IL GLOBO 3D!
echo ============================================
echo.
echo Ora puoi avviare: GIOCA_GLOBO_3D.bat
echo.
pause

