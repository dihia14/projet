#!/bin/bash


echo "lancement de l'ids"
python3 ids.py &


echo "lancement de l'application flask"
python3 app.py &


echo "lancement redirection sur le port 9000"
ngrok http --url=accurate-actively-fox.ngrok-free.app 9000 &
