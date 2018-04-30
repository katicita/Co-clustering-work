import numpy as np
import math
from scipy.spatial import distance
from biclustering.biclustering import MSR

class Medidas(object):
	def __init__(self):
		pass

	def get_average_volume(self, Is, Js):
	    num_cogrupos = len(Is)   
	    sum_volume = 0
	    for p in range(num_cogrupos):
	        sum_volume += len(Is[p]) * len(Js[p])
	        
	    average_volume = float (sum_volume) / num_cogrupos
	    return average_volume

	def get_standard_deviation(self, mean, Is, Js):
	    num_cogrupos = len(Is)
	    sum_dist = 0.0
	    for p in range(num_cogrupos):
	        volume = len(Is[p]) * len(Js[p])
	        dif = abs(volume - mean)
	        sum_dist += dif * dif
	    standard_deviation = math.sqrt(sum_dist / num_cogrupos)
	    return standard_deviation

	#Dada I e J (lineas e colunas) del grupo o cogrupo obtiene el grupo (g) o cogrupo (c) de X dependiendo de la opcion
	def get_grupo_cogrupo(self, X, I, J, option):
	    I.sort()
	    J.sort()
	    if option == 'g':
	        grupo = X[I]
	        return grupo
	    elif option == 'c':
	        cogrupo = X[I][:,J]
	        return cogrupo

	def get_average_MSR(self, X, Is, Js):
	    num_cogrupos = len(Is)
	    sum_msr = 0
	    for p in range(num_cogrupos):
	        grupo = self.get_grupo_cogrupo(X, Is[p], Js[p], 'c')
	        sum_msr += MSR(grupo).H
	    average_msr = float (sum_msr) / num_cogrupos
	    return average_msr

	def num_elementos_cogrupo(self, X, Is, Js):
	    n, m = X.shape
	    matriz_temp = np.zeros(n*m).reshape(n,m)
	    num_cogrupos = len(Is)
	    num_elementos = 0
	    for p in range(num_cogrupos):
	        for i in range(len(Is[p])):
	            for j in range(len(Js[p])):
	                if matriz_temp[Is[p][i]][Js[p][j]] == 0:
	                    matriz_temp[Is[p][i]][Js[p][j]] = 1
	                    num_elementos = num_elementos + 1
	                    
	    #print("matriz_temp %s" %matriz_temp)
	    return num_elementos

	def get_percentage_coverage(self, X, Is, Js):
	    n, m = X.shape
	    tot_elementos = n*m
	    num_elementos = self.num_elementos_cogrupo(X, Is, Js)
	    percentage_coverage = (float (num_elementos)*100)/(tot_elementos)
	    return percentage_coverage

	def get_percentage_occupancy(self, X, Is, Js):
	    n, m = X.shape
	    matriz_temp = np.zeros(n*m).reshape(n,m)
	    num_cogrupos = len(Is)
	    num_elementos = 0
	    occupancy = 0
	    for p in range(num_cogrupos):
	        for i in range(len(Is[p])):
	            for j in range(len(Js[p])):
	                if matriz_temp[Is[p][i]][Js[p][j]] == 0:
	                    matriz_temp[Is[p][i]][Js[p][j]] = 1
	                    num_elementos = num_elementos + 1
	                    if X[Is[p][i]][Js[p][j]] != 0:
	                        occupancy = occupancy + 1
	    
	    percentage_occupancy = float (occupancy*100) / num_elementos
	    return percentage_occupancy

	def get_percentage_overlap(self, X, Is, Js):
	    n, m = X.shape
	    matriz_temp = np.zeros(n*m).reshape(n,m)
	    num_cogrupos = len(Is)
	    num_elementos = 0
	    num_overlap = 0
	    for p in range(num_cogrupos):
	        for i in range(len(Is[p])):
	            for j in range(len(Js[p])):
	                if matriz_temp[Is[p][i]][Js[p][j]] == 0:
	                    matriz_temp[Is[p][i]][Js[p][j]] = 1
	                    num_elementos = num_elementos + 1
	                elif matriz_temp[Is[p][i]][Js[p][j]] == 1:
	                    matriz_temp[Is[p][i]][Js[p][j]] = 2
	                    num_overlap = num_overlap + 1
	    percentage_overlap = float (num_overlap * 100) / num_elementos
	    return percentage_overlap
	    
	    