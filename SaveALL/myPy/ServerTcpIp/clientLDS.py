#//////Client///////
# Programmeur: Phung Arthur
# nom du projet: client.py
# Raspberry à utiliser: Client

#importation des librairies


import socket
import os
import time

# adresse IP du serveur et port de communication
hote = "192.168.185.93"
port = 12800

#Tentative de connexion au serveur
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))
#init des variables locales
memoire = 0 # mémoire de l'état de la barrière optique
Msg = "New"
Msg = Msg.encode()
conn.send(Msg)
time.sleep(10)
Msg = "Next"
Msg = Msg.encode()       
# si le bouton start = 0 envoie du message fin qui coupe la connexion
# du serveur et du client
Msg = "Off"
Msg = Msg.encode()
conn.send(Msg)
print("close")
print("Fermeture de la connexion")
conn.close()
