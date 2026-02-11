# Análisis de Opinión en Repositorios Git (PLN)

Este proyecto implementa un sistema de **Procesamiento de Lenguaje Natural (PLN)** para analizar la "salud" y opinión de proyectos de software Open Source.

El sistema extrae mensajes reales (Issues, Pull Requests y Comentarios) de GitHub y aplica técnicas de aprendizaje automático para detectar sentimientos, identificar temas recurrentes y buscar mensajes similares.

## Funcionalidades

El proyecto cumple con los siguientes objetivos de análisis:

* **Recolección (RF-01):** Conexión a la API de GitHub para descargar datasets reales.
* **Preprocesamiento (RF-02):** Limpieza de texto, eliminación de ruido (URLs, código), stopwords y Lematización.
* **Representación (RF-03):** Vectorización de textos usando el modelo **TF-IDF**.
* **Análisis de Sentimiento (RF-04):** Clasificación automática (Positivo, Negativo, Neutral) usando **VADER** y **Regresión Logística**.
* **Detección de Temas (RF-05):** Agrupamiento no supervisado usando **K-Means Clustering**.
* **Buscador Semántico (RF-06):** Búsqueda de mensajes similares mediante **Similitud del Coseno**.

## Estructura del Proyecto

Los archivos están organizados siguiendo el flujo de trabajo de datos:

```text
├── recoleccion_datos.py         # 1. Script de extracción (GitHub API)
├── dataset_github.csv           #    Salida: Datos crudos
│
├── procesamiento.py             # 2. Script de limpieza y normalización
├── dataset_procesado.csv        #    Salida: Datos limpios y lematizados
│
├── dataset_final_analizado.py   # 3. Script de Modelos (Sentimiento, K-Means, Similitud)
├── dataset_final_analizado.csv  #    Salida: Datos etiquetados y con clusters
│
├── Graficos.py                  # 4. Generador de Visualizaciones
├── grafico_pastel.png           #    Imagen: Distribución porcentual
├── grafico_barras.png           #    Imagen: Conteo de mensajes
└── nube_palabras.png            #    Imagen: WordCloud del repositorio
│
└── README.md                    # Documentación del proyecto
