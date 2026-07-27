# ==================== CONFIGURACION INICIAL ====================
import matplotlib
matplotlib.use('TkAgg')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Helvetica', 'sans-serif']
sns.set_style("whitegrid")

print("Librerias importadas correctamente")
print(f"Version de pandas: {pd.__version__}")

# ==================== CARGA DE DATOS ====================
try:
    datos = sns.load_dataset('titanic')
    print("Datos cargados desde seaborn")
except:
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    datos = pd.read_csv(url)
    print("Datos cargados desde URL")

print("\n=== PRIMEROS DATOS ===")
print(datos.head())

print("\n=== INFORMACION DE LOS DATOS ===")
print(datos.info())

print("\n=== ESTADISTICAS DESCRIPTIVAS ===")
print(datos.describe())

# ==================== LIMPIEZA DE DATOS ====================
print("\n=== LIMPIEZA DE DATOS ===")

print(f"Datos faltantes en Age: {datos['age'].isna().sum()}")

edad_media = datos['age'].mean()
datos['age'] = datos['age'].fillna(edad_media)
print(f"Edad imputada con la media: {edad_media:.2f}")

print(f"Datos faltantes en Age despues de imputacion: {datos['age'].isna().sum()}")

# ==================== ANALISIS EXPLORATORIO (EDA) ====================
print("\n=== ANALISIS EXPLORATORIO ===")

datos['Child'] = np.where(datos['age'] < 12, 'Child', 'Adulto')

# Convertir a categoricas
datos['sex'] = datos['sex'].astype('category')
datos['pclass'] = datos['pclass'].astype('category')

print("Variables creadas correctamente")

# Crear version numerica para calculos
datos_numeric = datos.copy()
datos_numeric['survived_num'] = datos_numeric['survived'].astype(int)

# ==================== NIVEL 1: GRAFICOS CON MATPLOTLIB ====================
print("\n=== NIVEL 1: GRAFICOS CON MATPLOTLIB ===")

print("\n--- Tabla de contingencia: Sexo vs Supervivencia ---")
contingencia_sexo = pd.crosstab(datos['sex'], datos['survived'])
print(contingencia_sexo)

porcentaje_sexo = pd.crosstab(datos['sex'], datos['survived'], normalize='index') * 100
print("\nPorcentajes por sexo:")
print(porcentaje_sexo)

# Boxplot - Figura 1 (R base style)
plt.figure(figsize=(10, 6))
sns.boxplot(data=datos, x='survived', y='age', color='lightblue')
plt.title('Distribucion de edad por supervivencia', fontsize=14)
plt.xlabel('Sobrevivio (0 = No, 1 = Si)')
plt.ylabel('Edad (Años)')
plt.xticks([0, 1], ['No', 'Si'])
plt.tight_layout()
plt.show()

# Tabla de contingencia clase
contingencia_clase = pd.crosstab(datos['pclass'], datos['survived'])
print("\n--- Tabla de contingencia: Clase vs Supervivencia ---")
print(contingencia_clase)

# Grafico de barras absolutas y porcentuales (igual que en R)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

contingencia_clase.plot(kind='bar', ax=ax1, color=['#FABD55', '#7BFF4F'])
ax1.set_title('Supervivencia por clase del pasajero')
ax1.set_xlabel('Clase')
ax1.set_ylabel('Cantidad de pasajeros')
ax1.legend(['No sobrevivio', 'Sobrevivio'])
ax1.grid(True, alpha=0.3)

contingencia_clase_prop = pd.crosstab(datos['pclass'], datos['survived'], normalize='index') * 100
contingencia_clase_prop.plot(kind='bar', ax=ax2, color=['#FABD55', '#7BFF4F'])
ax2.set_title('Porcentaje de supervivencia por clase')
ax2.set_xlabel('Clase')
ax2.set_ylabel('Porcentaje (%)')
ax2.legend(['No sobrevivio', 'Sobrevivio'])
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ==================== NIVEL 2: GRAFICOS CON SEABORN ====================
print("\n=== NIVEL 2: GRAFICOS CON SEABORN ===")

