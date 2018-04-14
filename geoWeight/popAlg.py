
import pandas as pd

def calculateCompetitionWeight(population, unemployment_rate):
    profession_count = 12.0
    return round((population * unemployment_rate)/profession_count)


def getRegionScore(work_objects):
    from collections import defaultdict

    #Extract unique regions name from our work list
    unique_regions = {obj.region_code for obj in work_objects}
    groups = defaultdict(list)
    
    for obj in work_objects:
        groups[obj.region_code].append(obj)

    #Get 2D list with job for each regions in seperate lists
    work_regional_list = groups.values()

    #Get dictionaries for population, unemploment rate
    region_population_score = {}

    #Get population score for each region
    for region in unique_regions:
        region_population_score.update({region:calculateCompetitionWeight(TODO,TODO)})
        

if __name__ == '__main__':
    print calculateCompetitionWeight(1000000, 0.2)

       
