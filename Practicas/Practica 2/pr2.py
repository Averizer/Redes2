import re
import threading as th
import math as m
import time

#Constantes
productores = 5
consumidores = 5
Nproducciones = 3
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
    semZonaCriticaL[i] = th.Semaphore(1)
    semZonaCriticaN[i] = th.Semaphore(1)

#creacion de nombres de archivos
for f in range(0,len(tipoLetra)):
    archivos[f] = "Archivo_" + str(tipoLetra[f]) + ".txt"
    archivos[f+len(tipoLetra)] = "Archivo_" + str(tipoNumero[f]) + ".txt" 


# Funciones para los hilos
def productor(id):
    letra = tipoLetra[id]
    numero = tipoNumero[id]
    #print("Hola soy el hilo productor ", id)
    aux = 0
    for i in range(Nproducciones*2):
        while True:
            
            #reseteo de indice
            if(aux == 3):
                aux = 0
            #Determina numero o letra
            if(i%2 == 0): #Numeros
                simbolo = numero
                if(len(zcNumeros[aux]) is 0):
                    semZonaCriticaN[aux].acquire()
                    if(len(zcNumeros[aux]) is 0):
                        zcNumeros[aux] = simbolo
                        #print("Hola soy el hilo productor " + str(id)+" produciendo: "+ simbolo)
                        semZonaCriticaN[aux].release()
                        time.sleep(0.2)
                        break
                    else:
                        #semZonaCriticaN[aux].release()
                        aux += 1
                               
            else: #Letras
                simbolo = letra
                if(len(zcNumeros[aux]) is 0):
                    semZonaCriticaL[aux].acquire()
                    if(len(zcNumeros[aux]) is 0):
                        zcLetras[aux] = simbolo
                        #print("Hola soy el hilo productor " + str(id)+" produciendo: "+ simbolo)
                        semZonaCriticaL[aux].release()
                        time.sleep(0.2)
                        break
                else:
                    semZonaCriticaL[aux].release()
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
            #consumir dependiendo de paridad
            if(zona == 0): #numeros
                
                if (len(zcNumeros[aux]) is not 0):
                    semZonaCriticaN[aux].acquire()
                    if (len(zcNumeros[aux]) is not 0):
                        letraR = zcNumeros[aux]
                    #escribiendo
                    #semArchivo.acquire()
                        """if(letraR == tipoLetra[id]):
                            print(archivos[id])
                        open(archivos[id])
                        archivos[id].write(letraR+"\n")
                        semArchivo.release()
                    if(letraR == tipoNumero[id]):
                        archivos[id+5].write(letraR+"\n")
                        semArchivo.release()"""

                        print("Consumidor "+str(id)+" consumiendo: "+ letraR+ " iteracion: "+str(i))
                        zcNumeros[aux] = ""
                        semZonaCriticaN[aux].release()
                        print("El valor del semaforo "+ str(id)+" Es "+ str(semZonaCriticaN[aux]._value))
                        time.sleep(0.3)
                        break
                    else:
                        #semZonaCriticaN[aux].release()
                        time.sleep(0.3)
                        aux += 1
                        
                else:
                    #semZonaCriticaN[aux].release()
                    aux += 1
                    time.sleep(0.3)
            else: #letras
                
                if (len(zcLetras[aux]) is not 0):
                    semZonaCriticaL[aux].acquire()
                    if (len(zcLetras[aux]) is not 0):
                        letraR = zcLetras[aux]
                        #escribiendo
                        #semArchivo.acquire()
                        """if(letraR == tipoLetra[id]):
                            print(archivos[id])
                            open(archivos[id])
                            archivos[id].write(letraR+"\n")
                            semArchivo.release()
                        if(letraR == tipoNumero[id]):
                            archivos[id+5].write(letraR+"\n")
                            semArchivo.release()"""

                        
                        print("Consumidor "+str(id)+" consumiendo: "+ letraR+ " iteracion: "+str(i))
                        zcLetras[aux] = ""
                        semZonaCriticaL[aux].release()
                        time.sleep(0.4)
                        break
                    else:
                        #semZonaCriticaL[aux].release()
                        time.sleep(0.4)
                        aux += 1
                        
                        
                else:
                    #semZonaCriticaL[aux].release()
                    aux += 1
                    time.sleep(0.4)
    semZonaCriticaL[aux].release()
    semZonaCriticaN[aux].release()
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