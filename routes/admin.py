from flask import Blueprint, request, session, redirect, url_for, render_template
import bcrypt
import logging
import sqlite3
from managers.database_manager import UserDatabase
from managers.filePage_manager import list_files
from managers.password_manager import PasswordManager
from managers.utils_manager import UtilsManager
from managers.ip_manager import IPManager
from managers.mail_manager import EmailManager
from ids_alerts_parser import LogParserIdsAlert
from init_app import db_manager, mail_manager, ip_manager  # managers initiaux

admin_blueprint = Blueprint("admin", __name__, url_prefix="/admin")

@admin_blueprint.route("/<username>")
def admin(username):
    """
    Dashboard principal pour l'administrateur.
    """

    if 'username' not in session or not session.get('is_admin', False):
        return redirect(url_for('index.index', loging_msg="Unauthorized access"))

    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    logging.info(f"Admin page accessed by {session['username']} from {client_ip}")

    user_info = db_manager.get_user_infos(username)

    # logs et alertes
    #recent_logs = FileManager.get_last_logs()
    recent_logs = UtilsManager.get_last_logs()
    ids_alerts = LogParserIdsAlert.load_last_alerts(last_n=6)

    ip_data = ip_manager.load_ip_data()
    if client_ip not in ip_data:
        location = ip_manager.get_ip_location(client_ip)
        if location:
            lat, lon, country, city = location
            ip_data[client_ip] = {
                'lat': lat,
                'lon': lon,
                'country': country,
                'city': city
            }
            ip_manager.save_ip_data(ip_data)

    map_html = ip_manager.generate_map(ip_data)

    success_message = request.args.get('success')
    error_message = request.args.get('error')

    return render_template(
        'admin.html',
        logs=recent_logs,
        ids_alerts=ids_alerts,
        map_html=map_html,
        success_message=success_message,
        error_message=error_message,
        user_info=user_info
    )

@admin_blueprint.route("/file_page/<username>")
def admin_file_page(username):
    """
    Redirection vers la gestion des fichiers.
    """
    return redirect(url_for("file.file_page", username=username))

@admin_blueprint.route("/admin_users_manager")
def gestion_users():
    """
    Liste et gestion des utilisateurs.
    """
    users = db_manager.get_users()
    return render_template('admin_users_manager.html', users=users)

@admin_blueprint.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    """
    Supprime un utilisateur.
    """
    db_manager.delete_user(user_id)
    return redirect(url_for("admin.gestion_users"))

@admin_blueprint.route("/add_user", methods=["POST"])
def add_user_route():
    """
    Ajoute un utilisateur à la base de données.
    """
    username = request.form.get('username')
    email = request.form.get('email')
    password = PasswordManager.generate_password()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        db_manager.add_user(username, hashed_password, email, is_admin=False)
        mail_manager.send_confirmation_mail_user(username, email, password, True)
        return redirect(url_for('admin.admin', username=session['username'], success=f"User {username} has been successfully added."))
    except sqlite3.IntegrityError as e:
        error_message = "The email is already in use. Please choose another one." if "UNIQUE constraint failed" in str(e) else "An error occurred while adding the user."
        return redirect(url_for('admin.admin', username=session['username'], error=error_message))
    except Exception as e:
        return redirect(url_for('admin.admin', username=session['username'], error=f"Unexpected error: {str(e)}"))
