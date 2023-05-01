from app_utils.acc_secrets import connection_parameters
from snowflake.snowpark import Session

import pandas as pd

session = Session.builder.configs(connection_parameters).create()


fact = pd.read_csv('DataModel/FactCrimes.csv')
date = pd.read_csv('DataModel/DateDim.csv')
types = pd.read_csv('DataModel/CrimeTypesDim.csv')
region = pd.read_csv('DataModel/RegionDim.csv')
time = pd.read_csv('DataModel/TimeDim.csv')
victim = pd.read_csv('DataModel/VictimDim.csv')


fact.columns = map(str.upper, fact.columns)
date.columns = map(str.upper, date.columns)
types.columns = map(str.upper, types.columns)
region.columns = map(str.upper, region.columns)
time.columns = map(str.upper, time.columns)
victim.columns = map(str.upper, victim.columns)

session.write_pandas(fact, 'FACTCRIMES', auto_create_table=True,  overwrite = True) 
session.write_pandas(date, 'DATEDIM', auto_create_table=True,  overwrite = True) 
session.write_pandas(types, 'CRIMETYPESDIM', auto_create_table=True,  overwrite = True) 
session.write_pandas(region, 'REGIONDIM', auto_create_table=True,  overwrite = True) 
session.write_pandas(time, 'TIMEDIM', auto_create_table=True,  overwrite = True) 
session.write_pandas(victim, 'VICTIMDIM', auto_create_table=True,  overwrite = True) 

# Crime Type Distribution": A pie chart or bar chart that shows the percentage or count of each crime type in the dataset, providing an overview of the most common types of crimes occurring.
# "Victim Category Analysis": A stacked bar chart that breaks down the crime types by victim category, such as people, buildings, vehicles, houses, etc., providing insights into which victim categories are most frequently targeted by different types of crimes.
# "Crime Hotspots Map": A heatmap or choropleth map that visualizes the geographical distribution of crimes, highlighting areas with the highest concentration of crimes, and identifying crime hotspots or patterns in different geographic regions.
# "Time of Day Analysis": A line chart or histogram that shows the distribution of crimes by time of day, providing insights into when crimes are more likely to occur during the day or night, and identifying patterns or trends in crime timing.
# "Day of the Week Analysis": A bar chart or line chart that shows the distribution of crimes by day of the week, identifying which days have higher or lower crime rates, and detecting any day-specific patterns or trends in crime occurrence.
# "Long-term Crime Trend": A time series line chart that shows the trend of crimes over a period of time, such as years or months, providing insights into long-term changes in crime patterns, identifying trends, and evaluating the effectiveness of crime prevention measures over time.
# "Crime by Location Type": A bar chart or stacked bar chart that shows the distribution of crimes by location type, such as residential areas, commercial areas, public areas, etc., providing insights into which types of locations are more vulnerable to different types of crimes.
# "Victim Demographics Analysis": A demographic analysis of crime victims, such as age, gender, or occupation, using charts such as pie charts or bar charts, providing insights into the demographics of crime victims and identifying any demographic-specific patterns or trends in victimization.
# These are just a few examples of the insights that could be generated from the data model. The specific insights would depend on the data available in the model and the analyses performed, and can be customized to suit the specific requirements and goals of the analysis.
