import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

## Matplot lib
# Datos para el grafico de ejemplo
edades = [20, 25, 30, 25, 40]
plt.plot(edades)
plt.title("Mi primer grafico en Python")
plt.show()

sns.get_dataset_names()
titanic = sns.load_dataset("titanic")
print(titanic.head())
print(titanic.info())

plt.scatter(titanic['age'], titanic['fare'])
plt.xlabel("Edad")
plt.ylabel("Tarifa")
plt.title("Relación entre Edad y Tarifa");
plt.show()

## Seaborn Edad vs Supervivencia
# Cajas y bigotes de edad por supervivencia
sns.boxplot(x='survived', y='age', data=titanic, palette='pastel')
plt.title("Distribuición de Edad por Supervivencia")
plt.show()

# Barras de supervivencia por clase (%)
sns.barplot(x='pclass', y='survived', data=titanic, errorbar=None, hue='pclass', palette='muted', legend = False)
plt.title("Tasa de supervivencia por clase")
plt.show()

## Ploty - Graficos interactivos
fig = px.scatter(titanic, x='age', y='fare', color='survived', title="Relación entre Edad-Tarifa por supervivencia", labels={'survived':'Supervivencia'})
fig.show()

fig1 = px.scatter_3d(titanic, x='age', y='fare', z='pclass', color='survived', symbol="sex", title="Analisis 3D - Titanic", labels={'survived':'Supervivencia'})
fig1.show()