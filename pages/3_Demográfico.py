import folium
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

from PIL import Image
#from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

dados_demograficos = pd.read_csv('/home/marcelo/repos_cds/kawa/data_treated/estados.csv')


def make_sidebar(df):
    st.sidebar.markdown("## Filtro")

    estados = st.sidebar.selectbox(
        'Escolha as Tags',
        options=dados_demograficos['state'].unique().tolist(),
        index=0,
        placeholder='Selecione'
    )

    return estados

#def create_map(dados_demograficos):
#    f = folium.Figure(width=1920, height=1080)
#    
#    m = folium.Map(max_bounds=True).add_to(f)
#
#    marker_cluster = MarkerCluster().add_to(m)
#
#    for _, line in dados_demograficos.iterrows():

    

def main():
    st.set_page_config(page_title="Dados Demográficos", page_icon="🌍", layout="wide")

    st.title('Dados Demográficos')

    # Gráfico de barras de porcentagem de compras por estado
    st.subheader('Porcentagem de Compras por Estado')
    fig = px.bar(dados_demograficos, x='state', y='unique_invoice_count_state', labels={'unique_invoice_count_state': 'Porcentagem de Compras'})

    # Customize the layout
    fig.update_xaxes(title='Estado')
    fig.update_yaxes(title='Porcentagem de Compras')
    st.plotly_chart(fig)

    st.write(dados_demograficos)
    return None


if __name__ == "__main__":
    main()