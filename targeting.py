import pandas as pd
import requests
import json
import math
import numpy as np
import models

area = pd.read_csv('./data/area.csv',index_col='area_code')
population = pd.read_csv('./data/population_rating.csv',index_col='area_code')

def findArea(shop,addr):
    print("도착 ",addr)
    headers = {
        'Authorization': 'key',
    }
    data = {
        'query' : addr
    }
    response = requests.get('https://dapi.kakao.com/v2/local/search/address.json', headers=headers, data=data)
    j = json.loads(response.text)
    WGS_y = j.get("documents")[0].get("road_address").get('y')
    WGS_x = j.get("documents")[0].get("road_address").get('x')

    MIN = 999999
    index = -1
    for i in area.index:
        x = area['lon'][i]
        y = area['lat'][i]
        temp = math.pow(float(WGS_x) - x, 2) + math.pow(float(WGS_y) - y, 2)
        if temp < MIN:
            index = i
            MIN = temp
    print(index)

    return index;

