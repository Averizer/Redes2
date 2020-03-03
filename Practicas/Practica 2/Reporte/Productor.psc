Algoritmo Productores
	Para i<-0 Hasta Nproducciones Hacer
		Mientras True Hacer
			Si aux >= 4 Entonces
				aux = 0
			FinSi
			Si i%2 == 0 Entonces
				// V(SemGlobalN)
				// V(SemZonaCriticaN)
				Si zcNumeros = "" Entonces
					zcNumeros = simbolo
					prodN = prodN + 1
					totalProdN = totalProdN +1
					// P(semZonaCritN)
				SiNo
					// P(semZonaCriticaN)
					// P(semGlobalN)
					aux = aux + 1
				FinSi
			SiNo
				// V(SemGlobalL)
				// V(SemZonaCriticaL)
				Si zcLetras  = "" Entonces
					zcLetra = simbolo
					prodL = prodL + 1
					
					// P(SemCritL)
				SiNo
					// P(semZonaCriticaL)
					// P(semGlobalL)
					aux = aux + 1
				FinSi
			FinSi
		FinMientras
		Si prod  = Buffer Entonces
			// LiberarSemaforos
		FinSi
		Si prodGlobal = totalAproducir Entonces
			// Liberal semaforo global
		FinSi
	FinPara
FinAlgoritmo
