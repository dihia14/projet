#from  modules.log_http import LogHTTP
from  modules.log_http_mac import LogHTTP    # mac 

import threading

if __name__ == "__main__":
    # Fichiers de configuration
    #LOG_FILE = "/home/dihia/Desktop/test/file.log"
    LOG_FILE = "/Users/jafjafnora/Desktop/NORA/projet/logs/app.log"

    LOG_RULES = "rules/log_rules.json"
   # NETWORK_RULES = "rules/network_rules.json"

    log_http = LogHTTP(LOG_FILE, LOG_RULES)
   
    log_http.start_monitoring()
    threading.Thread(target=log_http.start_monitoring).start()