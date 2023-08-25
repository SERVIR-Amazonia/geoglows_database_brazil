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

# Routine to download and format the observed data
def get_observed_data(url, station_code):
    # Request data from ANA API
    response = requests.get(url, verify=False)
    # Parse data to xml
    soup = BeautifulSoup(response.content, "xml")
    # Get datetimes
    times = soup.find_all('DataHora')
    monthly__time = []
    # Get daily values
    valuesDay01 = soup.find_all('Vazao01')
    values01 = []
    valuesDay02 = soup.find_all('Vazao02')
    values02 = []
    valuesDay03 = soup.find_all('Vazao03')
    values03 = []
    valuesDay04 = soup.find_all('Vazao04')
    values04 = []
    valuesDay05 = soup.find_all('Vazao05')
    values05 = []
    valuesDay06 = soup.find_all('Vazao06')
    values06 = []
    valuesDay07 = soup.find_all('Vazao07')
    values07 = []
    valuesDay08 = soup.find_all('Vazao08')
    values08 = []
    valuesDay09 = soup.find_all('Vazao09')
    values09 = []
    valuesDay10 = soup.find_all('Vazao10')
    values10 = []
    valuesDay11 = soup.find_all('Vazao11')
    values11 = []
    valuesDay12 = soup.find_all('Vazao12')
    values12 = []
    valuesDay13 = soup.find_all('Vazao13')
    values13 = []
    valuesDay14 = soup.find_all('Vazao14')
    values14 = []
    valuesDay15 = soup.find_all('Vazao15')
    values15 = []
    valuesDay16 = soup.find_all('Vazao16')
    values16 = []
    valuesDay17 = soup.find_all('Vazao17')
    values17 = []
    valuesDay18 = soup.find_all('Vazao18')
    values18 = []
    valuesDay19 = soup.find_all('Vazao19')
    values19 = []
    valuesDay20 = soup.find_all('Vazao20')
    values20 = []
    valuesDay21 = soup.find_all('Vazao21')
    values21 = []
    valuesDay22 = soup.find_all('Vazao22')
    values22 = []
    valuesDay23 = soup.find_all('Vazao23')
    values23 = []
    valuesDay24 = soup.find_all('Vazao24')
    values24 = []
    valuesDay25 = soup.find_all('Vazao25')
    values25 = []
    valuesDay26 = soup.find_all('Vazao26')
    values26 = []
    valuesDay27 = soup.find_all('Vazao27')
    values27 = []
    valuesDay28 = soup.find_all('Vazao28')
    values28 = []
    valuesDay29 = soup.find_all('Vazao29')
    values29 = []
    valuesDay30 = soup.find_all('Vazao30')
    values30 = []
    valuesDay31 = soup.find_all('Vazao31')
    values31 = []
    # Bucle
    for i in range(0, len(times)):
        monthlyTime = times[i].next
        monthly__time.append(monthlyTime)
        value01 = valuesDay01[i].next
        values01.append(value01)
        value02 = valuesDay02[i].next
        values02.append(value02)
        value03 = valuesDay03[i].next
        values03.append(value03)
        value04 = valuesDay04[i].next
        values04.append(value04)
        value05 = valuesDay05[i].next
        values05.append(value05)
        value06 = valuesDay06[i].next
        values06.append(value06)
        value07 = valuesDay07[i].next
        values07.append(value07)
        value08 = valuesDay08[i].next
        values08.append(value08)
        value09 = valuesDay09[i].next
        values09.append(value09)
        value10 = valuesDay10[i].next
        values10.append(value10)
        value11 = valuesDay11[i].next
        values11.append(value11)
        value12 = valuesDay12[i].next
        values12.append(value12)
        value13 = valuesDay13[i].next
        values13.append(value13)
        value14 = valuesDay14[i].next
        values14.append(value14)
        value15 = valuesDay15[i].next
        values15.append(value15)
        value16 = valuesDay16[i].next
        values16.append(value16)
        value17 = valuesDay17[i].next
        values17.append(value17)
        value18 = valuesDay18[i].next
        values18.append(value18)
        value19 = valuesDay19[i].next
        values19.append(value19)
        value20 = valuesDay20[i].next
        values20.append(value20)
        value21 = valuesDay21[i].next
        values21.append(value21)
        value22 = valuesDay22[i].next
        values22.append(value22)
        value23 = valuesDay23[i].next
        values23.append(value23)
        value24 = valuesDay24[i].next
        values24.append(value24)
        value25 = valuesDay25[i].next
        values25.append(value25)
        value26 = valuesDay26[i].next
        values26.append(value26)
        value27 = valuesDay27[i].next
        values27.append(value27)
        value28 = valuesDay28[i].next
        values28.append(value28)
        value29 = valuesDay29[i].next
        values29.append(value29)
        value30 = valuesDay30[i].next
        values30.append(value30)
        value31 = valuesDay31[i].next
        values31.append(value31)
    ##
    daily_time = []
    monthly_time = []
    ##
    for i in range(0, len(monthly__time)):
            year = int(monthly__time[i][0:4])
            month = int(monthly__time[i][5:7])
            day = int(monthly__time[i][8:10])
            if day != 1:
                day = 1
            hh = int(monthly__time[i][11:13])
            mm = int(monthly__time[i][14:16])
            ss = int(monthly__time[i][17:19])
            monthlyTime = dt.datetime(year, month, day, hh, mm)
            monthly_time.append(monthlyTime)
            if month == 1:
                for j in range(0, 31):
                    date = dt.datetime(year, month, j + 1, hh, mm)
                    daily_time.append(date)
            elif month == 2:
                if calendar.isleap(year):
                    for j in range(0, 29):
                        date = dt.datetime(year, month, j + 1, hh, mm)
                        daily_time.append(date)
                else:
                    for j in range(0, 28):
                        date = dt.datetime(year, month, j + 1, hh, mm)
                        daily_time.append(date)
            elif month == 3:
                for j in range(0, 31):
                    date = dt.datetime(year, month, j + 1, hh, mm)
                    daily_time.append(date)
            elif month == 4:
                for j in range(0, 30):
                    date = dt.datetime(year, month, j + 1, hh, mm)
                    daily_time.append(date)
            elif month == 5:
                for j in range(0, 31):
                    date = dt.datetime(year, month, j + 1, hh, mm)
                    daily_time.append(date)
            elif month == 6:
                for j in range(0, 30):
                    date = dt.datetime(year, month, j + 1, hh, mm)
                    daily_time.append(date)
            elif month == 7:
                for j in range(0, 31):
                    date = dt.datetime(year, month, j + 1, hh, mm)
                    daily_time.append(date)
            elif month == 8:
                for j in range(0, 31):
                    date = dt.datetime(year, month, j + 1, hh, mm)
                    daily_time.append(date)
            elif month == 9:
                for j in range(0, 30):
                    date = dt.datetime(year, month, j + 1, hh, mm)
                    daily_time.append(date)
            elif month == 10:
                for j in range(0, 31):
                    date = dt.datetime(year, month, j + 1, hh, mm)
                    daily_time.append(date)
            elif month == 11:
                for j in range(0, 30):
                    date = dt.datetime(year, month, j + 1, hh, mm)
                    daily_time.append(date)
            elif month == 12:
                for j in range(0, 31):
                    date = dt.datetime(year, month, j + 1, hh, mm)
                    daily_time.append(date)
    ##
    dischargeValues = []
    ##
    for date in daily_time:
            if date.day == 1:
                discharge = values01[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 2:
                discharge = values02[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 1, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 3:
                discharge = values03[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 2, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 4:
                discharge = values04[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 3, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 5:
                discharge = values05[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 4, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 6:
                discharge = values06[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 5, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 7:
                discharge = values07[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 6, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 8:
                discharge = values08[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 7, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 9:
                discharge = values09[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 8, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 10:
                discharge = values10[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 9, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 11:
                discharge = values11[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 10, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 12:
                discharge = values12[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 11, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 13:
                discharge = values13[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 12, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 14:
                discharge = values14[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 13, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 15:
                discharge = values15[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 14, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 16:
                discharge = values16[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 15, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 17:
                discharge = values17[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 16, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 18:
                discharge = values18[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 17, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 19:
                discharge = values19[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 18, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 20:
                discharge = values20[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 19, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 21:
                discharge = values21[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 20, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 22:
                discharge = values22[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 21, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 23:
                discharge = values23[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 22, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 24:
                discharge = values24[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 23, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 25:
                discharge = values25[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 24, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 26:
                discharge = values26[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 25, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 27:
                discharge = values27[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 26, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 28:
                discharge = values28[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 27, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 29:
                discharge = values29[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 28, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 30:
                discharge = values30[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 29, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
            elif date.day == 31:
                discharge = values31[
                    monthly_time.index(dt.datetime(date.year, date.month, date.day - 30, date.hour, date.minute))]
                dischargeValues.append(str(discharge))
    ##
    pairs = [list(a) for a in zip(daily_time, dischargeValues)]
    pairs = sorted(pairs, key=lambda x: x[0])
    ##
    observed_df = pd.DataFrame(pairs, columns=['Datetime', station_code])
    observed_df.set_index('Datetime', inplace=True)
    observed_df = observed_df.replace(r'^\s*$', np.NaN, regex=True)
    observed_df[station_code] = pd.to_numeric(observed_df[station_code], downcast="float")
    ##
    observed_df[observed_df < 0] = 0
    observed_df.index = observed_df.index.to_series().dt.strftime("%Y-%m-%d")
    observed_df.index = pd.to_datetime(observed_df.index)
    observed_df = observed_df.groupby(observed_df.index.strftime("%Y-%m-%d")).mean()
    observed_df.index = pd.to_datetime(observed_df.index)
    ##
    return(observed_df)

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
db= create_engine(token)
conn = db.connect()


# Retrieve data from database
stations =  pd.read_sql("select code from streamflow_station;", conn)

# Download observed streamflow data
now = dt.datetime.now()
YYYY = str(now.year)
MM = str(now.month)
DD = now.day

error_list = []

n = len(stations.code)
for i in range(n):
    code = stations.code[i]
    # Progress
    prog = round(100 * i/n, 3)
    print("Progress: {0} %. Station: {1}".format(prog, code))
    # Download
    url = 'http://telemetriaws1.ana.gov.br/ServiceANA.asmx/HidroSerieHistorica?codEstacao={0}&DataInicio=01/01/1900&DataFim={1}/{2}/{3}&tipoDados=3&nivelConsistencia=1'.format(code, DD, MM, YYYY)
    try:
        #temp_data = get_observed_data(url, "h{0}".format(code))
        #out_data = out_data.merge(temp_data, how='outer', left_index=True, right_index=True)
        #print(out_data.shape)
        temp_data = get_observed_data(url, code)
        temp_data.index.name = "datetime"
        print(temp_data.shape)
        # Define the table and delete if exist
        table = 'sf_{0}'.format(code)
        print("Start drop database")
        conn.execute("DROP TABLE IF EXISTS {0};".format(table))
        print("End drop database")
        temp_data.to_sql(table, con=conn, if_exists='replace', index=True)
    except:
        print("Error downloading data in station {0}".format(code))
        error_list = np.append(error_list, code)


# Close connection
conn.close()

