from flask import Blueprint, request, session, redirect, url_for, render_template, abort
import logging
import bcrypt
from managers.database_manager import UserDatabase
from managers.password_manager import PasswordManager
from managers.mail_manager import EmailManager
from managers.utils_manager import UtilsManager
from managers.query_manager import QueryDetector
from rules.brute_force_rule import check_brute_force, log_failed_attempt
from init_app import db_manager, mail_manager, ip_manager  # Managers initiaux (ajouter le query detector , ... )
import pyotp
from urllib.parse import unquote




index_blueprint = Blueprint("index", __name__)
#print("test", db_manager.get_user('admin'))


@index_blueprint.route("/")
def index():
    """
    Page d'accueil du site.
    """
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    logging.info(f"Home page loaded from {client_ip}")

    query_string = request.query_string.decode("utf-8")
    print(f"Query String Received: {query_string} ")

    if QueryDetector.is_malicious(query_string) : 
        return render_template("errors/forbidden.html")
 
    print(f"Current session: {dict(session)}")

    #UtilsManager.write_last_ip(client_ip) ## pas besoin ici page d'accueil !! => plutot dans login 

# it works , ... 
    # if not UtilsManager.authorize(client_ip):
    #     #return "Access unauthorized"
    #     return render_template("errors/unauthorized.html")

    

    loging_msg = request.args.get("loging_msg", "")
    return render_template("index.html", loging_msg=loging_msg) , 302




@index_blueprint.route("/login", methods=["POST"])
def login():
    """
    Authentification de l'utilisateur.
    """
    
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    logging.info(f"Home page loaded from {client_ip}")
    
    
    print("TEST ")
    username = request.form.get("username")
    password = request.form.get("password")
    print(f"Received username: {username}, password: {password}")

    query_string = request.query_string.decode("utf-8")

    if QueryDetector.is_malicious(query_string) :         
        return render_template("errors/forbidden.html") ### si une query malveillante a été detecté , bloque l'acces direct + envoie du mail via l'IDS 

    UtilsManager.write_last_ip(client_ip) 

    # if not UtilsManager.authorize(client_ip):
    #     return render_template("errors/unauthorized.html"), 403 # forbidden


    
    
    loging_msg = ""
    username = request.form.get("username")
    password = request.form.get("password")

    logging.info(f"Login attempt for user: {username}")
    if check_brute_force(username):
        logging.error(f"Too many failed attempts for {username}. Please try again later.")
        loging_msg = "Too many failed attempts. Please try again later."
        return redirect(url_for("index.index", loging_msg=loging_msg)), 429  # too Many Requests


    user = db_manager.get_user(username)

    if user:
        hashed_password = user[2]
        is_admin = user[4]
        if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
            
            # double authentification
            otp_secret = pyotp.random_base32()
            otp = pyotp.TOTP(otp_secret)
            session['otp_secret'] = otp_secret




            # Initialisation de la session utilisateur
            session["username"] = username
            session["is_admin"] = is_admin
            session["user_id"] = user[0]
            session.permanent = True
            
            
            # envoie du code à l'user 
            email = user[3]
            
            ### À DECOMMENTER POUR LA DOUBLE AUTHENTIFICATION 
            # otp_code = otp.now()
            # mail_manager.send_otp_mail(username, email, otp_code)

            # logging.info(f"OTP sent to user: {username}")
            # return render_template('otp_verification.html', username=username)



##### ÇA EST MIS DANS /verify_otp NORMALEMENT (MAIS POUR L'INSTANT GARDÉ CAR J'AI RETIRÉ LE DOUBLE AUTHENTIFICATION POUR LES TESTS )
            if is_admin:
                logging.info(f"Admin login successful for: {username}")
                return redirect(url_for("admin.admin", username=username)), 302 # redirection tmp 
            else:
                logging.info(f"User login successful for: {username}")
                return redirect(url_for("user.user_settings_page", username=username)), 302
        else:
            logging.error(f"Invalid password for user: {username}")
            loging_msg = f"Invalid password for: {username}"
            log_failed_attempt(username)
            return redirect(url_for("index.index", loging_msg=loging_msg)), 401  # unauthorized
    else:
        logging.warning(f"Attempt to connect with a user not found: {username}")
        loging_msg = f"Attempt to connect with a user not found: {username}"
        return redirect(url_for("index.index", loging_msg=loging_msg)), 404 # not found 





@index_blueprint.route("/logout")
def logout():
    """
    Déconnexion de l'utilisateur.
    """
    session.clear()
    logging.info("User successfully logged out")
    return render_template("index.html")



@index_blueprint.route("/reset_password", methods=["POST"])
def reset_password():
    """
    Réinitialisation du mot de passe de l'utilisateur.
    """
    username = request.form.get("username")
    email = request.form.get("email")

    
    user = db_manager.get_user(username)

    if not user or user[3] != email:  
        loging_msg = "Erreur : Utilisateur ou email non trouvé."
        return redirect(url_for("index.index", loging_msg=loging_msg)), 401

    # Générer un nouveau mot de passe et le hacher
    new_password = PasswordManager.generate_password()
    hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())

    # Mettre à jour le mot de passe dans la base de données
    db_manager.update_password_username(username, hashed_password)

    # Envoyer l'email avec le nouveau mot de passe
    mail_manager.send_confirmation_mail_user(username, email, new_password, False)

    # Rediriger vers l'index avec un message de confirmation
    loging_msg = "Un email avec votre nouveau mot de passe a été envoyé."
    return redirect(url_for("index.index", loging_msg=loging_msg)), 302 




###otp verification 
@index_blueprint.route("/verify_otp", methods=["POST"])
def verify_otp():
    
    otp_code = request.form.get('otp')
    otp_secret = session.get('otp_secret')
    username = session.get('username')

    print("test" , otp_secret, "and admin ", username)
    if not otp_secret or not username:
        return redirect(url_for('index.index', loging_msg="Session expired. Please log in again."))

    otp = pyotp.TOTP(otp_secret)

    if otp.verify(otp_code, valid_window=1): 
        logging.info(f"OTP verification successful for user: {username}")
        if session.get('is_admin'):
            return redirect(url_for('admin.admin', username=username, error=error_message))

        else:
            return redirect(url_for('user.user_settings_page', username=username))
    else:
        logging.warning(f"Invalid OTP entered for user: {username}")
        return render_template('otp_verification.html', username=username, error="Invalid OTP. Please try again.")

 
