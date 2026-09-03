# 02_imputacion.py
# Métodos de imputación para valores faltantes

from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from statsmodels.imputation.mice import MICEData

# ------------------------------------------------------------
# Configuración de rutas
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# Cargar datos
datos = pd.read_pickle(
    DATA_DIR / "datos_raw.pkl"
)

print("=== IMPUTACIÓN DE VALORES FALTANTES ===\n")


# ============================================================
# 1. IMPUTACIÓN POR MEDIANA
# ============================================================

print("1. Imputación por mediana...")

datos_median = datos.copy()

columnas_numericas = datos_median.select_dtypes(
    include=np.number
).columns

for columna in columnas_numericas:
    if datos_median[columna].isna().any():
        mediana = datos_median[columna].median()
        datos_median[columna] = (
            datos_median[columna].fillna(mediana)
        )

datos_median.to_pickle(
    DATA_DIR / "datos_median.pkl"
)

print(
    "   Valores faltantes restantes:",
    int(datos_median.isna().sum().sum())
)
print("   Completado\n")


# ============================================================
# 2. IMPUTACIÓN POR REGRESIÓN
# ============================================================

print("2. Imputación por regresión...")

datos_regresion = datos.copy()


# ------------------------------------------------------------
# Imputar edad
# ------------------------------------------------------------

predictores_edad = [
    "ingreso",
    "educacion",
    "experiencia"
]

filas_entrenamiento = datos_regresion["edad"].notna()
filas_prediccion = datos_regresion["edad"].isna()

if filas_prediccion.any():
    modelo_edad = LinearRegression()

    modelo_edad.fit(
        datos_regresion.loc[
            filas_entrenamiento,
            predictores_edad
        ],
        datos_regresion.loc[
            filas_entrenamiento,
            "edad"
        ]
    )

    predicciones_edad = modelo_edad.predict(
        datos_regresion.loc[
            filas_prediccion,
            predictores_edad
        ]
    )

    # Redondear y mantener edad mínima de 18
    predicciones_edad = np.maximum(
        18,
        np.rint(predicciones_edad)
    )

    datos_regresion.loc[
        filas_prediccion,
        "edad"
    ] = predicciones_edad


# ------------------------------------------------------------
# Imputar satisfacción
# ------------------------------------------------------------

predictores_satisfaccion = [
    "edad",
    "ingreso",
    "educacion",
    "experiencia"
]

filas_entrenamiento = (
    datos_regresion["satisfaccion"].notna()
)

filas_prediccion = (
    datos_regresion["satisfaccion"].isna()
)

if filas_prediccion.any():
    modelo_satisfaccion = LinearRegression()

    modelo_satisfaccion.fit(
        datos_regresion.loc[
            filas_entrenamiento,
            predictores_satisfaccion
        ],
        datos_regresion.loc[
            filas_entrenamiento,
            "satisfaccion"
        ]
    )

    predicciones_satisfaccion = (
        modelo_satisfaccion.predict(
            datos_regresion.loc[
                filas_prediccion,
                predictores_satisfaccion
            ]
        )
    )

    # Redondear y limitar al rango 1-10
    predicciones_satisfaccion = np.clip(
        np.rint(predicciones_satisfaccion),
        1,
        10
    )

    datos_regresion.loc[
        filas_prediccion,
        "satisfaccion"
    ] = predicciones_satisfaccion


datos_regresion.to_pickle(
    DATA_DIR / "datos_regresion.pkl"
)

print(
    "   Valores faltantes restantes:",
    int(datos_regresion.isna().sum().sum())
)
print("   Completado\n")


# ============================================================
# 3. IMPUTACIÓN MICE + PREDICTIVE MEAN MATCHING
# ============================================================

print("3. Imputación por MICE...")

# No usar ID como predictor.
datos_para_mice = (
    datos
    .drop(columns=["id"])
    .copy()
)

# MICEData usa Predictive Mean Matching (PMM).
imputador = MICEData(
    datos_para_mice,
    k_pmm=5
)

# Equivalente conceptual a varias iteraciones de MICE.
for _ in range(50):
    imputador.update_all()

datos_mice = imputador.data.copy()

# Recuperar ID sin usarlo en la imputación.
datos_mice.insert(
    0,
    "id",
    datos["id"].to_numpy()
)

# Mantener variables discretas en sus rangos esperados.
datos_mice["edad"] = np.maximum(
    18,
    np.rint(datos_mice["edad"])
)

datos_mice["satisfaccion"] = np.clip(
    np.rint(datos_mice["satisfaccion"]),
    1,
    10
)

datos_mice.to_pickle(
    DATA_DIR / "datos_mice.pkl"
)

print(
    "   Valores faltantes restantes:",
    int(datos_mice.isna().sum().sum())
)
print("   Completado\n")


# ============================================================
# RESUMEN
# ============================================================

print("=== IMPUTACIONES COMPLETADAS ===\n")

print(
    "Mediana:",
    int(datos_median.isna().sum().sum()),
    "valores faltantes restantes"
)

print(
    "Regresión:",
    int(datos_regresion.isna().sum().sum()),
    "valores faltantes restantes"
)

print(
    "MICE:",
    int(datos_mice.isna().sum().sum()),
    "valores faltantes restantes"
)

print("\nArchivos creados:")
print("   - data/datos_median.pkl")
print("   - data/datos_regresion.pkl")
print("   - data/datos_mice.pkl")
