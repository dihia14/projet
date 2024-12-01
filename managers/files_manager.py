


## reading, ... files 

# décorateur @classmethod +  inclure cls comme premier argument de toutes 
# les méthodes marquées avec @classmethod. 

## TODO : RENOMMER PLUTOT EN DATA 

class FileManager : 
    
    @classmethod
    def read_last_ip(cls):
        try:
            with open("./last_ip.txt", "r") as f:
                return f.read().strip()  
        except FileNotFoundError:
            return "Error"

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
            
    
        
    