# Crear una versión de survived como string para usar con palette
datos['survived_str'] = datos['survived'].astype(str)

# Boxplot con seaborn (similar a p1 en R) - SOLUCION DEFINITIVA
plt.figure(figsize=(10, 6))
ax = sns.boxplot(data=datos, x='survived_str', y='age',
                 palette={'0': '#FAC955', '1': '#2ECC71'})  # Usando strings
plt.title('Distribucion de edad por supervivencia', fontsize=14)
plt.xlabel('Supervivencia')
plt.ylabel('Edad (años)')
plt.xticks([0, 1], ['No Sobrevivio', 'Sobrevivio'])
plt.tight_layout()
plt.show()

# Boxplot con colores usando matplotlib (estilo R base)
plt.figure(figsize=(10, 6))
datos.boxplot(column='age', by='survived', grid=True, patch_artist=True,
              boxprops=dict(facecolor='#2ECC71'),
              medianprops=dict(color='red', linewidth=2))
plt.title('Distribucion de edad por supervivencia')
plt.suptitle('')
plt.xlabel('Sobrevivio (0 = No, 1 = Si)')
plt.ylabel('Edad (Años)')
plt.xticks([1, 2], ['No', 'Si'])
plt.tight_layout()
plt.show()

# Grafico de barras absoluto (similar a p2 en R) - SOLUCION DEFINITIVA
plt.figure(figsize=(10, 6))
ax = sns.countplot(data=datos, x='pclass', hue='survived_str',
                   palette={'0': '#79EFF2', '1': '#F0F279'})  # Usando strings
plt.title('Supervivencia por clase - Numeros absolutos', fontsize=14)
plt.xlabel('Clase del pasajero')
plt.ylabel('Cantidad de pasajeros')
plt.legend(title='', labels=['No sobrevivio', 'Sobrevivio'])
plt.tight_layout()
plt.show()

# Grafico de barras porcentuales (similar a p3 en R) - SOLUCION DEFINITIVA
plt.figure(figsize=(10, 6))
porcentaje_clase = pd.crosstab(datos['pclass'], datos['survived'], normalize='index') * 100
porcentaje_clase_melt = porcentaje_clase.reset_index().melt(id_vars='pclass', 
                                                            var_name='survived', 
                                                            value_name='percentage')
# Convertir survived a string en el dataframe de porcentajes
porcentaje_clase_melt['survived'] = porcentaje_clase_melt['survived'].astype(str)

ax = sns.barplot(data=porcentaje_clase_melt, x='pclass', y='percentage', hue='survived',
                 palette={'0': '#79EFF2', '1': '#F0F279'})  # Usando strings
plt.title('Supervivencia por clase (porcentaje)', fontsize=14)
plt.xlabel('Clase del pasajero')
plt.ylabel('Porcentaje (%)')
plt.legend(title='', labels=['No sobrevivio', 'Sobrevivio'])
# Agregar etiquetas de porcentaje
for i, bar in enumerate(ax.patches):
    height = bar.get_height()
    if height > 0:
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.show()

# Histograma con facetas (similar a p4 en R) - SOLUCION DEFINITIVA
plt.figure(figsize=(15, 5))

for i, clase in enumerate(sorted(datos['pclass'].unique())):
    plt.subplot(1, 3, i+1)
    subset = datos[datos['pclass'] == clase]
    sns.histplot(data=subset, x='age', hue='survived_str', 
                 alpha=0.6, bins=30, element='step',
                 palette={'0': '#DA79F2', '1': '#7999F2'})  # Usando strings
    plt.title(f'Clase {clase}')
    plt.xlabel('Edad (Años)')
    plt.ylabel('Cantidad de pasajeros')
    if i == 0:
        plt.legend(title='', labels=['No sobrevivio', 'Sobrevivio'])
    else:
        plt.legend().remove()

plt.suptitle('Distribucion por Edad, Clase y Supervivencia', fontsize=14)
plt.tight_layout()
plt.show()

