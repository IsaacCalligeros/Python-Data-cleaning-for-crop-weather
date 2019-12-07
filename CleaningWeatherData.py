import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, errno
import glob
import requests
import datetime
import tarfile
from math import cos, asin, sqrt


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))

def closest(data, v):
    return min(data, key=lambda p: distance(v['lat'],v['lon'],p['lat'],p['lon']))

def get_Weather(date, lat, lon):
    baseDirectory = r'C:\Users\Isaac\source\repos\Python-Play\Datasets\Climate'
    path = r'{}\{}\*.csv'.format(baseDirectory, date.year)
    lat_long = []
    for fname in glob.glob(path):
        latitude = float(fname.split("_")[-2])
        longitude = float(fname.split("_")[-1].split(".csv")[0])
        lat_long.append({'lat': latitude, 'lon': longitude})
    v = {'lat': lat, 'lon': lon}
    print(closest(lat_long, v))
    closestLocation = closest(lat_long, v)
    print(distance(v['lat'], v['lon'], closestLocation['lat'], closestLocation['lon']))

    data = pd.read_csv(r'{}\{}\{}_{}_{}.csv'.format(baseDirectory, date.year, date.year,
     closestLocation['lat'], closestLocation['lon']))
     
    date_time_str = date.strftime('%Y-%m-%dT%H:%M:%S')

    print('Date-time:', date_time_str)  

    for index, row in data.iterrows():
        if(row['DATE'].split("T")[0] == date_time_str.split("T")[0]):
            print(row['DATE'])

def download_weather_data():
    yearStart = 1901
    yearEnd = datetime.datetime.now().year
    baseDirectory = r'C:\Users\Isaac\source\repos\Python-Play\Datasets\Climate'

    for year in range(1901, yearEnd):
        os.makedirs(r'{}\{}'.format(baseDirectory, year), exist_ok=True)
        url = 'https://www.ncei.noaa.gov/data/global-hourly/archive/csv/{}.tar.gz'.format(year)
        filename = url.split("/")[-1]
        with open(r'{}\{}\{}'.format(baseDirectory, year, filename), "wb") as f:
            r = requests.get(url)
            f.write(r.content)
            
            if (filename.endswith("tar.gz")):
                tar = tarfile.open(r'{}\{}\{}'.format(baseDirectory, year, filename), "r:gz")
                tar.extractall(path=r'{}\{}'.format(baseDirectory, year))
                tar.close()
            elif (filename.endswith("tar")):
                tar = tarfile.open(r'{}\{}\{}'.format(baseDirectory, year, filename), "r:")
                tar.extractall(path=r'{}\{}'.format(baseDirectory, year))
                tar.close()

            path = r'{}\{}\*.csv'.format(baseDirectory, year)
            for fname in glob.glob(path):
                data = pd.read_csv(r'{}'.format(fname), nrows=1)
                latitude = data['LATITUDE'].values[0]
                longitude = data['LONGITUDE'].values[0]
                try:
                    os.rename(r'{}'.format(fname),
                    r'{}\{}\{}_{}_{}.csv'.format(baseDirectory, year, year, latitude, longitude))
                except WindowsError:
                    FileExistsError
        



def main():
    print("Hello World!")

if __name__ == "__main__":
    get_Weather(datetime.date(1901, 4, 13), 65, 20)
    #download_weather_data()

# corr = data.corr()
# fig = plt.figure()
# ax = fig.add_subplot(111)
# cax = ax.matshow(corr,cmap='coolwarm', vmin=-1, vmax=1)
# fig.colorbar(cax)
# ticks = np.arange(0,len(data.columns),1)
# ax.set_xticks(ticks)
# plt.xticks(rotation=90)
# ax.set_yticks(ticks)
# ax.set_xticklabels(data.columns)
# ax.set_yticklabels(data.columns)
# plt.show()