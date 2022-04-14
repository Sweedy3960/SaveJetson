import socket   # Utilisation d'un code externe / import uine libraire 
"""
import enum
from enum import Enum
"""
client = None   # Création de la variable vide pour l'instant type vide = cree zone mem vide
serv = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # Création de l'objet serveur
data = None
serv.bind(("192.168.0.30",6789))    # Choisi le nom du host et le numéro du port 
serv.listen(1)  # Passe en mode "réception" ou 
data =b'' # Définit le type de la variable   

while data != b"fin":
  
    if not client : # Si personne n'est connecté
        print("pas de client") 
        client,adr = serv.accept()  # Attend qu'un client demande la connexion et stocke l'adresse
        print("client connected ",adr)
    else:
        try:
            data = client.recv(1024)    # Reçoit la data par pack de 1024 bytes
        except:
            pass    # nop
    if not data: # Si on n'a pas de data, envoie la commande "répète"
        print("erreur") 
        reponse = "repeat" 
        reponseEncoded=reponse.encode() #encode le string
        print("envoi de :"+str(reponse))   
        client.send(reponseEncoded) # envoie le string encodé 
    else : 
        print("reception de :"+str(data))   #affiche le code reçu
        
        reponse = "5/5"
        reponseEncoded=reponse.encode()
        print("envoi de :"+str(reponse))   # affiche la data recue  
        n= client.send(reponseEncoded)     # Check le ACK et la taille
        if n != len(reponseEncoded):
            print("erreur")
        else:
            print("Envoi ok") 
  
reponse = "serveurclosed"
reponseEncoded=reponse.encode()
client.send(reponseEncoded)         # Envoie la commande pour fermer le serveur
print("envoi de :"+str(reponseEncoded))
client.close()  # Ferme le serveur
serv.close()