# ==================== NIVEL 3: ANALISIS AVANZADO CON PANDAS ====================
print("\n=== NIVEL 3: ANALISIS AVANZADO CON PANDAS ===")

print("\n--- Tasa de supervivencia por genero y clase ---")

tasa_supervivencia = (datos_numeric.groupby(['sex', 'pclass'])['survived_num']
                      .agg(['count', 'mean'])
                      .round(3))
tasa_supervivencia.columns = ['Total', 'Tasa_Supervivencia']
tasa_supervivencia['Tasa_Porcentaje'] = tasa_supervivencia['Tasa_Supervivencia'] * 100
print(tasa_supervivencia)

print("\n--- Analisis detallado por grupo ---")
analisis_grupo = (datos_numeric.groupby(['sex', 'pclass', 'Child'])
                  .agg({
                      'survived_num': ['count', 'mean', 'sum'],
                      'age': 'mean'
                  })
                  .round(2))
print(analisis_grupo)

# Visualizacion de la tasa de supervivencia (similar a p5 en R)
plt.figure(figsize=(12, 6))
tasa_plot = datos_numeric.groupby(['sex', 'pclass'])['survived_num'].mean().reset_index()
tasa_plot['Tasa'] = tasa_plot['survived_num'] * 100

ax = sns.barplot(data=tasa_plot, x='pclass', y='Tasa', hue='sex',
                 palette={'female': '#F7D69E', 'male': '#D1FFE1'})
plt.title('Tasa de supervivencia por genero y clase', fontsize=14)
plt.xlabel('Clase del pasajero')
plt.ylabel('Tasa de supervivencia (%)')
plt.legend(title='Genero', labels=['Hombre', 'Mujer'])
# Agregar etiquetas de porcentaje
for i, bar in enumerate(ax.patches):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 1,
            f'{height:.1f}%', ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.show()

# FacetGrid con KDE (alternativa a los histogramas)
g = sns.FacetGrid(datos, col='pclass', hue='survived', height=4, aspect=1.2,
                  palette={0: '#DA79F2', 1: '#7999F2'})
g.map(sns.kdeplot, 'age', fill=True, alpha=0.5)
g.set_axis_labels('Edad (Años)', 'Densidad')
g.set_titles(col_template='Clase {col_name}')
plt.suptitle('Distribucion de Edad por Clase y Supervivencia', y=1.05, fontsize=14)
# Agregar leyenda manualmente
plt.legend(labels=['No', 'Si'], title='Sobrevivio')
plt.tight_layout()
plt.show()

# Heatmap de correlacion
plt.figure(figsize=(10, 8))
variables_numericas = datos_numeric.select_dtypes(include=[np.number])
correlacion = variables_numericas.corr()
sns.heatmap(correlacion, annot=True, cmap='coolwarm', center=0, 
            fmt='.2f', square=True, linewidths=0.5)
plt.title('Matriz de correlacion del Titanic', fontsize=14)
plt.tight_layout()
plt.show()

# ==================== VISUALIZACIONES MULTIPLES ====================
print("\n=== VISUALIZACIONES MULTIPLES ===")

# Crear la columna survived_str si no existe (para usar en todos los gráficos)
if 'survived_str' not in datos.columns:
    datos['survived_str'] = datos['survived'].astype(str)

# Crear los 4 gráficos principales para grid
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# Gráfico 1: Boxplot (similar a p1) - CORREGIDO
sns.boxplot(data=datos, x='survived_str', y='age', 
            palette={'0': '#FAC955', '1': '#2ECC71'}, ax=axes[0,0])
axes[0,0].set_title('Distribución de edad por supervivencia')
axes[0,0].set_xlabel('Supervivencia')
axes[0,0].set_ylabel('Edad (años)')
axes[0,0].set_xticklabels(['No', 'Si'])

# Gráfico 2: Barras absolutas (similar a p2) - CORREGIDO
sns.countplot(data=datos, x='pclass', hue='survived_str',
              palette={'0': '#79EFF2', '1': '#F0F279'}, ax=axes[0,1])
