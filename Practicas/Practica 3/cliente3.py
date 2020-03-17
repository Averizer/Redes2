import socket
import sys

import tkinter 
from tkinter.filedialog import askopenfilename

class Cliente():
    def __init__(self, name):
        self.name = name

    def conectar(self):
        #Creacion del socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Coneccion del socket al puerto e ip 
        IP_server = 'localhost'
        puerto = 12345
        server_address = (IP_server, puerto)
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
                    message = (input("Ingresa el mensaje que deseas mandar: ").encode())
                    print('Información a enviar {!r}'.format(message))
                    sock.sendall(message)
                    amount_received = 0
                    amount_expected = len(message)
                
                    while amount_received < amount_expected:
                        data = sock.recv(1024)
                        amount_received += len(data)
                        print('Recibido del servidor: {!r}'.format(data))
                if(op == 2):
                    tkinter().Tk().withdraw() 
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

class iniciar():

    def __init__(self):
        #Proceso para realizar la interfaz grafica de usuario
        self.ventana = tkinter.Tk()
        self.ventana.geometry("350x150")
        self.ventana.title('Inicio Sesion')

        #texto de nickname
        self.nickname = tkinter.Entry(self.ventana, font='Helvetica 20')
        self.nickname.grid(row=0, column = 2)

        #Label de aviso
        self.nick_vacio = tkinter.Label(self.ventana,text='', bg ="white")
        self.nick_vacio.grid(row=2, column = 2)

        #boton de conexion
        self.conectar = tkinter.Button(self.ventana, text = "Conectar", command=self.nombre)
        self.conectar.grid(row = 1, column = 2)

        self.ventana.mainloop()

    #verificar nombre usuario
    def nombre(self):
        nick = self.nickname.get()
        if(len(nick) == 0):
            self.nick_vacio.configure(text='ingrese un nickname')
        else:
            self.nick_vacio.configure(text='')
            self.ventana.destroy()

            Sesion(nick)


class Sesion():
    def __init__(self, nombre):
        self.ventana = tkinter.Tk()
        self.ventana.geometry("350x150")
        self.ventana.title('Bienvenido: ' + str(nombre))
        
        actualizar = tkinter.Button(self.ventana, text = "Actualizar")
        actualizar.grid(row = 1, column = 1)
        
        #inicia conexion
        Cliente(nombre)

        self.ventana.mainloop()

    def actualizar(self):
        pass


class chat():
    def __init__(self):
        #Proceso para realizar la interfaz grafica de usuario
        self.ventana = tkinter.Tk()
        self.ventana.geometry("350x150")
        self.ventana.title('Chat')

        self.CajaTexto = tkinter.Text(self.ventana, font = 'Helvetica 30')
        self.CajaTexto.gird(row = 0, column = 0)

        self.ventana.mainloop()


empezar = iniciar()
