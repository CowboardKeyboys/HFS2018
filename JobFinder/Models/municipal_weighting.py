import numpy as np
import pandas as pd
import math
import csv
from JobFinder.Models.municipality import Municipality
import os

verbose = False

def invert_score(working_dictionary):
    if (working_dictionary):
        res = {}
        for k in working_dictionary:
           res[k] = 1 - working_dictionary[k]
        return res


def normalize_dictionary(working_dictionary):
  #  if (working_dictionary):
        factor = 1.0/sum(working_dictionary.values())
        res = {}
        for k in working_dictionary:
            res[k] = working_dictionary[k]*factor
        return res

def get_work_score(region_list):
    region_ws_dict = {}
    for region in region_list:
        total_work = [r.score for r in region]
        total_work_score = np.mean(total_work)
        print ([r.score for r in region], total_work_score)
        if (total_work_score > 0):
            weight = math.log(len(region), 2)
            if weight > 0:
                weighted_work_score = total_work_score * weight
            else:
                weighted_work_score = total_work_score

            region =str(int(region[0].region_code)).strip()
            region_ws_dict.update({region : weighted_work_score})
    return region_ws_dict


def calculate_competition_weight(population, unemployment_rate, n_jobs):
    print ("pop: ", population, "unempl", unemployment_rate, "n:jobs", n_jobs)
    if n_jobs > 0:
        return round((float(population) * (float(unemployment_rate)/100.0)) / n_jobs)
    else:
        return 0

def get_region_score(work_objects):
    municipals = []
    work_objects = filter(lambda obj : obj.region_code.strip() != "634" and obj.region_code.strip() != "305" and obj.region_code.strip() != "ALLA", work_objects)
    # Extract unique regions name from our work list
    unique_regions = list(set([str(int(obj.region_code)).strip() for obj in work_objects]))
    groups = {region: list(filter(lambda x: str(int(x.region_code)).strip() == region,work_objects)) for region in unique_regions}

    path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../Assets/"))
    kommunkoder = read_kommunkoder(path + '/kommunkoder.csv')
    population = read_population(path + '/befolkning_kommuner.csv')
    unemployment = read_unemployment(path + '/arbetsloshet_kommuner.csv')
    unemployment = regions_to_codes(kommunkoder, unemployment)

    region_population_score = {}
    # Get population score for each region
    for region in unique_regions:
        pop = population[region]
        try:
            ump = unemployment[region]
        except Exception as e:
            ump = 10
        n_jobs = len(groups[str(region)])
        region_population_score.update({region: calculate_competition_weight(pop, ump, n_jobs)})

    region_population_score = normalize_dictionary(region_population_score)
    region_population_score = invert_score(region_population_score)
    region_population_score = normalize_dictionary(region_population_score)
    if verbose: print(region_population_score)

    region_work_score = get_work_score(groups.values())
    region_work_score_norm = normalize_dictionary(region_work_score)
    if verbose: print(region_work_score_norm)

    kommunkoder_reversed = dict(zip(kommunkoder.values(), kommunkoder.keys()))
    print(unique_regions)
    for region in unique_regions:
        id = str(int(region))
        municipal = Municipality()
        municipal.region_id = id
        municipal.region_name = kommunkoder_reversed[id]
        municipal.competitive_score = region_population_score[id]
        municipal.working_score = region_work_score_norm[id]
        municipal.jobs = groups[id]
        municipals.append(municipal)

    if verbose: print(municipals)
    return municipals


def read_kommunkoder(csv_path):
    kommunkoder = {}
    with open(csv_path, 'rt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for index, row in enumerate(csv_reader):
            kommunkoder[str(row[0])] = row[1].strip()
    return kommunkoder


def read_population(csv_path):
    data_frame = pd.read_csv(csv_path, sep=';')
    regions = data_frame['region']
    pops = data_frame['pop']

    pop_sums = {}
    region_current = ''
    for index, region in enumerate(regions):
        if not pd.isnull(regions[index]):
            region_current = [str(int(s)) for s in str(region).split() if s.isdigit()][0]
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


def main():
    if verbose: print('done')

if __name__ == "__main__":
    main()
