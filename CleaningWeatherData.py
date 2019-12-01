import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, errno
import glob
import requests
import datetime
import tarfile

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
                print('File Already Exists')



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