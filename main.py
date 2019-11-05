from flask import Flask
from flask_restplus import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
import models
from models import db
import targeting

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://remoteyum:swmswm10@52.79.184.45/DNBN?charset=utf8'
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
    @api.doc('get')
    def get(self, user_id):
        shop = models.Shop.query.filter_by(provider_user_id =user_id).first()
        # + 로 문자열 append 하는 거 수정해야함
        addr = shop.addr_city +" " + shop.addr_dong + " " + shop.addr_dong + " " + shop.addr_detail
        print(addr)
        area_code = targeting.findArea(shop,addr)
        shop.area_code = area_code
        db.session.add(shop)
        db.session.commit()

        return {"text": "테스트"}



if __name__ == "__main__":
    app.run(debug=True)