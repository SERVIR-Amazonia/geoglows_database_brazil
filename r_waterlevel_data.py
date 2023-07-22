# Import libraries and dependencies
import os
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import datetime as dt
import requests
from bs4 import BeautifulSoup
import calendar
import numpy as np
import xml.etree.ElementTree as ET


# Function to get observed water level data
def get_observed_data(station_code):
    # Download observed streamflow data
    now = dt.datetime.now()
    YYYY = str(now.year)
    MM = str(now.month)
    DD = now.day
    # Rest API - URL
    params = {'codEstacao': '', 'dataInicio': '01/01/1900', 'dataFim': '{0}/{1}/{2}'.format(DD,MM,YYYY), 'tipoDados': '', 'nivelConsistencia': ''}
    data_types = {'3': ['Vazao{:02}'], '2': ['Chuva{:02}'], '1': ['Cota{:02}']}
    params['codEstacao'] = str(station_code)
    params['tipoDados'] = '1'
    # Get data in xlm format
    response = requests.get('http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroSerieHistorica', params, timeout=120.0)
    tree = ET.ElementTree(ET.fromstring(response.content))
    root = tree.getroot()
    df = []
    # Parse data to data.frame
    for month in root.iter('SerieHistorica'):
        code = month.find('EstacaoCodigo').text
        code = f'{int(code):08}'
        consist = int(month.find('NivelConsistencia').text)
        date = pd.to_datetime(month.find('DataHora').text, dayfirst=True)
        last_day = calendar.monthrange(date.year, date.month)[1]
        month_dates = pd.date_range(date, periods=last_day, freq='D')
        data = []
        list_consist = []
        ##
        for i in range(last_day):
            value = data_types[params['tipoDados']][0].format(i + 1)
            try:
                data.append(float(month.find(value).text))
                list_consist.append(consist)
            except TypeError:
                data.append(month.find(value).text)
                list_consist.append(consist)
            except AttributeError:
                data.append(None)
                list_consist.append(consist)
        ##
        index_multi = list(zip(month_dates, list_consist))
        index_multi = pd.MultiIndex.from_tuples(index_multi, names=["datetime", "Consistence"])
        df.append(pd.DataFrame({code: data}, index=index_multi))
    ##
    df = pd.concat(df)
    df = df.sort_index()
    ##
    drop_index = df.reset_index(level=1, drop=True).index.duplicated(keep='last')
    df = df[~drop_index]
    df = df.reset_index(level=1, drop=True)
    ##
    station_code_df = "h{0}".format(station_code)
    df.columns = [station_code_df]
    observed_df = df.groupby(df.index.strftime("%Y/%m/%d")).mean()
    observed_df.index = pd.to_datetime(observed_df.index)
    observed_df.index = pd.to_datetime(observed_df.index)
    observed_df.index = observed_df.index.to_series().dt.strftime("%Y-%m-%d")
    observed_df.index = pd.to_datetime(observed_df.index)
    ##
    min_value = observed_df[station_code_df].min()
    if min_value >= 0:
        min_value = 0
    ##
    observed_df = observed_df - min_value
    return(observed_df)


# Change the work directory
user = os.getlogin()
user_dir = os.path.expanduser('~{}'.format(user))
os.chdir(user_dir)
os.chdir("tethys_apps_brazil/backend-geoglows_brazil")

# Import enviromental variables
load_dotenv()
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')

# Generate the conection token
token = "postgresql+psycopg2://{0}:{1}@localhost:5432/{2}".format(DB_USER, DB_PASS, DB_NAME)
  
# Establish connection
db= create_engine(token)
conn = db.connect()

# Retrieve data from database
stations =  pd.read_sql("select code from waterlevel_station;", conn)

# Download observed water level data
error_list = []

# 
n = len(stations.code)
for i in range(n):
    code = stations.code[i]
    # Progress
    prog = round(100 * i/n, 3)
    print("Progress: {0} %. Station: {1}".format(prog, code))
    # Download
    try:
        temp_data = get_observed_data(code)
        print(temp_data.shape)
        # Define the table and delete if exist
        table = 'wl_{0}'.format(code)
        conn.execute("DROP TABLE IF EXISTS {0};".format(table))
        temp_data.to_sql(table, con=conn, if_exists='replace', index=True)
    except:
        print("Error downloading data in station {0}".format(code))
        error_list = np.append(error_list, code)


# Close connection
conn.close()