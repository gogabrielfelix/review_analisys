import os
from pyathena import connect
import streamlit as st


class Connection:

    def __init__(self):

        self.__access_key = 'AKIAQMK73MG6WEX6CETT'
        self.__secret_key = os.environ['AWS_SECRET_KEY']
        self.__region_name = 'us-east-1'
        self.__athena_dir = 's3://datalake.go/athena_results/'

        self.__table = 'datalake_processed.datalake_processed_stampedio_reviews'


    def get_reviews(self, initial_date, final_date, list_products=[]):

        __attributes = "reviewtitle, reviewmessage, reviewrating, productname, TO_CHAR(TO_DATE(split_part(datecreated,'T',1), 'yyyy-mm-dd'), 'dd-mm-yyyy')"
        __columns = ["Titulo", "Mensagem", "Nota", "Produto", "Data"]

        str_date = ''
        if initial_date != None:
            str_date += " AND datecreated >= '"+str(initial_date)+"'"
        if final_date != None:
            str_date += " AND datecreated <= '"+str(final_date)+"'"


        str_products = ''
        for idx, product in enumerate(list_products):
            if idx == 0:
                str_products += ' AND( '
            else:
                str_products += ' OR '
            str_products += "LOWER(productname) LIKE '"+product.lower()+"%'"
        if len(list_products)>0: str_products += ')'


        __conn = connect(aws_access_key_id=self.__access_key, aws_secret_access_key=self.__secret_key, region_name=self.__region_name, s3_staging_dir=self.__athena_dir)

        __query = "SELECT "+__attributes+" FROM "+self.__table+" WHERE LOWER(productname) NOT LIKE '%gift%'" + str_products + str_date + " ORDER BY datecreated DESC"
        # print(__query)

        __cursor = __conn.cursor()
        __cursor.execute(__query)

        results = __cursor.fetchall()
        #columns = [desc[0] for desc in __cursor.description]

        __cursor.close()
        __conn.close()

        return results, __columns



    # def get_counts_reviews(self):
    #     __attributes = "year(TO_DATE(split_part(datecreated,'T',1), 'yyyy-mm-dd')) AS year, week(TO_DATE(split_part(datecreated,'T',1), 'yyyy-mm-dd')) AS week, count(*) AS count_reviews"
    #
    #     __conn = connect(aws_access_key_id=self.__access_key, aws_secret_access_key=self.__secret_key, region_name=self.__region_name, s3_staging_dir=self.__athena_dir)
    #
    #     __query = "SELECT " + __attributes + " FROM " + self.__table + " GROUP BY year(TO_DATE(split_part(datecreated,'T',1), 'yyyy-mm-dd')), week(TO_DATE(split_part(datecreated,'T',1), 'yyyy-mm-dd')) ORDER BY year(TO_DATE(split_part(datecreated,'T',1), 'yyyy-mm-dd')) DESC, week(TO_DATE(split_part(datecreated,'T',1), 'yyyy-mm-dd')) DESC"
    #     print(__query)
    #
    #     __cursor = __conn.cursor()
    #     __cursor.execute(__query)
    #
    #     results = __cursor.fetchall()
    #     columns = [desc[0] for desc in __cursor.description]
    #
    #     __cursor.close()
    #     __conn.close()
    #
    #     return results, columns