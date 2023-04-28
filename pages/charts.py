import streamlit as st
import plotly.express as px
from session import session

import plotly.io as pio

st.set_page_config(layout='wide')

pio.templates[pio.templates.default].layout.colorway = ['#F8B27A', '#7AC0F8', '#F87A81']

with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

figures = []

df = session.sql("""
    SELECT
        COUNT(FACTCRIMES.DELITOID)  AS Total,
        DATEDIM.YEAR,
        DATEDIM.MONTHNAME,
        DATEDIM.MONTH
    FROM 
        FACTCRIMES
        LEFT JOIN DATEDIM ON DATEDIM.FECHAID = FACTCRIMES.FECHAID
        LEFT JOIN CRIMETYPESDIM ON CRIMETYPESDIM.DELITOID = FACTCRIMES.DELITOID
    WHERE CRIMETYPESDIM.DELITO = 'HOMICIDIO'
    GROUP BY DATEDIM.YEAR, DATEDIM.MONTHNAME, DATEDIM.MONTH;
""").to_pandas()

df = df.sort_values(["YEAR", "MONTH"])
homicides_time = px.line(df, x='MONTHNAME', y='TOTAL', color='YEAR', markers=True)
homicides_time.update_layout(yaxis_title = "Homicides", xaxis_title = None , 
    legend=dict(
    y = 1.15, 
    x = 0,
    orientation = "h"
))

figures.append(homicides_time)


df = session.sql("""
    SELECT
        CRIMETYPESDIM.DELITO AS CRIMES,
        COUNT(FACTCRIMES.DELITOID) AS TOTAL_CRIMES
    FROM
        FACTCRIMES
        JOIN CRIMETYPESDIM ON FACTCRIMES.DELITOID = CRIMETYPESDIM.DELITOID
    GROUP BY
        CRIMETYPESDIM.DELITO
    ORDER BY
        TOTAL_CRIMES DESC;
""").to_pandas()

crime_by_type = px.pie(

    data_frame = df,
    values = "TOTAL_CRIMES",
    names = "CRIMES",
    hole = .3,

)
figures.append(crime_by_type)






for figure in figures:
    figure.update_layout(

        paper_bgcolor = "#242530",
        plot_bgcolor = "#242530",

    )
    figure.update_xaxes(showgrid = False, zeroline = False)
    figure.update_yaxes(showgrid = True, zeroline = False)

st.write(crime_by_type)