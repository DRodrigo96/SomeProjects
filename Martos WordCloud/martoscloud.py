#!/usr/bin/env python3

# Author: David Sanchez (DRodrigo96)

# Paso 1: Packages y discurso.txt
#---------------------------------------------------------------------------------------------
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from scipy.ndimage import gaussian_gradient_magnitude
from wordcloud import WordCloud, ImageColorGenerator

%matplotlib inline

print("Paquetes importados.")

import urllib.request
link = 'https://raw.githubusercontent.com/DRodrigo96/SomeProjects/master/Martos%20WordCloud/SpeechFile/472121674WalterMartos.txt'
txtFile = urllib.request.urlopen(link)

ministro = str()
for line in txtFile:
    ministro += line.decode()

print("Discurso cargado.")


# Paso 2: Stopwords y puntuación
#---------------------------------------------------------------------------------------------
wordcloud = WordCloud(
    background_color="white", 
    collocations=False
    ).generate(ministro)

plt.figure(figsize=(7, 7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

# Esta lista completa no es necesaria, solo para efectos demostrativos de stopwords. Se capturan los 
# stopwrods comunes en español con stopwords.words('spanish'). SOLO generar una lista con palabras 
# que no sean stopwords comunes y se desean quitar de la nube.
lista_SW = [
    "el", "la", "que", "como", "una", "su", "está", "en", "un", "con", "este", "esto", "lo", "en", "del", "más", 
    "dé", "está", "nuestra","nuestro","para", "él", "nivel", "por", "se", "ésta", "esta", "asimismo", "la", "le", 
    "lo", " de", "contra", "a", "través", "traves", "fin", "ante", "hemos", "por", "ello", "ella", "fecha", "al", 
    "es", "muy", "de", "de ", "del", "las", "los", "ano", "ellas", "ellos", "línea", "De", " de ", "he", "hemos", 
    "ha", "se", "la", "así", "como", "cómo", "A", "He", "Hoy", "Como", "En", "Frente", "frente", "Asimismo", "soles", 
    "fecha", "asímismo", "esta", "a", "año", "ser", "manera", "nueva", "además", "asi", "mismo", "caso", "vamos", 
    "situación", "ello", "día", "nuevo", "asímísmo", "asimísmo", "soles", "persona", "dia", "julio", " asimismo", 
    "asimismo ", " asimismo ", "regionales", "todo"
]

# A) Stopwords de "nltk"
stop_words = stopwords.words('spanish')

# B) Complementamos con las palabras que queremos de la lista manual (lista_SW)
stop_words.extend(lista_SW)
stop_words = set(stop_words)

tokenizer = nltk.RegexpTokenizer(r"\w+")
text_one = tokenizer.tokenize(ministro)

for x in range(len(text_one)):
    text_one[x] = text_one[x].lower()

text_one_ministro = ' '.join([str(elem) for elem in text_one])

print('Primeras palabras del discurso:\n\n' + text_one_ministro[:1000])

print('Length del string:', len(text_one_ministro))

clean_text = [word for word in text_one_ministro.split() if word not in stop_words]
clean_text.sort()
clean_text
text = ' '.join([str(elem) for elem in clean_text])

print('Palabras sin stopwords:\n\n' + text[-500:])


# Paso 3: Tipo de letra
#---------------------------------------------------------------------------------------------
# Path del font en nuestro ordenador
fpath = r'C:\Users\RODRIGO\Desktop\54321\5 Fonts\DINPro-Medium_13936.ttf'

# Objeto WordCloud
wordcloud = WordCloud(
    background_color="white", 
    collocations=False,
    font_path=fpath).generate(text)

plt.figure(figsize=(7, 7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()


# Paso 4: Plantilla y colores
#---------------------------------------------------------------------------------------------
import requests
from io import BytesIO
parrotLink = 'https://github.com/DRodrigo96/SomeProjects/raw/master/Martos%20WordCloud/Image/parrot.jpg'
response = requests.get(parrotLink)
parrot = Image.open(BytesIO(response.content))

parrot

martoz = np.array(parrot)
martoz = martoz[::2, ::2]

martoz_mask = martoz.copy()
martoz_mask[martoz.sum(axis=2)==0] = 255

edges = np.mean([gaussian_gradient_magnitude(martoz[:, :, i] / 255., 2) for i in range(3)], axis=0)
martoz_mask[edges > .08] = 255


# Paso 5: Wordcloud
#---------------------------------------------------------------------------------------------
wc = WordCloud(
    font_path=fpath, # Tipo de letra (font)
    width=1800, height=900,
    max_words=5000,
    collocations=False,
    mask=martoz_mask, # Parrot mask
    scale = 3, 
    random_state=42, # Seed para replicar
    background_color = 'black', # Para fondo transparente: "rgba(255, 255, 255, 0)"
    mode="RGBA", 
    relative_scaling=0
    )
wc.generate(text)

image_colors = ImageColorGenerator(martoz) # Colores extraídos de la imagen
wc.recolor(color_func=image_colors)
plt.figure(figsize=(20, 20))
plt.axis("off")
plt.imshow(wc, interpolation="bilinear")

