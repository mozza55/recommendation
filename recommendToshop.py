import pandas as pd
import numpy as np
import math
from surprise import SVD
from surprise import KNNBasic
from surprise import Dataset
from surprise import accuracy
from surprise.model_selection import train_test_split
from surprise import Reader
from surprise.dataset import DatasetAutoFolds
from surprise import dump
from surprise.prediction_algorithms.predictions import Prediction
from sklearn.metrics.pairwise import cosine_similarity

class recommendation:
    channels= pd.read_csv('./data/channel.csv', index_col='ch_id')
    ratings = pd.read_csv('./data/ratings.csv')
    area = pd.read_csv('./data/area.csv', index_col='area_code')
    population = pd.read_csv('./data/population_rating.csv', index_col='area_code')

    def __init__(self):
        self.setSimialrChannel()
        self.setCandidateChannelList()
        self.setCFItemBased()

    # 유사한 채널 목록 리턴
    def getSimialrChannel(self,channel):
        return self.simialrChannel[channel.ch_id].tolist()

    # 유사한 채널 목록 생성
    def setSimialrChannel(self):
        ratings_matrix =self.ratings.pivot_table('rating',index='shop_id',columns='ch_id')
        ratings_matrix = ratings_matrix.fillna(0)
        ratings_matrix = ratings_matrix.transpose()
        item_sim = cosine_similarity(ratings_matrix,ratings_matrix)
        predictions = [np.argsort(item_sim[:, i], )[::-1][1:11] for i in range(len(item_sim))]
        self.simialrChannel = predictions

    # CF - itemBase 모델 생성
    def setCFItemBased(self):
        reader = Reader(line_format ='item user rating', sep=',',rating_scale=(1,5))
        data_folds = Dataset.load_from_df(self.ratings[['shop_id', 'ch_id','rating']], reader)
        trainset = data_folds.build_full_trainset()
        algo = KNNBasic()
        algo.fit(trainset)
        dump.dump('./model/cf_itembase_ForShop.py',algo=algo)

    # CF - itemBase 로 채널 추천
    def getCFItemBased(self,shop_id):
        pred,algo = dump.load('./model/cf_itembase_ForShop.py')
        return self.recomm_channel(algo,shop_id)

    # rating을 이용해 추천
    def recomm_channel(self,algo,shop_id, top_n =10):
        predictions =[algo.predict(channel_id,int(shop_id))for channel_id in self.channelList ]
        def sortkey_est(pred):
            return pred.est
        predictions.sort(key=sortkey_est, reverse=True)
        top_predictions = predictions[:top_n]
        top_ch_ids = [int(pred.uid) for pred in top_predictions]
        top_ch_rating = [pred.est for pred in top_predictions]
        #top_channels = [(id, rating) for id,rating in zip(top_ch_ids,top_ch_rating)]
        top_channels = [id for id in top_ch_ids]
        print(top_channels)
        return top_channels

    # 예측할 후보 리스트 리턴 (일단은 전체 채널 다~)
    def getCandidateChannelList(self):
        return self.channelList

    # 예측할 후보 리스트 생성 (일단은 전체 채널 다~)
    def setCandidateChannelList(self):
        self.channelList = self.channels.index.tolist()


    # 가게 기본 정보로 채널 추천
    def recomm_base(self,shop):
        prediction = []
        ageRate = self.population.loc[
            shop.area_code, ['m', 'fm', 'age10', 'age20', 'age30', 'age40', 'age50', 'age60']].values
        for idx in self.channels.index:
            rating = 0
            # 카테고리 비교
            if int(shop.category_id / 100000) == int(self.channels.loc[idx]['category_id'] / 100000):
                rating = rating + 3
            elif self.channels.loc[idx]['category_id'] == 800000:
                rating = rating +2
            # 지역
            if int(shop.h_code / 100000000) == int(self.channels.loc[idx]['h_code'] / 100000000):
                rating = rating + 2
                if int(shop.h_code / 100000) == int(self.channels.loc[idx]['h_code'] / 100000):
                    rating = rating + 1

                # 성별
            gender = 1 - math.pow(self.population.loc[shop.area_code]['m'] - self.channels.loc[idx]['target_m'],
                                  2) / 10000
            rating = rating + gender * 2

            # 연령
            age2 = self.channels.loc[
                idx, ['target_m', 'target_w', 'target_10', 'target_20', 'target_30', 'target_40', 'target_50',
                      'target_60']].values
            # 코사인유사도
            age = np.dot(ageRate, age2) / (np.linalg.norm(ageRate) * np.linalg.norm(age2))
            rating = rating + 2 * age
            prediction.append((idx, rating))
            # df.loc[idx] = [i, rating]
            # idx = idx+1
        prediction = sorted(prediction, key=lambda x: x[1], reverse=True)
        # print(prediction[:10])
        top_10_pred = []
        for i in range(10):
            top_10_pred.append(prediction[i][0])
        # print(top_10_pred)
        return top_10_pred

    def reloadChannel(self):
        #전역변수 처리 해야함
        self.channels = pd.read_csv('./data/channel.csv',index_col= 'ch_id')
        return

def main():
    r = recommendation()
    r.setCFItemBased()
    r.getCFItemBased(3)

if __name__ == '__main__':
  main()
