import tkinter
import sys 
import subprocess as sub
import socket as s
import os
import platform
import threading as th

semipact = th.Semaphore()
semipina = th.Semaphore()

ip_activos = []
ip_inactivo = []

#funcion del hilo
def realizarPing(inicio,fin, ip):
    for n in range(inicio,fin):
        checar_estadoIP(ip+str(n))


#obtiene el nombre del host asi como la ip
def conocer_entorno():
    nombre_equipo = s.gethostname()
    if(platform.system().lower() == "windows"):
        mine = os.popen('netsh interface ipv4 show config Wi-Fi ')
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


#Realiza un ping a la ip
def checar_estadoIP(ip):
    global ip_activos
    global ip_inactivo
    ping_str = "-n 1 -w 5 " if platform.system().lower()=="windows" else "-c 1 -w 5"
    response = os.system("ping "+ping_str+ip)
    if response == 0:
        semipact.acquire()
        ip_activos.append(ip)
        semipact.release()
    else:
        semipina.acquire()
        ip_inactivo.append(ip)
        semipina.release()

#funcion para el hilo que realiza el ping y obtencion de ip
def encontrar_ip():
    num = 11
    cantidad = int(253/num)
    [nom,ip] = conocer_entorno()
    hilos = []
    for i in range(num):
        inicio = cantidad * i #+ 1 if i == 0 else cantidad * i
        fin = cantidad * (i+1) #+ 1 if i == num-1 else cantidad * (i+1)
        t = th.Thread(name = ("Hilo " + str(i)), target = realizarPing, args=(inicio,fin, ip))
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
    print(ip_activos)



encontrar_ip()


#Proceso para realizar la interfaz grafica de usuario
ventana = tkinter.Tk()
ventana.geometry("500x600")

#boton que actualiza la tabla de usuarios conectados
#Aun falta mejorar
actualizar = tkinter.Button(ventana, text = "Actualizar")
#actualizar.pack()
actualizar.grid(row = 1, column = 1)
direccion = []
for ip in ip_activos:
    direccion.append([ip,1])

columna = 0
fila = 2

for i in range(len(direccion)):
    if columna > 2:
        columna = 0
        fila = fila + 1
    texto = "IP: {} {}".format(direccion[i][0], "Dispoible" if direccion[i][1] == 1 else "No disponible")
    clientes = tkinter.Button(ventana, text = texto)
    clientes.grid(row = fila, column = columna)
    columna = columna + 2

ventana.mainloop()