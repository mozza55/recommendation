import pandas as pd
import requests
import math
import json

with open('config.json', 'r') as f:
    config = json.load(f)

area = pd.read_csv('./data/area.csv',index_col='area_code')
population = pd.read_csv('./data/population_rating.csv',index_col='area_code')
influencers = pd.read_csv('./data/channel.csv',index_col= 'ch_id')

def findHcode(addr):
    headers = {
        'Authorization': config['KAKAOKEY'],
    }
    data = {
        'query' : addr
    }
    response = requests.get('https://dapi.kakao.com/v2/local/search/address.json', headers=headers, data=data)
    j = json.loads(response.text)
    h_code = j.get("documents")[0].get("address").get('h_code')
    return h_code

def findArea(shop,addr):
    print("도착 ",addr)
    headers = {
        'Authorization': config['KAKAOKEY'],
    }
    data = {
        'query' : addr
    }
    response = requests.get('https://dapi.kakao.com/v2/local/search/address.json', headers=headers, data=data)
    j = json.loads(response.text)
    print(j)
    WGS_y = j.get("documents")[0].get("road_address").get('y')
    WGS_x = j.get("documents")[0].get("road_address").get('x')
    h_code = j.get("documents")[0].get("address").get('h_code')
    MIN = 999999
    index = -1
    for i in area.index:
        x = area['lon'][i]
        y = area['lat'][i]
        temp = math.pow(float(WGS_x) - x, 2) + math.pow(float(WGS_y) - y, 2)
        if temp < MIN:
            index = i
            MIN = temp
    shop.area_code = index
    shop.h_code = h_code
    shop.target_m = population.loc[index,'m']
    shop.target_w = population.loc[index, 'fm']
    shop.target_10 = population.loc[index,'age10']
    shop.target_20 = population.loc[index,'age20']
    shop.target_30 = population.loc[index,'age30']
    shop.target_40 = population.loc[index,'age40']
    shop.target_50 = population.loc[index,'age50']
    shop.target_60 = population.loc[index,'age60']
    return 'sucess'

