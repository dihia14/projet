

import json
import requests
import folium

class IPManager:
    def __init__(self, storage_file='data/ips.json'):
        """
        Initialize the IPManager class.

        Args:
            storage_file (str): Path to the JSON file for storing IP data.
        """
        self.storage_file = storage_file

    def get_ip_location(self, ip):
        """
        Retrieve location data for an IP address using an API.

        Args:
            ip (str): The IP address to locate.

        Returns:
            tuple: (latitude, longitude, country, city) if successful, otherwise None.
        """
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url)
        data = response.json()

        if data.get("status") == "fail":
            return None

        return data["lat"], data["lon"], data["country"], data["city"]

    def load_ip_data(self):
        """
        Load IP data from the storage file.

        Returns:
            dict: A dictionary containing IP location data.
        """
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_ip_data(self, data):
        """
        Save IP data to the storage file.

        Args:
            data (dict): The IP data to save.
        """
        with open(self.storage_file, 'w') as f:
            json.dump(data, f, indent=4)

    def generate_map(self, ip_data):
        """
        Generate an interactive map with markers for each IP address.

        Args:
            ip_data (dict): A dictionary containing IP location data.

        Returns:
            str: The HTML representation of the generated map.
        """
        my_map = folium.Map(location=[20, 0], zoom_start=2)

        # place a marker for each IP
        for ip, data in ip_data.items():
            lat = data['lat']
            lon = data['lon']
            city = data['city']  # recheck 
            folium.Marker([lat, lon], popup=f"{city}").add_to(my_map)

        return my_map._repr_html_()  # retrieve the HTML code for the map
