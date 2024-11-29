from flask import Blueprint, request, session, redirect, url_for, render_template
from managers.database_manager import UserDatabase
from managers.filePage_manager import list_files
from managers.password_manager import * 
from managers.files_manager import * 
from managers.ip_manager import * 
from managers.mail_manager import * 





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




admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin")
db_manager = UserDatabase()

# @admin_blueprint.route("/<username>")
# def admin_dashboard(username):
#     user_info = db_manager.get_user_infos(username)
#     files = list_files(str(user_info[0]))
#     return render_template("admin_dashboard.html", user_info=user_info, files=files)


#init of the managers 


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

#@app.route('/admin')
#@app.route('/admin/<username>')
@admin_blueprint.route("/admin/<username>")
def admin(username):
    
    # if 'username' not in session or not session.get('is_admin', False):
    #     return redirect(url_for('index', loging_msg="Unauthorized access"))

    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    #logging.info(f"Admin page accessed by {session['username']} from {client_ip}")


    user_info = db_manager.get_user_infos(username)

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
        error_message=error_message,
        user_info=user_info
    )


#@app.route('/admin/file_page/<username>')
@admin_blueprint.route("/admin/file_page/<username>")
def admin_file_page(username) : 
    user_info = db_manager.get_user_infos(username)
    return redirect(url_for("file.file_page", username=username))



#@app.route('/admin_users_manager')
@admin_blueprint.route("/admin_users_manager")
def gestion_users():
    # ID , username, hash password, mail, privilèges 
    #users = get_users_db()
    users = db_manager.get_users()
    return render_template('admin_users_manager.html', users=users)  #






@admin_blueprint.route("/delete_user/<int:user_id>",methods=['POST'] )
def delete_user(user_id):
    db_manager.delete_user(user_id)
    return gestion_users()

@admin_blueprint.route("/add_user",methods=['POST'] )
def add_user_route():
    
    # retireve the data from the form 
    username = request.form.get('username')
    email = request.form.get('email')  
    password = PasswordManager.generate_password()

        
        
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    is_admin = False 
    
    try:
        db_manager.add_user(username, hashed_password, email, is_admin)
        mail_manager.send_confirmation_mail_user(username, email, password, True)
        #return redirect(url_for('admin', success=f"User {username} has been successfully added."))
        return redirect(url_for('admin.admin', username=session['username'], success=f"User {username} has been successfully added."))

    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed: users.email" in str(e):
            error_message = "The email is already in use. Please choose another one."
        else:
            error_message = "An error occurred while adding the user."
        #return render_template('admin.html', error=error_message)
        #return redirect(url_for('admin', error=error_message))
        return redirect(url_for('admin.admin', username=session['username'], error=error_message))

    except Exception as e:
        #return render_template('admin.html', error=f"Unexpected error: {str(e)}")
        return redirect(url_for('admin.admin', username=session['username'], error=f"Unexpected error: {str(e)}"))


