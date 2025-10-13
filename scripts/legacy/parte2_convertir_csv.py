##Parte 2 – Convertir a coma y guardar nuevo CSV

import os

ruta_corregida = os.path.join(os.path.dirname(ruta_original), "consulta_exportable_corregido.csv")

with open(ruta_original, "r", encoding="latin1") as infile:
    lineas = infile.readlines()

# Reemplazar tabulaciones por comas, limpiar espacios
lineas_convertidas = [line.strip().replace("\t", ",") for line in lineas if line.strip()]

with open(ruta_corregida, "w", encoding="utf-8", newline="") as outfile:
    for linea in lineas_convertidas:
        outfile.write(linea + "\n")

print("✅ CSV corregido guardado sin comillas en:", ruta_corregida)
