# 02_imputacion_r.R
# Metodos de imputacion por valores faltantes

library(tidyverse)
library(mice)
library(naniar)
library(here)

# Cargar  datos
datos <- readRDS(here("data/datos_raw.rds"))

cat("=== IMPUTACION DE VALORES FALTANTES ===\n\n")

# 1. Imputacion por mediana
cat("1. Imputacion por mediana...\n")

datos_median <- datos
for (col in names(datos_median)){
  if(is.numeric(datos_median[[col]])){
    datos_median[[col]][is.na(datos_median[[col]])]<-
      median(datos_median[[col]],na.rm = TRUE)
  }
}
saveRDS(datos_median, here("data/datos_median.rds"))
cat("Completado\n")

# 2. Imputacion por regresion
cat("2. Imputacion por regresion...\n")
datos_regresion <- datos
modelo_edad <- lm(edad ~ ingreso + educacion + experiencia, data = datos)
indices_na_edad <- which(is.na(datos_regresion$edad))
if (length(indices_na_edad) > 0){
  datos_regresion$edad[indices_na_edad] <-
    predict(modelo_edad, newdata = datos_regresion[indices_na_edad, ])
}
saveRDS(datos_regresion, here("data/datos_regresion.rds"))
cat("Completado\n")

# 3. Imputacion por MICE
cat("3. Imputacion por MICE\n")
imputaciones <- mice(datos, m = 5, method = 'pmm',
                     maxit = 50, seed = 123, printFlag = FALSE)
datos_mice <- complete(imputaciones, 1)
saveRDS(datos_mice, here("data/datos_mice.rds"))
cat("Completado\n")

cat("Todas las imputaciones se han completado\n")
