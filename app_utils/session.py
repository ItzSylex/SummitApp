# from app_utils.acc_secrets import connection_parameters
from snowflake.snowpark import Session
import streamlit as st

@st.cache_resource(show_spinner=False)
def get_session():
    conn = st.experimental_connection('snowpark')
    session = conn.session

    return session