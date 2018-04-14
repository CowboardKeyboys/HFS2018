import numpy as np
import pandas as pd
import math
import csv
from collections import defaultdict
from dashboard.Municipal import Municipal
import os

verbose = False


def invert_score(working_dictionary):
    for k in working_dictionary:
        working_dictionary[k] = 1 - working_dictionary[k]

    return working_dictionary


def normalize_dictionary(working_dictionary):

    factor = 1.0/sum(working_dictionary.values())

    for k in working_dictionary:
        working_dictionary[k] = working_dictionary[k]*factor

    return working_dictionary


def get_work_score(region_list):
    region_ws_dict = {}
    for region in region_list:
        total_work_score = [r['score'] for r in region]
        total_work_score = np.mean(total_work_score)
        weight = math.log(len(region), 2)
        if weight > 0:
            weighted_work_score = total_work_score * weight
        else:
            weighted_work_score = total_work_score
        region_ws_dict.update({region[0]['region_code']: weighted_work_score})
    return region_ws_dict


def calculate_competition_weight(population, unemployment_rate, n_jobs):
    return round((population * (unemployment_rate/100.0)) / n_jobs)


def get_jobs_from_region(regions, region_id):
    for region in regions:
        if region[0]['region_code'] == region_id:
            return region


def get_region_score(work_objects):
    municipals = []

    # Extract unique regions name from our work list
    unique_regions = {int(obj['region_code']) for obj in work_objects}
    unique_regions = list(unique_regions)
    groups = defaultdict(list)

    for obj in work_objects:
        groups[obj['region_code']].append(obj)

    # Get 2D list with job for each regions in seperate lists
    work_regional_list = groups.values()
    if verbose: print(work_regional_list)
    # Get dictionaries for population, unemploment rate

    path = os.path.dirname(__file__)
    kommunkoder = read_kommunkoder(path + '/kommunkoder.csv')
    population = read_population(path + '/befolkning_kommuner.csv')
    unemployment = read_unemployment(path + '/arbetsloshet_kommuner.csv')
    unemployment = regions_to_codes(kommunkoder, unemployment)
    region_population_score = {}

    # Get population score for each region
    for idx,region in enumerate(unique_regions):
        pop = population[region]
        try:

            ump = unemployment[region]
        except Exception as e:
            ump = 10
            #region = 1489
            #unique_regions[idx]=1489
            #continue


        n_jobs = len(get_jobs_from_region(work_regional_list, region))
        region_population_score.update({region: calculate_competition_weight(pop, ump, n_jobs)})

    region_population_score = normalize_dictionary(region_population_score)
    region_population_score_inverted = invert_score(region_population_score)
    region_population_score_inverted = normalize_dictionary(region_population_score_inverted)
    if verbose: print(region_population_score_inverted)

    region_work_score = get_work_score(work_regional_list)
    region_work_score_norm = normalize_dictionary(region_work_score)
    if verbose: print(region_work_score_norm)

    kommunkoder_reversed = dict(zip(kommunkoder.values(), kommunkoder.keys()))
    for region in unique_regions:
        municipal = Municipal()
        municipal.region_id = region
        municipal.region_name = kommunkoder_reversed[region]
        municipal.competitive_score = region_population_score_inverted[region]
        municipal.working_score = region_work_score_norm[region]
        municipal.jobs = get_jobs_from_region(work_regional_list, region)
        municipals.append(municipal)

    if verbose: print(municipals)
    return municipals


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
            region_current = [int(s) for s in str(region).split() if s.isdigit()][0]
            pop_sums[region_current] = int(pops[index])
        else:
            if region_current in pop_sums:
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
            if verbose: print('could not find ', region)
    return regions_converted

def test_data():
    '''
     region_code:
     score:

	ALE
	Alingsas
    '''

    data0 = {'region_code': 1440, 'score': 0.1}
    data1 = {'region_code': 1440, 'score': 0.3}
    data2 = {'region_code': 1440, 'score': 0.2}
    data3 = {'region_code': 1489, 'score': 0.4}

    our_list=[data0, data1,data2,data3]
    get_region_score(our_list)
def main():
    #kommunkoder = read_kommunkoder('kommunkoder.csv')
    #population = read_population('befolkning_kommuner.csv')
    #unemployment = read_unemployment('aretsloshet_kommuner.csv')
    #unemployment = regions_to_codes(kommunkoder, unemployment)
    test_data()
    if verbose: print('done')

if __name__ == "__main__":
    main()
