# Análisis Exploratorio de Datos con Python

Proyecto desarrollado completamente en Python para realizar un flujo de análisis de datos que incluye:

- Generación de datos.
- Introducción de valores faltantes MCAR y MAR.
- Generación de valores atípicos.
- Imputación por mediana.
- Imputación por regresión.
- Imputación mediante MICE.
- Detección de outliers mediante IQR.
- Tratamiento de outliers mediante winsorización.
- Análisis exploratorio.
- Generación de visualizaciones.

---

## Estructura del proyecto

```text
analisis_exploratorio_eda/
│
├── __init__.py
├── 01_carga_datos.py
├── 02_imputacion.py
├── 03_outliers.py
├── Analisis_Exploratorio.py
├── README.md
├── requirements.txt
│
├── data/
│   ├── datos_raw.csv
│   ├── datos_raw.pkl
│   ├── datos_median.pkl
│   ├── datos_regresion.pkl
│   ├── datos_mice.pkl
│   └── datos_winsor.pkl
│
└── outputs/
    ├── 01_valores_faltantes.png
    ├── 02_comparacion_imputacion.png
    └── 03_comparacion_outliers.png
```

---

# Archivos del proyecto

## 01_carga_datos.py

Genera un conjunto de datos de ejemplo con 1000 observaciones.

Las variables utilizadas son:

- id
- edad
- ingreso
- educacion
- experiencia
- satisfaccion

También introduce de manera controlada:

- 50 valores faltantes MCAR en `edad`.
- 30 valores faltantes MAR en `satisfaccion`.
- 20 valores atípicos en `ingreso`.

Genera los archivos:

```text
data/datos_raw.pkl
data/datos_raw.csv
```

---

## 02_imputacion.py

Realiza tres métodos de imputación de valores faltantes.

### Imputación por mediana

Los valores faltantes de variables numéricas son reemplazados por la mediana.

Genera:

```text
data/datos_median.pkl
```

### Imputación por regresión

Se utilizan modelos de regresión para estimar los valores faltantes de:

- edad
- satisfaccion

Genera:

```text
data/datos_regresion.pkl
```

### Imputación mediante MICE

Se utiliza Multiple Imputation by Chained Equations con Predictive Mean Matching.

La variable `id` no es utilizada como predictor.

Genera:

```text
data/datos_mice.pkl
```

---

## 03_outliers.py

Utiliza los datos previamente imputados mediante MICE.

Los valores atípicos de la variable `ingreso` son detectados mediante el método del rango intercuartílico (IQR).

La regla utilizada es:

```text
Límite inferior = Q1 - 1.5 × IQR

Límite superior = Q3 + 1.5 × IQR
```

Posteriormente se aplica winsorización utilizando:

```text
Percentil inferior = 5%

Percentil superior = 95%
```

Genera:

```text
data/datos_winsor.pkl
```

---

## Analisis_Exploratorio.py

Es el archivo final del proyecto.

Carga todos los conjuntos de datos generados anteriormente y realiza:

- Resumen estadístico.
- Identificación de valores faltantes.
- Comparación de métodos de imputación.
- Comparación de distribuciones de edad.
- Comparación de ingreso antes y después de la winsorización.
- Generación de conclusiones.
- Creación automática de visualizaciones.

Las gráficas se almacenan en:

```text
outputs/
```

Se generan:

```text
01_valores_faltantes.png
02_comparacion_imputacion.png
03_comparacion_outliers.png
```

---

# Instalación

Se recomienda utilizar Python 3.10 o superior.

Instalar las dependencias con:

```bash
pip install -r requirements.txt
```

---

# Dependencias

El archivo `requirements.txt` debe contener:

```text
numpy
pandas
matplotlib
scikit-learn
statsmodels
```

---

# Ejecución

Los programas deben ejecutarse en el siguiente orden.

## Paso 1

Generar los datos:

```bash
python 01_carga_datos.py
```

## Paso 2

Realizar las imputaciones:

```bash
python 02_imputacion.py
```

## Paso 3

Detectar y tratar los outliers:

```bash
python 03_outliers.py
```

## Paso 4

Ejecutar el análisis exploratorio:

```bash
python Analisis_Exploratorio.py
```

---

# Flujo del proyecto

```text
01_carga_datos.py
        |
        v
datos_raw.pkl
        |
        v
02_imputacion.py
        |
        +-----------------------+
        |           |           |
        v           v           v
datos_median   datos_regresion  datos_mice
                                    |
                                    v
                            03_outliers.py
                                    |
                                    v
                            datos_winsor.pkl
                                    |
                                    v
                       Analisis_Exploratorio.py
                                    |
                                    v
                              outputs/
```

---

# Resultado

Al finalizar correctamente la ejecución, el proyecto tendrá:

- Los datos originales.
- Los conjuntos de datos imputados.
- Los datos tratados mediante winsorización.
- Estadísticas descriptivas.
- Comparaciones entre métodos de imputación.
- Comparaciones antes y después del tratamiento de outliers.
- Gráficas exportadas automáticamente en formato PNG.

Todo el proceso se realiza utilizando Python.