from app_utils.acc_secrets import connection_parameters
from snowflake.snowpark import Session

session = Session.builder.configs(connection_parameters).create()