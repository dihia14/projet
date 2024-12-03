import re
from urllib.parse import unquote


## The QueryDetector class is used to analyse and detect whether a query contains malicious pattern. 

class QueryDetector:
    """rules : Set of patterns used to detect sql injection. For the moment, same as for IDS. 
    """
    rules = [
        {"pattern": "UNION|SELECT|DROP|' OR '|'%20OR%20'| '1' = '1'", "description": "SQL Injection"},
        {"pattern": "\.\./\.\./", "description": "Directory Traversal"},
        {"pattern": "sqlmap|nikto", "description": "Automated Scan"}
    ]
    

    """Returns if the received query is malicious or not. 
    
    Args :
        query (str): The query to analyse. 

    Returns:
        bool: True, if malicious, False otherwise. 
    """
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
