import socket
import sys
class TCP:
    """
    Serveurttcp ip pour communiquer avec automate et twincat 
    """
    def __init__(self):
        self.adr = ''
        self.port = 6789
        self.serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.serveur.bind((self.adr,self.port))
        self.serveur.listen(1)
        self.client=None
        self.adresseClient=None
        self.MsgRe=None
        self.running=True
        print("ecoute")
    def ClienAccept(self):
        self.client, self.adresseClient = self.serveur.accept()
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

    def Recieving(self):
        print("recieving")
        self.MsgRe = self.client.recv(1024)
        print(self.MsgRe)
        self.MsgRe =  self.MsgRe.decode()
        print(self.MsgRe)
            
        if ( self.MsgRe == "pos") | ( self.MsgRe == "mus") | ( self.MsgRe == "fin"):
                #allume la troisième reçoit un message
                print("Reçu {}".format( self.MsgRe))
                # si le message fin est détecté
                if  self.MsgRe == "pos":
                    self.Respond("position des robotzs")
                else:
                    if  self.MsgRe == "mus":
                        self.Respond("points du musé")
                    else:
                        if  self.MsgRe == "fin":
                            self.Respond("Serveur closed")
                            self.ServClosed()
                            self.running=False
        self.MsgRe= " "


    def __del__(self):
        print ('Fermeture de la connexion avec le client.')
        self.client.close()
        print ('Arret du serveur.')
        self.serveur.close()
    def main(self):
        while self.client ==None:
            self.ClienAccept()
        while self.running:
            self.Recieving()
        

def main() :
    tcp = TCP()
    tcp.main()
    sys.exit(0)

    return 0


if __name__ == "__main__":
    main()

