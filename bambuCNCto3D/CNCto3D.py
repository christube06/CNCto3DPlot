# Created By : Christube
# Date: 01/06/2025

import zipfile
import os
import shutil
import tempfile

def modifica_gcode(file_input, file_output):
    routermode = 0
    # Leggi il file di input riga per riga
    with open(file_input, 'r') as f:
        righe = f.readlines()

    # Inserisci 'G28' tra la riga 12 e 13
    if len(righe) >= 13:
        righe.insert(12, "G28\n")
    else:
        print("Attenzione: il file ha meno di 13 righe. Inserimento G28 saltato.")

    # Inserisci 'G1 X50 Y50' e 'G92 X0 Y0 Z0' tra la riga 19 e 20
    if len(righe) >= 20:
        righe.insert(19, "G1 X50 Y50\n")
        righe.insert(20, "G92 X0 Y0 Z0\n")
    else:
        print("Attenzione: il file ha meno di 20 righe. Inserimento G1 e G92 saltato.")

    # Sostituisci 'M5' con 'G1 Z3' e 'M3' con 'G1 Z-3'
    nuove_righe = []
    for riga in righe:
        if "Cutting mode: Router" in riga:
            print("Modalità di taglio: Router rilevata. impostare modalità laser e riprovare.")
            routermode = 1
        riga = riga.replace('M5', 'G1 Z3')
        riga = riga.replace('M3', 'G1 Z-3')
        riga = riga.replace('F200', 'F2000')
        nuove_righe.append(riga)
    if routermode == 1:
        print("Modalità Router non supportata. Assicurati di utilizzare un file G-code compatibile con il laser.")
    else:
        print("Modalità di taglio: Laser to 3D")
        with open(file_output, 'w') as f:
            f.writelines(nuove_righe)

        print(f"Modifica completata! File salvato come '{file_output}'.")


def inserisci_gcode_in_3mf(file_3mf_input, file_gcode, file_3mf_output):
    """
    Inserisce un file G-code all'interno di un file .gcode.3mf (input)
    creando un nuovo file .gcode.3mf (output) con il G-code inserito
    nella sottocartella Metadata come Plate_1.gcode.

    :param file_3mf_input: Percorso del file .gcode.3mf di input (file zip)
    :param file_gcode: Percorso del file .gcode da inserire
    :param file_3mf_output: Percorso del file .gcode.3mf di output
    """
    # Controllo esistenza file
    if not os.path.isfile(file_3mf_input):
        raise FileNotFoundError(f"Il file .gcode.3mf di input '{file_3mf_input}' non esiste.")
    if not os.path.isfile(file_gcode):
        raise FileNotFoundError(f"Il file .gcode '{file_gcode}' non esiste.")

    # Creazione di una cartella temporanea per la modifica
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Estrai l'intero contenuto del file .gcode.3mf di input
        with zipfile.ZipFile(file_3mf_input, 'r') as zip_ref:
            zip_ref.extractall(tmpdirname)

        # Percorso per la cartella Metadata all'interno del .gcode.3mf
        metadata_folder = os.path.join(tmpdirname, 'Metadata')
        os.makedirs(metadata_folder, exist_ok=True)

        # Copia il file .gcode e rinominalo in Plate_1.gcode
        plate_gcode_path = os.path.join(metadata_folder, 'Plate_1.gcode')
        shutil.copyfile(file_gcode, plate_gcode_path)

        # Crea un nuovo archivio .gcode.3mf di output
        with zipfile.ZipFile(file_3mf_output, 'w', compression=zipfile.ZIP_DEFLATED) as zip_out:
            for root, dirs, files in os.walk(tmpdirname):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Calcola il path relativo per inserirlo correttamente nel .gcode.3mf
                    rel_path = os.path.relpath(file_path, tmpdirname)
                    zip_out.write(file_path, rel_path)

    print(f"File '{file_gcode}' inserito correttamente in '{file_3mf_output}' come 'Metadata/Plate_1.gcode'.")

# Esempio d'uso:
# inserisci_gcode_in_3mf('stampa.gcode.3mf', 'stampa.gcode')

# Esempio di utilizzo
if __name__ == "__main__":
    file_input = input("inserire il nome del file >>    ")   # <-- Sostituisci con il nome del tuo file di input
    nome_input = file_input.replace(".gcode" or ".nc", "")   # Assicurati che il file abbia l'estensione .gcode
    file_output = "outputTEMP.gcode" # <-- Sostituisci con il nome del tuo file di output
    modifica_gcode(file_input, file_output)
    inserisci_gcode_in_3mf("DATA/default.gcode.3mf", "outputTEMP.gcode", f"{nome_input}.gcode.3mf")
    os.remove("outputTEMP.gcode")  # Rimuove il file temporaneo dopo l'inserimento
