import pandas as pd
import numpy as np
import nltk
import ssl
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

#Descarga de recursos necesarios para sentimiento
print("Configurando recursos de NLTK...")
try:
    nltk.download('vader_lexicon', quiet=True)
    print("Diccionario VADER listo.")
except Exception as e:
    print(f"No se pudo descargar VADER automáticamente ({e}).")

def main():
    #Cargar el dataset
    archivo_entrada = "dataset_procesado.csv"
    try:
        df = pd.read_csv(archivo_entrada)
        #Limpieza de seguridad: eliminar filas donde el texto limpio quedó vacío
        df = df.dropna(subset=['texto_limpio'])
        print(f"Datos cargados: {len(df)} registros listos para análisis.")
    except FileNotFoundError:
        print(f"Error: No encuentro '{archivo_entrada}'.")
        return

    #Usamos VADER para etiquetar automáticamente
    sia = SentimentIntensityAnalyzer()
    def clasificar_vader(texto):
        #VADER funciona mejor con el texto original
        puntaje = sia.polarity_scores(str(texto))
        compuesto = puntaje['compound']
        # Umbrales estándar
        if compuesto >= 0.05:
            return 'Positivo'
        elif compuesto <= -0.05:
            return 'Negativo'
        else:
            return 'Neutral'
    # Aplicamos la clasificación
    df['sentimiento_etiqueta'] = df['texto'].apply(clasificar_vader)
    print("   Distribución de opiniones encontradas:")
    print(df['sentimiento_etiqueta'].value_counts())
    #Entrenamos el Modelo Supervisado
    print("   Entrenando modelo de Regresión Logística...") 
    #Vectorización TF-IDF
    vectorizer = TfidfVectorizer(max_features=5000, min_df=2, max_df=0.95)
    X = vectorizer.fit_transform(df['texto_limpio'])
    y = df['sentimiento_etiqueta']
    #División Train/Test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    #Modelo
    modelo = LogisticRegression(max_iter=1000)
    modelo.fit(X_train, y_train)
    #Evaluación
    y_pred = modelo.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"   Exactitud (Accuracy) del modelo: {acc:.2f}")
    print("   (Un valor cercano a 1.0 es perfecto, >0.70 es aceptable)")
    
    #K-Means para agrupar mensajes en 5 temas
    num_temas = 5
    kmeans = KMeans(n_clusters=num_temas, random_state=42, n_init=10)
    kmeans.fit(X)
    df['tema_grupo'] = kmeans.labels_
    #Mostrar de qué trata cada tema
    print("   Palabras clave por cada tema detectado:")
    centroides = kmeans.cluster_centers_.argsort()[:, ::-1]
    terminos = vectorizer.get_feature_names_out()
    for i in range(num_temas):
        palabras_top = [terminos[ind] for ind in centroides[i, :5]]
        print(f"   - Tema {i}: {', '.join(palabras_top)}")

    #Función para buscar mensajes parecidos
    def buscar_similares(consulta):
        #Vectorizamos la consulta del usuario
        consulta_vec = vectorizer.transform([consulta])
        #Calculamos similitud con todos los mensajes
        similitudes = cosine_similarity(consulta_vec, X).flatten()
        #Tomamos los 3 índices más altos
        indices_top = similitudes.argsort()[::-1][:3]
        
        print(f"   Búsqueda: '{consulta}'")
        for idx in indices_top:
            score = similitudes[idx]
            if score > 0:
                print(f"   [Similitud: {score:.2f}] {df.iloc[idx]['texto'][:80]}...")
    # Prueba automática con un término común en desarrollo
    buscar_similares("error in code")
    
    #Guardado archivo
    archivo_final = "dataset_final_analizado.csv"
    df.to_csv(archivo_final, index=False)
    print(f"\nResultados guardados en '{archivo_final}'")

if __name__ == "__main__":
    main()