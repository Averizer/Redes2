import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP

#Hacer reusable el puerto
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

# Activar el modo de broadcast
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

client.bind(("", 37020))
while True: 
    
    data, addr = client.recvfrom(1024)
    print("Mensaje recibido: %s"%data)