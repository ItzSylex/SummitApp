# from app_utils.acc_secrets import connection_parameters
from snowflake.snowpark import Session
import streamlit as st

@st.cache_resource(show_spinner=False)
def get_session():
    session = Session.builder.configs(**st.secrets["snowflake"]).create()
    return session