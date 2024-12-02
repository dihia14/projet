from locust import HttpUser, task, between

class LoadTest(HttpUser):

    #host = "https://accurate-actively-fox.ngrok-free.app"
    host = "http://localhost:9000"

    wait_time = between(1, 3)

    @task
    def home_page(self):
        # envoir de requête GET à la page d'accueil/index  "/"
        self.client.get("/")

    @task
    def login(self):
        # envoi de requete POST
        self.client.post("/login", data={"username": "admin", "password": "adminpassword"})
