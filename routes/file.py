from flask import Blueprint, request, session, redirect, url_for, render_template, abort
import os
from managers.filePage_manager import list_files, upload_file, delete_file
from managers.database_manager import UserDatabase
from flask import send_from_directory

file_blueprint = Blueprint("file", __name__)

db_manager = UserDatabase()



@file_blueprint.route("/file_page/<username>")
def file_page(username):
    """
    Affiche la page de gestion des fichiers pour un utilisateur spécifique.
    """
    user_info = db_manager.get_user_infos(username)
    user_id = user_info[0]
    files = list_files(str(user_id))
    print(f"USER INFO : {user_id} , FILES {files}")
    return render_template("file_page.html", files=files, user_id=str(user_id), user_info=user_info)

@file_blueprint.route("/upload", methods=["POST"])
def upload():
    """
    Upload un fichier pour l'utilisateur connecté.
    """
    user_id = session["user_id"]
    response, status_code = upload_file(request, user_id)
    if status_code == 200:
        username_ = session["username"]
        user_info = db_manager.get_user_infos(username_)
        user_id = user_info[0]
        files = list_files(str(user_id))
        response["files"] = files
    return response, status_code

@file_blueprint.route("/delete_file", methods=["POST"])
def delete_file_route():

    user_id = session["user_id"]
    username = session["username"]
    file_name = request.form.get("file_name")
    response, status_code = delete_file(user_id, file_name)
    return redirect(url_for("file.file_page", username=username))

@file_blueprint.route("/download/<user_id>/<filename>")
def download_file(user_id, filename):

    print("IN DOWNLOAD FILE")
    user_folder = os.path.join("uploads", user_id)
    file_path = os.path.join(user_folder, filename)

    if os.path.exists(file_path):
        return send_from_directory(user_folder, filename, as_attachment=True)
    else:
        abort(404, description="File not found")
