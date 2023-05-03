from app_utils.session import session
import streamlit as st

st.write(session.sql('SELECT * FROM FACTCRIMES LIMIT 10').to_pandas())