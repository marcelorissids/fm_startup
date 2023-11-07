import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

from PIL import Image

df = pd.read_csv('./data/kawa_rfm.csv')
data_fatu = pd.read_csv('./data/faturamento_mes.csv')
data_sell = pd.read_csv('./data/semana_ticket.csv')

def make_sidebar(df):
    image_path = './images/'
    image = Image.open(image_path + 'logo_target.png')

    st.sidebar.image(image, width=240)
    st.write("---")
    st.sidebar.markdown("## Filtro")

    ordem_classes = [
    'Campeão',
    'Cliente leais',
    'Lealdade potencial',
    'Clientes Recentes',
    'Promissores',
    'Precisam de atenção',
    'Prestes a hibernar',
    'Clientes em risco',
    'Não posso perdê-lo',
    'Hibernando',
    'Clientes Perdidos'
    ]

    classes = st.sidebar.selectbox(
        'Escolha o Cluster',
        options=ordem_classes,
        index=0,
    )

    return classes


def main():
    st.set_page_config(page_title="Análise RFM", page_icon=":bar-chart:", layout="wide")

    selected_class = make_sidebar(df)

    st.markdown("# Análise RFM")

#    image_path = './images/'
#    image = Image.open(image_path + 'matriz_rfm.png')

#    st.image(image)

    if selected_class != 'Selecione':
        filtered_df = df[df['Classe'] == selected_class]
        st.dataframe(filtered_df)

    if st.button('Baixar Planilha'):
            if selected_class != 'Selecione':
                 csv_data = filtered_df.to_csv(index=False).encode('utf-8')
                 st.download_button(
                      label='Clique aqui',
                      data=csv_data,
                      file_name='classe_.csv',
                      mime='text/csv',
            )
    with st.container():
        st.write("---")
        st.subheader('Cluster Selecionado')
        clientes = filtered_df.groupby('Classe')['customer_id'].count()
        fatu_tags = filtered_df.groupby('Classe')['ValorMonetário'].sum()
        pedidos_tags = filtered_df.groupby('Classe')['Frequência'].sum()
        ticket_medio = (fatu_tags / pedidos_tags).round(2)
        recencia_media = filtered_df.groupby('Classe')['Recência'].mean().round().astype(int)

        resumo_df = pd.DataFrame({
             'Quantidade de Clientes': clientes,
            'Média de Recência':recencia_media,
            'Total de Pedidos': pedidos_tags,
            'Faturamento Total': fatu_tags,
            'Ticket Médio': ticket_medio
        })

        st.write(resumo_df)


    with st.container():
        st.write("---")
        st.subheader('Quantidade de Clientes por Classe')

        ordem_classes = [
            'Campeão',
            'Cliente leais',
            'Lealdade potencial',
            'Clientes Recentes',
            'Promissores',
            'Precisam de atenção',
            'Prestes a hibernar',
            'Clientes em risco',
            'Não posso perdê-lo',
            'Hibernando',
            'Clientes Perdidos'
            ]
        
        counts = df['Classe'].value_counts()
        percentages = (counts / counts.sum()) * 100
        colors = ['blue' if classe in ['Campeão', 'Cliente leal', 'Lealdade potencial'] else 'red' for classe in counts.index]
        
        data = pd.DataFrame({'Classe': counts.index, 'Quantidade de Clientes': counts.values, 'Porcentagem': percentages.values, 'Color': colors})
        ordem_df = pd.DataFrame({'Classe': ordem_classes})
        data = pd.merge(ordem_df, data, on='Classe', how='left')
        data = data.append({'Classe': 'Não posso perdê-lo', 'Quantidade de Clientes': 0, 'Porcentagem': 0, 'Color': 'gray'}, ignore_index=True)
#        st.write(data)
        
        fig = px.bar(data, 
                     x='Quantidade de Clientes', 
                     y='Classe', 
                     color='Classe', 
                     text='Porcentagem',
                     color_discrete_sequence=[
                          '#A6290d',
                          '#A6290d',
                          '#A6290d',
                          '#B7b5b4',
                          '#B7b5b4',
                          '#B7b5b4',
                          '#B7b5b4',
                          '#B7b5b4',
                          '#B7b5b4',
                          '#B7b5b4',
                          '#B7b5b4'],
                     )
        
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='inside', marker=dict(line=dict(width=1, color='black')))        
        fig.update_layout(xaxis_title='Quantidade de Clientes', yaxis_title='Classe')
        fig.update_xaxes(showgrid=True, zeroline=False)
        fig.update_yaxes(showgrid=False)
        st.plotly_chart(fig)
    
    with st.container():
        st.write("---")
        st.subheader('Ticket Médio por Cluster')

        ordem_classes = [
            'Campeão',
            'Cliente leais',
            'Lealdade potencial',
            'Clientes Recentes',
            'Promissores',
            'Precisam de atenção',
            'Prestes a hibernar',
            'Clientes em risco',
            'Não posso perdê-lo',
            'Hibernando',
            'Clientes Perdidos'
            ]
        
        tm_cluster = (df.groupby('Classe')['ValorMonetário'].sum() / df.groupby('Classe')['Frequência'].sum()).reset_index()
        tm_cluster = tm_cluster.rename(columns={0: 'Ticket Médio'})
        tm_cluster['Classe'] = tm_cluster['Classe'].astype('category')
        tm_cluster['Classe'].cat.set_categories(ordem_classes, inplace=True)
        tm_cluster = tm_cluster.sort_values('Classe')

        tm_cluster['Ticket Médio'] = 'R$' + tm_cluster['Ticket Médio'].round(2).astype(str)

        st.write(tm_cluster.to_html(index=False, escape=False), unsafe_allow_html=True)

#        valor_medio_por_classe = df.groupby('Classe')['ValorMonetário'].mean()
#        valor_medio_por_classe = valor_medio_por_classe.loc[counts.index]  # Reordena de acordo com a contagem
#        # Create a DataFrame for the chart
#        data = pd.DataFrame({'Classe': valor_medio_por_classe.index, 'Valor Médio de Ticket': valor_medio_por_classe.values})
#
#        # Create the horizontal bar chart using Plotly Express
#        fig = px.bar(data, x='Valor Médio de Ticket', y='Classe', orientation='h', title='Valor Médio de Ticket por Classe', color='Classe')
#
#        # Customize the layout
#        fig.update_xaxes(title='Valor Médio de Ticket')
#        fig.update_yaxes(title='Classe')
#        st.plotly_chart(fig)

#    with st.container():
#        st.write("---")
#        st.subheader('Recência Média por Classe')
#        # Substitua 'classe' e 'Recência' pelos nomes reais das colunas
#        # nos dados de vendas
#        recencia_media_por_classe = df.groupby('Classe')['Recência'].mean()
#        recencia_media_por_classe = recencia_media_por_classe.loc[counts.index]  # Reordena de acordo com a contagem
#        # Create a DataFrame for the chart
#        data = pd.DataFrame({'Classe': recencia_media_por_classe.index, 'Recência Média': recencia_media_por_classe.values})
#
#        # Create the horizontal bar chart using Plotly Express
#        fig = px.bar(data, x='Recência Média', y='Classe', orientation='h', title='Recência Média por Classe', color='Classe')
#
#        # Customize the layout
#        fig.update_xaxes(title='Recência Média')
#        fig.update_yaxes(title='Classe')
#        st.plotly_chart(fig)



if __name__ == "__main__":
    main()