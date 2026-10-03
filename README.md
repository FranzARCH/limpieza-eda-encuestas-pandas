# Limpieza y análisis exploratorio de encuestas con pandas

Proyecto que toma un archivo de encuestas de satisfacción con errores típicos (duplicados, nulos, formatos mezclados, valores imposibles) y lo convierte en un dataset confiable para analizar.

> **Nota sobre los datos:** el CSV es **sintético** (`generar_datos_sucios.py`, semilla fija) e incluye errores introducidos a propósito. Las conclusiones servirán para demostrar el método, no como hallazgos reales.

## Estado

🚧 En progreso. Ya está disponible el generador de datos; el script de limpieza y análisis (`limpieza_eda.py`) y el informe de resultados se agregarán próximamente.

## Cómo generar los datos

`§bash
pip install pandas numpy
python generar_datos_sucios.py   # crea datos/encuestas_crudo.csv
`§
