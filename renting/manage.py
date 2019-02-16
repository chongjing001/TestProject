from flask import Flask,render_template
from flask_script import Manager
from app.models import db
from app.order_views import blue_o
from app.user_views import blue, login_manage
from app.home_views import blue_h

app = Flask(__name__)

app.register_blueprint(blueprint=blue,url_prefix='/user')
app.register_blueprint(blueprint=blue_h,url_prefix='/home')
app.register_blueprint(blueprint=blue_o,url_prefix='/order')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@120.79.51.163/renting'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')


login_manage.init_app(app)

app.secret_key = 'fadiofdaii23ior4u9iowjeiou73ri4jo'

manage = Manager(app)

if __name__ == '__main__':
    manage.run()
