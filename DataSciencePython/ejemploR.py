# Importar librerías necesarias
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import matplotlib
matplotlib.use('TkAgg')  # Para evitar problemas de fuentes en Windows
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
import os
import warnings
warnings.filterwarnings('ignore')

# Configurar para evitar problemas de fuentes en Windows
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Helvetica', 'sans-serif']

print("Librerías importadas correctamente")
print(f"Versión de pandas: {pd.__version__}")
print(f"Backend de matplotlib: {matplotlib.get_backend()}\n")

# ==================== CREACIÓN DE DATAFRAME ====================
# Crear un vector (lista en Python)
nombres = ["Falcon 9", "Saturn V", "soyuz", "Ariane 5", "Delta IV"]
anios = [2010, 196, 1966, 1996, 2002]

# Crear DataFrame
cohetes = pd.DataFrame({
    'Nombre': nombres,
    'Primer Lanzamiento': anios
})
print("=== DATAFRAME DE COHETES ===")
print(cohetes)
print()

# Extraer el lanzamiento más antiguo
indice_antiguo = cohetes['Primer Lanzamiento'].idxmin()
print(f"el cohete mas antiguo es: {cohetes.loc[indice_antiguo, 'Nombre']}\n")

# ==================== CARGA DE DATOS ====================
# Cargar datos desde URL
ruta = "https://raw.githubusercontent.com/abemen/datasets/refs/heads/main/antropometricas.csv"
try:
    antropometricas = pd.read_csv(ruta)
    print("=== DATOS ANTROPOMÉTRICOS ===")
    print(antropometricas.head())
    print(f"Dimensiones: {antropometricas.shape}\n")
except Exception as e:
    print(f"Error al cargar datos: {e}")

# ==================== WEB SCRAPING ====================
# Cargar página web
nasa = "https://www.nasa.gov/2026-news-releases/"
try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(nasa, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extraer por clase CSS
    titulos = soup.find_all(class_="hds-a11y-heading-22")
    titulos_textos = [titulo.get_text(strip=True) for titulo in titulos]
    if titulos_textos:
        print("=== TÍTULOS EXTRAÍDOS ===")
        for i, titulo in enumerate(titulos_textos[:5], 1):
            print(f"{i}. {titulo}")
    else:
        print("No se encontraron títulos con esa clase CSS")
except Exception as e:
    print(f"Error al cargar la página web: {e}\n")

# ==================== SECUENCIAS ====================
print("=== SECUENCIAS ===")
print(f"2:8 en R = {list(range(2, 9))}")
print(f"seq(2,3, by=0.1) = {list(np.arange(2, 3.1, 0.1))}")
print(f"rep(1:3, times=3) = {list(np.repeat(np.arange(1, 4), 3))}")
print(f"rep(1:3, each=4) = {list(np.repeat(np.arange(1, 4), 4))}")

# Almacenar un vector
x = np.arange(1, 5.5, 0.5)
print(f"x = {x}\n")

# ==================== FUNCIONES ====================
def doble(x):
    return x * 2

print("=== OPERACIONES CON VECTORES ===")
print(f"x + 10 = {x + 10}")
print(f"x * 3 = {x * 3}")

m = 0.5
b = -2
y = m * x + b
print(f"y = {y}\n")

# ==================== SELECCIÓN DE DATOS ====================
print("=== SELECCIÓN DE DATOS ===")
print(f"y[3] = {y[2]}")  # Python es 0-based (el tercer elemento es índice 2)
print(f"Todos los elementos excepto el tercero: {np.delete(y, 2)}")
print(f"x[x > 3] = {x[x > 3]}\n")

# ==================== MATRICES ====================
print("=== MATRICES ===")

# Matriz 3x3 (necesita 9 elementos)
matriz3x3 = np.array(x[:9]).reshape(3, 3)
print("Matriz 3x3:")
print(matriz3x3)

# Matriz 3x6 (necesita 18 elementos)
# Como x solo tiene 9 elementos, necesitamos repetirlo o crear más datos
# Opción 1: Repetir x para tener 18 elementos
x_extendido = np.concatenate([x, x])  # Duplicar x para tener 18 elementos
matriz3x6 = x_extendido.reshape(3, 6)
print("\nMatriz 3x6 (usando x repetido):")
print(matriz3x6)

# Opción 2: Usar np.arange para crear 18 elementos directamente
x_18 = np.arange(1, 10, 0.5)  # Esto crea 18 elementos: 1, 1.5, 2, ..., 9.5
matriz3x6_v2 = x_18.reshape(3, 6)
print("\nMatriz 3x6 (usando secuencia de 18 elementos):")
print(matriz3x6_v2)

# Opción 3: Usar una matriz más pequeña si no necesitas 3x6
print("\nOtras opciones de matrices:")
print("Matriz 3x3:")
print(np.array(x[:9]).reshape(3, 3))
print("\nMatriz 1x9:")
print(np.array(x[:9]).reshape(1, 9))
print("\nMatriz 9x1:")
print(np.array(x[:9]).reshape(9, 1))

# ==================== GRÁFICOS ====================
print("\n=== GENERANDO GRÁFICOS ===")

# Gráfico simple
try:
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, 'o-', color='blue', linewidth=2, markersize=8)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Gráfico de x vs y')
    plt.grid(True, alpha=0.3)
    plt.show()
    print("Gráfico 1 mostrado correctamente")
except Exception as e:
    print(f"Error al mostrar gráfico 1: {e}")

# ==================== INFORMACIÓN DEL DATASET ====================
if 'antropometricas' in locals():
    print("\n=== INFORMACIÓN DEL DATASET ===")
    print(f"Número de columnas: {len(antropometricas.columns)}")
    print(f"Dimensiones: {antropometricas.shape}")
    print(f"Longitud de columna Sexo: {len(antropometricas['Sexo'])}")
    print(f"Máximo de Peso: {antropometricas['Peso'].max()}")
    print(f"Mínimo de Peso: {antropometricas['Peso'].min()}")
    print(f"Índice del máximo de Peso: {antropometricas['Peso'].idxmax()}")
    if len(antropometricas['Peso']) > 34:
        print(f"Valor en posición 34 (índice 33): {antropometricas['Peso'].iloc[33]}")

# ==================== GRÁFICOS CON SEABORN ====================
# Crear DataFrame similar al de misiones
misiones = pd.DataFrame({
    'Mision': ["Apollo 11", "Apollo 13", "Crew-1", "Starliner", "Artemis I"],
    'Exito': [1, 0, 1, 0, 1],
    'Costo': [355, 400, 220, 450, 500]
})

print("\n=== DATAFRAME DE MISIONES ===")
print(misiones)

# Gráfico de barras con seaborn
try:
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(data=misiones, 
                x='Mision', 
                y='Costo', 
                hue='Exito',
                palette={0: 'red', 1: 'blue'})

    plt.title('Misiones espaciales\nRojo/Fracaso, Azul/Éxito', fontsize=14)
    plt.ylabel('Costo (Millones USD)')
    plt.xlabel('Misión')
    plt.legend(title='¿Éxito?', labels=['No', 'Sí'])
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    print("Gráfico 2 mostrado correctamente")
except Exception as e:
    print(f"Error al mostrar gráfico 2: {e}")

print("\n¡Ejecución completada!")