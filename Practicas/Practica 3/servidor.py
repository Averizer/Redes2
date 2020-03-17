import tkinter
import sys 
import subprocess as sub
import socket as s
import os
import platform
import threading as th
import socket

class Servidor():

    def __init__(self):
        self.semipact = th.Semaphore()
        self.semipina = th.Semaphore()

        self.ip_activos = []
        self.ip_inactivo = []

        #dinamico
        self.hilos = []

        self.nombre_IP = {}

        self.ventana = tkinter.Tk()
        self.frame = tkinter.Frame(self.ventana)

        self.encontrar_ip()
        
        actualizar = tkinter.Button(self.frame, text = "Actualizar", command=self.encontrar_ip)
        actualizar.grid(row = 1, column = 1)

        #self.abrirConexion()

        self.ventana.mainloop()
        

    #funcion del hilo
    def realizarPing(self, inicio, fin, ip):
        for n in range(inicio,fin):
            self.checar_estadoIP(ip+str(n))


    #obtiene el nombre del host asi como la ip
    def conocer_entorno(self):
        nombre_equipo = s.gethostname()
        if(platform.system().lower() == "windows"):
            tipo_conexion = self.revisar_Conexion()
            mine = os.popen('netsh interface ipv4 show config ' + tipo_conexion)
            direccion_ip = mine.read()
            mine.close()
            direccion_ip = direccion_ip.split()
            direccion_ip = direccion_ip[direccion_ip.index("IP:")+1]
            direccion_ip = direccion_ip.split('.')
            direccion_ip = direccion_ip[0:3]
            direccion_ip = direccion_ip[0]+'.'+direccion_ip[1]+'.'+direccion_ip[2]+'.'
        else:
            mine = os.popen('ifconfig | grep "inet" | cut -c 14-25 | head -n 1')
            direccion_ip = mine.read()
            mine.close()
            direccion_ip = direccion_ip.split('.')
            direccion_ip = direccion_ip[0:3]
            direccion_ip = direccion_ip[0]+'.'+direccion_ip[1]+'.'+direccion_ip[2]+'.'
        return [nombre_equipo, direccion_ip]


    def revisar_Conexion(self):
        activo = os.popen('netsh interface ipv4 show interfaces')
        conectado = activo.read()
        activo.close()
        conectado = conectado.split()
        while(1):
            if(conectado[conectado.index("connected")+ 1] == 'Ethernet'):
                tipo_conexion = 'Ethernet '
                break
            elif(conectado[conectado.index("connected")+ 1] == 'Wi-Fi'):
                tipo_conexion = 'Wi-Fi '
                break
            else: 
                conectado.pop(conectado.index("connected"))
        
        return tipo_conexion

    #Realiza un ping a la ip
    def checar_estadoIP(self, ip):
        ping_str = "-n 1 -w 5 " if platform.system().lower()=="windows" else "-c 1 -w 5"
        response = os.system("ping "+ping_str+ip)
        if response == 0:
            self.semipact.acquire()
            if ip in self.ip_inactivo:
                self.ip_inactivo.pop(self.ip_inactivo.index(ip))
            if not ip in self.ip_activos:
                self.ip_activos.append(ip)
            self.semipact.release()
        else:
            self.semipina.acquire()
            if ip in self.ip_activos:
                self.ip_activos.pop(self.ip_activos.index(ip))
            if not ip in self.ip_inactivo:
                self.ip_inactivo.append(ip)
            self.semipina.release()

            

    #funcion para el hilo que realiza el ping y obtencion de ip
    def encontrar_ip(self):
        num = 11
        cantidad = int(253/num)
        [nom,ip] = self.conocer_entorno()
        hilos = []
        for i in range(num):
            inicio = cantidad * i #+ 1 if i == 0 else cantidad * i
            fin = cantidad * (i+1) #+ 1 if i == num-1 else cantidad * (i+1)
            t = th.Thread(name = ("Hilo " + str(i)), target = self.realizarPing, args=(inicio,fin, ip))
            hilos.append(t)

        #inicializacion de hilos
        for i in range(num):
            p = hilos[i]
            p.start()

        #Finalizacion de hilos    
        for i in range(num):
            p = hilos[i]
            p.join()

        print("IP activos: ")
        print(self.ip_activos)
        self.frame = self.actualizar_frame()

    def actualizar_frame(self):
        """direccion = []
        for ip in self.ip_activos:
            direccion.append([ip,1])"""
        self.frame.destroy()
        frame = tkinter.Frame(self.ventana)
        
        frame.config(bg='Lightblue')
        frame.config(width = 350, height = 400)

        actualizar = tkinter.Button(frame, text = "Actualizar", command=self.encontrar_ip)
        actualizar.grid(row = 1, column = 1)

        columna = 0
        fila = 2
        
        for i in range(len(self.ip_activos)):
            if columna > 2:
                columna = 0
                fila = fila + 1
            texto = "IP: {} {}".format(self.ip_activos[i], "Disponible" )#if direccion[i][1] == 1 else "No disponible")
            clientes = tkinter.Button(frame, text = texto)
            clientes.grid(row = fila, column = columna)
            columna = columna + 2
        
        frame.pack()

        return frame

    def abrirConexion(self):
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        IP_server = 'localhost'
        puerto = 12345
        server_address = (IP_server, puerto)
        print('starting up on {} port {}'.format(*server_address))
        sock.bind(server_address)

        # Listen for incoming connections
        num_conexion = 15
        sock.listen(num_conexion)

        while True:
            # Wait for a connection
            print('waiting for a connection')
            connection, client_address = sock.accept()
            try:
                print('connection from', client_address)

                #agregamos hilo y lo iniciamos
                t = th.Thread(name = ("Hilo "), target = self.escuchar, args=(connection, client_address))
                self.hilos.append(t) 

            finally:
                # Clean up the connection
                connection.close()

    def escuchar(self, connection, client_address):
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1024)

            if(data[0] == 0):
                nick = data[1]
                self.nombrar(client_address, nick)
            elif(data[0] == -1):
                del self.nombre_IP[data[1]]
            elif(data[0] == 5): #Refrescar frame
                data = self.nombre_IP
                connection.sendall(data)
            #agregar opcion de archivos
    def nombrar(self, ip, nick):
        self.nombre_IP[ip] = nick

s = Servidor()