axes[0,1].set_title('Supervivencia por clase - Absoluto')
axes[0,1].set_xlabel('Clase')
axes[0,1].set_ylabel('Cantidad')
axes[0,1].legend(['No', 'Si'])

# Gráfico 3: Barras porcentuales (similar a p3) - CORREGIDO
porcentaje_clase = pd.crosstab(datos['pclass'], datos['survived'], normalize='index') * 100
porcentaje_clase_melt = porcentaje_clase.reset_index().melt(id_vars='pclass', 
                                                            var_name='survived', 
                                                            value_name='percentage')
# Convertir survived a string
porcentaje_clase_melt['survived'] = porcentaje_clase_melt['survived'].astype(str)

sns.barplot(data=porcentaje_clase_melt, x='pclass', y='percentage', hue='survived',
            palette={'0': '#79EFF2', '1': '#F0F279'}, ax=axes[1,0])
axes[1,0].set_title('Supervivencia por clase - Porcentaje')
axes[1,0].set_xlabel('Clase')
axes[1,0].set_ylabel('Porcentaje (%)')
axes[1,0].legend(['No', 'Si'])

# Gráfico 4: Histogramas facetados (similar a p4) - CORREGIDO
# Usar un solo subplot para el histograma combinado
sns.histplot(data=datos, x='age', hue='survived_str', 
             alpha=0.6, bins=20, element='step',
             palette={'0': '#DA79F2', '1': '#7999F2'}, ax=axes[1,1])
axes[1,1].set_title('Distribución por Edad y Supervivencia')
axes[1,1].set_xlabel('Edad (Años)')
axes[1,1].set_ylabel('Cantidad')
axes[1,1].legend(['No', 'Si'])

# Ajustar el layout
plt.suptitle('Análisis completo del Titanic - Múltiples visualizaciones', fontsize=16, y=1.02)
plt.tight_layout()
plt.show()

# ==================== GRAFICO CON R BASE STYLE ====================
print("\n=== GRAFICO CON R BASE STYLE ===")

# Crear gráficos tipo R base con subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Boxplot (similar a R base)
datos.boxplot(column='age', by='survived', ax=axes[0], grid=True, patch_artist=True,
              boxprops=dict(facecolor='lightblue'),
              medianprops=dict(color='red', linewidth=2))
axes[0].set_title('Boxplot de Supervivencia')
axes[0].set_xlabel('Sobrevivio')
axes[0].set_ylabel('Edad')
axes[0].set_xticklabels(['No', 'Si'])

# Barplot (similar a R base)
contingencia_clase = pd.crosstab(datos['pclass'], datos['survived'])
contingencia_clase.plot(kind='bar', ax=axes[1], color=['#7BFF4F', '#FABD55', '#FFB3F7'])
axes[1].set_title('Clase Vs. Supervivencia')
axes[1].set_xlabel('Clase')
axes[1].set_ylabel('Cantidad')
axes[1].legend(['No sobrevivio', 'Sobrevivio'])
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ==================== ESTADISTICAS ADICIONALES ====================
print("\n=== ESTADISTICAS ADICIONALES ===")

print(f"\nTasa de supervivencia general: {datos_numeric['survived_num'].mean()*100:.2f}%")

supervivencia_genero = datos_numeric.groupby('sex')['survived_num'].mean() * 100
print(f"\nSupervivencia por genero:")
print(f"  - Hombres: {supervivencia_genero['male']:.2f}%")
print(f"  - Mujeres: {supervivencia_genero['female']:.2f}%")

supervivencia_clase = datos_numeric.groupby('pclass')['survived_num'].mean() * 100
print(f"\nSupervivencia por clase:")
for clase in [1, 2, 3]:
    print(f"  - {clase}ra clase: {supervivencia_clase[clase]:.2f}%")

supervivencia_child = datos_numeric.groupby('Child')['survived_num'].mean() * 100
print(f"\nSupervivencia por edad:")
print(f"  - Ninos (<12 anos): {supervivencia_child['Child']:.2f}%")
print(f"  - Adultos: {supervivencia_child['Adulto']:.2f}%")

print("\nAnalisis completado exitosamente")