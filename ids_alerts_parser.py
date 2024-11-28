import re

class LogParserIdsAlert:
    
    file_path = "./logs/ids_alerts.log"
    raw_logs = []  

    @classmethod
    def load_logs(cls, last_n=5):
        try:
            with open(cls.file_path, 'r', encoding='utf-8') as file:
                cls.raw_logs = file.readlines()[-last_n:]
        except FileNotFoundError as e:
            print(f"Error: {e}")
            cls.raw_logs = []
            
    @classmethod
    def parse_logs(cls):
        if not cls.raw_logs:
            print("No logs found")
            return []

        log_pattern = r"\{'description': '(.*?)', 'severity': '(.*?)', 'event': '.*?'\}"
        parsed_logs = []

        for line in cls.raw_logs:
            match = re.search(log_pattern, line)
            if match:
                description, severity = match.groups()
                parsed_logs.append({"description": description, "severity": severity})

        return parsed_logs


    @classmethod
    def load_last_alerts(cls, last_n=6):
        cls.load_logs(last_n=last_n) 
        return cls.parse_logs()  