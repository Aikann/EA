# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 16:52:35 2018

@author: guillaume.crognier
"""

from __future__ import division
from pyomo.environ import *
from PL import model
from xlwt import Workbook, easyxf
import pandas as pd
import numpy as np

data_filename='input'
bookings_filename='data_bookings_060218'
schedule_filename='data_schedule_060218'


opt = SolverFactory('cplex')

print('Création du modèle...')
instance = model.create_instance(data_filename+'.dat')
print('Résolution...')
results = opt.solve(instance)
print(results)
 
print("Ecriture...")

#Récupération de certaines données
wb = pd.read_csv(bookings_filename+'.csv',sep=';',encoding='latin-1')
bookings_names = np.array(wb['Id'])
bookings_position= np.array(wb[['MDP','LDP','LDC']].fillna(0))
wb = pd.read_csv(schedule_filename+'.csv',sep=';',encoding='latin-1')
aircraft_names = np.array(wb['Aircraft'])

#Création du workbook 
book = Workbook()
 
#Ajout de la feuille et des titres
feuil1 = book.add_sheet('feuille 1')
feuil1.write(0,0,'Id')#,style = easyxf('font: bold 1'))
feuil1.write(0,1,'Acceptation')
feuil1.write(0,2,'Aircraft')
feuil1.write(0,3,'MDP')
feuil1.write(0,4,'LDP')
feuil1.write(0,5,'LDC')

feuil1.write(0,7,'Aircraft')
feuil1.write(0,8,'Remplissage (%)')
feuil1.write(0,9,"Gain de l'avion")
feuil1.write(0,10,'Liste des colis')

feuil1.write(0,12,'Gain total')
feuil1.write(0,13,'Remplissage total (%)')

# Récupération du nombre de vols et de colis
cardV=instance.cardV.value
cardN=instance.cardN.value

#Ecriture des résultats
L=[[] for v in range(cardV)] # liste de la liste des colis
V=[0 for v in range(cardV)] # liste des volumes des avions
G=[0 for v in range(cardV)] # liste des gains des avions
for i in range(1,cardN+1):
    accepted=False
    feuil1.write(i,0,bookings_names[i-1])
    for v in range(1,cardV+1):    
        if instance.x[i,v].value>=0.999:
            L[v-1].append(bookings_names[i-1])
            V[v-1] += instance.V[i]
            G[v-1] += instance.g[i]
            feuil1.write(i,1,"Accepté")
            feuil1.write(i,2,aircraft_names[v-1])
            feuil1.write(i,3,int(bookings_position[i-1,0]))
            feuil1.write(i,4,int(bookings_position[i-1,1]))
            feuil1.write(i,5,int(bookings_position[i-1,2]))
            accepted=True
    if not accepted:
            feuil1.write(i,1,"Refusé")
V_tot=0
for v in range(1,cardV+1):
    V_tot += instance.V_max[v] 
    feuil1.write(v,7,aircraft_names[v-1])
    feuil1.write(v,8,100*V[v-1]/instance.V_max[v])
    feuil1.write(v,9,G[v-1])
    feuil1.write(v,10,str(L[v-1]))
feuil1.write(1,12,sum(G))
feuil1.write(1,13,100*sum(V)/V_tot)
                
book.save("output_"+bookings_filename+'2.xls')

print("Fini !")