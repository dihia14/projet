# # from watchdog.observers import Observer
# # from watchdog.events import FileSystemEventHandler
# # import time
# # import os

# # from modules.rule_engine import RuleEngine


# # class LogHTTP:
# #     def __init__(self, log_file, rule_file):
# #         self.log_file = log_file
# #         self.rule_engine = RuleEngine(rule_file)

# #     def analyze_line(self, line):
# #         alerts = self.rule_engine.match_rules(line)
# #         for alert in alerts:
# #             print(f"[ALERT] {alert['description']} - Gravité : {alert['severity']}")
# #             self.log_alert(alert)

# #     def log_alert(self, alert):
# #         with open("logs/ids_alerts.log", "a") as f:
# #             f.write(f"{alert}\n")

# #     def start_monitoring(self):
# #         print(f"Démarrage de la surveillance des logs : {self.log_file}")
# #         handler = self.LogHandler(self)
# #         observer = Observer()
# #         observer.schedule(handler, path=os.path.dirname(self.log_file), recursive=False)
# #         observer.start()
# #         try:
# #             while True:
# #                 print("Surveillance en cours...")
# #                 time.sleep(1)
# #         except KeyboardInterrupt:
# #             observer.stop()
# #         observer.join()

# #     class LogHandler(FileSystemEventHandler):
# #         def __init__(self, monitor):
# #             self.monitor = monitor
# #             self.last_position = os.path.getsize(monitor.log_file)  # Initialise à la fin du fichier

# #         def on_modified(self, event):
# #             print("[DEBUG] Modification détectée")
# #             if event.src_path == self.monitor.log_file:
# #                 print(f"[DEBUG] Modification du fichier cible : {self.monitor.log_file}")
# #                 time.sleep(0.1) 
# #                 current_size = os.path.getsize(self.monitor.log_file)
                
# #                 # Si le fichier a rétréci, réinitialisez la position
# #                 if current_size < self.last_position:
# #                     print("[DEBUG] Fichier tronqué, réinitialisation de la position")
# #                     self.last_position = 0
                
# #                 # Lisez les nouvelles lignes
# #                 with open(self.monitor.log_file, "r") as f:
# #                     f.seek(self.last_position)
# #                     new_lines = f.readlines()
# #                     self.last_position = f.tell()  # Mettez à jour l'offset
# #                     print(f"[DEBUG] Nouvelles lignes détectées : {new_lines}")
# #                     for line in new_lines:
# #                         line = line.strip()
# #                         if line:
# #                             print(f"[DEBUG] Ligne analysée : {line}")
# #                             self.monitor.analyze_line(line)





# # from fsevents import Observer, Stream
# # import os
# # import time
# # from modules.rule_engine import RuleEngine


# # class LogHTTP:
# #     def __init__(self, log_file, rule_file):
# #         self.log_file = log_file
# #         self.rule_engine = RuleEngine(rule_file)
# #         self.last_position = os.path.getsize(log_file) 

# #     def analyze_line(self, line):
# #         alerts = self.rule_engine.match_rules(line)
# #         for alert in alerts:
# #             print(f"[ALERT] {alert['description']} - Gravité : {alert['severity']}")
# #             self.log_alert(alert)

# #     def log_alert(self, alert):
# #         with open("logs/ids_alerts.log", "a") as f:
# #             f.write(f"{alert}\n")

# #     def process_log(self):
# #         """Lit les nouvelles lignes ajoutées au fichier log."""
# #         with open(self.log_file, "r") as f:
# #             f.seek(self.last_position)
# #             new_lines = f.readlines()
# #             self.last_position = f.tell()
# #             for line in new_lines:
# #                 line = line.strip()
# #                 if line:
# #                     print(f"[DEBUG] Ligne analysée : {line}")
# #                     self.analyze_line(line)

# #     def start_monitoring(self):
# #         def callback(event):
# #             if event.name == self.log_file and event.mask & 0x00000002:  
# #                 print(f"[DEBUG] Modification détectée dans {event.name}")
# #                 self.process_log()

# #         print(f"Démarrage de la surveillance des logs : {self.log_file}")
# #         observer = Observer()
# #         stream = Stream(callback, os.path.dirname(self.log_file), file_events=True)
# #         observer.schedule(stream)
# #         observer.start()

# #         try:
# #             while True:
# #                 print("Surveillance en cours...")
# #                 time.sleep(1)
# #         except KeyboardInterrupt:
# #             print("Arrêt de la surveillance.")
# #             observer.stop()
# #         observer.join()





# from fsevents import Observer, Stream
# import os
# import time
# from modules.rule_engine import RuleEngine


# class LogHTTP:
#     def __init__(self, log_file, rule_file):
#         self.log_file = log_file
#         self.rule_engine = RuleEngine(rule_file)
#         self.last_position = os.path.getsize(log_file)  # Initialise la position de lecture

#     def analyze_line(self, line):
#         alerts = self.rule_engine.match_rules(line)
#         for alert in alerts:
#             print(f"[ALERT] {alert['description']} - Gravité : {alert['severity']}")
#             self.log_alert(alert)

#     def log_alert(self, alert):
#         with open("logs/ids_alerts.log", "a") as f:
#             f.write(f"{alert}\n")

#     def process_log(self):
#         """Lit les nouvelles lignes ajoutées au fichier log."""
#         with open(self.log_file, "r") as f:
#             f.seek(self.last_position)
#             new_lines = f.readlines()
#             self.last_position = f.tell()
#             for line in new_lines:
#                 line = line.strip()
#                 if line:
#                     print(f"[DEBUG] Ligne analysée : {line}")
#                     self.analyze_line(line)

#     # def start_monitoring(self):
#     #     def callback(event):
#     #         if event.name == self.log_file and event.mask & 0x00000002:  # check si le fichier est modifié
#     #             print(f"[DEBUG] Modification détectée dans {event.name}")
#     #             self.process_log()

#     #     print(f"Démarrage de la surveillance des logs : {self.log_file}")
#     #     observer = Observer()
#     #     stream = Stream(callback, os.path.dirname(self.log_file), file_events=True)
#     #     observer.schedule(stream)
#     #     observer.start()

#     #     try:
#     #         while True:
#     #             print("Surveillance en cours...")
#     #             time.sleep(1)
#     #     except KeyboardInterrupt:
#     #         print("Arrêt de la surveillance.")
#     #         observer.stop()
#     #     observer.join()
    
   


# last test 

from fsevents import Observer, Stream
import os
import time
from modules.rule_engine import RuleEngine
from managers.mail_manager import send_email_alerte_injection_sql

class LogHTTP:
    def __init__(self, log_file, rule_file):
        self.log_file = log_file
        self.rule_engine = RuleEngine(rule_file)
        self.last_position = os.path.getsize(log_file)  # Initialise à la fin du fichier

    def analyze_line(self, line):
        alerts = self.rule_engine.match_rules(line)
        for alert in alerts:
            print(f"[ALERT] {alert['description']} - Gravité : {alert['severity']}")
            send_email_alerte_injection_sql()
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

