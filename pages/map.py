import pandas as pd
import plotly.express as px
import streamlit as st
import json 

from app_utils.session import session



st.set_page_config(
    page_title = 'Summit App Dashboard',
    page_icon = '📈',
    layout = 'wide'
)

with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

with open("costa_rica.geojson") as f:
    geojson = json.load(f)

df = session.sql("""
SELECT
  REGIONDIM.GEO_ID,
  count(FACTCRIMES.*) AS TOTAL_CRIMES
FROM
  FACTCRIMES
  JOIN REGIONDIM ON FACTCRIMES.REGIONID = REGIONDIM.REGIONID
GROUP BY
  REGIONDIM.GEO_ID;""").to_pandas()

st.write(df)
fig = px.choropleth(df, geojson=geojson, locations=df.GEO_ID, color=df.TOTAL_CRIMES, featureidkey = 'properties.id')

st.plotly_chart(fig)