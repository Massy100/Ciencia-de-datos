# Paquetes necesarios
# !pip install pywalker
# !pip install streamlit
import pandas as pd
import pygwalker as pyg
import seaborn as sns

df = pd.read_csv('netflix_titles.csv')
print(df.head())

df['date_added'] = df['date_added'].str.strip()
df['date_added'] = pd.to_datetime(df['date_added'])
print(df.head())
print(df.dtypes)

df['date_added_year'] = df['date_added'].dt.year.fillna(0).astype(int)
df['date_added_month'] = df['date_added'].dt.month.fillna(0).astype(int)

df['duration_valor'] = df['duration'].str.extract(r'(\d+)').astype(float).fillna(0).astype(int)
df['duration_unit'] = df['duration'].fillna('0 -').str.split('').str[1]
print(df)

panel = pyg.walk(df, dark='light')

