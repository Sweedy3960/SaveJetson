import socket

s = socket.socket()

host = ''
port = 6789	

s.bind((host, port))

s.listen(1)
print("ecoute")

conn, addr = s.accept()
print("connected")
print('Connection address:', addr)
conn.send(b'connected')
while 1:
    data = conn.recv(1024)
    if not data: break
    print("Received data:", data)
    response = input("Send to client: ")
    conn.send(bytes(response, "utf-8"))  # echo

conn.close()
