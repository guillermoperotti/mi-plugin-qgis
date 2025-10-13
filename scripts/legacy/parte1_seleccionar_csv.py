##Parte 1 – Seleccionar el CSV original

from qgis.PyQt.QtWidgets import QFileDialog

ruta_original, _ = QFileDialog.getOpenFileName(None, "Seleccionar CSV original", "", "CSV Files (*.csv)")
print("📄 Ruta seleccionada:", ruta_original)
