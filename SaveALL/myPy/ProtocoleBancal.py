from pip import List
import socket
import sys
import time 


class TCP:
    """
    Serveurttcp ip pour communiquer avec automat et twincat 
    Modif clients:
    soit pas envoyer fin, soit pas faire de cocket connect h24

    """
    def __init__(self):
        self.adr = ''
        self.port = 6789
        self.serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serveur.bind((self.adr,self.port))
        self.serveur.listen(5)
        self.clients=list()
        self.ClientWaited=2
        self.MsgRe=None
        self.running=True
        print("ecoute")

    def ClienAccept(self):
        try:
            client, _ = self.serveur.accept()
            print("client connecté")
        except TimeoutError as e:
            print(e)
            raise TimeoutError("Timeout3")
        self.ConnectAck(client)
        self.clients.append(client)
        self.ClientWaited=self.ClientWaited-1
        print("les clients connectés:{}".format(str(self.clients)))

    def ConnectAck(self,_client): 
        reponse = "connected"
        print ('Envoi de :{}'.format(reponse))  
        rep_enc=reponse.encode()
        n = _client.send(rep_enc)
        if (n != len(rep_enc)):
            print('Erreur envoi.')
        else:
            print ('Envoi ok.')

    def Respond(self,_respond,_clien):
        reponse = _respond
        print ('Envoi de :{}'.format(reponse))
        rep_enc=reponse.encode()
        n = _clien.send(rep_enc)
        if (n != len(reponse)):
            print('Erreur envoi.')
        else:
            print ('Envoi ok.')

    def Recieving(self):
        print("recieving")
       # self.serveur.settimeout(2)
        for i in self.clients:
            try:
                self.MsgRe = i.recv(1024)
            except (TimeoutError , ConnectionResetError)as e:
                print(e)
                raise TimeoutError("Timeout1")
         
            if self.MsgRe == b'':
                raise TimeoutError("Timeout2")
            self.MsgRe =  self.MsgRe.decode()

            print("Reçu {}".format( self.MsgRe))


            if  self.MsgRe == "pos":
                self.Respond("position des robots",i)
            elif  self.MsgRe == "mus":
                self.Respond("points du muse",i)
            elif  self.MsgRe == "fin":
                self.Respond("fin",i)
            else:
                self.MsgRe=" "

    def __del__(self):
        print ('Fermeture de la connexion avec le client par destructeur.')
        self.client.close()
        self.serveur.shutdown(socket.SHUT_RDWR)

    def main(self):
        while self.ClientWaited !=0:
            self.ClienAccept()
        while 1 :
            try:
                self.Recieving()
            except( TimeoutError ,ConnectionError):
                print("error")

                
                 

        

def main() :
    tcp = TCP()
    tcp.main()
    sys.exit(0)

    return 0


if __name__ == "__main__":
    main()

