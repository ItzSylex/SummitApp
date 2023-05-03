# from app_utils.acc_secrets import connection_parameters
from snowflake.snowpark import Session
import streamlit as st

conn = st.experimental_connection('snowpark')
session = conn.session