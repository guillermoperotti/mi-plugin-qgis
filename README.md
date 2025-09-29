# Consulta Exportable – Scripts QGIS
Plugin para QGIS usado por el SIME (Servicio de Instalaciones Mecánicas y Eléctricas) de la IM


Este repositorio contiene **scripts en Python** para automatizar el tratamiento de archivos CSV exportados desde la base de datos del sistema **SIME** y usarlos en **QGIS**.  

Los scripts permiten:
- Seleccionar un CSV original.
- Convertir el delimitador (de tabulador → coma).
- Cargarlo como capa en QGIS.
- Transformar campos de fecha al formato estándar `AAAA-MM-DD`.
- Asegurar que ciertos atributos se mantengan como **números enteros (Integer 32 bit)** en lugar de texto:
  - `Padron`
  - `Concepto`
  - `Diferenciador`
  - `Capacidad`

---

## 📂 Estructura del repositorio:

qgis-scripts/
├── parte1_seleccionar_csv.py
│   └─ Abre un cuadro de diálogo para elegir el CSV original
├── **parte2_convertir_csv.py
│   └─ Convierte delimitadores de tabulación a coma
└── parte3y4_cargar_y_transformar.py
    └─ Carga en QGIS y aplica transformaciones (fechas + enteros)



---

## 🚀 Cómo usar los scripts en QGIS

1. Abrir **QGIS**.
2. Ir al menú **Complementos → Consola de Python** (`Ctrl+Alt+P`).
3. Copiar y pegar el contenido de los scripts en este orden:
   1. `parte1_seleccionar_csv.py`  
   2. `parte2_convertir_csv.py`  
   3. `parte3y4_cargar_y_transformar.py`  
4. Seguir las instrucciones en pantalla:
   - Elegir el archivo CSV original.
   - Se genera automáticamente un CSV corregido (`consulta_exportable_corregido.csv`).
   - Se carga la capa en QGIS y se transforman los campos.

---

## 🧩 Requisitos

- **QGIS 3.x**
- **Python 3.x** (incluido en QGIS)
- Librerías que ya vienen con QGIS:
  - `qgis.core`
  - `PyQt5.QtCore`

👉 No se necesitan instalaciones adicionales.

---

## 📖 Ejemplo de flujo

1. Selecciono un CSV crudo con tabuladores:  

Expediente Padron Concepto Diferenciador ...
62053 120122 15 1 ...


2. El script lo convierte a formato CSV válido con comas:  

Expediente,Padron,Concepto,Diferenciador,...
62053,120122,15,1,...


3. Al cargarlo en QGIS:
- Las fechas aparecen como `2025-06-02` en lugar de `02/06/2025`.
- Los campos `Padron`, `Concepto`, `Diferenciador` y `Capacidad` son enteros (no texto).

---

## 👨‍💻 Autor

- **Guillermo Perotti**  
- 📧 guillermoperottichape@gmail.com  

---

## 🤝 Contribuir

Si querés proponer mejoras:
1. Hacé un **fork** del repositorio.
2. Creá una rama nueva para tus cambios.
3. Mandá un **pull request** explicando qué mejoraste.

---

## 📜 Licencia

Este proyecto está bajo la licencia **GPL v3** – podés usarlo, modificarlo y compartirlo libremente siempre que mantengas la misma licencia.