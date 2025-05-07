from flask import Flask
from .config import Configuration   # import config class
from .routes import orders, session     #import blueprint instances
from .models import db, Employee        #import created models + the SQLAlchemy instance
from flask_login import LoginManager



app = Flask(__name__)
app.config.from_object(Configuration)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://order_up:9uCxydbt@localhost/order_up_dev'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# print(app.config['SQLALCHEMY_DATABASE_URI'])
app.register_blueprint(orders.bp)
app.register_blueprint(session.bp)
db.init_app(app)            #bind the SQLAlchemy instance to the flask instance


login = LoginManager(app)
login.login_view = "session.login"  #telling it which blueprint view function to use
                                    #when applying the @login_required decorator


@login.user_loader      #how login manager can get the user from the db
def load_user(id):
    return Employee.query.get(int(id))
