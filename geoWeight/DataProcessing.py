import numpy as np
import math
import pandas as pd
import csv


def read_population(csv_path):
    data_frame = pd.read_csv(csv_path, sep=';')
    regions = data_frame['region']
    pops = data_frame['pop']

    pop_sums = {}
    region_current = ''
    for index, region in enumerate(regions):
        if not pd.isnull(regions[index]):
            region_current = str(region)
            pop_sums[region_current] = int(pops[index])
        else:
            if str(region_current) in pop_sums:
                pop_sums[str(region_current)] += int(pops[index])
    return pop_sums

def read_unemployment(csv_path):
    unemployment = {}
    with open(csv_path, 'rt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for index, row in enumerate(csv_reader):
            unemployment[str(row[0])] = np.float(row[1])
    return unemployment


def main():
    population = read_population('befolkning_kommuner.csv')
    unemployment = read_unemployment('arbetsloshet_kommuner.csv')

if __name__ == "__main__":
    main()
