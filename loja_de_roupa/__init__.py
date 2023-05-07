from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
app = Flask(__name__)
app.config['SECRET_KEY'] = '03c77822093b006a32880572d8294c08'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lojaderoupas.db'

database = SQLAlchemy(app) #criou um vínculo entre a database, o SQLALCHEMY e o app
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Faça o login anteriormente'
login_manager.login_message_category = 'alert-danger'

from loja_de_roupa import routers