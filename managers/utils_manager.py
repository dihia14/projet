


## reading, ... files 

# décorateur @classmethod +  inclure cls comme premier argument de toutes 
# les méthodes marquées avec @classmethod. 

## TODO : RENOMMER PLUTOT EN DATA ou utils 

class UtilsManager : 
    
    """Just read the last ip from a file. 

    Returns:
        str: The last IP. ## dans le rapport : expliquer comment on a fait => mais se pose la question de si plusieur connexions multiples ont lieux. 
    """
    @classmethod
    def read_last_ip(cls):
        try:
            with open("./last_ip.txt", "r") as f:
                return f.read().strip()  
        except FileNotFoundError:
            return "Error"

        """Blacklist an IP by saving it a dedicated file. 
        """
    @classmethod
    def black_list_ip(cls,client_ip):
        with open("./black_list.txt", "a") as f:
            f.write(f"{client_ip}\n")
            f.flush()
            
            
    @classmethod
    def get_last_logs(cls):
        with open('./logs/app.log', 'r') as f:
                logs = f.readlines()
            
        recent_logs = logs[-20:] 
        return recent_logs
    
    
        
    @classmethod   
    def write_last_ip(cls, client_ip):
        with open("last_ip.txt", "w") as f:
            f.write(f"{client_ip}\n")

    @classmethod
    def authorize(cls, client_ip): 
        try:
            with open("black_list.txt", "r") as f:
                lst_ip = f.read().strip().splitlines() # retrieve the black ips 
            
            if client_ip in lst_ip:
                return False  # not authorized access 
            else:
                return True  # authorized access 
        
        except FileNotFoundError:
            print("Error.")
            return True
            
            
        
    
        
    