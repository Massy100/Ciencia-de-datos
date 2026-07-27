install.packages(c("readxl", "jsonlite", "googlesheets4","rvest", "ggplot2", "dplyr"))
library(dplyr)
library(googlesheets4)
library(rvest)
# Crea un vector
nombres <- c("Falcon 9","Saturn V", "soyuz", "Ariane 5", "Delta IV")
anios = c(2010, 196, 1966, 1996, 2002)
data.frame(Nombre = nombres, "Primer Lanzamiento" = anios) -> cohetes
cohetes
print(cohetes)

#Extraer un dato: mostrar el lanzamiento mas antiguo
indice_antiguo = which.min(cohetes$Primer.Lanzamiento)
print(paste("el cohete mas antiguo es:", cohetes$Nombre[indice_antiguo]))
#Carga de datos
ruta = "https://raw.githubusercontent.com/abemen/datasets/refs/heads/main/antropometricas.csv"
antropometricas = read.csv((ruta))
print(antropometricas)
nasa = "https://www.nasa.gov/2026-news-releases/"
pagina <- read_html(nasa)

# --- Forma 1: EXTRAYENDO POR CLASE CSS (LA MAS PRECISA) ---
#Usamos html_nodes() con el sector clase .hds-a11y-heading-2

titulos <- pagina %>%
  html_nodes(".hds-a11y-heading-22") %>%
  html_text(trim = TRUE) #trim = TRUE elimina espacios innecesarios
print(titulos)

library(ggplot2)

# Secuencias
2:8
# Secuencia indicando el paso
seq(2,3, by=0.1)
# Vector repetitivo
rep(1:3, times=3)
# Vector con elementos repetidos
rep(1:3, each= 4)
# Almacenar un vector
x <- seq(1, 5, by=0.5)

# Crear funciones
doble <- function(x){
  res <- x * 2
  return(res)
}
# Operaciones con vectores
x + 10
x * 3

m = 0.5
b = -2
y = m*x + b
y

# Seleccionar datos
y[3]
# Omitir datos
y[-3]
# Mostrar elementos segun una condicion
x[x>3]

# Generar una matriz
m = matrix(x, nrow=3, ncol=3)
m

n = matrix(x, nrow = 3, ncol = 6)
n

# Gráficas
plot(x, y)

datos2 = read.delim(file="clipboard")

# Dimensión del cojunto de datos (variables)
length(antropometricas)

# Dimensión de una columna (1 variable)
length(antropometricas$Sexo)

max(antropometricas$Peso)
min(antropometricas$Peso)
which.max(antropometricas$Peso)

antropometricas$Peso[34]

# Gráfivos utilizando ggplot
# tres capas = data, aes, geom
misiones <- data.frame(
  Mision = c("Apollo 11", "Apollo 13", "Crew-1", "Starliner", "Artemis I"),
  Exito = c(1, 0, 1, 0, 1),
  Costo = c(355, 400, 220, 450, 500)
)

# Gráfico de barras de costo por misión, coloreado por éxito
ggplot(misiones, aes(x=Mision, y=Costo, fill = as.factor(Exito))) + 
  geom_bar(stat = "identity") + 
  labs(title = "Misiones espaciales", 
       subtitle = "Rojo/Fracaso, Axul/Éxito",
       y = "Costo (Millones USD)", x= "Misión",
       fill = "¿Éxito?"
  ) +
  theme_minimal()







