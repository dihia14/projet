from flask import Flask, request, render_template, session, redirect, url_for
import bcrypt
import logging
import subprocess
import os
import sys
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from routes import * 
import time 

from managers.mail_manager import *
from managers.password_manager import *
from managers.ip_manager import * 
import rules.brute_force_rule
from init_app import initialize_app, db_manager, ip_manager, mail_manager

# first initiliaze the db : 
#db._initialize_database() #only once 




initialize_app() #init les managers ( marche pas encore correctement .... )
app = Flask(__name__, template_folder='./templates')  
app.secret_key = 'fa66975909197233d5647efdbb3006931e5f5452ec9385abb49dca1f7c7fee49'
# api key generated 
# from import secrets
# print(secrets.token_hex(32))  # 64 car 
#app.secret_key = os.getenv('FLASK_SECRET_KEY')
# print(app.secret_key)
# export FLASK_SECRET_KEY='fa66975909197233d5647efdbb3006931e5f5452ec9385abb49dca1f7c7fee49'
from datetime import timedelta

app.permanent_session_lifetime = timedelta(minutes=30)  # Durée de vie des sessions

register_routes(app)



# for the style : run the command npx tailwind -i ./static/style.css -o ./static/output.css  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)





  
