conda install pandas nltk scikit-learn
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

#Configuración inicial
#Descargamos los diccionarios de palabras de NLTK
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
# Inicializamos herramientas
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english')) # GitHub suele estar en inglés
def limpiar_texto(texto):
#Aplica la limpieza básica y normalización requerida en RF-02.
    if not isinstance(texto, str):
        return ""
    #Conversión a minúsculas
    texto = texto.lower()
    #Eliminación de URLs (http://...) y menciones de usuario (@usuario)
    texto = re.sub(r'http\S+|www\S+|https\S+', '', texto, flags=re.MULTILINE)
    texto = re.sub(r'@\w+', '', texto)
    #Eliminación de signos de puntuación, números y caracteres especiales
    #Conservamos solo letras (a-z) y espacios.
    texto = re.sub(r'[^a-z\s]', '', texto)
    #Tokenización
    tokens = texto.split()
    #Eliminación de Stopwords y Lematización
    tokens_limpios = [
        lemmatizer.lemmatize(word) 
        for word in tokens 
        if word not in stop_words and len(word) > 2
    ]    
    return " ".join(tokens_limpios)

def main():
    print("-Preprocesamiento y Representación -")  
    #Cargar el dataset
    try:
        df = pd.read_csv("dataset_github.csv")
        print(f"Cargados {len(df)} mensajes originales.")
    except FileNotFoundError:
        print("Error: No se encuentra 'dataset_github.csv'. Ejecuta primero la Fase 1.")
        return
    #Aplicar limpieza
    print("Aplicando limpieza y normalización")
    # Creamos una nueva columna 'texto_limpio' para no perder el original
    df['texto_limpio'] = df['texto'].apply(limpiar_texto)
    # Eliminamos filas que hayan quedado vacías después de la limpieza
    df = df[df['texto_limpio'] != ""]
    print(f"Mensajes válidos después de limpieza: {len(df)}")
    print("Ejemplo limpio:", df['texto_limpio'].iloc[0])
    #Representación Vectorial TF-IDF (RF-03)
    print("\nGenerando matriz TF-IDF")
    # Configuración según RF-03
    vectorizer = TfidfVectorizer(
        max_features=5000,      
        min_df=2,               
        max_df=0.95,            
        ngram_range=(1, 1)
    )
    #Ajustamos el modelo y transformamos el texto a números
    tfidf_matrix = vectorizer.fit_transform(df['texto_limpio'])

    # Guardamos el CSV limpio
    df.to_csv("dataset_procesado.csv", index=False)
    print("\n- Resultados -")
    print(f"Vocabulario aprendido: {len(vectorizer.get_feature_names_out())} palabras únicas.")
    print(f"Dimensiones de la matriz TF-IDF: {tfidf_matrix.shape}")
    print("Archivo guardado: 'dataset_procesado.csv'")

if __name__ == "__main__":
    main()