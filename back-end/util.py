import pickle
import json
import numpy as np
import pandas as pd
import os

__form_info = None
__model = None

   
def get_form_info():
    return __form_info

def get_estimated_price(
    apartment_type,
    metro_station,
    minutes_to_metro,
    region,
    number_of_rooms,
    area,
    living_area,
    kitchen_area,
    floor,
    number_of_floors,
    renovation_type
):
    
    is_penthouse = False
    if floor == number_of_floors:
        is_penthouse = True
      
    observation = [[
        apartment_type,
        metro_station,
        minutes_to_metro,
        region,
        number_of_rooms,
        area,
        living_area,
        kitchen_area,
        floor,
        number_of_floors,
        renovation_type,
        is_penthouse
    ]]

    observation_df = pd.DataFrame(observation, columns=__form_info.keys())

    return round(np.expm1(__model.predict(observation_df)[0]),4)


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __form_info
    global __model

    script_dir = os.path.dirname(__file__)

    form_info_path = os.path.join(
        script_dir, 'artifacts', 'unique_values_dict.json'
    )

    with open(form_info_path, "r") as f:
        __form_info = json.load(f)


    model_path = os.path.join(
        script_dir, 'artifacts', 'final_model.pickle'
    )


    if __model is None:
        with open(model_path, 'rb') as f:
            __model = pickle.load(f)
    
    print("loading saved artifacts...done")

if __name__ == '__main__':
    load_saved_artifacts()
    # print(get_form_info())
    # print(get_estimated_price(
    #     'previously owned',
    #     'опалиха',
    #     6,
    #     'moscow region',
    #     1,
    #     30.6,
    #     11.1,
    #     8.5,
    #     25,
    #     25,
    #     'cosmetic'
    # ))
    