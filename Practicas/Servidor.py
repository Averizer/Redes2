import socket
import time

imagenes = ["1.png", "2.png", "3.png","4.png"]	#Lista con los nombres de las 4 imagenes a enviar

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)	#Se crea el socket UDP
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)					#Se configura para reutilizar
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)					#Se configura como broadcast

while True:
	for img in imagenes:										#for que recorre las cuatro imagenes
		print("Transmitiendo imagen " + img)
		img2send = "/home/emiliano/Escritorio/Broadcast/" + str(img)
		f = open(img2send, "rb")								#Abro el archibo en lectura de bytes
		content = f.read(512)									#Leo 512 bytes
		content = bytes("1", "utf-8") + content					#Le concateno un 1 para que el cliente sepa que es el primer datagrama del archivo
		while content:									
			server.sendto(content, ('<broadcast>', 37020))		#Envio el datagrama
			content = f.read(512)								#Leo 512 bytes
			if len(content) < 512:								#Si leo menos de 512 esque es el ultimo datagrama
				content = bytes("0", "utf-8") + content			#Le concateno un 0 para que el cliente sepa que es el ultimo
				server.sendto(content, ('<broadcast>', 37020))	#Le envio el datagrama
				time.sleep(2)									#Espero 2 segundos
				break
			else:												#En caso de que sea un datagrama intermedio
				content = bytes("2", "utf-8") + content			#Le concateno un 2 para que el cliente sepa que es un datagrama intermedio

		f.close()												#Cierro el archivo

server.close()	#Cierro el socket 