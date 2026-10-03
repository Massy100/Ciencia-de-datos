"""
Manejo del dataset vgsales.csv con PyGWalker.

Este archivo esta inspirado en el ejemplo manejo_pygwalker.py,
pero trabaja directamente con el archivo de ventas de videojuegos.
"""

import pandas as pd
import pygwalker as pyg
from typing import Optional, Dict, Any


class VisualizadorVideojuegos:
    """
    Clase para cargar, explorar, filtrar y visualizar de manera
    interactiva el dataset vgsales.csv utilizando PyGWalker.
    """

    def __init__(self, ruta_dataset: str = "vgsales.csv"):
        self.ruta_dataset = ruta_dataset
        self.df: Optional[pd.DataFrame] = None

        self._cargar_dataset()
        self._limpiar_dataset()

    def _cargar_dataset(self) -> None:
        """Carga el archivo CSV."""
        try:
            self.df = pd.read_csv(self.ruta_dataset)
            print(f"Dataset '{self.ruta_dataset}' cargado con exito.")
        except FileNotFoundError:
            raise FileNotFoundError(
                f"No se encontro el archivo '{self.ruta_dataset}'. "
                "Coloca vgsales.csv en la misma carpeta que este programa."
            )
        except Exception as e:
            raise ValueError(
                f"No se pudo cargar el dataset. Error: {e}"
            )

    def _limpiar_dataset(self) -> None:
        """Realiza una limpieza basica antes de usar PyGWalker."""
        if self.df is None:
            raise RuntimeError("No hay dataset cargado.")

        self.df["Year"] = pd.to_numeric(
            self.df["Year"], errors="coerce"
        ).astype("Int64")

        self.df["Publisher"] = self.df["Publisher"].fillna("Desconocido")

        columnas_texto = ["Name", "Platform", "Genre", "Publisher"]

        for columna in columnas_texto:
            self.df[columna] = self.df[columna].astype(str).str.strip()

        # Columnas calculadas utiles para las visualizaciones.
        self.df["Regional_Sales"] = (
            self.df["NA_Sales"]
            + self.df["EU_Sales"]
            + self.df["JP_Sales"]
            + self.df["Other_Sales"]
        )

        self.df["Sales_Difference"] = (
            self.df["Global_Sales"] - self.df["Regional_Sales"]
        ).round(2)

        self.df["Sales_Category"] = pd.cut(
            self.df["Global_Sales"],
            bins=[-1, 0.5, 1, 5, float("inf")],
            labels=[
                "Menos de 0.5M",
                "0.5M a 1M",
                "1M a 5M",
                "Mas de 5M",
            ],
        )

    def explorar(self) -> Dict[str, Any]:
        """Devuelve un resumen exploratorio del dataset."""
        if self.df is None:
            raise RuntimeError("No hay dataset cargado.")

        resumen = {
            "shape": self.df.shape,
            "columnas": list(self.df.columns),
            "tipos": self.df.dtypes.astype(str).to_dict(),
            "nulos": self.df.isnull().sum().to_dict(),
            "estadisticas": self.df.describe(include="all").to_dict(),
        }

        return resumen

    def mostrar_resumen(self) -> None:
        """Imprime un resumen legible del dataset."""
        if self.df is None:
            raise RuntimeError("No hay dataset cargado.")

        print("\n" + "=" * 60)
        print("RESUMEN DEL DATASET VENTAS DE VIDEOJUEGOS")
        print("=" * 60)

        print(f"\nDimensiones: {self.df.shape}")

        print("\nPrimeras 5 filas:")
        print(self.df.head())

        print("\nTipos de datos:")
        print(self.df.dtypes)

        print("\nValores nulos por columna:")
        print(self.df.isnull().sum())

        print("\nTop 10 videojuegos por ventas globales:")
        print(
            self.df[
                ["Name", "Platform", "Year", "Genre", "Global_Sales"]
            ]
            .sort_values("Global_Sales", ascending=False)
            .head(10)
        )

        print("\n" + "=" * 60)

    def visualizar_interactivo(
        self,
        tema: str = "light",
        ocultar_botones: bool = False,
        spec_guardado: Optional[str] = None,
    ):
        """
        Lanza PyGWalker para crear graficas interactivas.

        Algunos campos recomendados:
        - Year
        - Platform
        - Genre
        - Publisher
        - NA_Sales
        - EU_Sales
        - JP_Sales
        - Other_Sales
        - Global_Sales
        """

        if self.df is None:
            raise RuntimeError("No hay dataset cargado.")

        kwargs = {
            "dataset": self.df,
            "theme_key": tema,
            "appearance": "dark" if tema == "dark" else "light",
            "computation": "kernel",
            "hide_data_source_config": ocultar_botones,
        }

        if spec_guardado is not None:
            kwargs["spec_path"] = spec_guardado

        print(f"Lanzando PyGWalker con tema '{tema}'...")

        return pyg.walk(**kwargs)

    def filtrar(self, condiciones: Dict[str, Any]) -> "VisualizadorVideojuegos":
        """
        Filtra el DataFrame por igualdad.

        Ejemplo:
        viz_wii = viz.filtrar({"Platform": "Wii"})
        """

        if self.df is None:
            raise RuntimeError("No hay dataset cargado.")

        df_filtrado = self.df.copy()

        for columna, valor in condiciones.items():
            if columna not in df_filtrado.columns:
                raise ValueError(
                    f"La columna '{columna}' no existe en el DataFrame."
                )

            df_filtrado = df_filtrado[df_filtrado[columna] == valor]

        nueva = VisualizadorVideojuegos.__new__(VisualizadorVideojuegos)
        nueva.ruta_dataset = self.ruta_dataset
        nueva.df = df_filtrado.copy()

        print(
            f"Dataset filtrado correctamente: "
            f"{df_filtrado.shape[0]} filas restantes."
        )

        return nueva

    def exportar_html(
        self,
        ruta: str = "videojuegos_pygwalker.html",
    ) -> None:
        """Exporta una version HTML interactiva del dataset."""
        if self.df is None:
            raise RuntimeError("No hay dataset cargado.")

        html = pyg.to_html(
            self.df,
            theme_key="light",
            use_kernel_calc=True,
        )

        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(html)

        print(f"Visualizacion HTML guardada en: {ruta}")


# ============================================================
# EJEMPLO DE USO
# ============================================================

if __name__ == "__main__":

    # 1. Crear el visualizador
    viz = VisualizadorVideojuegos("vgsales.csv")

    # 2. Mostrar informacion general
    viz.mostrar_resumen()

    # 3. Abrir PyGWalker
    viz.visualizar_interactivo(tema="light")

    # Ejemplos opcionales:
    #
    # Mostrar solo juegos de Wii:
    # viz_wii = viz.filtrar({"Platform": "Wii"})
    # viz_wii.visualizar_interactivo()
    #
    # Mostrar solo juegos del genero Action:
    # viz_action = viz.filtrar({"Genre": "Action"})
    # viz_action.visualizar_interactivo()
    #
    # Exportar a HTML:
    # viz.exportar_html()
