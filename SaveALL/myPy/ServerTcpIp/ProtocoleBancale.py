import socket
import sys
import time 
class TCP:
    """
    Serveurttcp ip pour communiquer avec automat et twincat 
    """
    def __init__(self):
        self.adr = ''
        self.port = 6789
        self.serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serveur.bind((self.adr,self.port))
        self.serveur.listen(5)
        self.client=None
        self.adresseClient=None
        self.MsgRe=None
        self.running=True
        print("ecoute")
    def ClienAccept(self):
        try:
            self.client, self.adresseClient = self.serveur.accept()
        except TimeoutError as e:
            print(e)
            raise TimeoutError("Timeout3")
        self.ConnectAck()
        print("les clients connectés:{}".format(str(self.client)))
    def ConnectAck(self): 
        reponse = "connected"
        print ('Envoi de :{}'.format(reponse))  
        rep_enc=reponse.encode()
        n = self.client.send(rep_enc)
        if (n != len(rep_enc)):
            print('Erreur envoi.')
        else:
            print ('Envoi ok.')
    def Respond(self,_respond):
        reponse = _respond
        print ('Envoi de :{}'.format(reponse))
        rep_enc=reponse.encode()
        n = self.client.send(rep_enc)
        if (n != len(reponse)):
            print('Erreur envoi.')
        else:
            print ('Envoi ok.')
    def ServClosed(self):
        print ('Fermeture de la connexion avec le client.')
        self.client.close()
        print ('Arret du serveur.')
        self.serveur.close()
    def Deco(self):
        print ('Fermeture de la connexion avec le client.')
        self.client.close()
        self.NewCLi()
    def NewCLi(self):
        self.client=None
        self.ClienAccept()
        
    def Recieving(self):
        print("recieving")
       # self.serveur.settimeout(2)
        try:
            self.MsgRe = self.client.recv(1024)
        except (TimeoutError , ConnectionResetError)as e:
            print(e)
            raise TimeoutError("Timeout1")
        if self.MsgRe == b'':
            raise TimeoutError("Timeout2")
        self.MsgRe =  self.MsgRe.decode()
        print(self.MsgRe)
        
        if ( self.MsgRe == "pos") | ( self.MsgRe == "mus") | ( self.MsgRe == "fin"):
                #allume la troisième reçoit un message
                print("Reçu {}".format( self.MsgRe))
                # si le message fin est détecté
                if  self.MsgRe == "pos":
                    self.Respond("position des robots")
                else:
                    if  self.MsgRe == "mus":
                        self.Respond("points du muse")
                    else:
                        if  self.MsgRe == "fin":
                            self.Respond("Serveur closed")
                            #self.running=False
                            self.Deco()
                            
        self.MsgRe= " "


    def __del__(self):
        print ('Fermeture de la connexion avec le client par destructeur.')
        self.client.close()
        self.serveur.shutdown(socket.SHUT_RDWR)

    def main(self):
        while self.client ==None:
            self.ClienAccept()
           # self.running=True
        while self.running:
            try:
                self.Recieving()
            except( TimeoutError ,ConnectionError):
                print("error")
                self.Deco()
                
                 

        

def main() :
    tcp = TCP()
    tcp.main()
    sys.exit(0)

    return 0


if __name__ == "__main__":
    main()

