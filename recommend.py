import pandas as pd
import numpy as np
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
    channels= pd.read_csv('./data/channel.csv')
    ratings = pd.read_csv('./data/ratings.csv')

    def __init__(self):
        self.setSimialrChannel()
        self.channelList = self.getChannelList()

    def getSimialrChannel(self):
        return self.simialrChannel

    def setSimialrChannel(self):
        ratings_matrix =self.ratings.pivot_table('rating',index='shop_id',columns='ch_id')
        ratings_matrix = ratings_matrix.fillna(0)
        ratings_matrix = ratings_matrix.transpose()
        item_sim = cosine_similarity(ratings_matrix,ratings_matrix)
        predictions = [np.argsort(item_sim[:, i], )[::-1][1:11] for i in range(len(item_sim))]
        self.simialrChannel = predictions

    def setCFItemBased(self):
        reader = Reader(line_format ='item user rating', sep=',',rating_scale=(1,5))
        data_folds = Dataset.load_from_df(self.ratings[['shop_id', 'ch_id','rating']], reader)
        trainset = data_folds.build_full_trainset()
        algo = KNNBasic()
        algo.fit(trainset)
        dump.dump('./model/cf_itembase_ForShop.py',algo=algo)

    def getCFItemBased(self,shop_id):
        pred,algo = dump.load('./model/cf_itembase_ForShop.py')
        self.recomm_channel(algo,shop_id)

    def recomm_channel(self,algo,shop_id, top_n =10):
        predictions =[algo.predict(channel_id,shop_id)for channel_id in self.channelList ]
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

    # 예측할 채널 리스트 (일단은 전체 채널 다~)
    def getChannelList(self):
        total_channels = self.channels.index.tolist()
        return total_channels

r = recommendation()
r.setCFItemBased()
r.getCFItemBased(3)