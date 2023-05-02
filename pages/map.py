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
WHERE GEO_ID != 8
GROUP BY
  REGIONDIM.GEO_ID;""").to_pandas()

import geopandas as gpd

gdf = gpd.read_file('costa_rica.geojson')
gdf['id'] = gdf['id'].astype(int)

merged_gdf = gdf.merge(df, left_on='id', right_on='GEO_ID', how='left')


st.write(merged_gdf)

fig = px.choropleth_mapbox(
  merged_gdf,
  geojson=merged_gdf.geometry,
  locations=merged_gdf.shapeName,
  color=merged_gdf.TOTAL_CRIMES,
  center={"lat": 9.9281, "lon": -84.0907},
  zoom=6,
  mapbox_style="carto-positron"
)

st.plotly_chart(fig)