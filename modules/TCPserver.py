from socket import *

host_name=gethostname()
port_num=8000
server = socket(AF_INET, SOCK_STREAM)
server.bind((host_name, port_num))
server.listen(5)
print("server is ready to accept")
connectionsocket,addr = server.accept()
msg=connectionsocket.recv(1024) #bytes形式. decode是变成文字，encode是变成bytes
if int.from_bytes(msg, byteorder='big')<101:
    print("got the msg from client: " + str(int.from_bytes(msg, byteorder='big')))
    connectionsocket.send(msg)
else:
    server.close()