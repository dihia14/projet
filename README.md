# projet



### un message d'erreur du style RuntimeError: The session is unavailable because no secret key was set.  Set the secret_key on the application to something unique and secret. devrait apparaitre : 

### sur le meme terminale que python3 app.py est lancé : 
### lancer : export FLASK_SECRET_KEY='fa66975909197233d5647efdbb3006931e5f5452ec9385abb49dca1f7c7fee49'

### (clé générer aléatoirement, ... )

### puis app.secret_key = os.getenv('FLASK_SECRET_KEY') pour la récupérer depuis les variable d'environnement 