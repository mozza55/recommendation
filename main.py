from flask import Flask
from flask_restplus import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
import models
import targeting
import json
import csv
import pandas as pd
from sqlalchemy.orm import load_only

with open('config.json', 'r') as f:
    config = json.load(f)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['DB_URI']
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
models.db.init_app(app)

api = Api(app, version='1.0', title='Recommendation API',
          description='DNBN recommendation service',
          )

#가게 위치 정보로 상권 분석으로 타겟 분류
@api.route('/set/shop-target/<provider_user_id>')
class setShopTarget(Resource):
    @api.doc('post')
    def post(self, user_id):
        shop = models.Shop.query.filter_by(provider_user_id =user_id).first()
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

#가게 기본정보를 바탕으로 인플루언서 추천
@api.route('/recommend/info-based/<provider_user_id>')
class basedRecommendationList(Resource):
    @api.doc('get')
    def get(self,user_id):
        shop = models.Shop.query.filter_by(provider_user_id =user_id).first()
        top_10_pred = targeting.recommendation_base(shop)
        return {"recommendations": top_10_pred}


# 유사 인플루언서 추천
@api.route('/recommend/similar-influencer/<ch_id>')
class similarRecommendationList(Resource):
    @api.doc('get')
    def get(self, ch_id):
        channel = models.Channel.query.filter_by(ch_id =ch_id).first()
        top_10_pred = targeting.recommendation_similar(channel)
        return {"recommendations":top_10_pred}


#DB 조회해서 기준 인플루언서 목록 업데이트 (전체 인플루언서를 읽어옴)
@api.route('/save/recommendation-data/channel')
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
        targeting.reloadChannel()
        return {"test": "테스트"}



if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)