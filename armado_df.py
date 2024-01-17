import os
import pandas as pd
import streamlit as st 
from nlp_cleaning import *
from transformers import pipeline


def concat_csv_files(directory):
    # Lista de archivos CSV 
    csv_files = [csv_file for csv_file in os.listdir(directory) if csv_file.endswith('.csv')]

    # Verificar si hay archivos CSV 
    if not csv_files:
        print(f"No se encontraron archivos CSV en el directorio: {directory}")
        return None

    # Inicializar un DataFrame vacío 
    concat_df = pd.DataFrame()

    # Concatenar los archivos CSV en un solo DF
    for csv_file in csv_files:
        file_path = os.path.join(directory, csv_file)
        df = pd.read_csv(file_path)
        concat_df = pd.concat([concat_df, df], ignore_index=True)
    
    if 'Unnamed: 0' in concat_df.columns:
        concat_df.drop('Unnamed: 0', axis=1, inplace=True)

    return concat_df

path = os.getcwd()
data= concat_csv_files(path)
data['title_preprocesado'] = data['title'].apply(lambda x: preprocesar_texto(x))
data['preprocesado'] = data['summary'].apply(lambda x: preprocesar_texto(x))

def load_sentiment_analysis_model():
    model = pipeline('sentiment-analysis', model='nlptown/bert-base-multilingual-uncased-sentiment')
    return model

model = load_sentiment_analysis_model()
data['bert'] = data['preprocesado'].astype(str).apply(lambda x: model(x)[0]['label'])
data['bert_label'] = data['bert'].apply(lambda x: categorize_bert(x))

data.to_csv('data_st.csv', index= False)