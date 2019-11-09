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

    def cf_itemBased(self):
        reader = Reader(line_format ='item user rating', sep=',',rating_scale=(1,5),skip_lines=1)
        data_folds = DatasetAutoFolds(ratings_file='./data/ratings_random.csv', reader=reader)
        trainset = data_folds.build_full_trainset()
        algo = KNNBasic()
        algo.fit(trainset)
        dump.dump('./model/cf_itembase.py',algo=algo)

    def getSimialrChannel(self):
        return self.simialrChannel

    def setSimialrChannel(self):
        ratings_matrix =self.ratings.pivot_table('rating',index='shop_id',columns='ch_id')
        ratings_matrix = ratings_matrix.fillna(0)
        ratings_matrix = ratings_matrix.transpose()
        item_sim = cosine_similarity(ratings_matrix,ratings_matrix)
        predictions = [np.argsort(item_sim[:, i], )[::-1][1:11] for i in range(len(item_sim))]
        self.simialrChannel = predictions

