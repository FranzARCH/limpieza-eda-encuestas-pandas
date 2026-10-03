"""Genera un CSV SINTETICO 'sucio' de encuestas de satisfaccion (con errores tipicos)
para practicar limpieza de datos con pandas. Semilla fija = resultado reproducible."""
import random
from pathlib import Path

import numpy as np
import pandas as pd

random.seed(7)
np.random.seed(7)
N = 1200
SALIDA = Path(__file__).parent / "datos" / "encuestas_crudo.csv"

distritos = ["Miraflores", "San Isidro", "Surco", "Lince", "Comas", "Ate", "San Borja"]
canales = ["Web", "Tienda", "Telefono", "App"]

df = pd.DataFrame({
    "id_encuesta": range(1, N + 1),
    "distrito": np.random.choice(distritos, N),
    "canal": np.random.choice(canales, N, p=[0.35, 0.3, 0.1, 0.25]),
    "edad": np.random.normal(34, 11, N).round(),
    "monto_compra": np.random.lognormal(4.6, 0.7, N).round(2),
    "puntaje": np.random.choice([1, 2, 3, 4, 5], N, p=[0.06, 0.1, 0.19, 0.35, 0.3]),
    "fecha": pd.to_datetime("2025-01-01") + pd.to_timedelta(np.random.randint(0, 330, N), unit="D"),
})

# --- ensuciar los datos ---
df["fecha"] = df["fecha"].dt.strftime("%Y-%m-%d")
mix = df.sample(frac=0.25, random_state=1).index
df.loc[mix, "fecha"] = pd.to_datetime(df.loc[mix, "fecha"]).dt.strftime("%d/%m/%Y")   # formatos mezclados
idx = df.sample(frac=0.3, random_state=2).index
df.loc[idx, "distrito"] = df.loc[idx, "distrito"].str.upper() + " "                    # mayusculas + espacios
df.loc[df.sample(frac=0.08, random_state=3).index, "edad"] = np.nan                     # nulos
df.loc[df.sample(frac=0.05, random_state=4).index, "monto_compra"] = np.nan
df.loc[df.sample(6, random_state=5).index, "edad"] = [150, -3, 999, 0, 210, 17.5]        # edades imposibles
df.loc[df.sample(8, random_state=6).index, "monto_compra"] = 250000                      # outliers de monto
df.loc[df.sample(frac=0.04, random_state=8).index, "canal"] = "web"                     # categorias inconsistentes
df = pd.concat([df, df.sample(40, random_state=9)], ignore_index=True)                   # duplicados

SALIDA.parent.mkdir(exist_ok=True)
df.to_csv(SALIDA, index=False)
print(f"Archivo creado: {SALIDA} ({len(df)} filas)")
