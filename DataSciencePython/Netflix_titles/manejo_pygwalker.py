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
        
    def explorar(self) -> Dict[str, Any]:
        # Devuelve un resumen exploratorio del Dataset
        if self.df is None:
            raise RuntimeError("No hay dataset cargado")
        
        resumen = {
            "shape": self.df.shape,
            "columnas": list(self.df.columns),
            "tipos": self.df.dtypes.astype(str).to_dict(),
            "nulos": self.df.isnull().sum().to_dict(),
            "estadisticas": self.df.describe(include="all").to_dict(),
        }
        return resumen

    def mostrar_resumen(self) -> None:
        # Imprime un resumen legible del dataset
        print("\n" + "="*50)
        print(f"Resumen del DataSet: {self.nombre_dataset.upper()}")
        print("\n" + "="*50)
        print(f"Dimensiones: {self.df.shape}")
        print("Primeras 5 filas: \n{self.df.head()}")
        print(f"\nTipos de datos: \n{self.df.dtypes}")
        print(f"\nValores nulos por columna: \n{self.df.isnull().sum()}")
        print("\n" + "="*50)
        
    def visualizar_interactivo(
        self,
        tema: str = "dark",
        modo: str = "explore",
        size: str = "auto",
        ocultar_botones: bool = False,
        spec_guardado: Optional[str] = None,
    ):
        # Genera la visualizacion interactiva con Pygwalker
        # tema: str -> Tema visual: 'dark', 'light', 'streamlit', 'vega', 'cream'
        if self.df is None:
            raise RuntimeError("No hay dataset cargado")
        
        kwargs = {
            "dataset": self.df,
            "theme_key": tema, # Usar theme key en lugar de theme
            "apperance": "dark" if tema == "dark" else "media", # Reemplaza el parametro de apperance
            "computation": "kernel", # Usar computation en lugar de parametros obsoletos
            "hide_data_source_config": ocultar_botones,
        }
        
        # Solo incluir spec_path si se proporciono un valor valido
        if spec_guardado is not None:
            kwargs["spec_path"] = spec_guardado
            
        print(f"Lanzando Pygwalker con tema '{tema}' y modo '{modo}'")
        
        return pyg.walk(**kwargs)
        
    def visualizar_personalizado(
        self,
        spec_json: str,
        tema: str = "dark"
    ):
        # Renderiza PyGWalker con una especificacion JSON predefinida
        
        if self.df is None:
            raise RuntimeError("No hay dataset cargado")
        
        return pyg.render(self.df, spec=spec_json, theme=tema)
    def guardar_spec(self, ruta: str = "especificacion.json") -> None:
        # Guarda la especificacion actual de la visualizacion
        # Util para reproducir graficas posteriormente
        if self.df is None:
            raise RuntimeError("No hay dataset cargado")
        # Generar el HTML / JS con la spec embebida
        html = pyg.to_html(
            self.df,
            spec_path = ruta,
            theme = "dark",
            use_kernel_calc = True,
        )
        
        with open(ruta.replace(".json", ".html"), "w", encoding="utf-8") as f:
            f.write(html)
            
        print(f"Especificacion guardada en {ruta} y HTML generado en {ruta.replace('.json', 'html')}")
        print(f"HTML exportado en {ruta.replace('.json', '.html')}")
        
    def filtrar(self, condiciones: Dict[str, Any]) -> "VisualizadorAvanzado":
        # Filtra el dataset y devuelve una nueva instancia de la clase
        if self.df is None:
            raise RuntimeError("No hay dataset cargado")
        
        df_filtrado = self.df.copy()
        for col, val in condiciones.items():
            if col not in df_filtrado.columns:
                raise ValueError(f"La columna '{col}' no existe en el DataFrame")
            df_filtrado = df_filtrado[df_filtrado[col] == val]
        
        # Crear nueva instancia sin recargar desde seaborn
        nueva = VisualizadorAvanzado.__new____(VisualizadorAvanzado)
        nueva.nombre_dataset = f"{self.nombre_dataset} (filtrado)"
        nueva.df = df_filtrado
        print(f"Dataset filtrado: {df_filtrado.shape[0]} filas restantes")
        return nueva
    
    @classmethod
    def listar_datasets(cls) -> List[str]:
        # Devuelve la lista de datasets soportados
        return cls.DATASETS_DISPONIBLES
    
## EJEMPLO DE USO
# # 1. Instanciar la clase con un dataset
# viz = VisualizadorAvanzado("tips")
    
# # 2. Ver el resumen del DataSet
# viz.mostrar_resumen()

# # Lanzar la visualizacion interactiva (recomendado: tema 'dark')
# viz.visualizar_interactivo(tema="dark", modo="explore")


viz = VisualizadorAvanzado("diamonds")
viz.visualizar_interactivo(tema="vega")
        
        