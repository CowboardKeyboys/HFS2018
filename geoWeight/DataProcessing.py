import numpy as np
import pandas as pd
import csv

def read_csv(csv_path):
    pd.read_csv(csv_path)

def main():
    read_csv('/media/sf_Joakim/Documents/HFS2018/geoWeight/befolkning_kommuner.csv')
        
if __name__ == "__main__":
    main()
