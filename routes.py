

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

from rules.brute_force_rule import * 
import sqlite3
from ids_alerts_parser import LogParserIdsAlert

# injections sql => bloque adresse IP 
# emplacement pour afficher les alertes pour l'admin 
# statistiques : nb d'attaques des ≠ types : par jours, minutes, ...
# voire pour ransom ( voir avec le Sftp , ... )
# analyse d'un fichier malveillant .. 
# Sftp, "drive" pour des "chiffré" des files 


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

#password_manager = PasswordManager()

def write_last_ip(client_ip):
    with open("last_ip.txt", "w") as f:
        f.write(f"{client_ip}\n")


def authorize(client_ip): 
    try:
        with open("black_list.txt", "r") as f:
            lst_ip = f.read().strip().splitlines() # retrieve the black ips 
        
        if client_ip in lst_ip:
            return False  # not authorized access 
        else:
            return True  # authorized access 
    
    except FileNotFoundError:
        print("Error.")
        return True



#bloquer ensuite les @ips tentant de faire cela ? 

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
            # STOP THE PROGRAM    , exit 
            return "access unauthorized"
            #abort(400) 


        else :
            print("ACCES autorisé ")     
 
 
        loging_msg = request.args.get('loging_msg', '') 
        return render_template('index.html', loging_msg=loging_msg)

    @app.route('/logout')
    def logout():
        session.clear()  
        logging.info("User successfully logged out")
        return render_template('index.html')
        
    @app.route('/admin')
    def admin():
        
        if 'username' not in session or not session.get('is_admin', False):
            return redirect(url_for('index', loging_msg="Unauthorized access"))
    
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        logging.info(f"Admin page accessed by {session['username']} from {client_ip}")
    
    
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

        print("in admin", client_ip)


        recent_logs = FileManager.get_last_logs()
        

        ids_alerts = LogParserIdsAlert.load_last_alerts(last_n=6)
        
        
        ip_data = ip_manager.load_ip_data()

        # TODO : recheck ici, une autre méthode ? 
        if client_ip not in ip_data:
            location = ip_manager.get_ip_location(client_ip)
            if location:
                lat, lon, country, city = location
                ip_data[client_ip] = {
                    'lat': lat,
                    'lon': lon,
                    'country': country,
                    'city' : city
                }
                ip_manager.save_ip_data(ip_data)  
                
        map_html = ip_manager.generate_map(ip_data)

        logging.info(f"Admin page via {client_ip}")

        success_message = request.args.get('success')
        error_message = request.args.get('error')

        return render_template(
            'admin.html',
            logs=recent_logs,
            ids_alerts = ids_alerts,
            map_html=map_html,
            success_message=success_message,
            error_message=error_message
        )


    @app.route('/')
    def user_page():
        
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

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
        #users = get_users_db()
        users = db_manager.get_users()
        return render_template('admin_users_manager.html', users=users)  #


   # @app.route('/user_settings_page')
    @app.route('/user_settings_page/<username>')
    def user_settings_page(username):
        # ID , username, hash password, mail, privilèges 
        #user_info = get_user_infos(username)
        user_info = db_manager.get_user_infos(username)
        print(user_info)
        return render_template('user_settings_page.html', user_info=user_info)  #

    
    @app.route('/delete_user/<int:user_id>', methods=['POST'])
    def delete_user(user_id):
        db_manager.delete_user(user_id)
        return gestion_users()

    @app.route('/add_user', methods=['POST'])
    def add_user_route():
        
        # retireve the data from the form 
        username = request.form.get('username')
        email = request.form.get('email')  
        password = PasswordManager.generate_password()

            
            
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        is_admin = False 
        
        try:
            db_manager.add_user(username, hashed_password, email, is_admin)
            mail_manager.send_confirmation_mail_user(username, email, password)
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

        
        user = db_manager.get_user(username)

        if user:
            hashed_password = user[2] 
            is_admin = user[4]  
            #print("is admin ? ", is_admin)
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                
                # retrieve session data 
                session['username'] = username
                session['is_admin'] = is_admin
                #session.permanent = True  

            
                if is_admin:
                    logging.info(f"Admin login successful for : {username}")
                    return admin()
                else:
                    logging.info(f"User login successful for : {username}")
                    #return admin()  # juste pour le test apres mettre la page adéquate i.e user()
                    return user_settings_page(username)
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

