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
 
 
def vacioLleno(lista):
    for i in lista:
        if i != "":
            lleno = 1
            break
        else:
            lleno = 0
    return lleno


# Funciones para los hilos
def productor(id):
    letra = tipoLetra[id]
    numero = tipoNumero[id]
    #print("Hola soy el hilo productor ", id)
    aux = 0
    for i in range(Nproducciones*2):
        while True:
            #reseteo de indice
            if(aux >= 3):
                aux = 0
            #Determina numero o letra
            if(i%2 is 0): #Numeros
                simbolo = numero
                semZonaCriticaN[aux].acquire()
                if(len(zcNumeros[aux]) is 0):
                    zcNumeros[aux] = simbolo
                    print("Hola soy el hilo productor " + str(id)+" produciendo: "+ simbolo)
                    #print(zcNumeros)
                    semZonaCriticaN[aux].release()
                    break
                else:
                    semZonaCriticaN[aux].release()
                    time.sleep(0.2)
                    aux += 1
                    break
            else: #Letras
                simbolo = letra
                semZonaCriticaL[aux].acquire()
                if(len(zcLetras[aux]) is 0):
                    zcLetras[aux] = simbolo
                    print("Hola soy el hilo productor " + str(id)+" produciendo: "+ simbolo)
                    semZonaCriticaL[aux].release()
                    #print(zcLetras)
                    break
                else:
                    semZonaCriticaL[aux].release()
                    time.sleep(0.2)
                    aux += 1
    print("Productor "+str(id)+" termino de producir")                
    

def consumidor(id):
    aux = 0
    zona = 0
    for i in range(Nproducciones*2):
        while True:
            #reseteo de indice
            if(aux == 3):
                aux = 0
                if(zona == 0):
                    zona = 1
                else:
                    zona = 0
            #consumir dependiendo de ZONA CRITICA
            if(zona == 0): #numeros
                if (len(zcNumeros[aux]) is not 0):
                    semZonaCriticaN[aux].acquire()
                    if (len(zcNumeros[aux]) is not 0):
                        letraR = zcNumeros[aux]
                        print("Consumidor "+str(id)+" consumiendo: ", letraR)
                        zcNumeros[aux] = ""
                        semZonaCriticaN[aux].release()
                        break
                    else:
                        print("Se registro una sobrescritura")
                        semZonaCriticaN[aux].release()
                        time.sleep(0.3)
                        aux += 1
                        #break
                else:
                    print("Hilo que muere =" + str(id))
                    print(zcLetras)
                    print(zcNumeros)
                    time.sleep(0.3)
                    aux += 1
            else: #letras
                
                if (len(zcLetras[aux]) is not 0):
                    semZonaCriticaL[aux].acquire()
                    if (len(zcLetras[aux]) is not 0):
                        letraR = zcLetras[aux]
                        print("Consumidor "+str(id)+" consumiendo: ", letraR)
                        zcLetras[aux] = ""
                        semZonaCriticaL[aux].release()
                    else:
                        print("Se registro una sobrescritura")
                        semZonaCriticaN[aux].release()
                        time.sleep(0.3)
                        aux += 1
                        #break
                        
                else:
                    semZonaCriticaL[aux].release()
                    print("Hilo que muere =" + str(id))
                    print(zcLetras)
                    print(zcNumeros)
                    time.sleep(0.3)
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

