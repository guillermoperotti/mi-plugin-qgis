# Unificado: Seleccionar CSV, convertir a comas, cargar y transformar campos

from qgis.PyQt.QtWidgets import QFileDialog
from qgis.core import (
    QgsVectorLayer, QgsProject, QgsFields, QgsField, QgsFeature,
    QgsExpression, QgsExpressionContext, QgsExpressionContextUtils
)
from PyQt5.QtCore import QVariant
import os

# === PARTE 1: Seleccionar el CSV original ===
ruta_original, _ = QFileDialog.getOpenFileName(None, "Seleccionar CSV original", "", "CSV Files (*.csv)")
if not ruta_original:
    print("❌ No se seleccionó archivo. Abortando.")
else:
    print("📄 Ruta seleccionada:", ruta_original)

    # === PARTE 2: Convertir a coma y guardar nuevo CSV ===
    ruta_corregida = os.path.join(os.path.dirname(ruta_original), "consulta_exportable_corregido.csv")

    with open(ruta_original, "r", encoding="latin1") as infile:
        lineas = infile.readlines()

    # Reemplazar tabulaciones por comas, limpiar espacios
    lineas_convertidas = [line.strip().replace("\t", ",") for line in lineas if line.strip()]

    with open(ruta_corregida, "w", encoding="utf-8", newline="") as outfile:
        for linea in lineas_convertidas:
            outfile.write(linea + "\n")

    print("✅ CSV corregido guardado sin comillas en:", ruta_corregida)

    # === PARTE 3 y 4: Cargar el nuevo CSV y transformar fechas/enteros ===
    layer = QgsVectorLayer(ruta_corregida, "ConsultaExportable", "ogr")

    if not layer.isValid():
        print("❌ Error: La capa no se pudo cargar.")
    else:
        print("✅ Capa CSV cargada correctamente.")

        campos_int = ["Padron", "Concepto", "Diferenciador", "Capacidad"]
        campos_fecha = ["A_asignar_desde", "Fecha_Ultima_Habilitacion", "Fecha_Ultima_Inspeccion"]

        nuevos_campos = QgsFields()
        for campo in layer.fields():
            nombre = campo.name().strip()
            if nombre in campos_int:
                nuevos_campos.append(QgsField(nombre, QVariant.Int))
            else:
                nuevos_campos.append(QgsField(nombre, QVariant.String))

        capa_corregida = QgsVectorLayer("None", layer.name(), "memory")
        capa_corregida.dataProvider().addAttributes(nuevos_campos)
        capa_corregida.updateFields()

        context = QgsExpressionContext()
        context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))

        for feat in layer.getFeatures():
            nueva = QgsFeature()
            valores = []

            for campo in nuevos_campos:
                nombre = campo.name()
                valor = feat[nombre]

                # Transformar fechas DD/MM/AAAA ➜ AAAA-MM-DD
                if nombre in campos_fecha and valor not in [None, ""]:
                    try:
                        expr = QgsExpression(
                            f"substr('{valor}', 7, 4) || '-' || substr('{valor}', 4, 2) || '-' || substr('{valor}', 1, 2)"
                        )
                        context.setFeature(feat)
                        valor = expr.evaluate(context)
                        if expr.hasEvalError():
                            valor = None
                    except:
                        valor = None

                # Convertir a entero
                elif nombre in campos_int:
                    try:
                        valor = int(valor) if valor not in ["", None] else None
                    except:
                        valor = None

                valores.append(valor)

            nueva.setAttributes(valores)
            capa_corregida.dataProvider().addFeature(nueva)

        QgsProject.instance().removeMapLayer(layer.id())
        QgsProject.instance().addMapLayer(capa_corregida)

        print("✅ Capa corregida con fechas e enteros aplicada con éxito.")