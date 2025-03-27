from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

appSite = Flask(__name__)

#-----configuracoes para acesso ao banco de dados
appSite.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///fkpinterest.db'
database = SQLAlchemy(appSite)

#-----configuracoes para login/criação de um usuario
# senha abaixo gerada por secrets.token_hex(16), para garantir a seguranca do app Flask
# OBS IMPORTANTE -  bcrypt usa esse SECRET_KEY para criar as senhas dos usuarios
#                   com o metodo  bcrypt.generate_password_hash()
#                   (CUIDADO ao alterar esse codigo pois nao poderá mais recuperar
#                   as senhas do usuario com o bcrypt.check_password_hash() )
appSite.config["SECRET_KEY"] = '860b4119a38c6727dcb0f3e1010826b1'
bcrypt = Bcrypt(appSite)
login_manager = LoginManager(appSite)
#-- caso o usuario nao esteja logado, para qual url(rota) o flask vai redirecionar o usuario
login_manager.login_view = 'home'

#-----configuracoes para upload de fotos
appSite.config["UPLOAD_FOLDER"] = 'static/fotos_posts'

#-- importar routes no final pois o routes.py necessita do appSite.
#       Se for importado no inicio irá criar um erro de referencia circular
from projeto5fakepinterest import routes
