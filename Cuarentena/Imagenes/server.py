import os
import zipfile
import socket
import time

port = 37020

#Lista con los nombres de las 4 imagenes a enviar
imagenes = ["1.png", "2.png", "3.png","4.png"]	

#definicion de modo broadcast en el socket mediante UDP
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)	#Se crea el socket UDP
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while True:
	for img in imagenes:
		print("Transmitiendo imagen " + img)
		file = "/home/"+ socket.gethostname() + "/" + str(img)

		#enviar titulo
		content = bytes(img, "utf-8")
		content = bytes("3", "utf-8") + content
		server.sendto(content,('<broadcast>', port))

		#abrir imagenes en bytes
		f = open(file,"rb")
		content = f.read(512)
		content = bytes("1", "utf-8") + content

		while content:
			server.sendto(content,('<broadcast>', port))
			content = f.read(512)
			if len(content) < 512:
				content = bytes("0", "utf-8") + content
				server.sendto(content, ('<broadcast>', port))
				time.sleep(2)
				break
			else:
				content = bytes("2", "utf-8") + content

		f.close()


#Cierro el socket 
server.close()	
