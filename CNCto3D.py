# Created By : Christube
# Date: 01/06/2025

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

# Esempio di utilizzo
if __name__ == "__main__":
    file_input = input("inserire il nome del file >>    ")   # <-- Sostituisci con il nome del tuo file di input
    file_output = "output.gcode" # <-- Sostituisci con il nome del tuo file di output
    modifica_gcode(file_input, file_output)
