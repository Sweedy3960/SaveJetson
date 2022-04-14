import socket
import cv2 as cv
run=True
ADRESSE = ''
PORT = 6789

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind((ADRESSE, PORT))
serveur.listen(1)
print("ecoute")
client, adresseClient = serveur.accept()
print ('Connexion de '), adresseClient
if cv.waitKey(1) & 0xFF == ord('q'):
   run=False
#donnees = client.recv(1024)
if run:
    reponse = "hello"
    print ('Envoi de :{}'.format(reponse)) 
    z=reponse.encode('utf8')
    n = client.send(z)
    if (n != len(reponse)):
        print('Erreur envoi.')
    else:
        print ('Envoi ok.')
else:

    print ('Fermeture de la connexion avec le client.')
    client.close()
    print ('Arret du serveur.')
    serveur.close()