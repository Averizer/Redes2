
import re
import threading as th
import math as m
import time

#Constantes
productores = 5
consumidores = 5
Nproducciones = 5
TamBuffer = 4
tipoLetra = ['A', 'B', 'C', 'D', 'E']
tipoNumero = ['1', '2', '3', '4', '5']

#Zona critica
zcLetras = ["","","",""]
nzcNumeros = ['\0','\0','\0','\0']
archivos = [None] * 5

#declaracion de semaforos
semGlobal = th.Semaphore(1)
semArchivo = th.Semaphore(1)
semZonaCritica = [None] * TamBuffer

#creacion de los semaforos del buffer
for i in range(0,TamBuffer):
    semZonaCritica[i] = th.Semaphore()

"""for f in range(0,len(tipoLetra)):
    archivos[f] = open("Archivo_" + str(tipoLetra[f]) + ".txt","w+" )"""



# Funciones para los hilos
def productor(id):
    letra = tipoLetra[id]
    numero = tipoNumero[id]
    print("Hola soy el hilo productor ", id)
    aux = 0
    for i in range(5):
        while True:
            #print("iterando en productor: "+ str(i))
            if(aux == 3):
                aux = 0
            
            semZonaCritica[aux].acquire()
            if(len(zcLetras[aux]) is 0):
                zcLetras[aux] = letra
                semZonaCritica[aux].release()
                print(zcLetras)
                break
            else:
                semZonaCritica[aux].release()
                time.sleep(0.2)
                aux += 1

def consumidor(id):
    for i in range(5):
        #print("Iteración numero: "+ str(i))
        aux = 0
        while True:
            if(aux == 3):
                aux = 0

            semZonaCritica[aux].acquire()
            if (len(zcLetras[aux]) is not 0):
                letraR = zcLetras[aux]
                print("Consumidor "+str(id)+" consumiendo: ", letraR)
                zcLetras[aux] = ""
                semZonaCritica[aux].release()
                break
            else:
                semZonaCritica[aux].release()
                time.sleep(0.2)
                aux += 1
    
    print("Consumidor "+str(id)+" termino de consumir")

hilosC = [] #hilos consumidores
hilosP = [] #hilos productores

#Creación de hilos
for i in range(5):
    t = th.Thread(name = ("Hilo " + str(i)), target = productor, args=(i,))
    hilosP.append(t)
    t2 = th.Thread(name = ("Hilo " + str(i)), target = consumidor, args=(i,))
    hilosC.append(t2)

#Inicializacion de hilos
for i in range(5):
    p = hilosP[i]
    p.start()
    p2 = hilosC[i]
    p2.start()

#Finalización de hilos    
for i in range(5):
    p = hilosP[i]
    p.join()
    p2 = hilosC[i]
    p2.join()
    
#cierre de los archivos
"""for f in range(0,len(tipoLetra)):
    archivos[f].close()"""

print("Terminaron todos los hilos bye")


ssiiiiiii ya esta xD 
