import socket 
class Serveur:
    def __init__(self):
        
        self.hote = 
        self.port=
        self.adress=(self.hote,self.port)
        self.MsgToSend =
        self.MsgRecieve=
        
    def ServerStart(self):
        self.ThatServ= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return "serv run"
    def bind(self):
       self.ThatServ.bind(self.adress)
       return "serv binded"
    def Listen(self):
        self.ThatServ.listen(1)
        return "listenning"
    def ClienConnect(self):
        ThatSe 
