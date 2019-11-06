from flask import Flask
from flask_restplus import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
import models
import targeting

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://아이디:패스워드0@52.79.184.45/DNBN?charset=utf8'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
models.db.init_app(app)
#db = SQLAlchemy(app)
#app.secret_key = 'swmswm10'

api = Api(app, version='1.0', title='Recommendation API',
          description='DNBN recommendation service',
          )

@api.route('/set/target/<user_id>')
class setTargetForStore(Resource):
    @api.doc('post')
    def post(self, user_id):
        shop = models.Shop.query.filter_by(provider_user_id =user_id).first()
        # + 로 문자열 append 하는 거 수정해야함
        addr = shop.addr_city +" " + shop.addr_dong + " " + shop.addr_dong + " " + shop.addr_detail
        targeting.findArea(shop,addr)
        models.db.session.add(shop)
        models.db.session.commit()
        return {"text": "테스트"}

@api.route('/recommend/default/<user_id>')
class defaultRecommendationList(Resource):
    @api.doc('get')
    def get(self,user_id):
        shop = models.Shop.query.filter_by(provider_user_id =user_id).first()
        targeting.recommendation_base(shop)
        return {"text": 'default'}


if __name__ == "__main__":
    app.run(debug=True)