from flask import Flask
from flask_restplus import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
import models
import targeting
import json
import csv
import pandas as pd
from sqlalchemy.orm import load_only
import recommendToshop
import gaReportToRating as ga
import channelReport

with open('config.json', 'r') as f:
    config = json.load(f)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['DB_URI']
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
models.db.init_app(app)
recommendToshop = recommendToshop.recommendation()
channelReport = channelReport.reporting()
api = Api(app, version='1.0', title='Recommendation API',
          description='DNBN recommendation service',
          )

recomm = api.namespace('recommend',description='추천 리스트를 전달')
report = api.namespace('report',description ='리포트 내용 전달')

#가게 위치 정보로 상권 분석으로 타겟 분류
@api.route('/set/shop-target/<shop_id>')
class setShopTarget(Resource):
    @api.doc('post')
    def put(self, shop_id):
        shop = models.Shop.query.filter_by(shop_id =shop_id).first()
        # + 로 문자열 append 하는 거 수정해야함
        addr = shop.addr_city +" " + shop.addr_gu + " " + shop.addr_dong +" " +shop.addr_detail
        targeting.findArea(shop,addr)
        models.db.session.add(shop)
        models.db.session.commit()
        return {"test": "타겟팅 데이터 입력"}

#주소로 행정동 코드 입력
@api.route('/set/channel-hcode/<ch_id>')
class setTargetForStore(Resource):
    @api.doc('post')
    def post(self, ch_id):
        channel = models.Channel.query.filter_by(ch_id =ch_id).first()
        # + 로 문자열 append 하는 거 수정해야함
        addr = channel.addr_city +" " + channel.addr_dong + " " + channel.addr_dong
        channel.h_code=targeting.findHcode(addr)
        models.db.session.add(channel)
        models.db.session.commit()
        return {"message": "channel h_code update"}

#추천 : 가게 기본정보를 바탕으로 인플루언서 추천
#@api.route('/recommend/info-based/<provider_user_id>')
@recomm.route('/info-based/<shop_id>')
@recomm.param('shop_id','shop의 shop_id를 입력해주세요')
class basedRecommendationList(Resource):
    @api.doc('get')
    def get(self,shop_id):
        '''가게의 user id를 입력하면 상권 분석을 통해 만들어진 추천 채널 id 리스트를 생성'''
        shop = models.Shop.query.filter_by(shop_id =shop_id).first()
        top_10_pred = recommendToshop.recomm_base(shop)
        return {"recommendations": top_10_pred}

#추천 : rating 데이터 만들어진 CF 알고리즘을 통해 인플루언서 추천
#@api.route('/recommend/cf-channelbased/<provider_user_id>')
@recomm.route('/cf-channelbased/<shop_id>')
@recomm.param('shop_id','shop의 shop_id를 입력해주세요')
class cfRecommendationList(Resource):
    @api.doc('get')
    def get(self,shop_id):
        '''가게의 user id를 입력하면 cf로 만들어진 추천 채널 id 리스트를 생성'''
        top_10_pred = recommendToshop.getCFItemBased(shop_id)
        return {"recommendations": top_10_pred}

#추천 : 유사 인플루언서 추천
#@api.route('/recommend/similar-influencer/<ch_id>')
@recomm.route('/similar-influencer/<ch_id>')
@recomm.param('ch_id','channel의 id를 입력해주세요')
class similarRecommendationList(Resource):
    @api.doc('get')
    def get(self, ch_id):
        '''채널의 id를 입력하면 유사 채널의 id 리스트를 생성'''
        channel = models.Channel.query.filter_by(ch_id =ch_id).first()
        top_10_pred = recommendToshop.getSimialrChannel(channel)
        return {"recommendations":top_10_pred}

#리포트 : 채널 리포트 제공
@report.route('/channel-report/<ch_id>')
@report.param('ch_id','channel의 id를 입력해주세요')
class specificChannelReport(Resource):
    @api.doc('get')
    def get(self,ch_id):
        return channelReport.getChannelReport(int(ch_id),100000)

#DB 조회해서 기준 인플루언서 목록 업데이트 (전체 인플루언서를 읽어옴)
@api.route('/set/recommendation-data/channel')
class saveRecommendation(Resource):
    def get(self):
        # 방법 1
        fields= ['ch_id','name','follower_num','category_id','cost','views','addr_city','addr_gu','addr_dong','h_code','target_m','target_w','target_10','target_20','target_30','target_40','target_50','target_60']
        channels = models.Channel.query.options(load_only(*fields))
        # 방법 2
        #channels = models.Channel.query.with_entities(models.Channel.ch_id, models.Channel.name,models.Channel.follower_num, models.Channel.cost,models.Channel.views,
        #                                             models.Channel.addr_city, models.Channel.addr_gu, models.Channel.addr_dong,models.Channel.h_code,
        #                                            models.Channel.target_m, models.Channel.target_w, models.Channel.target_10)

        # all()이 붙지않아서 실행은 안됨
        df = pd.read_sql(channels.statement, channels.session.bind) #실제 쿼리가 실행됨
        df.to_csv("./data/channel.csv",index=False)
        recommendToshop.reloadChannel()
        return {"test": "테스트"}

@api.route('/set/recommendation-data/rating/weblog')
class saveWeblogRating(Resource):
    def put(self):
        ga.update_logRating()
        return {"update": "WebLog Rating 저장"}


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)