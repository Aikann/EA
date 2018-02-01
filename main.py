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
bookings_filename='data_bookings_300118'
schedule_filename='data_schedule_300118'


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

# Récupération du nombre de vols et de colis
cardV=instance.cardV.value
cardN=instance.cardN.value

#Ecriture des résultats
for i in range(1,cardN+1):
    accepted=False
    feuil1.write(i,0,bookings_names[i-1])
    for v in range(1,cardV+1):    
        if instance.x[i,v]==1:
            feuil1.write(i,1,"Accepté")
            feuil1.write(i,2,aircraft_names[v-1])
            feuil1.write(i,3,int(bookings_position[i-1,0]))
            feuil1.write(i,4,int(bookings_position[i-1,1]))
            feuil1.write(i,5,int(bookings_position[i-1,2]))
            accepted=True
    if not accepted:
            feuil1.write(i,1,"Refusé")
                
book.save("output_"+bookings_filename+'.xls')

print("Fini !")