import socket 

serv = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

serv.bind(("",6789))
serv.listen(1) 
client,adr = serv.accept()
print("client connected ",adr)

data = client.recv(1024)
if not data:
     print("erreur")
else : 
    print("reception de :"+str(data))
    reponse = data.upper()
    print("envoi de :"+str(reponse))
    n= client.send(reponse)
    if n != len(reponse):
        print("erreur")
    else:
        print("Envoi ok")

client.close()
serv.close()