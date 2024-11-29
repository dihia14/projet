### mettre tout ce qui est write last_ip, authorize , .... ?? 


def write_last_ip(client_ip):
    with open("last_ip.txt", "w") as f:
        f.write(f"{client_ip}\n")


def authorize(client_ip): 
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

