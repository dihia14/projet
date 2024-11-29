import os
from werkzeug.utils import secure_filename

# Dossier pour stocker les fichiers
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Fonction pour obtenir le dossier d'un utilisateur
def get_user_folder(user_id):
    user_id_str = str(user_id)
    user_folder = os.path.join(UPLOAD_FOLDER, user_id_str)
    os.makedirs(user_folder, exist_ok=True)  # Crée le dossier si n'existe pas
    return user_folder


def upload_file(request, user_id):
    if 'files' not in request.files:
        return {"error": "No files part"}, 400

    files = request.files.getlist('files')


    
    print("INNN get user foleder ", user_id)

    if not user_id:
        return {"error": "User name is missing"}, 400

    user_folder = get_user_folder(user_id)

    uploaded_files = []
    for file in files:
        if file.filename:
            filename = secure_filename(file.filename)  # Sécuriser le nom du fichier
            file_path = os.path.join(user_folder, filename)
            file.save(file_path)
            uploaded_files.append(filename)

    return {"message": "Files uploaded successfully", "files": uploaded_files}, 200

# Fonction pour lister les fichiers d'un utilisateur
def list_files(user_id):
    user_folder = get_user_folder(user_id)
    return os.listdir(user_folder)  # Renvoie la liste des fichiers dans le dossier de l'utilisateur


def delete_file(user_id, file_name):
    user_folder = get_user_folder(user_id)
    file_path = os.path.join(user_folder, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": "File deleted successfully"}, 200
    else:
        return {"error": "File not found"}, 404
