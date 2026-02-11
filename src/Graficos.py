conda install seaborn
conda install wordcloud
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

#Cargar datos
try:
    df = pd.read_csv("dataset_final_analizado.csv")
except FileNotFoundError:
    print("Error: No encuentro 'dataset_final_analizado.csv'")
    exit()

#Gráfico de Pastel (Porcentajes)
plt.figure(figsize=(6,6))
df['sentimiento_etiqueta'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['#66b3ff','#99ff99','#ff9999'])
plt.title("Distribución de Sentimientos")
plt.ylabel("")
plt.savefig("grafico_pastel.png")
plt.close()
print("Gráfico de pastel guardado.")

#Gráfico de Barras (Cantidades)
plt.figure(figsize=(8, 6))
sns.countplot(x='sentimiento_etiqueta', data=df, palette=['#66b3ff','#99ff99','#ff9999'], order=['Positivo', 'Neutral', 'Negativo'])
plt.title('Cantidad de Mensajes por Sentimiento')
plt.xlabel('Sentimiento')
plt.ylabel('Cantidad')
plt.savefig("grafico_barras.png")
plt.close()
print("Gráfico de barras guardado.")

#Nube de Palabras
text = " ".join(texto for texto in df.texto_limpio.dropna())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
plt.figure(figsize=(10,5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.savefig("nube_palabras.png")
plt.close()
print("Nube de palabras guardada.")
