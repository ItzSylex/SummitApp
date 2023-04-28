import streamlit as st
from session import session

keys = {
    "year" : "FECHAID",
    "province" : "REGIONID",
    "time_of_day" : "HORAID",
    "gender" : "VICITIMAID",
}

def build_chart(query, identifier):
    if identifier == 'TOTAL_CRIMES':
        total_crimes_count = session.sql(query).collect()[0][0]
        print(query)
        return st.subheader(f'{total_crimes_count:,}k')
        

def apply_filters(base_query, identifier, year = None, province = None, time_of_day = None, gender = None):
    print(year, province, time_of_day, gender)
    
    filters = {}

    if not year and not province and not time_of_day and not gender:
        return build_chart(base_query, identifier)
    else:
        if year:
            base_query += f' LEFT JOIN DATEDIM ON DATEDIM.FECHAID = FACTCRIMES.FECHAID'
            filters['YEAR'] = year
        if province:
            base_query += f' LEFT JOIN REGIONDIM ON REGIONDIM.REGIONID = FACTCRIMES.REGIONID'
            filters['PROVINCIA'] = province
        if time_of_day:
            base_query += f' LEFT JOIN TIMEDIM ON TIMEDIM.HORAID = FACTCRIMES.HORAID'
            filters['HORAS'] = time_of_day
        if gender:
            base_query += f' LEFT JOIN VICTIMDIM ON VICTIMDIM.VICTIMAID = FACTCRIMES.VICTIMAID'
            filters['GENERO'] = gender

        for filter_key, filter_value in filters.items():
            base_query += " WHERE = {filter_key} = '{filter_value}'"
        
        print



def get_query(identifier):
    queries = {
        'TOTAL_CRIMES': """SELECT COUNT(*) FROM FACTCRIMES"""
    }

    return queries[identifier]

    