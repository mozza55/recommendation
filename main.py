from flask import Flask
from flask_restplus import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
import models
import targeting
import json
import csv

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

@api.route('/set/shoptarget/<user_id>')
class setTargetForStore(Resource):
    @api.doc('post')
    def post(self, user_id):
        shop = models.Shop.query.filter_by(provider_user_id =user_id).first()
        # + 로 문자열 append 하는 거 수정해야함
        addr = shop.addr_city +" " + shop.addr_dong + " " + shop.addr_dong + " " + shop.addr_detail
        targeting.findArea(shop,addr)
        models.db.session.add(shop)
        models.db.session.commit()
        return {"test": "타겟팅 데이터 입력"}

@api.route('/recommend/base/<user_id>')
class basedRecommendationList(Resource):
    @api.doc('get')
    def get(self,user_id):
        shop = models.Shop.query.filter_by(provider_user_id =user_id).first()
        top_10_pred = targeting.recommendation_base(shop)
        return {"recommendations": top_10_pred}

@api.route('/save/influencer/')
class saveData(Resource):
    def get(self):
        influencers = models.Channel.query.all()
        return {"test": len(influencers)}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000,debug=True)