from acc_secrets import connection_parameters
from snowflake.snowpark import Session

import pandas as pd

session = Session.builder.configs(connection_parameters).create()


fact = pd.read_csv('DataModel/FactCrimes.csv')
date = pd.read_csv('DataModel/DateDim.csv')
types = pd.read_csv('DataModel/CrimeTypesDim.csv')
region = pd.read_csv('DataModel/RegionDim.csv')
time = pd.read_csv('DataModel/TimeDim.csv')
victim = pd.read_csv('DataModel/VictimDim.csv')

session.write_pandas(fact, 'FACTCRIMES', auto_create_table=True,  overwrite = True) 
session.write_pandas(date, 'DATEDIM', auto_create_table=True,  overwrite = True) 
session.write_pandas(types, 'CRIMETYPESDIM', auto_create_table=True,  overwrite = True) 
session.write_pandas(region, 'REGIONDIM', auto_create_table=True,  overwrite = True) 
session.write_pandas(time, 'TIMEDIM', auto_create_table=True,  overwrite = True) 
session.write_pandas(victim, 'VICTIMDIM', auto_create_table=True,  overwrite = True) 



