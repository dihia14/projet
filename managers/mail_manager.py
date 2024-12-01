import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailManager:
    smtp_server = None
    port = None
    sender_email = None
    sender_password = None

    @classmethod
    def initialize(cls, smtp_server, port, sender_email, sender_password):
        """
        Initialize class-level attributes.

        Args:
            smtp_server (str): SMTP server address.
            port (int): SMTP port number.
            sender_email (str): Sender email address.
            sender_password (str): Sender email password or app key.
        """
        cls.smtp_server = smtp_server
        cls.port = port
        cls.sender_email = sender_email
        cls.sender_password = sender_password

    @classmethod
    def send_email(cls, recipient_email, subject, body):
        """
        Send an email.

        Args:
            recipient_email (str): The recipient's email address.
            subject (str): The subject of the email.
            body (str): The body of the email.

        Returns:
            None
        """
        print("DEEEEE" , cls.smtp_server)

        try:
            msg = MIMEMultipart()
            msg['From'] = cls.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(cls.smtp_server, cls.port)
            print("DEEEEE" , cls.smtp_server)
            server.starttls()
            server.login(cls.sender_email, cls.sender_password)
            server.send_message(msg)
            print(f"Email sent successfully to {recipient_email}.")
            server.quit()
            
   
    
        except Exception as e:
            print(f"Error sending email: {e}")




    @classmethod
    def send_otp_mail(cls, username, email, otp_code ):
        subject = "Your ont time code is here "
        body = (
            f"* One time code : {otp_code}\n"
            f"Login link: https://accurate-actively-fox.ngrok-free.app"
        )
        cls.send_email(email, subject, body)
        
        
        
        
    # is_new_password_generated = True : the initial generated password (i.e when the account is created)
    # false : when it's a new one asked 
    @classmethod
    def send_confirmation_mail_user(cls, username, email, password, is_new_password_generated ):
        """
        Send a confirmation email to a new user.

        Args:
            username (str): The username of the user.
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            None
        """
        if is_new_password_generated == True : 
            subject = "Your account has been created!"

            body = (
                f"The system administrator has added you to the database. Here is your login information:\n"
                f"* Username: {username}\n"
                f"* Password: {password}\n"
                f"Login link: https://accurate-actively-fox.ngrok-free.app"
            )
        else : 
            subject = "Here's your new password !"

            body = (
                f"\n"
                f"Hello  {username}\n"
                f"Here's your new password : \n"
                f"* Password: {password}\n"
                f"Login link: https://accurate-actively-fox.ngrok-free.app"
            )
                   

        cls.send_email(email, subject, body)

    @classmethod
    def send_email_alerte_admin(cls, username):
        """
        Send an alert email to the admin for brute force attempts.

        Args:
            username (str): The username of the account under attack.

        Returns:
            None
        """
        subject = "Brute Force Attempt Alert"
        body = f"A series of failed login attempts were detected for the user {username}. Please investigate."
        cls.send_email(cls.sender_email, subject, body)

    @classmethod
    def send_email_alerte_injection_sql(cls):
        """
        Send an alert email to the admin for a SQL injection attempt.

        Returns:
            None
        """
        subject = "SQL Injection Attempt Alert"
        body = "A SQL injection attempt has been detected. Please investigate immediately."
        cls.send_email(cls.sender_email, subject, body)
        
        
  
        
 