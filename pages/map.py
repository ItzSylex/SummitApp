import pandas as pd
import plotly.express as px
import streamlit as st

from app_utils.session import session



st.set_page_config(
    page_title = 'Summit App Dashboard',
    page_icon = '📈',
    layout = 'wide'
)

#load custom css
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)



df = session.sql("""SELECT
    REGIONDIM.LATITUDE,
    REGIONDIM.LONGITUDE,
    COUNT(*) AS TOTAL_CRIMES
FROM
    FACTCRIMES
    JOIN REGIONDIM ON FACTCRIMES.REGIONID = REGIONDIM.REGIONID
GROUP BY
    REGIONDIM.LATITUDE,
    REGIONDIM.LONGITUDE""").to_pandas()

# Create the map
fig = px.scatter_mapbox(df, lat="LATITUDE", lon="LONGITUDE", color="TOTAL_CRIMES", size="TOTAL_CRIMES",
                  color_continuous_scale=px.colors.sequential.Oranges, zoom=6,
                  mapbox_style="carto-positron")

with st.expander('Map',expanded=True):
    st.plotly_chart(fig, use_container_width=True)