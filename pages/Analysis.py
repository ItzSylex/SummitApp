import streamlit as st
from streamlit_extras.no_default_selectbox import selectbox

from build_chart import apply_filters, get_query

st.set_page_config(
    page_title = 'Summit App Dashboard',
    page_icon = '📈',
    layout = 'wide'
)

#load custom css
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)


with st.sidebar:

    with st.form('filters'):
        PROVINCES = ['Cartago', 'San Jose', 'Guanacaste', 'Heredia', 'Alajuela', 'Limon', 'Puntarenas', 'Unknown']

        with st.expander('', expanded = True):
            year = selectbox("Year", options = [2019, 2020, 2021], label_visibility = 'visible', no_selection_label = 'All')
        with st.expander('', expanded = True):
            province = selectbox("Province", options = PROVINCES, label_visibility = 'visible', no_selection_label = 'All')
        with st.expander('', expanded = True):
            time_day = selectbox("Time of day", options = ['Early Morning', 'Morning', 'Night', 'Afternoon'], label_visibility = 'visible', no_selection_label = 'All')
        with st.expander('', expanded = True):
            gender = selectbox("Gender", options = ['Male', 'Female', 'Non applicable'], label_visibility = 'visible', no_selection_label = 'All')

        st.form_submit_button('Apply filters', type = 'primary', use_container_width= True)

col1, col2 = st.columns([1, 3])
with col1:
    with st.expander('Total Crimes', expanded = True):
        apply_filters(get_query('TOTAL_CRIMES'), 'TOTAL_CRIMES', year, province, time_day, gender)

with col2:
    with st.expander(' ', expanded = True):
        st.write(' ')

with st.expander('Crimes Across time', expanded = True):
    st.write(' ')



