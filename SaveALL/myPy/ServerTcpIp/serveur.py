
#importation des librairy
import socket
import select
#init du port de communication est ip
hote = ''
port = 12800
#tentative de connexion
try:
    connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_principale.bind((hote, port))
    connexion_principale.listen(5)
    print("Le serveur écoute à présent sur le port {}".format(port)) 
except:
    print("erreur: port déjà ouvert")

# Tant que le serveur ne reçoit pas le message de fin
serveur_lance = True
clients_connectes = []
ClientConn = 0
while serveur_lance:
    # On va vérifier que de nouveaux clients ne demandent pas à se connecter
    # Pour cela, on écoute la connexion_principale en lecture
    # On attend maximum 50ms
    connexions_demandees, wlist, xlist = select.select([connexion_principale],[],[],0.05)
    
    for connexion in connexions_demandees:
        try:
            connexion_avec_client, infos_connexion = connexion.accept()
        except:
            pass
        # On ajoute le socket connecté à la liste des clients
        clients_connectes.append(connexion_avec_client)
        
    # Maintenant, on écoute la liste des clients connectés
    # On attend là encore 50ms maximum
    # On enferme l'appel à select.select dans un bloc try
    
    memoire = 0
    clients_a_lire = []
    Clients_a_informer = []
    
    try:
        clients_a_lire, clients_a_informer, xlist = select.select(clients_connectes,clients_connectes, [], 0.01)
    except:
        pass
    else:
        # On parcout la liste des clients à lire
        for client in clients_a_lire:
            msg_recu = client.recv(1024)
            msg_recu = msg_recu.decode()
            if (msg_recu == "New") | (msg_recu == "Next") | (msg_recu == "Off"):
                #allume la troisième reçoit un message
                
                print("Reçu {}".format(msg_recu))
            
                # si le message fin est détecté
                if msg_recu == "Next":
                   print("esapce")
                else:
                    if msg_recu == "New":
                        ClientConn += 1
                    else:
                        if msg_recu == "Off":
                            ClientConn -= 1
                            if ClientConn == 0:
                                serveur_lance = False
          
    msg_recu = " "
                
# fin de connexion et remise à 0 des ports de sorties
print("Fermeture des connexions")
for client in clients_connectes:
    client.close()
connexion_principale.close()
