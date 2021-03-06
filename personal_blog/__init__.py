import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

mail = Mail()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .posts import posts as post_blueprint
    app.register_blueprint(post_blueprint, url_prefix='/posts')

    from .categories import categories as categories_blueprint
    app.register_blueprint(categories_blueprint, url_prefix="/categories")

    from .errors import errors as error_blueprint
    app.register_blueprint(error_blueprint, url_prefix='/error')

    if not os.path.exists(os.path.join(basedir, 'logs')):
        os.mkdir(os.path.join(basedir, 'logs'))
        file_handler = RotatingFileHandler('logs/personal_blog.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.ERROR)
    app.logger.info('Start Personal Blog')

    return app
