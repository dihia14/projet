from flask import Flask
from datetime import timedelta
from init_app import initialize_app
from init_app import *

import os 
initialize_app() # pour init les managers (globaux) que seront utilisés dans les routes . 


from routes.admin import admin_blueprint
from routes.user import user_blueprint
from routes.file import file_blueprint
from routes.index import index_blueprint


### test dos 
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def create_app():
    """
    Crée + init  l'application Flask.
    """
    app = Flask(__name__, template_folder='./templates')
    app.secret_key = 'fa66975909197233d5647efdbb3006931e5f5452ec9385abb49dca1f7c7fee49'
    
    
    
    ### test : 
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["100 per minute"]
    )  
    
     
    app.permanent_session_lifetime = timedelta(minutes=30)  # duree de vie des sessions

    app.register_blueprint(index_blueprint, url_prefix="/")
    app.register_blueprint(admin_blueprint, url_prefix="/admin")
    app.register_blueprint(user_blueprint, url_prefix="/user")
    app.register_blueprint(file_blueprint, url_prefix="/file")

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=9000, debug=True)


# style run : npx tailwind -i ./static/style.css -o ./static/output.css  