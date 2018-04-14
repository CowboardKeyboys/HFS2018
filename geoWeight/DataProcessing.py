import numpy as np
import pandas as pd
import csv
from collections import defaultdict


def calculate_competition_weight(population, unemployment_rate):
    profession_count = 12.0
    return round((population * (unemployment_rate/100.0)) / profession_count)


def get_region_score(work_objects):

    # Extract unique regions name from our work list
    unique_regions = {obj.region_code for obj in work_objects}
    groups = defaultdict(list)

    for obj in work_objects:
        groups[obj.region_code].append(obj)

    # Get 2D list with job for each regions in seperate lists
    work_regional_list = groups.values()

    # Get dictionaries for population, unemploment rate
    kommunkoder = read_kommunkoder('kommunkoder.csv')
    population = read_population('befolkning_kommuner.csv')
    unemployment = read_unemployment('arbetsloshet_kommuner.csv')
    unemployment = regions_to_codes(kommunkoder, unemployment)
    region_population_score = {}

    # Get population score for each region
    for str(region) in unique_regions:
        region_population_score.update({region: calculate_competition_weight(population[region], unemployment[region])})


def read_kommunkoder(csv_path):
    kommunkoder = {}
    with open(csv_path, 'rt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for index, row in enumerate(csv_reader):
            kommunkoder[str(row[0])] = np.int(row[1])
    return kommunkoder


def read_population(csv_path):
    data_frame = pd.read_csv(csv_path, sep=';')
    regions = data_frame['region']
    pops = data_frame['pop']

    pop_sums = {}
    region_current = ''
    for index, region in enumerate(regions):
        if not pd.isnull(regions[index]):
            region_current = [s for s in str(region).split() if s.isdigit()][0]
            pop_sums[region_current] = int(pops[index])
        else:
            if str(region_current) in pop_sums:
                pop_sums[region_current] += int(pops[index])
    return pop_sums

def read_unemployment(csv_path):
    unemployment = {}
    with open(csv_path, 'rt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for index, row in enumerate(csv_reader):
            unemployment[str(row[0])] = np.float(row[1])
    return unemployment


def regions_to_codes(kommunkoder, regions):
    regions_converted = {}
    for region in regions:
        if region in kommunkoder:
            code = kommunkoder[region]
            regions_converted[code] = regions[region]
        else:
            print('could not find ', region)
    return regions_converted

def main():
    kommunkoder = read_kommunkoder('kommunkoder.csv')
    population = read_population('befolkning_kommuner.csv')
    unemployment = read_unemployment('arbetsloshet_kommuner.csv')
    unemployment = regions_to_codes(kommunkoder, unemployment)
    print('done')

if __name__ == "__main__":
    main()
