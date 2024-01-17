import nltk
nltk.download('vader_lexicon')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import SnowballStemmer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import pandas as pd
import re
import streamlit as st


# Funcion para preprocesar texto
def preprocesar_texto(texto):
  if pd.notna(texto):
      # 1: Minusculas
      texto_preproc = texto.lower()

      # 2: Remover signos de puntuacion
      texto_preproc = re.sub(r'[^\w\s]', '', texto_preproc)

      # 3: Tokenización
      tokens = word_tokenize(texto_preproc)

      # 4: Remover stopwords
      tokens = remover_stopwords(tokens) 

      # 5: Lemmatizacion
      lemmatizer = WordNetLemmatizer()
      normal_tokens = [lemmatizer.lemmatize(token) for token in tokens]

      # 6: Recontruir el texto
      texto_preproc = ' '.join(normal_tokens)
      return texto_preproc
  else:
      return texto

# Funcion para remover stopwords
def remover_stopwords(tokens):
    stop_words = set(stopwords.words('spanish'))
    custom_stop_words_esp = ["de", "la", '#']
    stop_words.update(custom_stop_words_esp)
    filt_tokens = [token for token in tokens if token not in stop_words]
    return filt_tokens

# Funcion para categorizar bert
def categorize_bert(star_value):
    if star_value == '5 stars':
      return 'POSITIVA'
    elif star_value == '1 star':
      return 'NEGATIVA'
    else:
      return 'NEUTRAL'