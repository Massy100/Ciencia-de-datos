"""
Analisis exploratorio del dataset vgsales.csv
Adaptado a partir del ejemplo de netflix_titles.py
"""

import pandas as pd

# =========================
# 1. CARGA DEL DATASET
# =========================
df = pd.read_csv("vgsales.csv")

print("\n" + "=" * 70)
print("DATASET DE VENTAS DE VIDEOJUEGOS")
print("=" * 70)

print("\nPrimeras 5 filas:")
print(df.head())

print("\nDimensiones del dataset:")
print(f"Filas: {df.shape[0]}")
print(f"Columnas: {df.shape[1]}")

print("\nColumnas disponibles:")
print(df.columns.tolist())

print("\nTipos de datos originales:")
print(df.dtypes)


# =========================
# 2. LIMPIEZA DE DATOS
# =========================

# Year contiene valores nulos y originalmente se carga como float.
# Se convierte a entero anulable para conservar los datos faltantes.
df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")

# Reemplazar publishers faltantes por una etiqueta descriptiva.
df["Publisher"] = df["Publisher"].fillna("Desconocido")

# Eliminar espacios innecesarios en columnas de texto.
columnas_texto = ["Name", "Platform", "Genre", "Publisher"]

for columna in columnas_texto:
    df[columna] = df[columna].astype(str).str.strip()


# =========================
# 3. COLUMNAS NUEVAS
# =========================

# Suma de ventas regionales.
df["Regional_Sales"] = (
    df["NA_Sales"]
    + df["EU_Sales"]
    + df["JP_Sales"]
    + df["Other_Sales"]
)

# Diferencia entre Global_Sales y la suma de ventas regionales.
# Sirve para comprobar posibles diferencias por redondeo.
df["Sales_Difference"] = (
    df["Global_Sales"] - df["Regional_Sales"]
).round(2)

# Clasificacion sencilla de acuerdo con las ventas globales.
df["Sales_Category"] = pd.cut(
    df["Global_Sales"],
    bins=[-1, 0.5, 1, 5, float("inf")],
    labels=[
        "Menos de 0.5M",
        "0.5M a 1M",
        "1M a 5M",
        "Mas de 5M",
    ],
)


# =========================
# 4. INFORMACION GENERAL
# =========================

print("\n" + "=" * 70)
print("INFORMACION GENERAL")
print("=" * 70)

print("\nTipos de datos despues de la limpieza:")
print(df.dtypes)

print("\nValores nulos por columna:")
print(df.isnull().sum())

print("\nEstadisticas descriptivas:")
print(df.describe(include="all"))


# =========================
# 5. ANALISIS DEL DATASET
# =========================

print("\n" + "=" * 70)
print("ANALISIS DE VENTAS")
print("=" * 70)

print("\nTop 10 videojuegos por ventas globales:")
print(
    df[
        ["Rank", "Name", "Platform", "Year", "Genre", "Publisher", "Global_Sales"]
    ]
    .sort_values("Global_Sales", ascending=False)
    .head(10)
)

print("\nTop 10 plataformas por ventas globales:")
ventas_plataforma = (
    df.groupby("Platform")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print(ventas_plataforma)

print("\nVentas globales por genero:")
ventas_genero = (
    df.groupby("Genre")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
)
print(ventas_genero)

print("\nTop 10 publishers por ventas globales:")
ventas_publisher = (
    df.groupby("Publisher")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print(ventas_publisher)

print("\nTop 10 anios por ventas globales:")
ventas_anio = (
    df.dropna(subset=["Year"])
    .groupby("Year")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print(ventas_anio)

print("\nVentas totales por region:")
ventas_region = pd.Series(
    {
        "Norteamerica": df["NA_Sales"].sum(),
        "Europa": df["EU_Sales"].sum(),
        "Japon": df["JP_Sales"].sum(),
        "Otras regiones": df["Other_Sales"].sum(),
        "Global": df["Global_Sales"].sum(),
    }
)
print(ventas_region)

print("\nCantidad de videojuegos por categoria de ventas:")
print(df["Sales_Category"].value_counts().sort_index())

print("\nAnalisis finalizado correctamente.")
