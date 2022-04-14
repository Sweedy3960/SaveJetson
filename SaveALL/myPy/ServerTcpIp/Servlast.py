import socket
ADRESSE = ''
PORT = 6789

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind((ADRESSE, PORT))
serveur.listen(1)
print("ecoute")
client, adresseClient = serveur.accept()
print ('Connexion de '), adresseClient

donnees = client.recv(1024)

if not donnees:
    print( 'Erreur de reception.')  
else:
    u=donnees.decode()

    print('Reception de:' )+ u

    reponse = "helo"
    print ('Envoi de :') + reponse
    z=reponse.encode()
    n = client.send(z)
    if (n != len(reponse)):
        print('Erreur envoi.')
    else:
        print ('Envoi ok.')


print ('Fermeture de la connexion avec le client.')
client.close()
print ('Arret du serveur.')
serveur.close()