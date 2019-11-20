import pandas as pd

class reporting:
    def __init__(self):
        self.report = pd.read_csv('./data/reporting.csv')
        self.getTotalReport()
        self.category_name=['전체','음식','교육','스포츠오락','생활','미용','IT','패션','엔터']

    def getTotalReport(self):
        channel= self.report
        channel =channel[["rating","ER","play_count","viewing_time","chat_count","buy_count","cart_count"]]
        self.avg = channel.mean()


    def getChannelReport(self,ch_id,ch_info,category_id):
        cate_name =self.category_name[int(category_id/100000)]
        re = {}
        re['gender'] =[ch_info.target_w, ch_info.target_m]
        re['age'] = [ch_info.target_10, ch_info.target_20,ch_info.target_30, ch_info.target_40,ch_info.target_50, ch_info.target_50]
        re['category'] = [cate_name]
        channel = self.report[self.report['ch_id']==ch_id]
        #데이터가 없을 경우
        if channel.index.size ==0:
            re['rating'] = [0, 5]
            re['view'] = [self.avg['play_count'], 0,0]
            re['chat'] = [self.avg['chat_count'], 0,0]
            re['buy'] = [self.avg['buy_count'], 0,0]
            re['er'] = [round(self.avg['ER'], 1), 0,0]
            return re

        channel = channel.drop(['ch_id', 'prod_id','brod_id'], axis='columns')
        tot= channel.mean()[["rating","ER","category_id","play_count","viewing_time","chat_count","buy_count","cart_count"]]
        tot["category_id"] =0
        channel.loc[channel.index.size] = tot

        # 업데이트가 되면 새 데이터가 쌓일 테니 그룹바이도 그때그때 하는게 나은
        ch = channel.groupby("category_id").mean()[["rating","ER","play_count","viewing_time","chat_count","buy_count","cart_count"]]
        ch['count'] = channel.groupby("category_id")["rating"].count()
        ch.loc[0,'count'] = ch["count"].sum()-1

        # 없는 카테고리일 경우 인덱스 처리해야함
        if category_id not in ch.index:
            ch.loc[category_id] = 0

        re['category_cnt'] = [int(ch.loc[category_id,"count"]), int(ch.loc[0,"count"]-ch.loc[category_id,"count"])]
        re['rating']=[round(ch.loc[0,"rating"],1),round(5-ch.loc[0,"rating"],1)]
        re['view']=[self.avg['play_count'],ch.loc[0,"play_count"],ch.loc[category_id,"play_count"]]
        re['chat']=[self.avg['chat_count'],ch.loc[0,"chat_count"],ch.loc[category_id,"chat_count"]]
        re['buy']=[self.avg['buy_count'],ch.loc[0,"buy_count"],ch.loc[category_id,"buy_count"]]
        re['er']=[round(self.avg['ER'],1),round(ch.loc[0,"ER"],1),round(ch.loc[category_id,"ER"],1)]
        print(re)
        return re


def main():
    r = reporting()
    #r.getChannelReport(1,100000)

if __name__ == '__main__':
  main()
