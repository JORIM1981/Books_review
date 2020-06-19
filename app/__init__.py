from flask import Flask 
from config import config_options
from flask_mail import Mail
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet,configure_uploads
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'users.login'
photos = UploadSet('photos',IMAGES)



def create_app(config_name):
    #initialize the application 
    app = Flask(__name__)

   # Creating the app configurations
    app.config.from_object(config_options[config_name])
    
    app.config['SECRET_KEY'] = 'secret'

    # Initializing flask extensions
    bootstrap.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)

    # configure UploadSet
    configure_uploads(app,photos)


    from .users.routes import users as users_blueprint
    from .posts.routes import posts as posts_blueprint
    from .main.routes import main as main_blueprint
    
    app.register_blueprint(users_blueprint)
    app.register_blueprint(posts_blueprint)
    app.register_blueprint(main_blueprint)
    
   
    return app
