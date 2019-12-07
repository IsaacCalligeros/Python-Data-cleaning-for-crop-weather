import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, errno
import glob
import requests
import datetime
import tarfile
from math import cos, asin, sqrt
import codecs
from lxml import html
import bs4
#fix from to rows issue

def writeData(data):
    print(data)
    # data
    # data.to_csv(r'c:\data\pandas.txt', header=None, index=None, sep=' ', mode='a')

def fix_FileFormat():
    baseDirectory = r'C:\Users\Isaac\source\repos\Python-Play\Datasets\FAOData'
    BLOCKSIZE = 1048576 # or some other, desired size in bytes
    path = r'{}\*.csv'.format(baseDirectory)
    for fname in glob.glob(path):
        with codecs.open(fname, "r", "ANSI") as sourceFile:
            with codecs.open(fname.split(".csv")[0] + "_fix" + ".csv", "w", "utf-8") as targetFile:
                while True:
                    contents = sourceFile.read(BLOCKSIZE)
                    if not contents:
                        break
                    targetFile.write(contents)

def tidy_FAOData():
    baseDirectory = r'C:\Users\Isaac\source\repos\Python-Play\Datasets\FAOData'
    path = r'{}\*Production_CropsProcessed_E_All_Data_(Normalized)_fix.csv'.format(baseDirectory)
    
    chunksize = 10 ** 2
    print(path)
    for fname in glob.glob(path):
        row_count = 0
        last_count = 1
        current_Indexes = []
        data = pd.DataFrame()
        chunk_row_count = 0
        for chunk in pd.read_csv(r'{}'.format(fname), chunksize=chunksize):
            identifier = chunk.iloc[0]
            print(identifier)
            tail_chunk = chunk.tail(0)
            year_max = chunk['Year'].min()
            year_min = chunk['Year'].max()
            value_max = chunk['Value'].min()
            value_min = chunk['Value'].max()
            chunk_row_count = 0
            for count, row in chunk.iterrows():
                if((identifier['Area'] == chunk.iloc[chunk_row_count]['Area']) and
                 (identifier['Item'] == chunk.iloc[chunk_row_count]['Item']) and
                 (identifier['Element'] == chunk.iloc[chunk_row_count]['Element'])):
                    current_Indexes.append(chunk_row_count)
                else:
                    print(last_count)
                    print(count)
                    if(data.empty):
                        data = data.append(chunk.iloc[last_count%chunksize: chunk_row_count])
                    else:
                        data = data.append(chunk.iloc[0: chunk_row_count])
                    last_count = count
                    
                    current_Indexes = []
                    current_Indexes.append(chunk_row_count)
                    identifier = chunk.iloc[chunk_row_count]
                    
                    writeData(data)
                    data = pd.DataFrame()
                chunk_row_count += 1
                row_count += 1
            data = data.append(chunk.iloc[last_count%100:chunk_row_count])
            

            

def main():
    print("Hello World!")

if __name__ == "__main__":
    #fix_FileFormat()
    tidy_FAOData()