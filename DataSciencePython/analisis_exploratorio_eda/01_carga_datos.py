# 01_carga_datos.py
# Generación y carga de datos

from pathlib import Path
import numpy as np
import pandas as pd

# ------------------------------------------------------------
# Configuración de rutas
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# Función para generar datos de ejemplo
# ------------------------------------------------------------

def generar_datos(n=1000, seed=123):
    rng = np.random.default_rng(seed)

    print("=== GENERACIÓN DE DATOS ===\n")

    datos = pd.DataFrame({
        "id": np.arange(1, n + 1),

        # Edad mínima de 18 años
        "edad": np.maximum(
            18,
            np.rint(rng.normal(loc=35, scale=12, size=n))
        ),

        "ingreso": np.rint(
            rng.normal(loc=50000, scale=15000, size=n)
        ),

        "educacion": rng.choice(
            [1, 2, 3, 4, 5],
            size=n,
            replace=True,
            p=[0.10, 0.20, 0.30, 0.25, 0.15]
        ),

        # Evitar experiencia negativa
        "experiencia": np.maximum(
            0,
            np.rint(rng.normal(loc=10, scale=7, size=n))
        ),

        "satisfaccion": np.rint(
            rng.uniform(low=1, high=10, size=n)
        )
    })

    # --------------------------------------------------------
    # Introducir valores faltantes MCAR en edad
    # --------------------------------------------------------

    indices_na = rng.choice(
        datos.index,
        size=50,
        replace=False
    )

    datos.loc[indices_na, "edad"] = np.nan

    # --------------------------------------------------------
    # Introducir outliers en ingreso
    # --------------------------------------------------------

    indices_outliers = rng.choice(
        datos.index,
        size=20,
        replace=False
    )

    datos.loc[indices_outliers, "ingreso"] = (
        datos.loc[indices_outliers, "ingreso"] * 5
    )

    # --------------------------------------------------------
    # Introducir valores faltantes MAR en satisfacción
    # --------------------------------------------------------

    candidatos_mar = datos.index[
        datos["educacion"] >= 4
    ].to_numpy()

    cantidad_mar = min(30, len(candidatos_mar))

    indices_mar = rng.choice(
        candidatos_mar,
        size=cantidad_mar,
        replace=False
    )

    datos.loc[indices_mar, "satisfaccion"] = np.nan

    # --------------------------------------------------------
    # Resumen
    # --------------------------------------------------------

    print("Datos generados correctamente")
    print(f"   - Observaciones: {len(datos)}")
    print(f"   - Variables: {datos.shape[1]}")
    print(
        "   - Valores faltantes en edad:",
        int(datos["edad"].isna().sum())
    )
    print(
        "   - Valores faltantes en satisfacción:",
        int(datos["satisfaccion"].isna().sum())
    )
    print(
        "   - Outliers introducidos en ingreso:",
        len(indices_outliers)
    )

    return datos


# ------------------------------------------------------------
# Generar y guardar datos
# ------------------------------------------------------------

if __name__ == "__main__":
    datos = generar_datos()

    # Pickle conserva el DataFrame para trabajar en Python
    datos.to_pickle(DATA_DIR / "datos_raw.pkl")

    # CSV para poder inspeccionarlo fácilmente
    datos.to_csv(
        DATA_DIR / "datos_raw.csv",
        index=False
    )

    print("\n=== ARCHIVOS GENERADOS ===")
    print("data/datos_raw.pkl")
    print("data/datos_raw.csv")
