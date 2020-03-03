import re
import threading as th
import math as m
import time

#Constantes
productores = 5 #numero de productores
consumidores = 5 #numero de consumidores
Nproducciones = 3 #numero de producciones
TamBuffer = 4   #tamaño del buffer o seccion crítica
tipoLetra = ['A', 'B', 'C', 'D', 'E']   #elementos de productores
tipoNumero = ['1', '2', '3', '4', '5']  #elementos de productores

#variables

#Letras
produccionesL = 0 #determina si las producciones son el numero de la zona
consumidosL = 0  #determina si se han consumido todas las producciones
totalproducidoL = 0 #determina si se han acabado todas las producciones
totalAproducirL = productores * Nproducciones #total de producciones
totalconsumidoL = 0
totalAconsumirL = consumidores * Nproducciones
#numeros
produccionesN = 0 #determina si las producciones son el numero de la zona
consumidosN = 0  #determina si se han consumido todas las producciones
totalproducidoN = 0 #determina si se han acabado todas las producciones
totalAproducirN = productores * Nproducciones #total de producciones
totalconsumidoN = 0
totalAconsumirN = consumidores * Nproducciones

#Zona critica
zcLetras = ["","","",""]    
zcNumeros = ["","","",""]
archivos = [None] * (len(tipoLetra)+len(tipoNumero))
indices = [None] * (len(tipoLetra)+len(tipoNumero))

#declaracion de semaforos
semGlobalLL = th.Semaphore(0)    #indice lleno de letras
semGlobalVL = th.Semaphore(4)    #indica vacio de letras
semZonaCriticaL = [None] * TamBuffer    #zona critica para las letras

semGlobalLN = th.Semaphore(0)    #indice lleno de numeros
semGlobalVN = th.Semaphore(4)    #indica vacio de numeros
semZonaCriticaN = [None] * TamBuffer    #zona critica para los numeros

semArchivo = th.Semaphore(1)    #para bloquear el archivo

#creacion de los semaforos del buffer
for i in range(0,TamBuffer):
    semZonaCriticaL[i] = th.Semaphore()
    semZonaCriticaN[i] = th.Semaphore()

#creacion de nombres de archivos
for f in range(0,len(tipoLetra)):
    indices[f] = str(tipoLetra[f] + ".txt")
    indices[f+len(tipoLetra)] = str(tipoNumero[f] + ".txt") 
    archivos[f] = open(str(tipoLetra[f]) + ".txt","w+" )
    archivos[f+len(tipoLetra)] = open(str(tipoNumero[f]) + ".txt","w+" )    

# Funciones para los hilos
def productor(id):
    global zcLetras
    global zcNumeros
    global semZonaCriticaL
    global semZonaCriticaN
    global produccionesL
    global totalproducidoL
    global produccionesN
    global totalproducidoN

    letra = tipoLetra[id]
    numero = tipoNumero[id]
    #print("Hola soy el hilo productor ", id)
    aux = 0
    for i in range(Nproducciones*2):
        while True:
            #reseteo de indice
            if(aux >= 4):
                aux = 0

            if(i%2 == 0):
                simbolo = numero
                semGlobalVN.acquire()
                semZonaCriticaN[aux].acquire()

                if(len(zcNumeros[aux]) is 0):
                    zcNumeros[aux] = simbolo
                    print("Hola soy el hilo productor " + str(id)+" produciendo: "+ simbolo)
                    produccionesN += 1
                    totalproducidoN += 1
                    #print(zcLetras)
                    #print(producciones)
                    semZonaCriticaN[aux].release()
                    break
                
                else:
                    semZonaCriticaN[aux].release()
                    semGlobalVN.release()
                    time.sleep(0.2)
                    aux += 1

            else:
                simbolo = letra
                semGlobalVL.acquire()
                semZonaCriticaL[aux].acquire()
                
                if(len(zcLetras[aux]) is 0):
                    zcLetras[aux] = simbolo
                    print("Hola soy el hilo productor " + str(id)+" produciendo: "+ simbolo)
                    produccionesL += 1
                    totalproducidoL += 1
                    #print(zcLetras)
                    #print(producciones)
                    semZonaCriticaL[aux].release()
                    break
                
                else:
                    semZonaCriticaL[aux].release()
                    semGlobalVL.release()
                    time.sleep(0.2)
                    aux += 1
        #letras
        if(produccionesL == 4):
            semGlobalLL.release()
            semGlobalLL.release()
            semGlobalLL.release()
            semGlobalLL.release()
            produccionesL = 0
        
        if(totalproducidoL == totalAproducirL):
            for i in range(produccionesL):
                semGlobalLL.release()
        
        #numeros
        if(produccionesN == 4):
            semGlobalLN.release()
            semGlobalLN.release()
            semGlobalLN.release()
            semGlobalLN.release()
            produccionesN = 0
        
        if(totalproducidoN == totalAproducirN):
            for i in range(produccionesN):
                semGlobalLN.release()

            
    print("Productor "+str(id)+" termino de producir")                
    

def consumidor(id):
    global zcLetras
    global zcNumeros
    global semZonaCriticaL
    global semZonaCriticaN
    global consumidosL
    global totalconsumidoL
    global consumidosN
    global totalconsumidoN

    aux = 0
    zona = 0
    for i in range(Nproducciones*2):
        while True:
            #reseteo de indice
            if(aux >= 4):
                aux = 0
            
            if(i%2 == 0):
                semGlobalLN.acquire()
                semZonaCriticaN[aux].acquire()
                if(len(zcNumeros[aux]) is not 0):
                    letraR = zcNumeros[aux]
                    print("Consumidor "+str(id)+" consumiendo: "+ letraR+ " iteracion: "+str(i))
                    zcNumeros[aux] = ""
                    consumidosN += 1
                    totalconsumidoN += 1
                    semArchivo.acquire()
                    indice = indices.index(str(letraR)+".txt")
                    archivos[indice].write(letraR + "\n")
                    semArchivo.release()
                    semZonaCriticaN[aux].release()
                    #print(zcLetras)
                    #print(consumidos)
                    break
                    
                else:
                    semZonaCriticaN[aux].release()
                    semGlobalLN.release()
                    time.sleep(0.2)
                    aux += 1
            else:
                semGlobalLL.acquire()
                semZonaCriticaL[aux].acquire()
                if(len(zcLetras[aux]) is not 0):
                    letraR = zcLetras[aux]
                    print("Consumidor "+str(id)+" consumiendo: "+ letraR+ " iteracion: "+str(i))
                    zcLetras[aux] = ""
                    consumidosL += 1
                    totalconsumidoL += 1
                    semArchivo.acquire()
                    indice = indices.index(str(letraR)+".txt")
                    archivos[indice].write(letraR + "\n")
                    semArchivo.release()
                    semZonaCriticaL[aux].release()
                    #print(zcLetras)
                    #print(consumidos)
                    break
                    
                else:
                    semZonaCriticaL[aux].release()
                    semGlobalLL.release()
                    time.sleep(0.2)
                    aux += 1

        #Letras
        if(consumidosL == 4):
            semGlobalVL.release()
            semGlobalVL.release()
            semGlobalVL.release()
            semGlobalVL.release()
            consumidosL = 0

        if(totalconsumidoL == totalAconsumirL):
            break

        #Numeros
        if(consumidosN == 4):
            semGlobalVN.release()
            semGlobalVN.release()
            semGlobalVN.release()
            semGlobalVN.release()
            consumidosN = 0

        if(totalconsumidoN == totalAconsumirN):
            break

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


for f in range(0,len(tipoLetra)):
    archivos[f].close()

print("Terminaron todos los hilos bye")
