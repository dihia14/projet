import re
from urllib.parse import unquote


class QueryDetector:
    # same as IDS pour le moment 
    rules = [
        {"pattern": "UNION|SELECT|DROP|' OR '|'%20OR%20'| '1' = '1'", "description": "SQL Injection"},
        {"pattern": "\.\./\.\./", "description": "Directory Traversal"},
        {"pattern": "sqlmap|nikto", "description": "Automated Scan"}
    ]

    @classmethod
    def is_malicious(cls, query):
        """Analyse une query string et retourne True si elle est malveillante."""
        # first, decode 
        decoded_query = unquote(query)

        for rule in cls.rules:  
            if re.search(rule["pattern"], decoded_query , re.IGNORECASE):
                print(f"Malicious pattern found: {rule['description']}")
                return True
        return False
