import pandas as pd
import requests
import math
import numpy as np
import models
import json


with open('config.json', 'r') as f:
    config = json.load(f)

area = pd.read_csv('./data/area.csv',index_col='area_code')
population = pd.read_csv('./data/population_rating.csv',index_col='area_code')
influencers = pd.read_csv('./data/influencer.csv',index_col= 'channel_id')

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


def recommendation_base(shop):
    prediction = []
    ageRate = population.loc[shop.area_code, ['m','fm','age10','age20','age30','age40','age50','age60']].values
    for idx in influencers.index:
        rating =0
        #카테고리 비교
        if int(shop.category_id / 100000) == int(influencers.loc[idx]['category_id'] / 100000):
            rating = rating + 3
        # 지역
        if int(shop.h_code/100000000)== int(influencers.loc[idx]['addr_code'] / 100000000):
            rating = rating + 2
            if int(shop.h_code / 100000) == int(influencers.loc[idx]['addr_code'] / 100000):
                rating = rating + 1

            # 성별
        gender = 1 - math.pow(population.loc[shop.area_code]['m'] - influencers.loc[idx]['target_m'],
                              2) / 10000
        rating = rating + gender * 2

        # 연령
        age2 = influencers.loc[
            idx, ['target_m', 'target_w', 'target_10', 'target_20', 'target_30', 'target_40', 'target_50',
                'target_60']].values
        # 코사인유사도
        age = np.dot(ageRate, age2) / (np.linalg.norm(ageRate) * np.linalg.norm(age2))
        rating = rating + 2 * age
        prediction.append((idx, rating))
        # df.loc[idx] = [i, rating]
        # idx = idx+1
    prediction = sorted(prediction,key=lambda x:x[1], reverse=True)
    #print(prediction[:10])
    top_10_pred = []
    for i in range(10):
        top_10_pred.append(prediction[i][0])
    #print(top_10_pred)
    return top_10_pred


def test2():
    df = pd.read_csv('./data/influencer2.csv')
    print(df)
    return

