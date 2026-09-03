# 03_outliers.py
# Detección y tratamiento de valores atípicos

from pathlib import Path
import pandas as pd

# ------------------------------------------------------------
# Configuración de rutas
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# Cargar datos imputados mediante MICE
datos = pd.read_pickle(
    DATA_DIR / "datos_mice.pkl"
)

print("=== DETECCIÓN Y TRATAMIENTO DE OUTLIERS ===\n")


# ============================================================
# 1. DETECCIÓN DE OUTLIERS MEDIANTE IQR
# ============================================================

def detectar_outliers_iqr(serie):
    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)

    iqr_val = q3 - q1

    limite_inferior = q1 - 1.5 * iqr_val
    limite_superior = q3 + 1.5 * iqr_val

    return (
        (serie < limite_inferior) |
        (serie > limite_superior)
    )


outliers_ingreso = detectar_outliers_iqr(
    datos["ingreso"]
)

numero_outliers = int(
    outliers_ingreso.sum()
)

print(
    "Outliers detectados en ingreso:",
    numero_outliers
)


# ============================================================
# 2. FUNCIÓN DE WINSORIZACIÓN
# ============================================================

def winsorizar(
    serie,
    percentil_inferior=0.05,
    percentil_superior=0.95
):
    limite_inferior = serie.quantile(
        percentil_inferior
    )

    limite_superior = serie.quantile(
        percentil_superior
    )

    return serie.clip(
        lower=limite_inferior,
        upper=limite_superior
    )


# ============================================================
# 3. APLICAR WINSORIZACIÓN
# ============================================================

datos_winsor = datos.copy()

datos_winsor["ingreso"] = winsorizar(
    datos_winsor["ingreso"]
)


# ============================================================
# 4. COMPROBAR RESULTADOS
# ============================================================

outliers_despues = detectar_outliers_iqr(
    datos_winsor["ingreso"]
)

numero_outliers_despues = int(
    outliers_despues.sum()
)

print("\nWinsorización aplicada correctamente\n")

print("Estadísticos antes de la winsorización:")
print(datos["ingreso"].describe())

print("\nEstadísticos después de la winsorización:")
print(datos_winsor["ingreso"].describe())

print(
    "\nOutliers según IQR antes:",
    numero_outliers
)

print(
    "Outliers según IQR después:",
    numero_outliers_despues
)


# ============================================================
# 5. GUARDAR RESULTADOS
# ============================================================

datos_winsor.to_pickle(
    DATA_DIR / "datos_winsor.pkl"
)

print("\nArchivo generado correctamente:")
print("   - data/datos_winsor.pkl")
