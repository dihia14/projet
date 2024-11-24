

from flask import Flask, request, render_template, session, redirect, url_for
import bcrypt
import logging
import requests
from routes import * 
from managers.database_manager import add_user_database , get_user, get_users_db, delete_user_database
from managers.mail_manager import send_confirmation_mail_user, send_email_alerte_admin
from managers.password_manager import generate_password
from managers.ip_manager import * 
from rules.brute_force_rule import * 
import sqlite3


# Initialise les routes pour notre application flasks 
def register_routes(app):
    
    # route pour afficher la page index.html 
    @app.route('/')
    def index():
        logging.info("Home page loaded")
        
        loging_msg = request.args.get('loging_msg', '') 
        return render_template('index.html', loging_msg=loging_msg)

    @app.route('/logout')
    def logout():
        logging.info("User successfully logged out")
        return render_template('index.html')
        
    @app.route('/admin')
    def admin():
        #client_ip = request.remote_addr
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

        
        #print("IP", client_ip)

        
        with open('./logs/app.log', 'r') as f:
            logs = f.readlines()
        recent_logs = logs[-20:] 

        ip_data = load_ip_data()

        # TODO : recheck ici, une autre méthode ? 
        if client_ip not in ip_data:
            location = get_ip_location(client_ip)
            if location:
                lat, lon, country, city = location
                ip_data[client_ip] = {
                    'lat': lat,
                    'lon': lon,
                    'country': country,
                    'city' : city
                }
                save_ip_data(ip_data)  
                
        map_html = generate_map(ip_data)

        logging.info(f"Admin page via {client_ip}")

        success_message = request.args.get('success')
        error_message = request.args.get('error')

        return render_template(
            'admin.html',
            logs=recent_logs,
            map_html=map_html,
            success_message=success_message,
            error_message=error_message
        )


    @app.route('/')
    def user():
    
        ip_data = load_ip_data()
        if client_ip not in ip_data:
            location = get_ip_location(client_ip)
            if location:
                lat, lon, country = location
                ip_data[client_ip] = {
                    'lat': lat,
                    'lon': lon,
                    'country': country # add city here * 
                }
                save_ip_data(ip_data)  
                
        logging.info(f"User page via {client_ip}") 
        return render_template('user.html')


    @app.route('/admin_users_manager')
    def gestion_users():
        # ID , username, hash password, mail, privilèges 
        users = get_users_db()
        return render_template('admin_users_manager.html', users=users)  #


    @app.route('/delete_user/<int:user_id>', methods=['POST'])
    def delete_user(user_id):
        delete_user_database(user_id)
        return gestion_users()

    @app.route('/add_user', methods=['POST'])
    def add_user_route():
        
        # retireve the data from the form 
        username = request.form.get('username')
        email = request.form.get('email')
        password = generate_password()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        is_admin = False 
        
        try:
            add_user_database(username, hashed_password, email, is_admin)
            send_confirmation_mail_user(username, email, password)
            #return admin() #+ MSG POUR CONFIRMER (OU PAS) QUE L'USER A ÉTÉ AJOUTÉ 
            return redirect(url_for('admin', success=f"User {username} has been successfully added."))

        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: users.email" in str(e):
                error_message = "The email is already in use. Please choose another one."
            else:
                error_message = "An error occurred while adding the user."
            #return render_template('admin.html', error=error_message)
            return redirect(url_for('admin', error=error_message))
        
        except Exception as e:
            return render_template('admin.html', error=f"Unexpected error: {str(e)}")

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

        
        user = get_user(username)

        if user:
            hashed_password = user[2] 
            is_admin = user[4]  
            #print("is admin ? ", is_admin)
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                if is_admin:
                    logging.info(f"Admin login successful for : {username}")
                    return admin()
                else:
                    logging.info(f"User login successful for : {username}")
                    return admin()  # juste pour le test apres mettre la page adéquate i.e user()
                    #return user()
            else:
                logging.error(f"Invalid password for user : {username}")
                loging_msg = f"Invalid password for : {username}"
                return redirect(url_for('index', loging_msg=loging_msg))

                #log_failed_attempt(username) #save la tentative de connexion 
                #return render_template('index.html')
        else:
            logging.warning(f"Attempt to connect with a user not found : {username}")
            loging_msg = f"Attempt to connect with a user not found : {username}"
            return redirect(url_for('index', loging_msg=loging_msg))
            #return render_template('index.html')

