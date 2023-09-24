import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

from PIL import Image

df = pd.read_csv('./data/kawa_rfm.csv')
data_fatu = pd.read_csv('./data/faturamento_mes.csv')
data_sell = pd.read_csv('./data/semana_ticket.csv')

def make_sidebar(df):
    st.sidebar.markdown("## Filters")

    classes = st.sidebar.selectbox(
        'Escolha as Tags',
        options=df['Classe'].unique().tolist(),
        index=0,
        placeholder='Selecione'
    )

    return classes


def main():
    st.set_page_config(page_title="Análise RFM", page_icon=":bar-chart:", layout="wide")

    selected_class = make_sidebar(df)

    st.markdown("# Análise RFM")

    image_path = './images/'
    image = Image.open(image_path + 'matriz_rfm.png')

    st.image(image)

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
        st.subheader('Quantidade de Clientes por Classe')
        counts = df['Classe'].value_counts()
        percentages = (counts / counts.sum()) * 100
        colors = ['red' if classe in ['Campeão', 'Cliente Leal'] else 'gray' for classe in counts.index]

        # Create a DataFrame for the chart
        data = pd.DataFrame({'Classe': counts.index, 'Quantidade de Clientes': counts.values, 'Porcentagem': percentages.values, 'Color': colors})

        # Create the horizontal bar chart using Plotly Express
        fig = px.bar(data, x='Quantidade de Clientes', y='Classe', color='Color', text='Porcentagem')
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='inside', marker=dict(line=dict(width=1, color='black')))

        # Customize the layout
        fig.update_layout(xaxis_title='Quantidade de Clientes', yaxis_title='Classe')
        fig.update_xaxes(showgrid=True, zeroline=False)
        fig.update_yaxes(showgrid=False)
        st.plotly_chart(fig)

    with st.container():
        st.write("---")
        st.subheader('Valor Médio de Ticket por Classe')
        valor_medio_por_classe = df.groupby('Classe')['ValorMonetário'].mean()
        valor_medio_por_classe = valor_medio_por_classe.loc[counts.index]  # Reordena de acordo com a contagem
        # Create a DataFrame for the chart
        data = pd.DataFrame({'Classe': valor_medio_por_classe.index, 'Valor Médio de Ticket': valor_medio_por_classe.values})

        # Create the horizontal bar chart using Plotly Express
        fig = px.bar(data, x='Valor Médio de Ticket', y='Classe', orientation='h', title='Valor Médio de Ticket por Classe', color='Classe')

        # Customize the layout
        fig.update_xaxes(title='Valor Médio de Ticket')
        fig.update_yaxes(title='Classe')
        st.plotly_chart(fig)

    with st.container():
        st.write("---")
        st.subheader('Recência Média por Classe')
        # Substitua 'classe' e 'Recência' pelos nomes reais das colunas
        # nos dados de vendas
        recencia_media_por_classe = df.groupby('Classe')['Recência'].mean()
        recencia_media_por_classe = recencia_media_por_classe.loc[counts.index]  # Reordena de acordo com a contagem
        # Create a DataFrame for the chart
        data = pd.DataFrame({'Classe': recencia_media_por_classe.index, 'Recência Média': recencia_media_por_classe.values})

        # Create the horizontal bar chart using Plotly Express
        fig = px.bar(data, x='Recência Média', y='Classe', orientation='h', title='Recência Média por Classe', color='Classe')

        # Customize the layout
        fig.update_xaxes(title='Recência Média')
        fig.update_yaxes(title='Classe')
        st.plotly_chart(fig)



if __name__ == "__main__":
    main()