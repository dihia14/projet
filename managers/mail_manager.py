import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


### 
def is_valid_email(email):
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    return re.match(pattern, email) is not None
 
 
### server parama - global variables ### 
smtp_server="smtp.gmail.com"
port=587 
sender_email="jafjafnora@gmail.com"
sender_password="luzz vnkb izzm lpps" #### clé d'app gmail 

    
    
def send_confirmation_mail_user(username, email, password) : 
    recipient_email=email
    subject="Your account has been created !"
    body=f"The system administrator has added you to the database. Here, your login information : \n*Your username is : {username} \n*Your password is :{password} \n The link to connect : https://accurate-actively-fox.ngrok-free.app "  ### TODO : switch to html format later 
    send_email_zimbra(smtp_server, port, sender_email, sender_password, recipient_email, subject, body)       

    
def send_email_alerte_admin(username): 
    subject="Alerte de tentative de brute force"
    body = f"Une série de tentatives de connexion échouées a été détectée pour l'utilisateur {username}. Veuillez vérifier."
    send_email_zimbra(smtp_server, port, sender_email, sender_password, sender_email, subject, body)
    



#changer zimbra 
def send_email_zimbra(smtp_server, port, sender_email, sender_password, recipient_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))  # add the body 
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  
        server.login(sender_email, sender_password)
        server.send_message(msg)
        print("e-mail envoyé avec succès.")  # TODO : add to logg 
        server.quit()

    except Exception as e:
        print(f"e-mail error {e}") # TODO : add to logg 
        
        
        
