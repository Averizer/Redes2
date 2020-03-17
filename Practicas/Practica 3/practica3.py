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
        mine = os.popen('ifconfig | grep "inet 192" | cut -c 14-25')
        direccion_ip = mine.read()
        mine.close()
        direccion_ip = direccion_ip.split('.')
        direccion_ip = direccion_ip[0:3]
        direccion_ip = direccion_ip[0]+'.'+direccion_ip[1]+'.'+direccion_ip[2]+'.'
    return [nombre_equipo, direccion_ip]


#Realiza un ping a la ip dada
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

