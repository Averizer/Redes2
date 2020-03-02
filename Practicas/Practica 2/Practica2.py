
import re
import threading as th
import math as m
import time

#Constantes
productores = 5
consumidores = 5
Nproducciones = 2
TamBuffer = 4
tipoLetra = ['A', 'B', 'C', 'D', 'E']
tipoNumero = ['1', '2', '3', '4', '5']

#Zona critica
zcLetras = ["","","",""]
zcNumeros = ["","","",""]
archivos = [None] * (len(tipoLetra)+len(tipoNumero))

#declaracion de semaforos
semGlobal = th.Semaphore(1)
semArchivo = th.Semaphore(1)
semZonaCriticaL = [None] * TamBuffer
semZonaCriticaN = [None] * TamBuffer

#creacion de los semaforos del buffer
for i in range(0,TamBuffer):
    semZonaCriticaL[i] = th.Semaphore()
    semZonaCriticaN[i] = th.Semaphore()

#creacion de nombres de archivos
for f in range(0,len(tipoLetra)):
    archivos[f] = "Archivo_" + str(tipoLetra[f]) + ".txt"
    archivos[f+len(tipoLetra)] = "Archivo_" + str(tipoNumero[f]) + ".txt"


# Funciones para los hilos
def productor(id):
    letra = tipoLetra[id]
    numero = tipoNumero[id]
    print("Hola soy el hilo productor ", id)
    aux = 0
    for i in range(Nproducciones*2):
        while True:
            #reseteo de indice
            if(aux == 3):
                aux = 0
            #Determina numero o letra
            if(i%2 is 0): #Numeros
                simbolo = numero
                semZonaCriticaN[aux].acquire()
                if(len(zcNumeros[aux]) is 0):
                    zcNumeros[aux] = simbolo
                    semZonaCriticaN[aux].release()
                    print(zcNumeros)
                    break
                else:
                    semZonaCriticaN[aux].release()
                    time.sleep(0.2)
                    aux += 1
            else: #Letras
                simbolo = letra
                semZonaCriticaL[aux].acquire()
                if(len(zcLetras[aux]) is 0):
                    zcLetras[aux] = simbolo
                    semZonaCriticaL[aux].release()
                    print(zcLetras)
                    break
                else:
                    semZonaCriticaL[aux].release()
                    time.sleep(0.2)
                    aux += 1

def consumidor(id):
    aux = 0
    for i in range(Nproducciones*2):
        while True:
            #reseteo de indice
            if(aux == 3):
                aux = 0
            #consumir dependiendo de paridad
            if(i%2 is 0): #numeros
                semZonaCriticaN[aux].acquire()
                if (len(zcNumeros[aux]) is not 0):
                    letraR = zcNumeros[aux]
                    #escribiendo
                    #semArchivo.acquire()
                    if(letraR == tipoLetra[id]):
                        print(archivos[id])
                        """open(archivos[id])
                        archivos[id].write(letraR+"\n")
                        semArchivo.release()
                    if(letraR == tipoNumero[id]):
                        archivos[id+5].write(letraR+"\n")
                        semArchivo.release()"""

                    print("Consumidor "+str(id)+" consumiendo: ", letraR)
                    zcNumeros[aux] = ""
                    semZonaCriticaN[aux].release()
                    break
                else:
                    semZonaCriticaN[aux].release()
                    time.sleep(0.2)
                    aux += 1
            else: #letras
                semZonaCriticaL[aux].acquire()
                if (len(zcLetras[aux]) is not 0):
                    letraR = zcLetras[aux]
                    #escribiendo
                    #semArchivo.acquire()
                    if(letraR == tipoLetra[id]):
                        print(archivos[id])
                        """open(archivos[id])
                        archivos[id].write(letraR+"\n")
                        semArchivo.release()
                    if(letraR == tipoNumero[id]):
                        archivos[id+5].write(letraR+"\n")
                        semArchivo.release()"""

                    print("Consumidor "+str(id)+" consumiendo: ", letraR)
                    zcLetras[aux] = ""
                    semZonaCriticaL[aux].release()
                    break
                else:
                    semZonaCriticaL[aux].release()
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



print("Terminaron todos los hilos bye")

