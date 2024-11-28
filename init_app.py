import logging
import os
import sys
from managers.mail_manager import EmailManager
from managers.ip_manager import IPManager
from managers.database_manager import UserDatabase

# Ajouter le répertoire parent pour accéder aux autres modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Gestionnaires globaux
db_manager = None
ip_manager = None
mail_manager = None

def configure_logging(log_file_path='./logs/app.log'):
    """
    Configure global logging settings.

    Args:
        log_file_path (str): Path to the log file.
    """
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)  # Créer le dossier si nécessaire

    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logging.getLogger().handlers[0].setStream(open(log_file_path, 'a', buffering=1))


def initialize_app():
    """
    Initialize global managers and configurations.
    """
    global db_manager, ip_manager, mail_manager

    # Configurer les logs
    configure_logging()

    # Initialiser les gestionnaires
    db_manager = UserDatabase()
    ip_manager = IPManager()

    # Initialiser les paramètres globaux pour EmailManager
    EmailManager.initialize(
        smtp_server="smtp.gmail.com",
        port=587,
        sender_email="jafjafnora@gmail.com",
        sender_password="luzz vnkb izzm lpps"
    )
    mail_manager = EmailManager

    logging.info("Application initialized successfully.")
