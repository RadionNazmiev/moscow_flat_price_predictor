import pickle
import json
import numpy as np
import pandas as pd
import os

__form_info = None
__model = None


    
def get_form_info():
    return __form_info

# def get_estimated_price(
#     apartment_type,
#     metro_station,
#     minutes_to_metro,
#     region,
#     number_of_rooms,
#     area,
#     living_area,
#     kitchen_area,
#     floor,
#     number_of_floors,
#     renovation_type
# ):
    
#     is_penthouse = False
#     if floor == number_of_floors:
#         is_penthouse = True
      
#     observation = [
#         apartment_type,
#         metro_station,
#         minutes_to_metro,
#         region,
#         number_of_rooms,
#         area,
#         living_area,
#         kitchen_area,
#         floor,
#         number_of_floors,
#         renovation_type,
#         is_penthouse
#     ]

#     observation_df = pd.DataFrame([observation], columns=__column_names)

#     return round(__model.predict(observation_df)[0],4)


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __form_info
    global __model

    # Determine the directory of the current script
    script_dir = os.path.dirname(__file__)

    # Construct the full path to the artifacts
    form_info_path = os.path.join(script_dir, 'artifacts', 'unique_values_dict.json')
    model_path = os.path.join(script_dir, 'artifacts', 'final_model.pickle')

    # Load the column names
    with open(form_info_path, "r") as f:
        __form_info = json.load(f)


    # Load the model
    if __model is None:
        with open(model_path, 'rb') as f:
            __model = pickle.load(f)
    
    print("loading saved artifacts...done")

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_form_info())

    # print(get_estimated_price(
    #     'newly built',
    #     'жулебино',
    #      14.0,
    #      'moscow region',
    #      2.0,
    #      59.21,
    #      30.2,
    #      13.6,
    #      15.0,
    #      14,
    #      'cosmetic'))
    # print(get_estimated_price('1st Phase JP Nagar',
    #  1000, 2, 2))
    # print(get_estimated_price('Kalhalli', 1000, 2, 2)) 
    # print(get_estimated_price('Ejipura', 1000, 2, 2))  
    