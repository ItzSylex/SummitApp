from app_utils.acc_secrets import connection_parameters
from snowflake.snowpark import Session
import streamlit as st

@st.cache_resource
def get_session():
    session = Session.builder.configs(connection_parameters).create()

    return session