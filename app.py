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
from managers.database_manager import add_user_database , get_user, get_users_db, delete_user_database

from managers.mail_manager import send_confirmation_mail_user, send_email_alerte_admin
from managers.password_manager import generate_password
from managers.ip_manager import * 
import rules.brute_force_rule


# 
# logging.basicConfig(
#     filename='./logs/app.log',
#     level=logging.INFO,  
#     format='%(asctime)s - %(levelname)s - %(message)s'  # msg format 
# )

logging.basicConfig(
    filename='./logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a',
    force=True
)

logging.getLogger().handlers[0].setStream(open('/Users/jafjafnora/Desktop/git/projet/logs/app.log', 'a', buffering=1))




app = Flask(__name__, template_folder='./templates')  
register_routes(app)


if __name__ == '__main__':
    tailwind_command = ["npx", "tailwindcss", "-i", "./static/style.css", "-o", "./static/output.css", "--watch"]
   
#   # changer le port en fonction .. 
    app.run(host='0.0.0.0', port=9000, debug=True)





  
 
# def get_user_log(username):
#     user_found = get_user(username)
#     logging.info(f"Searching for the user : {username}")
#     if user_found:
#         logging.info(f"User found :  {username}")
#     else:
#         logging.warning(f"User not found : {username}")
#     return user_found