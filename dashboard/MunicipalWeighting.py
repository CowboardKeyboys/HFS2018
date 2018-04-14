import numpy as np
import pandas as pd
import csv
from collections import defaultdict


def normalize_dictionary(working_dictionary):

    factor = 1.0/sum(working_dictionary.itervalues())

    for k in working_dictionary:
        working_dictionary[k]=working_dictionary[k]*factor

    return working_dictionary

def get_work_score(region_list):

    region_ws_dict = {}
    for region in region_list:
        region_ws_dict.update({region[0].region_code: sum(r.score for r in region)})
    return region_ws_dict


def calculate_competition_weight(population, unemployment_rate):
    profession_count = 12.0
    return round((population * (unemployment_rate/100.0)) / profession_count)


def get_region_score(work_objects):

    # Extract unique regions name from our work list
    unique_regions = {obj['region_code'] for obj in work_objects}
    groups = defaultdict(list)

    for obj in work_objects:
        groups[obj['region_code']].append(obj)

    # Get 2D list with job for each regions in seperate lists
    work_regional_list = groups.values()
    print work_regional_list
    # Get dictionaries for population, unemploment rate
    kommunkoder = read_kommunkoder('kommunkoder.csv')
    population = read_population('befolkning_kommuner.csv')
    unemployment = read_unemployment('arbetsloshet_kommuner.csv')
    unemployment = regions_to_codes(kommunkoder, unemployment)
    region_population_score = {}

    # Get population score for each region
    for region in unique_regions:
        pop = population[region]
        ump = unemployment[region]
        region_population_score.update({region: calculate_competition_weight(pop, ump)})

    print region_population_score
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

def test_data():
    '''
     region_code:
     score:

	ALE
	Alingsas
    '''

    data1 = {'region_code':'1440', 'score':0.3}
    data2 = {'region_code':'1440', 'score':0.2}
    data3 = {'region_code':'1489', 'score':0.5}

    our_list=[data1,data2,data3]
    get_region_score(our_list)
def main():
    #kommunkoder = read_kommunkoder('kommunkoder.csv')
    #population = read_population('befolkning_kommuner.csv')
    #unemployment = read_unemployment('aretsloshet_kommuner.csv')
    #unemployment = regions_to_codes(kommunkoder, unemployment)
    test_data()
    print('done')

if __name__ == "__main__":
    main()
