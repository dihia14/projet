import json
import re

#permet de matcher les regles pour trouver une correspondance 
class RuleEngine:
    def __init__(self, rule_file):
        self.rules = self.load_rules(rule_file)

    def load_rules(self, rule_file):
        """Charge les règles depuis un fichier JSON."""
        with open(rule_file, 'r') as f:
            rules = json.load(f)
            print(f"Règles chargées : {rules}")  
            return rules


    def match_rules(self, event):
        """Applique les règles sur un événement donné (ligne ou payload)."""
        alerts = []
        print(f"[DEBUG] Analyse de l'événement : {event}")
        for rule in self.rules:
            #print(f"[DEBUG] Vérification du pattern : {rule['pattern']}")
            if re.search(rule['pattern'], event, re.IGNORECASE):
                print(f"[DEBUG] Correspondance trouvée : {rule['description']}")
                alerts.append({
                    "description": rule['description'],
                    "severity": rule['severity'],
                    "event": event
                })
        return alerts
    

