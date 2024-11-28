import random
import string

class PasswordManager:
  
    @classmethod
    def generate_password(cls, length=13):
        """
        Generate a random password. Default length = 13 

        Args:
            length (int): The length of the password. 

        Returns:
            str: The generated password. 
        """
        # au moins une occurrence de chaque catégorie
        uppercase = random.choice(string.ascii_uppercase)
        lowercase = random.choice(string.ascii_lowercase)
        digit = random.choice(string.digits)
        special = random.choice(string.punctuation)

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
