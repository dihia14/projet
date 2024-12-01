from flask import Blueprint, request, session, redirect, url_for, render_template, abort, send_from_directory
import os
from managers.filePage_manager import *
from managers.database_manager import UserDatabase
from init_app import db_manager, mail_manager, ip_manager  # Managers initiaux

# Initialisation du Blueprint
file_blueprint = Blueprint("file", __name__, url_prefix="/file")



@file_blueprint.route("/page/<username>")
def file_page(username):
    """
    Affiche la page de gestion des fichiers pour un utilisateur spécifique.
    """
    user_info = db_manager.get_user_infos(username)
    user_id = user_info[0]

    files = list_files(str(user_id))
    print(f"USER INFO: {user_id}, FILES: {files}")
    return render_template("file_page.html", files=files, user_id=str(user_id), user_info=user_info)



# ICIIIII
@file_blueprint.route("/page/upload", methods=["POST"])
def upload():
    """
    Upload un fichier pour l'utilisateur connecté.
    """
    user_id = session.get("user_id")

    if not user_id:
        abort(403, description="User not authenticated.")
   
    print("in UPLOAD ")

    # Connexion SFTP
    # sftp = connect_sftp()

    response, status_code = upload_file(request, user_id)
    if status_code == 200:
        username = session.get("username")
        user_info = db_manager.get_user_infos(username)

        #files = list_files(str(user_id), sftp)
        files = list_files(str(user_id))
        response["files"] = files

        # Fermer la connexion SFTP après l'upload
        # if sftp:
        #     sftp.close()

    return response, status_code


@file_blueprint.route("/delete", methods=["POST"])
def delete_file_route():
    """
    Supprime un fichier pour l'utilisateur connecté.
    """
    print("herre")
    sftp = connect_sftp()

    user_id = session.get("user_id")
    username = session.get("username")
    if not user_id or not username:
        abort(403, description="User not authenticated.")

    file_name = request.form.get("file_name")
    if not file_name:
        abort(400, description="File name is required.")

    delete_file(user_id, file_name, sftp=sftp)  #  AVOIR  !

    if sftp:
            sftp.close()

    return redirect(url_for("file.file_page", username=username))



@file_blueprint.route("/download/<user_id>/<filename>")
def download_file(user_id, filename):
    """
    Permet de télécharger un fichier spécifique pour un utilisateur.
    """
    user_folder = os.path.join("../uploads", user_id)
    file_path = os.path.join(user_folder, filename)
    print("in download ")
    if os.path.exists(file_path):
        return send_from_directory(user_folder, filename, as_attachment=True)
    else:
        abort(404, description="File not found")
