import socket
import tkinter
import os
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) 	#Se crea el socket UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)					#Se configura para reutilizar
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)					#Se configura como broadcast
client.bind(("", 37020))														#Se vincula con la dirección broadcast y el puerto

id_num = os.getpid()						#Obtengo el ID del proceso para identficar a los archivos de cada cliente
name_img = str(id_num) + "_recibido.png"	#Le asigno un nombre al archivo donde recibiremos la imagen
print(name_img)								#imprimo el nombre del archivo en consola

raiz = tkinter.Tk()												#Creo una ventana de Tkinter
raiz.title("TRANSMISIÓN")										#Nombre de la ventana
label = tkinter.Label(raiz, text="En espera de imagenes....")	#Texto en la ventana
label.pack()													#Enpaqueto el label

def hilo():													#función que se encarga de recibir las datos del servidor
	while True:												
		data, addr = client.recvfrom(513)					#Recibo los datos del servidor
		if data[0] == 49:									#Verifica que es el comienzo de una nueva imagen
			f = open(name_img, "wb")						#Abro un archivo con el nombre de name_img
			f.write(data[1:len(data)])						#Escribo la primera parte del archivo recibido
			while True:										
				data, addr = client.recvfrom(513)			#Recibo los datos del servidor
				if data[0] == 50:							#Verifica que son datos intermedios de la imagen
					f.write(data[1:len(data)])				#Escribo las partes intermedias del archivo recibido
				elif data[0] == 48:							#Verifica que es el final de una imagen
					f.write(data[1:len(data)])				#Escribo la ultima parte del archivo recibido
					f.close()								#Cierro el archivo
					with open(name_img, "rb") as f:			#Vulevo a abrir el archivo
						data = f.read()						#Leo toda la informacion
						f.close()							#Vulevo a cerrar el archivo
					imagen = tkinter.PhotoImage(data=data)	#Obtengo el objeto de imagen para tkinter
					label.config(image=imagen)				#Agego la imagen recibida a la ventana
					break

threading.Thread(target=hilo).start() 	#Inicio el hilo
raiz.mainloop()							#Se crea la ventana principal
client.close()							#Cerramos el socket