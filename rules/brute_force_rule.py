    
import time 


MAX_ATTEMPTS = 5
TIME_WINDOW = 600  # 10 min 
failed_attempts = {}
from managers.mail_manager import EmailManager

mail = EmailManager()


def log_failed_attempt(username):
    if username not in failed_attempts:
        failed_attempts[username] = []
    failed_attempts[username].append(time.time())
    

def check_brute_force(username):
    current_time = time.time()
    #print("in")
    if username in failed_attempts:
        attempts = failed_attempts[username]
        attempts = [timestamp for timestamp in attempts if current_time - timestamp < TIME_WINDOW]

        failed_attempts[username] = attempts
        #print(failed_attempts)
        if len(attempts) >= MAX_ATTEMPTS:
            #print("in")
            mail.send_email_alerte_admin(username)  # send an alert 
            logging.warning(f"ATTENTION: Multiple failed login attempts for {username}")
            return True
    return False
    
