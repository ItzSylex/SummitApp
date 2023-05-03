from app_utils.session import session

st.write(session.sql('SELECT * FROM FACTCRIMES LIMIT 10').to_pandas())