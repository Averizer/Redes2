import tkinter as tk

colours = ['red','green','orange','white','yellow','blue']

r = 0
for c in colours:
    tk.Label(text=c, relief=tk.RIDGE, width=15).grid(row=r,column=0)
    tk.Entry(bg=c, relief=tk.SUNKEN, width=10).grid(row=r,column=1)
    r = r + 1

tk.mainloop()

import socket
import sys

from tkinter import Tk
from tkinter.filedialog import askopenfilename

#Creacion del socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Coneccion del socket al puerto e ip 
server_address = ('localhost', 12333)
print('Levantando servidor {} en el puerto {}'.format(*server_address))
sock.connect(server_address)
nuevo = 1
while nuevo:
    try:
        print("")
        # Seleccion de que tipo de archivo se quiere enviar
        print("Selecciona la opción que deseas: ")
        print("1.- Escribir mensaje")
        print("2.-Enviar archivo")
        print("3.- Salir")
        op = int(input("Opción: "))
        if(op == 1):
            message = (input("Ingresa el mensaje que deseas mandar").encode())
            print('Información a enviar {!r}'.format(message))
            sock.sendall(message)
            amount_received = 0
            amount_expected = len(message)
        
            while amount_received < amount_expected:
                data = sock.recv(1024)
                amount_received += len(data)
                print('Recibido del servidor: {!r}'.format(data))
        if(op == 2):
            Tk().withdraw() 
            filename = askopenfilename() 
            file = open(filename,'rb')
            contenido = file.read(1024)
            while contenido:
                sock.send(contenido)
                contenido = file.read(1024)
            print("Archivo enviado correctamente")
        if(op == 3):
            nuevo = 0
        # Look for the response                
            
    finally:
        print('Cerrando canal de comunicación del cliente')
        
sock.close()