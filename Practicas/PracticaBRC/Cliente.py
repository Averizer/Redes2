import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # UDP

# Enable port reusage so we will be able to run multiple clients and servers on single (host, port). 
# For linux hosts all sockets that want to share the same address and port combination must belong to processes 
# that share the same effective user ID!
# So, on linux(kernel>=3.9) you have to run multiple servers and clients under one user to share the same (host, port).
# Thanks to @stevenreddie
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

# Enable broadcasting mode
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

client.bind(("", 37020))

while True:
    for x in range(5):
        y = x + 1
        fname2 = "" + str(y) + ".jpg"
        fname = "/home/emiliano/Escritorio/Redes/BRC/img/" + fname2
        img = open("/home/emiliano/Escritorio/Redes/BRC/imagen", "wb")

        try:
            data = client.recv(1024)
        except socket.error:
            print("Error de lectura.")
            break
        else:
            if data:
                if isinstance(data, bytes):
                    end = data[0] == 1
                else: 
                    end = data == chr(1)
                if not end:
                    img.write(data)
                else:
                    img.close()
                    break
        print("Image recived successfully ")
        
    #client.close()

    #exit()
    #data, addr = client.recvfrom(1024)
    #print("received message: %s"%data)