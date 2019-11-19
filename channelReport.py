import pandas as pd

class reporting:
    report = pd.read_csv('./data/reporting.csv')

    def getChannelReport(self,ch_id):
        channel = self.report[self.report['ch_id']==ch_id]
        # 업데이트가 되면 새 데이터가 쌓일 테니 그룹바이도 그때그때 하는게 나은
        #ch = channel.groupby(["ch_id","category_id"]).mean()[["play_count","viewing_time","chat_count","buy_count","cart_count"]]
        #channel = channel["play_count","viewing_time","chat_count","buy_count","cart_count"]
        #ch['count'] =\
        #ch['count']=channel.groupby(["ch_id","category_id"])['prod_id'].count()
        tot= channel.groupby(["ch_id"]).mean()[["category_id","play_count","viewing_time","chat_count","buy_count","cart_count"]]
        tot["category_id"] =0
        channel=channel.append(tot)
        #print(channel.size)
        print(channel)


def main():
    r = reporting()
    r.getChannelReport(1)

if __name__ == '__main__':
  main()
