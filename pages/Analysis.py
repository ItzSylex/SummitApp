import streamlit as st

st.set_page_config(
    page_title = 'Summit App Dashboard',
    page_icon = '📈',
    layout = 'wide'
)

from streamlit_extras.no_default_selectbox import selectbox
from app_utils.build_chart import apply_filters, get_query

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

        st.form_submit_button('Apply    ', type = 'primary', use_container_width= True)

col1, col2, col3, col4 = st.columns([1.3, 2, 3, 3])
with col1:
    with st.expander('Total Crimes', expanded = True):
        st.caption('Total Crimes')
        apply_filters(get_query('TOTAL_CRIMES'), 'CRIMES_NUMBER', year, province, time_day, gender)
    with st.expander('Total Homicides', expanded = True):
        st.caption('Total lethal crimes')
        apply_filters(get_query('TOTAL_HOMICIDES'), 'CRIMES_NUMBER', year, province, time_day, gender)

with col2:
    with st.expander('Distribution per years', expanded = True):
        st.caption('Total crimes per year', help = 'The year 2019 has the most amount of crimes. In the year 2020 only 67.5% of the amount of crimes in 2019 occurred, however the amount of crimes registered in 2021 are 105% of the amount of crimes in 2020, showing an increase in May 2021')
        apply_filters(get_query('CRIMES_DISTRIBUTION_PER_YEARS'), 'CRIMES_DISTRIBUTION_PER_YEARS', year, province, time_day, gender)

with col3:
    with st.expander('Crimes per victim', expanded = True):
        st.caption('Crime distribution by victim target', help = 'By victims, compared to 2019, in the years 2020 and 2021, "houses", "vehicle" and "buildings" decreased by around 25%, while people as victims decreased by 44%')
        apply_filters(get_query('CRIMES_PER_VICTIM'), 'CRIMES_PER_VICTIM', year, province, time_day, gender)

with col4:
    with st.expander('Crimes per type', expanded = True):
        st.caption('Crimes by type', help = 'By type of crime, compared to 2019, in the years 2020 and 2021 there has been an important decrease in the crimes "assault" and "theft", and a smaller decrease in robbery, robbery of vehicles, and homicide.')
        apply_filters(get_query('CRIMES_PER_TYPE'), 'CRIMES_PER_TYPE', year, province, time_day, gender)


col1, col2 = st.columns([3,1])
with col1:
    with st.expander('Crimes Across time', expanded = True):
        with st.spinner('Loading map'):
            st.caption('Crime distribution by province', help = 'The crime concentration is in the capital San Jose')
            apply_filters(get_query('MAP'), 'MAP', year, province, time_day, gender)

with col2:
    with st.expander('10 Cantons with most crimes', expanded= True):
        st.caption('Regions with most crimes', help = 'Most of the crimes happened inside the GAM, however San Carlos is seen within the top 5 cantons with most crimes.')
        apply_filters(get_query('TOP_10_REGIONS'), 'TOP_10_REGIONS', year, province, time_day, gender)

col1, col2 = st.columns([1.4,3])

with col2:
    with st.expander('Crimes Across time', expanded = True):
        st.caption('Crimes Across time', help = 'Crimes in 2020 decreased significantly')
        apply_filters(get_query('CRIMES_TRU_TIME'), 'CRIMES_TRU_TIME', year, province, time_day, gender)

with col1:
    with st.expander('Gender distribution', expanded=True):
        st.caption('Gender distribution', help = 'Male victims are the most affected')
        apply_filters(get_query('CRIMES_BY_GENDER'), 'CRIMES_BY_GENDER', year, province, time_day, gender)

with st.expander('results', expanded=True):
    st.write('There are many factors that could determine the decrease of crimes on the year 2020 compared to the year 2019, one could be the global pandemic and the restrictions that this brought to the country, this would also make sense as the amount of crimes that involved people being the victim highly decreased compared to other victims such as cars or buildings.')

