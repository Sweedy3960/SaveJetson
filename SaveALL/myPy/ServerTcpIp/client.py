#//////Client///////
# Programmeur: Phung Arthur
# nom du projet: client.py
# Raspberry à utiliser: Client

#importation des librairies
import time
import RPi.GPIO as GPIO
import socket
import os

# init des GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)                           # Voyant du raspberry
GPIO.setup(7,GPIO.OUT)                            # Voyant état du client   
GPIO.setup(31,GPIO.IN)                            # Interrupteur
GPIO.setup(37,GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Bouton d'interruption
GPIO.setup(40,GPIO.IN)                            # Récepteur infrarouge

# Indique que le programme a démarré
GPIO.output(7,GPIO.HIGH)

# Fonction d'interruption
def Turn_Off():
    # Éteint voyant d'état du raspberry
    GPIO.output(7,GPIO.LOW)
    # Attente 2 secondes
    time.sleep(2)
    # Éteignage du raspberry
    os.system("sudo shutdown -h now")

GPIO.add_event_detect(37, GPIO.FALLING, callback=Turn_Off, bouncetime=300)

#variable globale
BOUTON = 0
Start = 0

# adresse IP du serveur et port de communication
hote = "10.3.141.1"
port = 12800

# Tant que le bouton est $ 0 fait clignoter la LED
while Start == 0:
    Start = GPIO.input(31)
    GPIO.output(11,GPIO.HIGH)
    time.sleep(1)
    GPIO.output(11,GPIO.LOW)
    time.sleep(1)
    
GPIO.output(11,GPIO.LOW)
#Tentative de connexion au serveur
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))

#allumage de la LED
GPIO.output(11,GPIO.HIGH)

#init des variables locales
memoire = 0 # mémoire de l'état de la barrière optique
Msg = "New"
Msg = Msg.encode()
conn.send(Msg)
time.sleep(10)
Msg = "Next"
Msg = Msg.encode()
#tant que le bouton start est actif
while Start !=0:
    #Lecteur du bouton start
    Start = GPIO.input(31)
    #sauvegarde de l'état de la barrière optique
    memoire = BOUTON
    #Lecture de la barrière optique
    BOUTON = GPIO.input(40)
    #Test si la barrière optique est coupé
    if(BOUTON == 0):
        #éteind la LED
        GPIO.output(11,GPIO.LOW)
    else:
        #allume la LED
        GPIO.output(11,GPIO.HIGH)
        #Test si la barrière optique est coupée
        if((BOUTON == 1)and(memoire == 0)):
            conn.send(Msg)
            print("Envoyé")
            # attente de 1sec avant de pouvoir relire
            # la valeur de la barrière optique
            time.sleep(1)
            
# si le bouton start = 0 envoie du message fin qui coupe la connexion
# du serveur et du client
Msg = "Off"
Msg = Msg.encode()
conn.send(Msg)

print("close")
GPIO.output(7,GPIO.LOW)
print("Fermeture de la connexion")
#conn.close()
Turn_Off()