# CNCto3DPlot
a python code to plot a cnc file

Creo questo script python per convertire i Gcode di macchine CNC creati da Gcoder in file per stampanti 3d modificate a plotter

per avere il gcode di input andate su questo sito : https://drandrewthomas.github.io/gcodercnc2d5/
impostate la velocita a 200 mm/min (che poi diventeranno 2000/min con il mio script (che equivalgono a circa 30 mm/sec))
e impostate la modalità di CNC a modalità LASER

ATTENZIONE questi gcode funzioneranno solo su stampanti 3d che hanno l'origine nell'angolo in basso a sinistra
Questo script funzionerà solo con stampanti Cartesiane le Delta non funzioneranno

ISTRUZIONI PER UTENTI BAMBULAB
c'è anche una cartella (nel mio repository) pensata appositamente per tutte le bambulab che come output al posto di dare un file ".gcode" da un file ".gcode.3mf" che attenzione non è la stessa cosa di un gcode quindi mettete il file di output nella micro sd nella sottocartella models
