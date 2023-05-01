import streamlit as st
import plotly.express as px
import plotly.io as pio
import re

from .session import session

pio.templates[pio.templates.default].layout.colorway = ['#4C9CB9', '#B79040', '#DF6E53', '#50B19E']

def format_number(number: int) -> str:
    if number >= 1000:
        formatted_number = f"{round(number/1000, 1)}k"
    else:
        formatted_number = str(number)
    return formatted_number

def build_chart(query, identifier):

    if identifier == 'TOTAL_CRIMES':
        total_crimes_count = session.sql(query).collect()[0][0]
        number = format_number(total_crimes_count)
        return st.subheader(number)
    
    if identifier == 'CRIMES_TRU_TIME':
        data = session.sql(query).to_pandas()
        data = data.sort_values(["YEAR", "MONTH"])

        fig = apply_styles(px.line(data, x='MONTHNAME', y='TOTAL', color='YEAR', markers=True, height=340))

        return st.plotly_chart(fig, use_container_width = True)

    if identifier == 'CRIMES_PER_TYPE':
        data = session.sql(query).to_pandas()
        data['YEAR'] = data['YEAR'].astype(str)
        fig = apply_styles(px.bar(data, x = 'DELITO', y = 'TOTAL', color='YEAR', barmode='group', height=200).update_traces(marker_line_width = 0))
        
        return st.plotly_chart(fig, use_container_width= True)
    
    if identifier == 'CRIMES_PER_VICTIM':
        df = session.sql(query).to_pandas()
        df['YEAR'] = df['YEAR'].astype(str)

        fig = apply_styles(px.bar(df, x='VICTIMA', y='TOTAL', color='YEAR', barmode='group', height=200).update_traces(marker_line_width = 0))
        return st.plotly_chart(fig, use_container_width=True)
    
    if identifier == 'TOP_10_REGIONS':
        df = session.sql(query).to_pandas()
        df = df.rename(columns={'TOTAL': 'Total Crimes', 'CANTON': 'Canton Name'})
        st.dataframe(df.set_index('Canton Name'), use_container_width=True)
    

def apply_filters(base_query, identifier, year=None, province=None, time_of_day=None, gender=None):
    joins = set()
    filters = []

    if year:
        if 'DATEDIM' not in base_query:
            joins.add('LEFT JOIN DATEDIM ON DATEDIM.FECHAID = FACTCRIMES.FECHAID')
        filters.append(f"YEAR = '{str(year).upper().replace('_', ' ')}'")

    if province:
        if 'REGIONDIM' not in base_query:
            joins.add('LEFT JOIN REGIONDIM ON REGIONDIM.REGIONID = FACTCRIMES.REGIONID')
        filters.append(f"PROVINCIA = '{province.upper().replace('_', ' ')}'")

    if time_of_day:
        if 'TIMEDIM' not in base_query:
            joins.add('LEFT JOIN TIMEDIM ON TIMEDIM.HORAID = FACTCRIMES.HORAID')
        filters.append(f"HORAS = '{time_of_day.upper().replace('_', ' ')}'")
        
    if gender:
        if 'VICTIMDIM' not in base_query:
            joins.add('LEFT JOIN VICTIMDIM ON VICTIMDIM.VICTIMAID = FACTCRIMES.VICTIMAID')
        filters.append(f"GENERO = '{gender.upper().replace('_', ' ')}'")

    if not filters:
        base_query = base_query.replace('[JOINS_HERE]', '').replace('[WHERE_CLAUSE_HERE]', '')
    else:
        joined_tables = ' '.join(joins)
        base_query = base_query.replace('[JOINS_HERE]', joined_tables)

        if re.search(r'\bWHERE\b', base_query, re.IGNORECASE):
            where_clause = '' + ' AND '.join(filters)
            where_clause = where_clause + ' AND '
        else:
            where_clause = 'WHERE ' + ' AND '.join(filters)

        base_query = base_query.replace('[WHERE_CLAUSE_HERE]', where_clause)

    return build_chart(base_query, identifier)



