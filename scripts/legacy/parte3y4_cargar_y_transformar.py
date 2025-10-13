from qgis.core import (
    QgsVectorLayer, QgsProject, QgsFields, QgsField, QgsFeature,
    QgsExpression, QgsExpressionContext, QgsExpressionContextUtils
)
from PyQt5.QtCore import QVariant

# 👉 Asegurate de definir esto con tu ruta corregida:
# ruta_corregida = "/ruta/absoluta/al/consulta_exportable_corregido.csv"

# Cargar la capa original desde el CSV
layer = QgsVectorLayer(ruta_corregida, "ConsultaExportable", "ogr")

if not layer.isValid():
    print("❌ Error: La capa no se pudo cargar.")
else:
    print("✅ Capa CSV cargada correctamente.")

    # === PASO 1: Preparar campos con tipos corregidos ===
    campos_int = ["Padron", "Concepto", "Diferenciador", "Capacidad"]
    campos_fecha = ["A_asignar_desde", "Fecha_Ultima_Habilitacion", "Fecha_Ultima_Inspeccion"]

    nuevos_campos = QgsFields()
    for campo in layer.fields():
        nombre = campo.name().strip()
        if nombre in campos_int:
            nuevos_campos.append(QgsField(nombre, QVariant.Int))
        else:
            nuevos_campos.append(QgsField(nombre, QVariant.String))

    # === PASO 2: Crear capa en memoria con tipos corregidos ===
    capa_corregida = QgsVectorLayer("None", layer.name(), "memory")
    capa_corregida.dataProvider().addAttributes(nuevos_campos)
    capa_corregida.updateFields()

    # === PASO 3: Transformar los valores y copiar a la nueva capa ===
    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(layer))

    for feat in layer.getFeatures():
        nueva = QgsFeature()
        valores = []

        for campo in nuevos_campos:
            nombre = campo.name()
            valor = feat[nombre]

            # 🧩 Si es campo de fecha, transformar DD/MM/AAAA ➜ AAAA-MM-DD
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

            # 🧩 Si es campo entero, convertir
            elif nombre in campos_int:
                try:
                    valor = int(valor) if valor not in ["", None] else None
                except:
                    valor = None

            valores.append(valor)

        nueva.setAttributes(valores)
        capa_corregida.dataProvider().addFeature(nueva)

    # === PASO 4: Reemplazar la capa original por la corregida ===
    QgsProject.instance().removeMapLayer(layer.id())
    QgsProject.instance().addMapLayer(capa_corregida)

    print("✅ Capa corregida con fechas e enteros aplicada con éxito.")

