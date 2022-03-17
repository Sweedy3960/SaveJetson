#///////Serveur///////
#Programe: Serveur.py
#Programmeur : Arthur Phung
# Date:02.12.2020

#importation des librairy
import RPi.GPIO as GPIO
import socket
import select
import os
import time
import pyautogui

#init des ports de sorties
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#indique que le programme a démarré
GPIO.output(3,GPIO.HIGH)
# attente du chargement du bureau
time.sleep(45)
GPIO.output(5,GPIO.HIGH)
#Démarrage du powerpoint
try:
	os.system("open /media/pi/*/*.odp")
	time.sleep(200)
	print("office run")
	pyautogui.press('F5')
except:
    	print("erreur 404: dossier pas trouver")

#Programmation de l'interruption d'éteignage
def my_callback():
   pyautogui.press('esc')
   time.sleep(3)
   pyautogui.hotkey('ctrl','s')
   time.sleep(20)
   pyautogui.hotkey('alt','F4')
   time.sleep(60)
   os.system("shutdown now -h") #éteind le système

GPIO.add_event_detect(37, GPIO.FALLING, callback=my_callback, bouncetime=300)

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
#si le serveur est connecté allume la deuxième led
GPIO.output(5,GPIO.HIGH)
  
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
                GPIO.output(7,GPIO.HIGH)
                print("Reçu {}".format(msg_recu))
            
                # si le message fin est détecté
                if msg_recu == "Next":
                   pyautogui.press('space')
                   print("esapce")
                else:
                    if msg_recu == "New":
                        ClientConn += 1
                    else:
                        if msg_recu == "Off":
                            ClientConn -= 1
                            if ClientConn == 0:
                                serveur_lance = False
                GPIO.output(7,GPIO.LOW)
    msg_recu = " "
                
# fin de connexion et remise à 0 des ports de sorties
print("Fermeture des connexions")
for client in clients_connectes:
    client.close()
GPIO.output(3,GPIO.LOW)
GPIO.output(5,GPIO.LOW)
GPIO.output(7,GPIO.LOW)
connexion_principale.close()
my_callback()
