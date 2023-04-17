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
This study presents a comprehensive analysis of crimes in Costa Rica based on the data provided by the Organismo de Investigación Judicial. The report offers detailed information on various types of crimes, including <span class='highlight'>theft, robbery, homicide, and vehicle theft</span>, and categorizes the victims according to different factors such as <span class='highlight'>people, buildings, vehicles, houses, and others</span>.

In addition, the report provides valuable insights into the specific <span class='highlight'>time</span> and <span class='highlight'>location</span> of the incidents, shedding light on the patterns and trends of criminal activities in the country. 

Data contains records from years 2019-2021
    """,
    unsafe_allow_html = True
) 


