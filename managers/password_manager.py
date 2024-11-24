import random
import string


def generate_password(length=13):

    # au moins une occ de chaque catégorie
    uppercase = random.choice(string.ascii_uppercase) 
    lowercase = random.choice(string.ascii_lowercase)  
    digit = random.choice(string.digits)              
    special = random.choice(string.punctuation)       
   
    # compléte avec des caractères aléatoires jusqu'à atteindre 13 ( ou plus ? 
    remaining_length = length - 4
    if remaining_length > 0:
        all_characters = string.ascii_letters + string.digits + string.punctuation
        remaining_characters = ''.join(random.choices(all_characters, k=remaining_length))
    else:
        remaining_characters = ''

    password_list = list(uppercase + lowercase + digit + special + remaining_characters)
    random.shuffle(password_list)  

    password = ''.join(password_list)
    return password
