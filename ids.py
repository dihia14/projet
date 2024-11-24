from  modules.log_http import LogHTTP
import threading

if __name__ == "__main__":
    # Fichiers de configuration
    LOG_FILE = "/home/dihia/Desktop/test/file.log"
    LOG_RULES = "rules/log_rules.json"
    NETWORK_RULES = "rules/network_rules.json"

    log_http = LogHTTP(LOG_FILE, LOG_RULES)
   

    threading.Thread(target=log_http.start_monitoring).start()

