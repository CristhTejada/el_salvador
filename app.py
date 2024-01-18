import pandas as pd
import numpy as np
import streamlit as st
#import altair as alt
#from transformers import AutoTokenizer, AutoModelForSequenceClassification
#from PIL import Image
import base64
import os
#from nlp_cleaning import *
#from armado_df import *
#from pysentimiento import create_analyzer
#from transformers import pipeline



#st.header('Omdena Local Chapter El Salvador')
st.image("Omdena-San-Salvador-Logo.jpeg", width=500)
st.sidebar.image("diarios.jpg",  width=300, use_column_width=False)
# Puedes incluso usar HTML si es necesario
st.markdown("<h1 style='font-family: Times New Roman, sans-serif; color: black; text-align: center;'>Análisis de Sentimiento en Noticias</h1>", unsafe_allow_html=True)
st.markdown(""" ---   
            
*¿Cómo se utilizan esta app?*:



*1. Seleccionar en la barra lateral el Diario y la sección deseada.*
            
*2. Elegir el titulo deseado.*
            
*3. Escribir el número del artículo deseado y se obtiene el sentimiento del resumen del artículo.*
            
---   
""")


#st.title("Análisis de Sentimiento en Noticias")
# path = os.getcwd()
# data= concat_csv_files(path)
# data['title_preprocesado'] = data['title'].apply(lambda x: preprocesar_texto(x))
# data['preprocesado'] = data['summary'].apply(lambda x: preprocesar_texto(x))

data = pd.read_csv('data_st.csv')
st.sidebar.markdown("<h2 style='font-family: Times New Roman, sans-serif; color: black; text-align: left;'>Diario</h2>", unsafe_allow_html=True)
#st.sidebar.header('Diario')
opciones_diario = ["Todos"] + list(data['source_id'].unique())
diario_seleccionado = st.sidebar.selectbox("Selecciona una opción", opciones_diario)

st.sidebar.markdown("<h2 style='font-family: Times New Roman, sans-serif; color: black; text-align: left;'>Sección</h2>", unsafe_allow_html=True)
#st.sidebar.header('Sección')
opciones_seccion = ['Todas', 'Política', 'Internacionales', 'Deportes'] 
seccion_seleccionada = st.sidebar.selectbox("Selecciona una opción", opciones_seccion)

data_filt = data[['source_id', 'category_id','title', 'summary', 'bert_label']]
# Aplicar filtros
if diario_seleccionado == "Todos" and seccion_seleccionada == "Todas":
    df_filtrado = data_filt  
else:
    # Aplicar filtros adicionales
    if diario_seleccionado != "Todos":
        df_filtrado = data_filt[data_filt['source_id'] == diario_seleccionado]
    else:
        df_filtrado = data_filt

    if seccion_seleccionada != "Todas":
        df_filtrado = df_filtrado[data_filt['category_id'] == seccion_seleccionada]



# @st.cache_data(ttl=86400)
# def load_sentiment_analysis_model():
#     model = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')
#     return model

# model = load_sentiment_analysis_model()
# df_filtrado['bert'] = df_filtrado['preprocesado'].astype(str).apply(lambda x: model(x)[0]['label'])
# df_filtrado['bert_label'] = df_filtrado['bert'].apply(lambda x: categorize_bert(x))


def df_showing(df):
    df_show = df[['title','source_id', 'category_id', 'bert_label']].rename(columns={
    'source_id': 'Diario', 'category_id': 'Sección','title': 'Título', 'bert_label':'Etiqueta'
    }).reset_index(drop = True)
    df_show.index += 1
    return df_show
df_show = df_showing(df_filtrado)
df_show_2= df_show[['Título','Diario']]
st.subheader('Artículos scrapeados de Diarios de "El Salvador"')
st.dataframe(df_show_2)



# Widget de entrada para el índice
indice_ingresado = st.number_input("Ingrese el número de artículo", min_value=df_show.index.min(), 
                                   max_value=df_show.index.max(), step=1)

if indice_ingresado in df_show.index:
    # Mostrar las filas correspondientes al índice ingresado
    fila_seleccionada = df_show.loc[indice_ingresado]
    
    # Emoji y mensaje según el valor de la columna 'bert_label'
    if fila_seleccionada['Etiqueta'] == 'POSITIVA':
        #t.markdown("<h2 style='font-family: Times New Roman, sans-serif; color: black; text-align: left;'>Sentimiento: Positivo :smiley:</h2>", unsafe_allow_html=True)
        st.markdown("**Sentimiento**: Positivo :smiley:")
        st.image("positivo.png")
    elif fila_seleccionada['Etiqueta'] == 'NEGATIVA':
        st.markdown("**Sentimiento**: Negativo :angry:")
        st.image("negativo.png")
    else:
        st.markdown("**Sentimiento**: Neutral 😐")
        st.image("neutral.png")
else:
    st.warning("El número de artículo ingresado no está presente en el DataFrame.")











