import streamlit as st
import streamlit.components.v1 as components
from st_pages import Page, show_pages, add_page_title
import jwt
import time


show_pages(
    [
        Page("app.py", "Home"),
        Page("pages/reviews.py", "Reviews"),
        Page("pages/insights.py", "Insights por Produto")
    ]
)

st.set_page_config(
    page_title='GoReviews',
    page_icon="https://www.gocase.com.br/favicon.png",
    layout='wide',
    menu_items={
        'About':"#GoReviews V1"
    }
)

METABASE_SITE_URL = "https://metabase.gocase.com.br"
METABASE_SECRET_KEY = "dd0a0beb26bf137e423583a0d5bed1be51558b5b36dcac09a090a92a8b4d5e1f"

payload = {
    "resource": {"dashboard": 964},
    "params": {

    },
    "exp": round(time.time()) + (60 * 10)  # 10 minute expiration
}
token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token + "#theme=night&bordered=false&titled=false"


st.markdown('## Visão Geral dos Reviews')

components.iframe(iframeUrl, height=1200)