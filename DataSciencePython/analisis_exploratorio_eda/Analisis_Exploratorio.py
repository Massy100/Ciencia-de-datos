# Analisis_Exploratorio.py
# Análisis exploratorio final y generación de visualizaciones

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"

# Crear carpeta de resultados si no existe
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# CARGAR DATOS
# ============================================================

print("=== CARGANDO DATOS ===\n")

datos_raw = pd.read_pickle(
    DATA_DIR / "datos_raw.pkl"
)

datos_median = pd.read_pickle(
    DATA_DIR / "datos_median.pkl"
)

datos_regresion = pd.read_pickle(
    DATA_DIR / "datos_regresion.pkl"
)

datos_mice = pd.read_pickle(
    DATA_DIR / "datos_mice.pkl"
)

datos_winsor = pd.read_pickle(
    DATA_DIR / "datos_winsor.pkl"
)

print("Datos cargados correctamente.\n")


# Evitar notación científica al mostrar números
pd.set_option(
    "display.float_format",
    lambda x: f"{x:,.2f}"
)


# ============================================================
# 1. ANÁLISIS EXPLORATORIO
# ============================================================

print("=== ANÁLISIS EXPLORATORIO ===\n")

print("Dimensiones del conjunto de datos:")
print(f"Observaciones: {datos_raw.shape[0]}")
print(f"Variables: {datos_raw.shape[1]}")


print("\nTipos de variables:")
print(datos_raw.dtypes)


print("\nPrimeras observaciones:")
print(datos_raw.head())


print("\nResumen estadístico:")
print(datos_raw.describe())


print("\nValores faltantes por variable:")
print(datos_raw.isna().sum())


# ============================================================
# 2. GRÁFICO DE VALORES FALTANTES
# ============================================================

faltantes = datos_raw.isna().sum()

plt.figure(
    figsize=(10, 6)
)

plt.bar(
    faltantes.index,
    faltantes.values
)

plt.title(
    "Valores faltantes por variable"
)

plt.xlabel(
    "Variables"
)

plt.ylabel(
    "Cantidad de valores faltantes"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()


# Guardar gráfico
plt.savefig(
    OUTPUT_DIR / "01_valores_faltantes.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

plt.close()


# ============================================================
# 3. COMPARACIÓN DE MÉTODOS DE IMPUTACIÓN
# ============================================================

fig, axes = plt.subplots(
    2,
    2,
    figsize=(12, 8)
)


# ------------------------------------------------------------
# Datos originales
# ------------------------------------------------------------

axes[0, 0].hist(
    datos_raw["edad"].dropna(),
    bins=20
)

axes[0, 0].set_title(
    "Original"
)

axes[0, 0].set_xlabel(
    "Edad"
)

axes[0, 0].set_ylabel(
    "Frecuencia"
)


# ------------------------------------------------------------
# Imputación por mediana
# ------------------------------------------------------------

axes[0, 1].hist(
    datos_median["edad"],
    bins=20
)

axes[0, 1].set_title(
    "Mediana"
)

axes[0, 1].set_xlabel(
    "Edad"
)

axes[0, 1].set_ylabel(
    "Frecuencia"
)


# ------------------------------------------------------------
# Imputación por regresión
# ------------------------------------------------------------

axes[1, 0].hist(
    datos_regresion["edad"],
    bins=20
)

axes[1, 0].set_title(
    "Regresión"
)

axes[1, 0].set_xlabel(
    "Edad"
)

axes[1, 0].set_ylabel(
    "Frecuencia"
)


# ------------------------------------------------------------
# Imputación mediante MICE
# ------------------------------------------------------------

axes[1, 1].hist(
    datos_mice["edad"],
    bins=20
)

axes[1, 1].set_title(
    "MICE"
)

axes[1, 1].set_xlabel(
    "Edad"
)

axes[1, 1].set_ylabel(
    "Frecuencia"
)


fig.suptitle(
    "Comparación de métodos de imputación",
    fontsize=16
)

plt.tight_layout()


# Guardar gráfico
plt.savefig(
    OUTPUT_DIR / "02_comparacion_imputacion.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

plt.close()


# ============================================================
# 4. COMPARACIÓN DE OUTLIERS
# ============================================================

plt.figure(
    figsize=(10, 6)
)

plt.boxplot(
    [
        datos_mice["ingreso"],
        datos_winsor["ingreso"]
    ],
    tick_labels=[
        "Original",
        "Winsorizado"
    ]
)

plt.title(
    "Comparación de Ingreso"
)

plt.ylabel(
    "Ingreso"
)

plt.tight_layout()


# Guardar gráfico
plt.savefig(
    OUTPUT_DIR / "03_comparacion_outliers.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

plt.close()


# ============================================================
# 5. ESTADÍSTICOS ANTES Y DESPUÉS DE LA WINSORIZACIÓN
# ============================================================

print(
    "\n=== COMPARACIÓN DE INGRESO ===\n"
)

print(
    "Estadísticos antes de la winsorización:"
)

print(
    datos_mice["ingreso"].describe()
)


print(
    "\nEstadísticos después de la winsorización:"
)

print(
    datos_winsor["ingreso"].describe()
)


# ============================================================
# 6. COMPARACIÓN DE VALORES FALTANTES
# ============================================================

print(
    "\n=== VALORES FALTANTES DESPUÉS DE IMPUTACIÓN ===\n"
)


print(
    "Datos originales:",
    int(
        datos_raw.isna().sum().sum()
    )
)


print(
    "Imputación por mediana:",
    int(
        datos_median.isna().sum().sum()
    )
)


print(
    "Imputación por regresión:",
    int(
        datos_regresion.isna().sum().sum()
    )
)


print(
    "Imputación por MICE:",
    int(
        datos_mice.isna().sum().sum()
    )
)


# ============================================================
# 7. CONCLUSIONES
# ============================================================

print(
    "\n=== CONCLUSIONES DEL ANÁLISIS ===\n"
)


print(
    "1. Datos faltantes:"
)

print(
    f"   - Edad: MCAR "
    f"({datos_raw['edad'].isna().sum()} valores)"
)

print(
    f"   - Satisfacción: MAR "
    f"({datos_raw['satisfaccion'].isna().sum()} valores)"
)


print(
    "\n2. Métodos de imputación:"
)

print(
    "   - Mediana: método simple y rápido."
)

print(
    "   - Regresión: utiliza las relaciones "
    "existentes entre las variables."
)

print(
    "   - MICE: método más sofisticado que "
    "realiza imputaciones múltiples utilizando "
    "las relaciones entre variables."
)


print(
    "\n3. Outliers:"
)

print(
    "   - Se detectaron valores atípicos "
    "en la variable ingreso."
)

print(
    "   - Se aplicó winsorización utilizando "
    "los percentiles 5% y 95%."
)


# ============================================================
# 8. ARCHIVOS GENERADOS
# ============================================================

print(
    "\n=== VISUALIZACIONES GENERADAS ===\n"
)

print(
    "outputs/01_valores_faltantes.png"
)

print(
    "outputs/02_comparacion_imputacion.png"
)

print(
    "outputs/03_comparacion_outliers.png"
)

print(
    "\nAnálisis exploratorio completado correctamente."
)