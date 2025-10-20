@echo off
echo ============================================
echo CREAZIONE PACCHETTO COMPLETO
echo ============================================
echo.

:: Verifica se l'EXE esiste
if not exist "dist\Axis_And_Allies_1942.exe" (
    echo ERRORE: EXE non trovato!
    echo Esegui prima CREA_EXE.bat
    echo.
    pause
    exit
)

:: Crea cartella pacchetto
echo [1/3] Creazione cartella pacchetto...
if exist "Axis_And_Allies_1942_Package" rmdir /s /q "Axis_And_Allies_1942_Package"
mkdir "Axis_And_Allies_1942_Package"

:: Copia file necessari
echo [2/3] Copia file...
copy "dist\Axis_And_Allies_1942.exe" "Axis_And_Allies_1942_Package\"
copy "centri.json" "Axis_And_Allies_1942_Package\"
copy "mappa_bn.jpg" "Axis_And_Allies_1942_Package\"
copy "mappa_hd.jpg" "Axis_And_Allies_1942_Package\"
copy "README.md" "Axis_And_Allies_1942_Package\"
copy "GIOCO_FINALE.md" "Axis_And_Allies_1942_Package\"
copy "SISTEMA_ESPANSIONE_E_MISSILI.md" "Axis_And_Allies_1942_Package\"
copy "PORTATA_UNITA.md" "Axis_And_Allies_1942_Package\"

:: Crea README per il pacchetto
echo [3/3] Creazione README...
(
echo ============================================
echo AXIS ^& ALLIES 1942 - ALLEANZE MONDIALI
echo ============================================
echo.
echo COME AVVIARE:
echo  1. Doppio click su Axis_And_Allies_1942.exe
echo  2. Aspetta che si apra la finestra di gioco
echo  3. Leggi GIOCO_FINALE.md per le istruzioni complete
echo.
echo REQUISITI:
echo  - Windows 10/11
echo  - Tutti i file nella stessa cartella
echo.
echo DOCUMENTAZIONE:
echo  - GIOCO_FINALE.md = Manuale completo
echo  - SISTEMA_ESPANSIONE_E_MISSILI.md = Territori e missili
echo  - PORTATA_UNITA.md = Sistema portata unita
echo  - README.md = Guida veloce
echo.
echo CARATTERISTICHE:
echo  - 5 fazioni giocabili
echo  - 100+ territori mondiali
echo  - Sistema 3 risorse (Soldi, Petrolio, Tecnologia)
echo  - Sviluppo territori progressivo
echo  - Missili a lungo raggio (livello 8+)
echo  - Portata differenziata (Fanteria 100px, Carri 200px, Aerei 500px)
echo  - IA avanzata per 4 fazioni
echo  - Bomba atomica (livello massimo)
echo.
echo CONTROLLI:
echo  - Click territorio = Apre armeria
echo  - A = Attacco
echo  - I = Info territorio
echo  - SPAZIO = Fine turno
echo  - ESC = Chiudi menu
echo.
echo Buon divertimento!
echo.
) > "Axis_And_Allies_1942_Package\LEGGIMI.txt"

echo.
echo ============================================
echo PACCHETTO CREATO!
echo ============================================
echo.
echo Cartella: Axis_And_Allies_1942_Package\
echo.
echo Puoi:
echo  1. Copiare la cartella su chiavetta USB
echo  2. Comprimere in ZIP e inviare
echo  3. Distribuire come vuoi!
echo.
pause

