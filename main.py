import streamlit as st
from snowflake.snowpark import Session

from streamlit_extras.no_default_selectbox import selectbox
# from secrets import connection_parameters

# session = Session.builder.configs(connection_parameters).create()

st.set_page_config(
    page_title = 'Summit App Dashboard',
    page_icon = '📈',
    layout = 'wide'
)

#load custom css
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

with st.sidebar:

    with st.expander('', expanded = True):
        year = selectbox("Year", options = [], label_visibility = 'visible', no_selection_label = 'All')
        province = selectbox("Province", options = [], label_visibility = 'visible', no_selection_label = 'All')
        age = selectbox("Age Group", options = [], label_visibility = 'visible', no_selection_label = 'All')
        time_day = selectbox("Time of day", options = [], label_visibility = 'visible', no_selection_label = 'All')
        gender = selectbox("Gender", options = [], label_visibility = 'visible', no_selection_label = 'All')



