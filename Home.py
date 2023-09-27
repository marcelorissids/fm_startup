#import folium
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

from PIL import Image
#from streamlit_folium import folium_static
#from folium.plugins import MarkerCluster



#with open('style.css') as f:
#    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



#================ Load Data ================
df = pd.read_csv('./data/kawa_rfm.csv')
data_fatu = pd.read_csv('./data/faturamento_mes.csv')
data_sell = pd.read_csv('./data/semana_ticket.csv')
data_demo = pd.read_csv('./data/estados.csv')


#================ Sidebar ==================
def create_sidebar(df):
    image_path = './images/'
    image = Image.open(image_path + 'logo_target.png')

    st.sidebar.image(image, width=240)

#    classes = st.sidebar.selectbox(
#        'Escolha as Tags',
#        options=df['Classe'].unique().tolist(),
#        index=None,
#        placeholder='Selecione'
#    )

    st.sidebar.markdown("""---""")
    st.sidebar.markdown('### Planilha Completa')

    processed_data = pd.read_csv('./data/kawa_rfm.csv')

    st.sidebar.download_button(
        label='Download',
        data=processed_data.to_csv(index=False, sep=";"),
        file_name='analise_rfm.csv',
        mime='text/csv',
    )

    return None

def main():

    st.set_page_config(
    page_title='Kawá Dashboard',
    page_icon=':hot_beverage:',
    layout='wide'
    )

    with st.container():
        st.header('Resumo das Métricas')

        customers = df['customer_id'].nunique()
        receita = df['ValorMonetário'].sum()
        pedidos = df['Frequência'].sum()
        ticket_medio = receita/pedidos


        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric('Receita Total', f'R${receita:,.2f}')
        
        with col2:
            st.metric('Total de Pedidos', f'{pedidos}')
        
        with col3:
            st.metric('Clientes únicos', f'{customers}')

        with col4:
            st.metric('Ticket Médio', f'R${ticket_medio:,.2f}')

    with st.container():
        st.write("---")
        st.subheader('Faturamento por Mês')
        meses = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
                 7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}
        
        data_fatu['mês'] = data_fatu['month'].map(meses)

        fig = px.bar(data_fatu, 
                         x='mês', 
                         y='faturamento', 
                         labels={'faturamento': 'Faturamento'},
                         )
        for i, row in data_fatu.iterrows():
            fatum = row['faturamento']
            text_label = f'R${fatum:.2f}'
            fig.add_annotation(
                x=row['mês'],
                y=row['faturamento']+9,
                text=text_label,
                showarrow=False,           
            )

        st.plotly_chart(fig)

    with st.container():
            st.write("---")
            st.subheader('Número de Vendas x Ticket Médio')
            fig = px.bar(data_sell, 
                         x='day_of_week', 
                         y='unique_invoice_count', 
                         labels={'unique_invoice_count': 'Número de Vendas'}, 
                         )
            
            for i, row in data_sell.iterrows():
                ticket_medio = row['average_ticket']
                text_label = f'RS{ticket_medio:.2f}'
                fig.add_annotation(
                    x=row['day_of_week'],
                    y=row['unique_invoice_count']+5,
                    text= text_label,
                    showarrow=False,
                )
#            fig.update_traces(text=data_sell['day_of_week'], textposition='outside')
#            fig.update_traces(text=data_sell['Dias da Semana'], textposition='outside')
#            linha = px.line(data_sell,
#                            x='Dias da Semana', 
#                            y='average_ticket', 
#                            labels={'average_ticket': 'Ticket Médio'},
#                            line_shape='linear',
#                            )
#            linha.update_traces(mode='markers+lines', marker=dict(size=10, symbol='circle-open', color='red'))
#
#            for trace in linha.data:
#                fig.add_trace(trace)
#                
            st.plotly_chart(fig) 
        
    select_classes = create_sidebar(df)

if __name__ == '__main__':
    main()