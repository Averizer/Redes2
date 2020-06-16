import sys
import telnetlib
import datetime
import subprocess

#Listas
HOSTS = ['192.168.1.254','192.168.5.3','192.168.6.3']

#variables
#ip = ''

#constantes
password = "redes2" 
fechaHoy = str(datetime.date.today())
nameConfig = "router-config-"
ipServer = "192.168.1.4"


def obtenerConfig(ip):
    print("----------------------------------------")
    print("Obteniendo archivo de configuracion")
    print("del router: " + ip)
    name = nameConfig + ip + '-' + fechaHoy 
    tn = telnetlib.Telnet(ip)
    if password:
        tn.write(password.encode('ascii') + b"\n")
    tn.write(b"en\n")
    tn.write(password.encode('ascii') + b"\n")
    tn.write(b"copy run tftp:\n")
    tn.write(ipServer.encode('ascii') + b"\n")
    tn.write(name.encode('ascii') + b"\n")
    tn.write(b"exit\n")
    tn.read_all().decode('ascii')

for ip in HOSTS:
    obtenerConfig(ip)


