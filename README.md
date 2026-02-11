# Análisis de Opinión en Repositorios Git

Este proyecto implementa un sistema de **Procesamiento de Lenguaje Natural (PLN)** clásico para analizar la "salud" y opinión de proyectos de software Open Source.

El sistema extrae mensajes reales (Issues, Pull Requests y Comentarios) de GitHub y aplica técnicas de aprendizaje automático para detectar sentimientos, identificar temas recurrentes y buscar mensajes similares.

## Funcionalidades

El proyecto cumple con los siguientes objetivos de análisis:

* **Recolección de Datos (RF-01):** Conexión a la API de GitHub para descargar datasets reales.
* **Preprocesamiento (RF-02):** Limpieza de texto, eliminación de ruido (URLs, código), stopwords y Lematización/Stemming.
* **Representación (RF-03):** Vectorización de textos usando el modelo **TF-IDF**.
* **Análisis de Sentimiento (RF-04):** Clasificación automática de mensajes (Positivo, Negativo, Neutral) usando Regresión Logística.
* **Detección de Temas (RF-05):** Agrupamiento no supervisado usando **K-Means Clustering**.
* **Buscador Semántico (RF-06):** Búsqueda de mensajes similares mediante **Similitud del Coseno**.

## Estructura del Repositorio

El proyecto sigue la estructura estándar solicitada:

```text
├── data/                                 # Datasets generados
│   ├── dataset_github.csv                # Datos crudos extraídos de la API
│   ├── dataset_procesado.csv             # Datos limpios y normalizados
│   └── dataset_final_analizado.csv       # Datos con etiquetas de sentimiento y temas
│
├── src/                            # Código fuente
│   ├── recoleccion_datos.py        # Script para conectar con GitHub API
│   ├── preprocesamiento.py         # Script de limpieza y TF-IDF
│   └── dataset_final_analizado.py  # Script de modelos (Sentimiento, K-Means, Similitud)
│
└── README.md                   # Documentación del proyecto
