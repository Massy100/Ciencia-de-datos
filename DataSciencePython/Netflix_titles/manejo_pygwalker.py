"""
    Clase para visualizaciones avanzadas con Pygwalker
    Ejemplo generado con DataSets de Seaborn
"""
import pandas as pd
import seaborn as sns
import pygwalker as pyg
from typing import Optional, Dict, Any, List

class VisualizadorAvanzado:
    """
    Clase que encapsula la carga de datasets de seaborn
    y la creacion de visualizaciones interactivas
    """
    # Datasets disponibles en seaborn (los mas comunes)
    DATASETS_DISPONIBLES = [
        "tips", "titanic", "iris", "penguins", "planets",
        "flights", "diamonds", "car_crashes", "exercise",
        "fmri", "gammas", "geyser", "mpg", "paintings",
        "taxis", "brain_networks", "dowjones", "attention"
    ]
    
    def __init__(self, nombre_dataset: str = "tips"):
        # Inicializa la clase cargando el dataset de seaborn 
        self.nombre_dataset = nombre_dataset
        self.df: Optional[pd.DataFrame] = None
        self._cargar_dataset()
        
    def _cargar_dataset(self) -> None:
        try:
            self.df = sns.load_dataset(self.nombre_dataset)
            print('Dataset cargado con exito')
        except Exception as e:
            raise ValueError(f'No se pudo cargar el dataset {self.nombre_dataset}. Verifique el nombre. Error {e}')
