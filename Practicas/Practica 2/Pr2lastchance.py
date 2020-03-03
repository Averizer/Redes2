
import os
import threading
import time
import random
import sys
random.seed(69420)
NUM_PRODUCTORES = 4
NUM_CONSUMIDORES = 3
num_producciones_x_productor = 1000
limiteDeReleases=7 #Equivalente al tamaño de la seccion critica, es cuantos hilos productores pueden estar en ella a la vez
num_consumos_globales = 0
semContadorGlobalConsumos = threading.Semaphore(1)
semFile = threading.Semaphore(1)
tproductores = [None] * NUM_PRODUCTORES
tconsumidores = [None] * NUM_CONSUMIDORES
semInd = [None ]* limiteDeReleases
for i in range(0,limiteDeReleases):
    semInd[i] = threading.Semaphore()
bufferSecCrit= [ None] *limiteDeReleases
Words = ["111111","Hola Mundo", "555555", "666666"]
files = [None]* limiteDeReleases
for f in range(0,limiteDeReleases):
    files[f] = open("Consumos" + str(f) + ".txt","w+" )
#ConsumerFile = open("Consumos.txt", "w+" )
def Productor():
    global bufferSecCrit
    global Words
    global NUM_PRODUCTORES
    global NUM_CONSUMIDORES
    global num_producciones_x_productor
    global semInd
    global num_consumos_globales
    global limiteDeReleases
    global ConsumerFile
    num_producciones = 0
    j=0
    #print("---PRODUCTOR starting----\n---Valor SemGlobConsu "+ str(semGlobCons._value) +"\tValor SemGlobProduc: " + str(semGlobPro._value))
    #semGlobPro.acquire()

    #for i in range(0, num_producciones_x_productor):
    while (num_producciones < num_producciones_x_productor):
        #print("J antes del sem",j)
        #semGlobPro.acquire()
        #print("Valor de J " + str(j) + " Valor de i: ", i )
        if (j >= limiteDeReleases):
            j = 0
        print(threading.current_thread().name)
        print("# de Producciones: "+ str(num_producciones)+ " del thread:"+ str(threading.get_ident()) + "\nValor de J " + str(j) + " Valor de i: "+ str(i))
        print("Thread: "+ threading.current_thread().name + " # de Producciones realizadas: "+ str(num_producciones)+  "\tValor de J " + str(j) )
        #semGlob.acquire()
        semInd[j].acquire()
        if not bufferSecCrit[j] :
            bufferSecCrit[j] = Words[j]
            #print("Produciendo en seccion: "+ str(j)+ " la cadena:" + str(bufferSecCrit[j] ) +" Por el Thread: "+ threading.current_thread().name + " Produccion numero:" + str(num_producciones+1))
            num_producciones=num_producciones +1
            semInd[j].release()
            print(bufferSecCrit)
            #print("Valor SemGlobConsu "+ str(semGlobCons._value) +"Valor SemGlobProduc" + str(semGlobPro._value))
            j=j+1
        else:
            semInd[j].release()
            j = j+1
            time.sleep(0.2)



    #print("\n!!!!"+ threading.current_thread().name + "finished !!!!\n")

def Consumidor():
    global bufferSecCrit
    global NUM_PRODUCTORES
    global NUM_CONSUMIDORES
    global num_producciones_x_productor
    global num_consumos_globales
    global limiteDeReleases
    global semInd
    global ConsumerFiles
    j=0
    #print(".....CONSUMIDOR starting......")
    while(num_consumos_globales <= num_producciones_x_productor*NUM_PRODUCTORES):
        if (num_consumos_globales == (num_producciones_x_productor*NUM_PRODUCTORES) ):
            sys.exit()
        if (j>= limiteDeReleases):
            j=0
        for j in range(0, limiteDeReleases):
            #semGlobCons.acquire()
            semInd[j].acquire()
            if bufferSecCrit[j] :
                semContadorGlobalConsumos.acquire()
                semFile.acquire()
                #print("###Consumo"+ str(num_consumos_globales)+" de: "+ str(num_producciones_x_productor*NUM_PRODUCTORES) +"### \n####Valor SemGlobProductor "+ str(semGlobPro._value) + " Valor SemGlobConsu "+ str(semGlobCons._value) )
                #print("\nConsumiendo en seccion: "+ str(j) + "la cadena: " bufferSecCrit[j] )

                #ConsumerFile.write(bufferSecCrit[j] + "\n")
                files[j].write(bufferSecCrit[j] + "\n")

                print("\t thread: "+ threading.current_thread().name +" num_consumos_globales: "+ str(num_consumos_globales) + " Valor de j" + str(j) + "\n###Consumiendo en seccion: "+ str(j) + " la cadena: " + bufferSecCrit[j] )
                #print("\tla cadena:" + str(bufferSecCrit[j] ) )
                bufferSecCrit[j] = ""

                num_consumos_globales = num_consumos_globales + 1
                semFile.release()
                semContadorGlobalConsumos.release()
                print(bufferSecCrit)
                semInd[j].release()
                #print("###Valor SemGlobProductor##"+ str(semGlobPro._value) + " Valor SemGlobConsu "+ str(semGlobCons._value) +"####" )
            else:
                semInd[j].release()
                time.sleep(1)

y=0
for i in range(0,NUM_PRODUCTORES):
    tproductores[i] = threading.Thread(target = Productor, name = "Productor" + str(i) )
for i in range(0,NUM_CONSUMIDORES):
    tconsumidores[i] = threading.Thread(target = Consumidor, name = "Consumidor" + str(i) )

if (NUM_PRODUCTORES >= NUM_CONSUMIDORES):
    for j in range(0, NUM_PRODUCTORES):
        tproductores[j].start()
        if (y < NUM_CONSUMIDORES):
            tconsumidores[y].start()
            y=y+1
else:
    for j in range(0, NUM_CONSUMIDORES):
        tconsumidores[j].start()
        if (y < NUM_PRODUCTORES):
            tproductores[y].start()
            y=y+1
for i in range(0,NUM_PRODUCTORES):
    tproductores[i].join()
for i in range(0,NUM_CONSUMIDORES):
    tconsumidores[i].join()

print("\nNum cons global:" + str(num_consumos_globales) + "  Seccion Critica: \n")
print(bufferSecCrit)
#ConsumerFile.close()
for f in range(0,limiteDeReleases):
    files[f].close()
print("All Threads done Exiting")