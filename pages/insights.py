import streamlit as st
from st_pages import Page, show_pages
from fuzzywuzzy import fuzz
import string
import sys
import os

# Obtenha o diretório do arquivo atual (onde insights.py está localizado)
current_dir = os.path.dirname(__file__)

# Obtenha o diretório do diretório pai (diretório principal)
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Adicione o diretório pai ao sys.path
sys.path.insert(0, parent_dir)

# Agora você pode importar QA_Model normalmente
from QA_Model import Model


show_pages(
    [
        Page("app.py", "Home"),
        Page("pages/reviews.py", "Reviews"),
        Page("pages/insights.py", "Insights por Produto")
    ]
)

st.set_page_config(
    page_title='Insights - GoReviews',
    page_icon="https://www.gocase.com.br/favicon.png",
    menu_items={
        'About':"#GoReviews V1"
    }
)


def compute_answers(list_products, initial_date, final_date):
    model = Model(list_products=list_products, initial_date=initial_date, final_date=final_date)
    answers = model.compute_answers()

    return answers


with st.sidebar:

    list_products = st.multiselect(
        'De quais Produtos você deseja obter os Reviews? (Vazio para Todos os Produtos)',
        ['Garrafa', 'Copo', 'Mochila', 'Bolsa', 'Carregador', 'Estojo', 'Carteira', 'Necessaire']
    )

    initial_date = st.date_input('Início do Período', format='YYYY-MM-DD', value=None)
    final_date = st.date_input('Término do Período', format='YYYY-MM-DD', value=None)

    button = st.button('Gerar')



threshold_sim_str = 85
threshold_score = 0.1
reliable = False


if button:
    with st.spinner('Carregando...'):
        answers = compute_answers(list_products=list_products, initial_date=initial_date, final_date=final_date)

        list_answers_good = []
        list_answers_bad = []

        for idx, answer in enumerate(answers[0]):
                for idx2 in range(idx+1, len(answers[0])):
                    if fuzz.ratio(answer, answers[0][idx2]) < threshold_sim_str:
                        list_answers_good.append(answer)
                    else:
                        if len(answer) > len(answers[0][idx2]):
                            list_answers_good.append(answer)
                        else:
                            list_answers_good.append(answers[0][idx2])

        for idx, answer in enumerate(answers[1]):
                for idx2 in range(idx+1, len(answers[1])):
                    if fuzz.ratio(answer, answers[1][idx2]) < threshold_sim_str:
                        list_answers_bad.append(answer)
                    else:
                        if len(answer) > len(answers[1][idx2]):
                            list_answers_bad.append(answer)
                        else:
                            list_answers_bad.append(answers[1][idx2])



        dict_answers_good = {}
        dict_answers_bad = {}

        if (list_answers_good[0]['score'] > threshold_score*2) and (list_answers_bad[0]['score'] > threshold_score*2):
            reliable = True

            for answer in list_answers_good:
                if answer['score'] > threshold_score:
                    dict_answers_good[answer['end']] = (answer['answer']).strip().capitalize().rstrip(string.punctuation)
            for answer in list_answers_bad:
                if answer['score'] > threshold_score:
                    dict_answers_bad[answer['end']] = (answer['answer']).strip().capitalize().rstrip(string.punctuation)




    if reliable:
        text = '### '+str(len(dict_answers_good.values()))+' Motivos para Comprar:'
        st.markdown(text)

        for idx, answer in enumerate(dict_answers_good.values()):
            text = str(idx+1)+'. '+answer
            st.markdown(text)


        st.write('---')

        text = '### '+str(len(dict_answers_bad.values()))+' Motivos para Não Comprar:'
        st.markdown(text)

        for idx, answer in enumerate(dict_answers_bad.values()):
            text = str(idx+1)+'. '+answer
            st.markdown(text)

    else:
        st.error("Não há Dados o Suficiente para Gerar Respostas Confiáveis. Por favor, Altere os Filtros.", icon="❗")

else:
    st.write('Preencha os Filtros ou Clique em Gerar')