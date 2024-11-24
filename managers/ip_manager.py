
import json
import requests
import folium



IP_STORAGE_FILE = 'data/ips.json'

# récupère les données via l'api 
def get_ip_location(ip):

    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "fail":
        return None
    return data["lat"], data["lon"], data["country"], data["city"]


def load_ip_data():
    try:
        with open(IP_STORAGE_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        #print(f"error json : {e}")
        return {}

def save_ip_data(data):
    with open(IP_STORAGE_FILE, 'w') as f:
        json.dump(data, f, indent=4)
        
    
        
def generate_map(ip_data):
    my_map = folium.Map(location=[20, 0], zoom_start=2)
    
    # place un pic pour chaque IP
    for ip, data in ip_data.items():
        lat = data['lat']
        lon = data['lon']
        # country = data['country']
        # folium.Marker([lat, lon], popup=f"{country}").add_to(my_map)
        city = data['city']
        folium.Marker([lat, lon], popup=f"{city}").add_to(my_map)
        
    map_html = my_map._repr_html_()  #retrieve le code HTML de la carte
    return map_html