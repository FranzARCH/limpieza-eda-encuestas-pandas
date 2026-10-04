"""Limpieza y analisis exploratorio (EDA) de encuestas de satisfaccion.

Entrada : datos/encuestas_crudo.csv
Salidas : datos/encuestas_limpio.csv, graficos/*.png, y un resumen impreso del proceso.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

AQUI = Path(__file__).parent
(AQUI / "graficos").mkdir(exist_ok=True)

# ---------- 1. Cargar y diagnosticar ----------
df = pd.read_csv(AQUI / "datos" / "encuestas_crudo.csv")
print("Filas iniciales:", len(df))
print("\nNulos por columna:\n", df.isna().sum().to_string())
print("Duplicados exactos:", df.duplicated().sum())

# ---------- 2. Limpiar ----------
n0 = len(df)
df = df.drop_duplicates()
print(f"\n[limpieza] duplicados eliminados: {n0 - len(df)}")

df["distrito"] = df["distrito"].str.strip().str.title()
df["canal"] = df["canal"].str.strip().str.title()

# fechas en dos formatos: se parsea cada formato por separado
iso = pd.to_datetime(df["fecha"], format="%Y-%m-%d", errors="coerce")
dmy = pd.to_datetime(df["fecha"], format="%d/%m/%Y", errors="coerce")
df["fecha"] = iso.fillna(dmy)
print("[limpieza] fechas no reconocidas:", df["fecha"].isna().sum())

# edades imposibles -> nulo; luego imputar con la mediana
edad_invalida = ~df["edad"].between(16, 90) & df["edad"].notna()
print("[limpieza] edades fuera de rango (16-90):", edad_invalida.sum())
df.loc[edad_invalida, "edad"] = np.nan
df["edad"] = df["edad"].fillna(df["edad"].median()).round().astype(int)

# outliers de monto por regla IQR: se marcan (no se borran) y se excluyen del promedio
q1, q3 = df["monto_compra"].quantile([0.25, 0.75])
limite = q3 + 3 * (q3 - q1)
df["monto_atipico"] = df["monto_compra"] > limite
print(f"[limpieza] montos atipicos (> {limite:,.0f}): {df['monto_atipico'].sum()}")
df["monto_compra"] = df["monto_compra"].fillna(df.loc[~df["monto_atipico"], "monto_compra"].median())

df.to_csv(AQUI / "datos" / "encuestas_limpio.csv", index=False)
print("Filas finales:", len(df))

# ---------- 3. EDA ----------
normal = df[~df["monto_atipico"]]
print("\nPuntaje promedio por canal:\n", df.groupby("canal")["puntaje"].mean().round(2).sort_values(ascending=False).to_string())
print("\nMonto promedio (sin atipicos) por distrito:\n", normal.groupby("distrito")["monto_compra"].mean().round(1).sort_values(ascending=False).to_string())
print("\nCorrelacion edad-puntaje:", round(df["edad"].corr(df["puntaje"]), 3))

fig, ax = plt.subplots(figsize=(7, 4))
df.groupby("canal")["puntaje"].mean().sort_values().plot.barh(ax=ax, color="#2a6f97")
ax.set(title="Puntaje promedio de satisfaccion por canal", xlabel="Puntaje (1-5)", ylabel="")
ax.set_xlim(0, 5)
fig.tight_layout(); fig.savefig(AQUI / "graficos" / "puntaje_por_canal.png", dpi=150); plt.close(fig)

fig, ax = plt.subplots(figsize=(7, 4))
normal["monto_compra"].plot.hist(bins=30, ax=ax, color="#2a6f97")
ax.set(title="Distribucion del monto de compra (sin atipicos)", xlabel="Monto (S/)", ylabel="Encuestas")
fig.tight_layout(); fig.savefig(AQUI / "graficos" / "distribucion_monto.png", dpi=150); plt.close(fig)

mensual = df.set_index("fecha").resample("MS")["puntaje"].mean()
fig, ax = plt.subplots(figsize=(7, 4))
mensual.plot(ax=ax, marker="o", color="#2a6f97")
ax.set(title="Puntaje promedio mensual", xlabel="", ylabel="Puntaje (1-5)", ylim=(1, 5))
fig.tight_layout(); fig.savefig(AQUI / "graficos" / "puntaje_mensual.png", dpi=150); plt.close(fig)
print("\nGraficos guardados en graficos/")
