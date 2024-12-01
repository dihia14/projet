import os
import paramiko
from werkzeug.utils import secure_filename

# Dossier pour stocker les fichiers
UPLOAD_FOLDER = '../uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Fonction pour obtenir le dossier d'un utilisateur
def get_user_folder(user_id):
    user_id_str = str(user_id)
    user_folder = os.path.join(UPLOAD_FOLDER, user_id_str)
    os.makedirs(user_folder, exist_ok=True)  # Crée le dossier si n'existe pas
    return user_folder

#+++++++++++++++++++++++++ Fonction pour se connecter au serveur SFTP  +++++++++++++++++++++++++++++++++++

def connect_sftp():
    hostname = "192.168.1.17"  
    username = "admin" 
    private_key_path = "/home/dihia/.ssh/id_rsa_new"  

    try:
       
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
        
        # creation d'une connexion sftp
        transport = paramiko.Transport((hostname, 22))
        transport.connect(username=username, pkey=private_key)
        sftp = paramiko.SFTPClient.from_transport(transport)
        print("Connexion sftp reussie ")
        return sftp
    except paramiko.AuthenticationException:
        print("Échec de l'authentification ")
    except Exception as e:
        print(f"Erreur lors de la connexion ... : {e}")
    return None

#+++++++++++++++++++++++++++++++++++++++ Uploads section local + SFTP +++++++++++++++++++++++++++++++++++++++++++++++++++

def upload_file(request, user_id, sftp):
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

            #
            # Upload sur le serveur SFTP
            if sftp:
                user_folder = f'/uploads/{user_id}'
                try:
                    
                    try:
                        sftp.stat(user_folder)
                    except FileNotFoundError: 
                        sftp.mkdir(user_folder) # le creer si il existe pas !
                    
                    file_path = os.path.join(user_folder, filename)
                    sftp.put(file_path, file_path)  # Upload sur SFTP
                    print(f"Fichier uploadé sur SFTP : {file_path}")
                except Exception as e:
                    print(f"Erreur SFTP pour {filename}: {e}")

    return {"message": "Files uploaded successfully", "files": uploaded_files}, 200

# Fonction pour lister les fichiers d'un utilisateur
def list_files(user_id):
    user_folder = get_user_folder(user_id)
    files =  os.listdir(user_folder)  # Renvoie la liste des fichiers dans le dossier de l'utilisateur

    # if sftp:   //  a Voir !!
    #     user_folder = f'/uploads/{user_id}'

    return files 


# ++++++++++++++++++++++++++++++++++++++++++Delete files local + SFTP ++++++++++++++++++++++++++++++++++++++++++++++++++

def delete_file(user_id, file_name, sftp=None):
    local_user_folder = get_user_folder(user_id)
    local_file_path = os.path.join(local_user_folder, file_name)

    if os.path.exists(local_file_path):
        os.remove(local_file_path)

        if sftp:
                user_folder = f'/uploads/{user_id}'
                file_path = os.path.join(user_folder, file_name)
                try:
                    sftp.remove(file_path)  # Supprimer le fichier distant
                    print(f"Fichier supprimé de SFTP : {file_path}")
                except Exception as e:
                    print(f"Erreur lors de la suppression du fichier distant : {e}")


        return {"message": "File deleted successfully"}, 200
    else:
        return {"error": "File not found"}, 404
