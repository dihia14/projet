from flask import Blueprint, request, session, redirect, url_for, render_template
from managers.database_manager import UserDatabase



from flask import Flask, request, render_template, session, redirect, url_for, abort 
import bcrypt
import logging
import requests
from routes import * 



from managers.database_manager import UserDatabase
from managers.mail_manager import EmailManager
from managers.ip_manager import IPManager
from managers.password_manager import PasswordManager
from managers.files_manager import FileManager
from managers.filePage_manager import * 
from rules.brute_force_rule import * 
import sqlite3
from ids_alerts_parser import LogParserIdsAlert
from .admin import *

from init_app import db_manager, mail_manager, ip_manager  # Managers initiaux



user_blueprint = Blueprint("user", __name__, url_prefix="/user")

@user_blueprint.route("/new_password/<username>")
def new_password(username):
    user_info = db_manager.get_user_infos(username)
    # ask for another password to generate 
    new_password = PasswordManager.generate_password()
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

    # send it to the user 
    email = user_info[2]
    mail_manager.send_confirmation_mail_user(username, email, new_password, False)
    
    #update the db 
    db_manager.update_password_username(username, hashed_password) ##
    print(f"NEW password requested for user: {username}")
    return render_template('user_settings_page.html', user_info=user_info)  



@user_blueprint.route("/user_settings_page/<username>")
def user_settings_page(username):
    # ID , username, hash password, mail, privilèges 
    #user_info = get_user_infos(username)
    user_info = db_manager.get_user_infos(username)
    print(user_info)
    print(f"Current session: {dict(session)}")  

    return render_template('user_settings_page.html', user_info=user_info)  #



