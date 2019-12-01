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

def download_weather_data():
    yearStart = 1901
    yearEnd = datetime.datetime.now().year
    baseDirectory = r'C:\Users\Isaac\source\repos\Python-Play\Datasets\Climate'

    for year in range(1901, yearEnd):
        lat_long = []
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
                lat_long.append({'lat': latitude, 'lon': longitude})
                try:
                    os.rename(r'{}'.format(fname),
                    r'{}\{}\{}_{}_{}.csv'.format(baseDirectory, year, year, latitude, longitude))
                except WindowsError:
                    print('File Already Exists')

        v = {'lat': 30, 'lon': -50}
        print(closest(lat_long, v))

def main():
    print("Hello World!")

if __name__ == "__main__":
    download_weather_data()

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