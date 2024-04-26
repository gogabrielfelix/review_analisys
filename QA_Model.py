from transformers import pipeline
import pandas as pd
from Connection import Connection

class Model:

    def __init__(self, list_products, initial_date, final_date, list_questions = ['Quais os pontos positivos do produto?','Quais os problemas mencionados do produto?']):
        self.model = pipeline("question-answering", "timpal0l/mdeberta-v3-base-squad2")
        self.list_products = list_products
        self.initial_date = initial_date
        self.final_date = final_date
        self.list_questions = list_questions

        self.context = self.get_context(self.list_products, self.initial_date, self.final_date)


    def compute_answers(self):

        answers = self.model(question=self.list_questions, context=self.context, top_k=10, max_answer_len=50)

        return answers



    def get_context(self, list_products, initial_date, final_date):

        con = Connection()
        reviews = con.get_reviews(initial_date, final_date, list_products)

        df = pd.DataFrame(data=reviews[0], columns=reviews[1])

        list_documents = df['Mensagem'].to_list()
        context = ' , '.join(list_documents)

        return context

