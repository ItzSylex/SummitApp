import streamlit as st

st.set_page_config(
    page_title = 'Summit App - About',
    page_icon = 'ℹ',
    layout = 'wide'
)

with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

st.header('Costa Rica - Crime Analysis')
st.markdown(
    """
This study presents a thorough analysis of crime in Costa Rica, utilizing data provided by the Organismo de Investigación Judicial and a geojson file, which was incorporated into Snowflake using a geometry data type. The report delves into various types of crimes, including <span class='highlight'>theft, robbery, homicide, and vehicle theft</span>, and categorizes victims on <span class='highlight'> people, buildings, vehicles, houses, and others.</span>

The report offers valuable insights into the specific <span class='highlight'> time and location</span> of the incidents, highlighting patterns and trends in criminal activity throughout the country. Notably, the data covers the years 2019-2021, with a focus on analyzing crime trends during the COVID-19 pandemic.

The study was conducted using, <span class='highlight'> Streamlit, Plotly, Snowflake, and CSS</span>, to ensure the highest level of accuracy and comprehensiveness in the analysis.
    """,
    unsafe_allow_html = True
) 


