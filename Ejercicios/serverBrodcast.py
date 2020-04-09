import socket
import time

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Activar puerto reusable
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

# Activar modo broadcast
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Establecer timeout para asegurar que no crashee
server.settimeout(0.2)
message = b"your very important message"
while True:
    server.sendto(message, ('<broadcast>', 37020))
    print("message sent!")
    time.sleep(1)