# Limpieza y análisis exploratorio de encuestas con pandas

Proyecto que toma un archivo de encuestas de satisfacción con errores típicos (duplicados, nulos, formatos mezclados, valores imposibles) y lo convierte en un dataset confiable para analizar.

> **Nota sobre los datos:** el CSV es **sintético** (`generar_datos_sucios.py`, semilla fija) e incluye errores introducidos a propósito. Las conclusiones sirven para demostrar el método, no como hallazgos reales.

## Problemas encontrados y cómo se resolvieron

| Problema | Cantidad | Solución |
|----------|----------|----------|
| Filas duplicadas | 40 | `drop_duplicates()` |
| Fechas en dos formatos (`2025-03-01` y `01/03/2025`) | ~25 % | Se parsea cada formato por separado y se combinan |
| Distritos con mayúsculas y espacios (`"COMAS "`) | ~30 % | `str.strip().str.title()` |
| Canales inconsistentes (`web` vs `Web`) | ~4 % | Normalización de texto |
| Edades nulas o imposibles (150, -3, 999) | 54 fuera de rango + 97 nulas | Fuera de rango (16-90) → nulo; imputación con la mediana |
| Montos atípicos (> Q3 + 3×IQR) | 23 | Se marcan en `monto_atipico` y se excluyen de los promedios, sin borrarlos |
| Montos nulos | 62 | Mediana de los montos no atípicos |

Resultado: de 1.240 filas crudas a 1.200 filas limpias.

## Cómo ejecutarlo

`§bash
pip install pandas numpy matplotlib
python generar_datos_sucios.py   # crea datos/encuestas_crudo.csv
python limpieza_eda.py           # limpia, analiza y genera graficos/ y datos/encuestas_limpio.csv
`§

Los gráficos (puntaje por canal, distribución de montos y puntaje mensual) no están incluidos en el repositorio: se generan en la carpeta `graficos/` al ejecutar el script.

## Resultados del EDA (datos simulados)

- Puntaje promedio por canal: App 3,77 · Tienda 3,68 · Web 3,65 · Teléfono 3,63. Las diferencias son pequeñas; con datos reales convendría una prueba estadística antes de concluir.
- La correlación entre edad y puntaje es prácticamente nula (-0,07).
- El monto promedio por distrito varía entre S/ 114 y S/ 128 (sin atípicos).

## Próximos pasos

- Repetir el flujo con un dataset abierto real (INEI o datosabiertos.gob.pe).
- Agregar una prueba de hipótesis (ANOVA) para comparar canales.
- Convertir el script en un notebook con explicación paso a paso.
