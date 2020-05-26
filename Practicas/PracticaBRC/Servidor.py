
import socket
import time

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Enable port reusage so we will be able to run multiple clients and servers on single (host, port).
# For linux hosts all sockets that want to share the same address and port combination must 
# belong to processes that share the same effective user ID!
# So, on linux(kernel>=3.9) you have to run multiple servers and clients
#  under one user to share the same (host, port).
# Thanks to @stevenreddie
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

# Enable broadcasting mode
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
server.settimeout(0.2)
#server.sendto(message,("<broadcast>", 37020))
while True:
    for x in range(5):
        y = x + 1
        fname2 = "" + str(y) + ".jpg"
        fname = "/home/emiliano/Escritorio/Redes/BRC/img/" + fname2
        fp = open(fname, 'rb')
        #server.send(fname)
        content = fp.read(1024)

        while content:
            server.sendto(content, ("<broadcast>", 37020))
            content = fp.read(1024)
        fp.close()
        try:
            server.sendto(bytes(chr(1)), ("<broadcast>", 37020))
        except TypeError:
            server.sendto(bytes(chr(1)), "utf-8", ("<broadcast>", 37020))
        fp.close()
        print("Image {} Sent successfully".format(fname))
    time.sleep(1)
    #server.sendto(message, ('<broadcast>', 37020))
    #print("message sent!")
    
