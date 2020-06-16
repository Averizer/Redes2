import socket
import zipfile
import sys
import threading
import os

port = 37020

#configuracion de conexion por broadcast
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) 	#Se crea el socket UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)					#Se configura como broadcast
client.bind(("", port))														#Se vincula con la dirección broadcast y el puerto

print('[+] esperando imagenes...')

filename = "/home/"+ socket.gethostname() +"/default.png"

while True:
	data, addr = client.recvfrom(513)
	print("Conexion de: {}".format(addr[0]))
	#verifica si es el comienzo de una nueva imagen
	if data[0] == 51:
		name = data[1:len(data)]
		filename = "/home/"+ socket.gethostname() +"/"+str(name)+".png"
	elif data[0] == 49:
		f = open(filename, "wb")
		f.write(data[1:len(data)])
		while True:
			data, addr = client.recvfrom(513)
			if data[0] == 50:
				f.write(data[1:len(data)])
			elif data[0] == 48:
				f.write(data[1:len(data)])
				f.close()
				break
		print("guardado")


client.close()	
