import streamlit as st
import plotly.express as px
import plotly.io as pio
import re
import geopandas

from .session import get_session

# Get session object from another module
session = get_session()

# Set the default color scheme for Plotly
pio.templates[pio.templates.default].layout.colorway = ['#4C9CB9', '#B79040', '#DF6E53', '#50B19E']

# Decorator to cache data returned by cache_map() function
@st.cache_data(show_spinner=False)
def cache_map(query):
    # Get data using cache_query() function and convert GEOMETRY column to GeoSeries
    df = cache_query(query)
    df['GEOMETRY'] = geopandas.GeoSeries.from_wkt(df['GEOMETRY'])
    gdf = geopandas.GeoDataFrame(df, geometry='GEOMETRY')
    gdf = gdf.set_index('GEO')

    # Generate choropleth map using Plotly and return the figure object
    fig = px.choropleth_mapbox(gdf, geojson=gdf.GEOMETRY, locations=gdf.index, color='TOTAL_CRIMES',
                               center={"lat": 9.9281, "lon": -84.0907}, zoom=6.2, mapbox_style="carto-darkmatter",
                               color_continuous_scale=["#fffaec", "#FCDA6F", "#F8B27A"], height=360)
    return fig

# Decorator to cache data returned by cache_query() function
@st.cache_data(show_spinner=False)
def cache_query(query):
    # Get data from session object and convert to pandas DataFrame
    df = session.sql(query).to_pandas()
    return df

# Function to format number with a "k" suffix if it's greater than or equal to 1000
def format_number(number: int) -> str:
    if number >= 1000:
        formatted_number = f"{round(number/1000, 1)}k"
    else:
        formatted_number = str(number)
    return formatted_number

# Function to apply custom styles to Plotly charts
def apply_styles(figure, legend=None):
    figure.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis_title=None, xaxis_title=None,
        legend_title=None,

        plot_bgcolor = '#181824',
        paper_bgcolor = '#181824',
)

    figure.update_xaxes(showgrid=False, zeroline=False)
    figure.update_yaxes(showgrid=True, zeroline=False, gridwidth=1, gridcolor='#525862', griddash='dot')

    if legend == 'top_legend':
        figure.update_layout(legend=dict( orientation="h", yanchor="bottom", y=1.2,  xanchor="right",  x=.8))

    return figure
    

# Function to create a Plotly bar chart
def create_bar_chart(data, x, y, color, height):
    data['YEAR'] = data['YEAR'].astype(str)
    fig = apply_styles(px.bar(data, x=x, y=y, color=color, barmode='stack', height=height).update_traces(marker_line_width=0))
    return fig

# Function to build all charts
def build_chart(query, identifier):

    if identifier == 'CRIMES_NUMBER':
        total_crimes_count = cache_query(query)
        total_crimes_count = total_crimes_count['COUNT(*)'].iloc[0]
        number = format_number(total_crimes_count)
        return st.subheader(number)
    
    if identifier == 'CRIMES_TRU_TIME':
        data = cache_query(query)
        data = data.sort_values(["YEAR", "MONTH"])

        fig = apply_styles(px.line(data, x='MONTHNAME', y='TOTAL', color='YEAR', markers=True, height=380))

        return st.plotly_chart(fig, use_container_width = True)

    if identifier == 'CRIMES_PER_TYPE':
        data = cache_query(query)
        fig = create_bar_chart(data, 'DELITO', 'TOTAL', 'YEAR', 220)
        return st.plotly_chart(fig, use_container_width= True)
    
    if identifier == 'CRIMES_PER_VICTIM':
        df = cache_query(query)
        fig = create_bar_chart(df, 'VICTIMA', 'TOTAL', 'YEAR', 220)
        return st.plotly_chart(fig, use_container_width=True)
    
    if identifier == 'TOP_10_REGIONS':
        df = cache_query(query)
        df = df.rename(columns={'TOTAL': 'Total Crimes', 'CANTON': 'Canton Name'})
        return st.dataframe(df.set_index('Canton Name'), use_container_width=True)

    if identifier == 'CRIMES_DISTRIBUTION_PER_YEARS':
        df = cache_query(query)
        fig = apply_styles(px.pie(df, values='TOTAL', names='YEAR', height=220, width=220, hole = .3))
        fig.update_traces(textposition='inside', textinfo='value+percent')
        fig = apply_styles(fig)
        return st.plotly_chart(fig, use_container_width=True)

    if identifier == 'MAP':
        fig = cache_map(query)
        fig = apply_styles(fig)
        return st.plotly_chart(fig, use_container_width=True)
    
    if identifier == 'CRIMES_BY_GENDER':
        df = cache_query(query)
        fig = apply_styles(px.bar(df, x = 'GENERO', y = 'TOTAL', color='GENERO', barmode='stack', height=380).update_traces(marker_line_width = 0), 'top_legend')
        return st.plotly_chart(fig, use_container_width= True)


# Dynamically generate the query based on the filters selected.
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
                            LIMIT 10""",

        'CRIMES_DISTRIBUTION_PER_YEARS': """SELECT
                                                DATEDIM.YEAR,
                                                COUNT(FACTCRIMES.*) AS TOTAL
                                            FROM
                                                FACTCRIMES
                                                LEFT JOIN DATEDIM ON FACTCRIMES.FECHAID = DATEDIM.FECHAID
                                            [JOINS_HERE]
                                            [WHERE_CLAUSE_HERE]
                                            GROUP BY
                                                DATEDIM.YEAR
                                            ORDER BY
                                                DATEDIM.YEAR ASC""",
        'MAP': "SELECT * FROM GEODATA", 

        'CRIMES_BY_GENDER': """SELECT 
                                    COUNT(FACTCRIMES.*) AS TOTAL, VICTIMDIM.GENERO
                                FROM
                                    FACTCRIMES
                                    LEFT JOIN VICTIMDIM ON FACTCRIMES.VICTIMAID = VICTIMDIM.VICTIMAID
                                [JOINS_HERE]
                                [WHERE_CLAUSE_HERE]
                                GROUP BY VICTIMDIM.GENERO"""
    }

    return queries[identifier]

    