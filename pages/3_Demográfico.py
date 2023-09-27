#import folium
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

from PIL import Image
#from streamlit_folium import folium_static
#from folium.plugins import MarkerCluster

df = pd.read_csv('./data/kawa_rfm.csv')
dados_state = pd.read_csv('./data/estados.csv')
dados_regiao = pd.read_csv('./data/regiao.csv')
porc_cluster = pd.read_csv('./data/demog.csv')


def make_sidebar(dados_regiao):
    image_path = './images/'
    image = Image.open(image_path + 'logo_target.png')

    st.sidebar.image(image, width=240)
    
    clusters = st.sidebar.selectbox(
        'Escolha o Cluster',
        options=df['Classe'].unique().tolist(),
        index=0,
        placeholder='Selecione'
    )

#    st.sidebar.markdown("## Filtro")

    return clusters

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

    clusters = make_sidebar(dados_regiao)

    st.title('Dados Demográficos')

    with st.container():
        st.write("---")
        st.subheader('Porcentagem de Clientes por Cluster')

        df_grouped = porc_cluster.groupby(['Classe', 'region'])['customer_id'].count().reset_index()
        tt_customer = porc_cluster['customer_id'].count()
#        df_total = porc_cluster.groupby('Classe')['customer_id'].count().reset_index()
#        df_total.rename(columns={'customer_id': 'total_customer'}, inplace=True)
#        df_result = pd.merge(df_grouped, df_total, on='Classe', how='left')
        df_grouped['percentage'] = (df_grouped['customer_id'] / tt_customer) * 100

        df_result_filt = df_grouped[df_grouped['Classe'] == clusters]

        df_result_filt['percentage'] = df_result_filt['percentage'].apply(lambda x: f'{x:.2f}%')

        df_result_filt = df_result_filt.rename(columns={'Classe': 'Cluster', 'region': 'Região', 'customer_id': 'Qtde Clientes', 'percentage': 'Porcentagem'})

        st.write(df_result_filt)

    with st.container():
        st.write("---")
        st.subheader('Pedidos por Estado')
        fig = px.bar(dados_state, x='state', y='unique_invoice_count_state', labels={'unique_invoice_count_state': 'Pedidos'})
        tp = dados_state['unique_invoice_count_state'].sum()
        dados_state['percentage'] = (dados_state['unique_invoice_count_state'] / tp) * 100

#        for i, row in dados_state.iterrows():
#            fig.add_annotation(
#                x=row['state'],
#                y=row['unique_invoice_count_state'],
#                text=f"{row['percentage']:.2f}%",
#                showarrow=False,
#                font=dict(size=12, color='black'),
#            )
        # Customize the layout
        fig.update_xaxes(title='Estados')
        fig.update_yaxes(title='Quantidade de Pedidos')
        st.plotly_chart(fig)

    with st.container():
        st.write("---")
        st.subheader('Pedidos por Região')
        fig = px.bar(dados_regiao, x='region', y='unique_invoice_count_region', labels={'unique_invoice_count_region': 'Pedidos'})

        # Customize the layout
        fig.update_xaxes(title='Regiões')
        fig.update_yaxes(title='Quantidade de Pedidos')
        st.plotly_chart(fig)


if __name__ == "__main__":
    main()