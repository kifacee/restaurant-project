from flask import Flask
from .config import Configuration   # import config class
from .routes import orders          #import blueprint instance
from .models import db              #import the SQLAlchemy instance

app = Flask(__name__)
app.config.from_object(Configuration)
app.register_blueprint(orders.bp)
db.init_app(app)            #bind the SQLAlchemy instance to the flask instance
