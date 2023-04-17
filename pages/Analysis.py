import streamlit as st
# from snowflake.snowpark import Session

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
    with st.expander('', expanded = True):
        province = selectbox("Province", options = [], label_visibility = 'visible', no_selection_label = 'All')
    with st.expander('', expanded = True):
        age = selectbox("Age Group", options = [], label_visibility = 'visible', no_selection_label = 'All')
    with st.expander('', expanded = True):
        time_day = selectbox("Time of day", options = [], label_visibility = 'visible', no_selection_label = 'All')
    with st.expander('', expanded = True):
        gender = selectbox("Gender", options = [], label_visibility = 'visible', no_selection_label = 'All')

col1, col2 = st.columns([1, 3])
with col1:
    with st.expander('Total Crimes', expanded = True):
        st.subheader('30k')

with col2:
    with st.expander('Hola', expanded = True):
        st.write('hola')

with st.expander('Crimes Across time', expanded = True):
    import streamlit as st
    import pandas as pd
    import numpy as np

    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])

    st.line_chart(chart_data)



