

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
from .user import * 

#init of the managers 
db_manager = UserDatabase()


#init the IP manager 
ip_manager = IPManager()


#init the mail manager 
mail_manager = EmailManager() ###recheck 

# Initialisation des paramètres globaux pour EmailManager only once (same as db recheck dans in init app )
EmailManager.initialize(
    smtp_server="smtp.gmail.com",
    port=587,
    sender_email="jafjafnora@gmail.com",
    sender_password="luzz vnkb izzm lpps"
)

from utils import *

# Initialise les routes pour notre application flasks 
def register_routes(app):
    
    # route pour afficher la page index.html 
    @app.route('/')
    def index():
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        logging.info(f"Home page loaded from {client_ip}" )
        write_last_ip(client_ip)
        print(f"Current session: {dict(session)}")  

        if not authorize(client_ip) : 
            return "access unauthorized"
        else :
            print("ACCES autorisé ")     
 
 
        loging_msg = request.args.get('loging_msg', '') 
        return render_template('index.html', loging_msg=loging_msg)

    @app.route('/logout')
    def logout():
        session.clear()  
        logging.info("User successfully logged out")
        return render_template('index.html')
 





    
    @app.route('/reset_password', methods=['POST'])
    def reset_password():
        username = request.form.get('username')
        email = request.form.get('email')

        # Vérifier si l'utilisateur existe
        user = db_manager.get_user(username)

        if not user or user[3] != email:  # Vérifier que l'email correspond également
            loging_msg = "Erreur : Utilisateur ou email non trouvé."
            return redirect(url_for('index', loging_msg=loging_msg))

        # Générer un nouveau mot de passe et le hacher
        new_password = PasswordManager.generate_password()
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

        # Mettre à jour le mot de passe dans la base de données
        db_manager.update_password_username(username, hashed_password)

        # Envoyer l'email avec le nouveau mot de passe
        mail_manager.send_confirmation_mail_user(username, email, new_password, False)

        # Rediriger vers l'index avec un message de confirmation
        loging_msg = "Un email avec votre nouveau mot de passe a été envoyé."
        return redirect(url_for('index', loging_msg=loging_msg))



        
    @app.route('/login', methods=['POST'])
    def login():
        
        loging_msg = ""
        
        # retrieve the data from the form 
        username = request.form.get('username')
        password = request.form.get('password')
        
        logging.info(f"Login attempt for user: {username}")
        if check_brute_force(username):
            
            logging.error(f"Too many failed attempts for {username}. Please try again later.'")
            loging_msg = "Too many failed attempts. Please try again later."
            #return render_template('index.html')
            return redirect(url_for('index', loging_msg=loging_msg))############

        
        user = db_manager.get_user(username)

        if user:
            hashed_password = user[2] 
            is_admin = user[4]  
            #print("is admin ? ", is_admin)
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                
                # retrieve session data 
                session['username'] = username
                session['is_admin'] = is_admin
                session['user_id'] = user[0]
                session.permanent = True  

            
                if is_admin:
                    logging.info(f"Admin login successful for : {username}")
                    return admin(username)
                else:
                    logging.info(f"User login successful for : {username}")
                    #return admin()  # juste pour le test apres mettre la page adéquate i.e user()
                    #return user_settings_page(username) ### faire un autre blu print de "general rooute" apres 
                    return redirect(url_for('user.user_settings_page', username=session['username']))
 
            else:
                logging.error(f"Invalid password for user : {username}")
                loging_msg = f"Invalid password for : {username}"
                log_failed_attempt(username) #save la tentative de connexion 

                return redirect(url_for('index', loging_msg=loging_msg))

                #return render_template('index.html')
        else:
            logging.warning(f"Attempt to connect with a user not found : {username}")
            loging_msg = f"Attempt to connect with a user not found : {username}"
            return redirect(url_for('index', loging_msg=loging_msg))
            #return render_template('index.html')


