# Import libraries and dependencies
import os
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Change the work directory
user = os.getlogin()
user_dir = os.path.expanduser('~{}'.format(user))
os.chdir(user_dir)
os.chdir("tethys_apps_brazil/geoglows_database_brazil")

# Import enviromental variables
load_dotenv()
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')

# Generate the conection token
token = "postgresql+psycopg2://{0}:{1}@localhost:5432/{2}".format(DB_USER, DB_PASS, DB_NAME)

# Establish connection
db = create_engine(token)
conn = db.connect()

# Read streamflow stations and insert to database
data = pd.read_excel('Brazil_Stations_Streamflow.xlsx', index_col=0) 
df = pd.DataFrame(data)
#conn.execute("DROP TABLE IF EXISTS streamflow_station;")
df.to_sql('streamflow_station', con=conn, if_exists='replace', index=False)

# Read water level stations and insert to database
data = pd.read_excel('Brazil_Stations_WaterLevel.xlsx', index_col=0) 
df = pd.DataFrame(data)
#conn.execute("DROP TABLE IF EXISTS waterlevel_station;")
df.to_sql('waterlevel_station', con=conn, if_exists='replace', index=False)


# Close connection
conn.close()