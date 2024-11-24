import pyinotify
from modules.rule_engine import RuleEngine

class LogHTTP:
    def __init__(self, log_file, rule_file):
        self.log_file = log_file
        self.rule_engine = RuleEngine(rule_file)

    def analyze_line(self, line):
        #print(f"Analyse de la ligne : {line}")  
        alerts = self.rule_engine.match_rules(line)
        for alert in alerts:
            print(f"[ALERT] {alert['description']} - Gravité : {alert['severity']}")
            self.log_alert(alert)


    def log_alert(self, alert):
        with open("logs/ids_alerts.log", "a") as f:
            f.write(f"{alert}\n")

    def start_monitoring(self):
        # """Démarrage de la surveillance des logs avec Pyinotify."""
        print(f"Démarrage de la surveillance des logs : {self.log_file}")
        wm = pyinotify.WatchManager()
        handler = self.LogHandler(self)
        notifier = pyinotify.Notifier(wm, handler)
        wm.add_watch(self.log_file, pyinotify.IN_MODIFY)
        notifier.loop()



#lire le fichier file.log
    class LogHandler(pyinotify.ProcessEvent):

        def __init__(self, monitor):
            self.monitor = monitor
            self.last_position = 0  # Position initiale dans le fichier

        def process_IN_MODIFY(self, event):
           
           # print(f"[DEBUG] Modification détectée dans le fichier : {event.pathname}")

            if event.pathname == self.monitor.log_file:
                with open(self.monitor.log_file, "r") as f:
                    f.seek(self.last_position)  
                    lines = f.readlines()  # Lis toutes les nouvelles lignes
                    self.last_position = f.tell()  # Met à jour la position pour la prochaine lecture
                    
                    for line in lines:
                        line = line.strip()
                        if line:
                            self.monitor.analyze_line(line)


