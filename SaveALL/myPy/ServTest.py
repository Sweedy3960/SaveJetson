import socket 
ServRun=True
client = None
serv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
data = None
serv.bind(("",6789))
serv.listen(1) 

while ServRun ==True:
  
    if not client :
        print("pas de client") 
        client,adr = serv.accept()
        print("client connected ",adr)
    else:
        try:
            data = client.recv(1024)
        except:
            pass
    if not data:
        print("erreur")
        reponse = "repeat"
        reponseEncoded=reponse.encode()
        print("envoi de :"+str(reponse))    
        client.send(reponseEncoded)
    else : 
        print("reception de :"+str(data))
        
        reponse = "5/5"
        reponseEncoded=reponse.encode()
        print("envoi de :"+str(reponse))    
        n= client.send(reponseEncoded)
        if n != len(reponseEncoded):
            print("erreur")
        else:
            print("Envoi ok") 
    if data == b'fin':
        reponse = "serveurclosed"
        reponseEncoded=reponse.encode()
        client.send(reponseEncoded) 
        print("envoi de :"+str(reponseEncoded))
        break
client.close()
serv.close()