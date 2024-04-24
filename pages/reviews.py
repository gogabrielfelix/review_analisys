import streamlit as st
from st_pages import Page, show_pages, add_page_title
import sys
import os
import pandas as pd

# Obtém o diretório pai do diretório atual (onde está arquivo_B.py)
diretorio_pai = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Adiciona o diretório pai ao sys.path
sys.path.append(diretorio_pai)

from Connection import Connection

con = Connection()


show_pages(
    [
        Page("app.py", "Home"),
        Page("pages/reviews.py", "Reviews"),
        Page("pages/insights.py", "Insights por Produto")
    ]
)

st.set_page_config(
    page_title='Reviews - GoReviews',
    layout='wide',
    page_icon="https://www.gocase.com.br/favicon.png",
    menu_items={
        'About':"#GoReviews V1"
    }
)

with st.sidebar:

    list_products = st.multiselect(
        'De quais Produtos você deseja obter os Reviews? (Vazio para Todos os Produtos)',
        ['Garrafa', 'Copo', 'Mochila', 'Bolsa', 'Carregador', 'Estojo', 'Carteira', 'Necessaire']
    )

    initial_date = st.date_input('Início do Período', format='YYYY-MM-DD', value=None)
    final_date = st.date_input('Término do Período', format='YYYY-MM-DD', value=None)

    button = st.button('Gerar')


if button:
    with st.spinner('Carregando...'):
        reviews = con.get_reviews(initial_date, final_date, list_products)
        df = pd.DataFrame(data=reviews[0], columns=reviews[1])

    st.dataframe(df)

else:
    st.write('Preencha os Filtros ou Clique em Gerar')