def get_query(identifier):
    queries = {
        'TOTAL_CRIMES': """SELECT COUNT(*) FROM FACTCRIMES [JOINS_HERE] [WHERE_CLAUSE_HERE]""",

        'CRIMES_TRU_TIME': """SELECT
                                COUNT(FACTCRIMES.*)  AS Total,
                                DATEDIM.YEAR,
                                DATEDIM.MONTHNAME,
                                DATEDIM.MONTH
                            FROM 
                                FACTCRIMES
                                LEFT JOIN DATEDIM ON DATEDIM.FECHAID = FACTCRIMES.FECHAID
                                [JOINS_HERE]
                                [WHERE_CLAUSE_HERE]
                            GROUP BY DATEDIM.YEAR, DATEDIM.MONTHNAME, DATEDIM.MONTH""",

        'CRIMES_PER_TYPE': """SELECT
                                DATEDIM.YEAR,
                                COUNT(FACTCRIMES.*) AS TOTAL,
                                CRIMETYPESDIM.DELITO
                            FROM 
                                FACTCRIMES
                                LEFT JOIN CRIMETYPESDIM ON CRIMETYPESDIM.DELITOID = FACTCRIMES.DELITOID
                                LEFT JOIN DATEDIM ON DATEDIM.FECHAID = FACTCRIMES.FECHAID
                                [JOINS_HERE]
                                [WHERE_CLAUSE_HERE]
                            GROUP BY CRIMETYPESDIM.DELITO, DATEDIM.YEAR
                            ORDER BY DATEDIM.YEAR, CRIMETYPESDIM.DELITO""",

        'TOTAL_HOMICIDES': """SELECT 
                                COUNT(*)
                            FROM 
                                FACTCRIMES
                                LEFT JOIN CRIMETYPESDIM ON CRIMETYPESDIM.DELITOID = FACTCRIMES.DELITOID
                                [JOINS_HERE]
                            WHERE
                                [WHERE_CLAUSE_HERE]
                                CRIMETYPESDIM.DELITO = 'HOMICIDE'""",

        'CRIMES_PER_VICTIM': """SELECT
                                    VICTIMDIM.VICTIMA,
                                    DATEDIM.YEAR,
                                    COUNT(FACTCRIMES.*) AS TOTAL
                                FROM
                                    FACTCRIMES
                                    LEFT JOIN VICTIMDIM ON VICTIMDIM.VICTIMAID = FACTCRIMES.VICTIMAID
                                    LEFT JOIN DATEDIM ON DATEDIM.FECHAID = FACTCRIMES.FECHAID
                                    [JOINS_HERE]
                                    [WHERE_CLAUSE_HERE]
                                GROUP BY VICTIMDIM.VICTIMA, DATEDIM.YEAR
                                ORDER BY DATEDIM.YEAR, VICTIMDIM.VICTIMA""",

        'TOP_10_REGIONS': """SELECT
                                COUNT(*) AS TOTAL,
                                REGIONDIM.CANTON
                            FROM 
                                FACTCRIMES
                                LEFT JOIN REGIONDIM ON REGIONDIM.REGIONID = FACTCRIMES.REGIONID
                            [JOINS_HERE]
                            [WHERE_CLAUSE_HERE]
                            GROUP BY REGIONDIM.CANTON
                            ORDER BY Total DESC
                            LIMIT 10"""
    }

    return queries[identifier]



def apply_styles(figure):
    figure.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis_title=None,
        xaxis_title=None,
        legend_title=None,

        plot_bgcolor = '#181824',
        paper_bgcolor = '#181824',
    )

    figure.update_xaxes(showgrid=False, zeroline=False)
    figure.update_yaxes(showgrid=True, zeroline=False, gridwidth=1, gridcolor='#525862', griddash='dot')

    return figure
    