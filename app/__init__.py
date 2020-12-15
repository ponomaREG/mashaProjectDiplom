from flask import Flask
from config import BaseConfig
from flask_login import LoginManager
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(BaseConfig)
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)
from app import views