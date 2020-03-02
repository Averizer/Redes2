import re
import threading as th
import math as m
semZC1 = th.Semaphore(4)
#semZC2 = th.Semaphore(1)
zcLetras = [" " ," "," "," "]
nzcNumeros = ['\0','\0','\0','\0']
tipoLetra = ['A', 'B', 'C', 'D', 'E']
tipoNumero = ['1', '2', '3', '4', '5']

# Funciones para los hilos
def productor(id):
    letra = tipoLetra[id]
    numero = tipoNumero[id]
    print("Hola soy el hilo productor ", id)
    aux = 0
    for i in range(5):
        while True:
            #print("iterando en productor: "+ str(i))
            aux += 1
            if(aux == 3):
                aux = 0
            if(zcLetras[aux].isspace()):
                semZC1.acquire()
                zcLetras[aux] = letra
                semZC1.release()
                break
        #print(zcLetras)
    pass
 

def consumidor(id):
    for i in range(5):
        #print("Iteración numero: "+ str(i))
        aux = 0
        while True:
            if(aux == 3):
                aux = 0
            if not(zcLetras[aux].isspace()):
                semZC1.acquire()
                letraR = zcLetras[aux]
                print("Consumidor "+str(id)+" consumiendo: ", letraR)
                zcLetras[aux] = " "
                semZC1.release()
                break
    print("Consumidor "+str(id)+" termino de consumir")
    pass

hilosC = []
hilosP = []

#Creación de hilos
for i in range(5):
    t = th.Thread(name = ("Hilo " + str(i)), target = productor, args=(i,))
    hilosC.append(t)
    t2 = th.Thread(name = ("Hilo " + str(i)), target = consumidor, args=(i,))
    hilosP.append(t2)

#Inicializacion de hilos
for i in range(5):
    p = hilosC[i]
    p.start()
    p2 = hilosP[i]
    p2.start()

#Finalización de hilos    
for i in range(5):
    p = hilosC[i]
    p.join()
    p2 = hilosP[i]
    p2.join()


#clonacion y push realizados correctamente
