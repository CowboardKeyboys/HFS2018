
import pandas as pd

def calculateCompetitionWeight(population, unemployment_rate):
    profession_count = 12.0
    return round((population * unemployment_rate)/profession_count)


def normalize_dictionary(working_dictionary):

    factor = 1.0/sum(working_dictionary.itervalues())

    for k in working_dictionary:
        working_dictionary[k]=working_dictionar[k]*factor

    return working_dictionary

def get_work_score(region_list):

    region_ws_dict = {}
    for region in region_list:
        region_ws_dict.update({region[0].region_code:sum(r.score for r in region)})

            

def getRegionScore(work_objects):
    from collections import defaultdict

    #Extract unique regions name from our work list
    unique_regions = {obj.region_code for obj in work_objects}
    groups = defaultdict(list)
    
    for obj in work_objects:
        groups[obj.region_code].append(obj)

    #Get 2D list with job for each regions in seperate lists
    work_regional_list = groups.values()

    #Get dictionaries for population, unemployment rate
    region_population_score = {}

    #Get population score for each region
    
    #for region in unique_regions:
    #    region_population_score.update({region:calculateCompetitionWeight(TODO,TODO)})
    
    #Here we probably want to calculate population score based on our job scores.


    #NEXT STEP JOB MARKET ESTIMATION


    #FINAL STEP ECONOMIC REGION ESTIMATION




    #RETURN REGION OBJECT LIST
if __name__ == '__main__':
    print calculateCompetitionWeight(1000000, 0.2)

       
