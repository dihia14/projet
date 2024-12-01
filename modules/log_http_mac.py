
from fsevents import Observer, Stream
import os
import time
from modules.rule_engine import RuleEngine
#from init_app import mail_manager  # car dans init_app c'est là que nos param du serveur port ... sont instanciés 
from managers.mail_manager import * 
from managers.utils_manager import UtilsManager

EmailManager.initialize(
    smtp_server="smtp.gmail.com",
    port=587,
    sender_email="jafjafnora@gmail.com",
    sender_password="luzz vnkb izzm lpps"
)
mail_manager = EmailManager


class LogHTTP:
    def __init__(self, log_file, rule_file):
        self.log_file = log_file
        self.rule_engine = RuleEngine(rule_file)
        self.last_position = os.path.getsize(log_file)  # Initialise à la fin du fichier

    def analyze_line(self, line): 
        
        alerts = self.rule_engine.match_rules(line)
        for alert in alerts:
            print(f"[ALERT] {alert['description']} - Gravité : {alert['severity']}")
            mail_manager.send_email_alerte_injection_sql()
            # black list l'email 
            #UtilsManager.black_list_ip(UtilsManager.read_last_ip())
            self.log_alert(alert)


    def log_alert(self, alert):
        with open("logs/ids_alerts.log", "a") as f:
            f.write(f"{alert}\n")

    def process_log(self):
        """Lit les nouvelles lignes ajoutées au fichier log."""
        try:
            with open(self.log_file, "r") as f:
                f.seek(self.last_position)
                new_lines = f.readlines()
                self.last_position = f.tell()  # update la position de lecture
                for line in new_lines:
                    line = line.strip()
                    if line:
                        print(f"[DEBUG] Ligne analysée : {line}")
                        self.analyze_line(line)
        except FileNotFoundError:
            print(f"[WARNING] Fichier introuvable : {self.log_file}")

    def start_monitoring(self):
        def callback(event):
            if event.name == self.log_file and event.mask & 0x00000002 :  # check si le fichier est modifié mask or kFSEventStreamEventFlagItemModified
                print(f"[DEBUG] Modification détectée dans {event.name}")
                self.process_log()

        print(f"Démarrage de la surveillance des logs : {self.log_file}")
        observer = Observer()
        stream = Stream(callback, os.path.dirname(self.log_file), file_events=True)
        observer.schedule(stream)
        observer.start()

        try:
            while True:
                self.periodic_check()  
                time.sleep(1)
        except KeyboardInterrupt:
            print("Arrêt de la surveillance.")
            observer.stop()
        observer.join()

    def periodic_check(self):
        """Vérifie périodiquement si de nouvelles lignes ont été ajoutées."""
        current_size = os.path.getsize(self.log_file)
        if current_size > self.last_position:
            print(f"[DEBUG] Vérification périodique : nouvelles lignes détectées.")
            self.process_log()

