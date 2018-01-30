# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 14:30:07 2017

@author: QVRP3307
"""

from __future__ import division
from pyomo.environ import *
from random import *

model = AbstractModel()


"""DECLARATION DES PARAMETRES 1D"""

model.cardN = Param(within=NonNegativeIntegers) #nombre de colis
model.cardV = Param(within=NonNegativeIntegers) #nombre de vols
#model.cardK = Param(within=NonNegativeIntegers) #nombre de type de soutes



"""DECLARATION DES PARAMETRES ENSEMBLISTES"""

model.indexN = RangeSet(model.cardN) # [N]
model.indexV = RangeSet(model.cardV) # [V]
#model.indexK = RangeSet(model.cardK) # [K]

model.V = Param(model.indexN, within=NonNegativeReals) #volume des colis
model.W = Param(model.indexN, within=NonNegativeReals) #poids des colis

model.V_max = Param(model.indexV, within=NonNegativeReals) #volume max des avions
model.W_max = Param(model.indexV, within=NonNegativeReals) #poids max des avions

#model.t_d = Param(model.indexN, within=NonNegativeReals) #date de dispo des colis
#model.t_f = Param(model.indexN, within=NonNegativeReals) #date de d'arrivée des colis
#model.T_d = Param(model.indexV, within=NonNegativeReals) #date de départ des vols
#model.T_f = Param(model.indexV, within=NonNegativeReals) #date de d'arrivée des vols

#model.s = Param(model.indexN, model.indexK, within=NonNegativeIntegers) #nombre de compartiments de type k nécessaires pour le colis i
#model.S_max = Param(model.indexV, model.indexK, within=NonNegativeIntegers) #nombre de compartiments de type k disponibles dans le vol v

model.p = Param(model.indexN, within=Binary) #colis périssable
model.r = Param(model.indexN, within=Binary) #colis radioactif


"""DECLARATION DES VARIABLES"""

model.x = Var(model.indexN, model.indexV, domain=Binary) #variable indiquant si le colis i est pris par le vol v
model.R = Var(model.indexV, domain=Binary) #vol considéré comme transportant des colis radioactifs
model.P = Var(model.indexV, domain=Binary) #vol considéré comme transportant des colis périssables



"""DECLARATION DE L'OBJECTIF"""

def ObjRule(model): #volume restant
    V_restant = 0
    for v in range(1,model.cardV+1):
        S=sum([model.V[i] * model.x[i,v] for i in range(1,model.cardN+1)])
        V_restant += model.V_max[v] - S    
    return V_restant
model.OBJ = Objective(rule=ObjRule)



"""DECLARATION DES CONTRAINTES"""

def Volume_Max(model,v): #volume max des avions
    return (sum([model.V[i]*model.x[i,v] for i in range(1,model.cardN+1)]) <= model.V_max[v])    
model.C2 = Constraint(model.indexV, rule=Volume_Max)



def Poids_Max(model,v): #poids max des avions
    return (sum([model.W[i]*model.x[i,v] for i in range(1,model.cardN+1)]) <= model.W_max[v])   
model.C3 = Constraint(model.indexV, rule=Poids_Max)



def Timing_depart(model,i): #un colis ne part que s'il est dispo
    return (model.t_d[i] <= sum([model.T_d[v]*model.x[i,v] for v in range(1,model.cardV+1)]))
#model.C4 = Constraint(model.indexN, rule=Timing_depart)



def Timing_arrivee(model,i): #un colis ne part que s'il arrive à temps
    return (sum([model.T_f[v]*model.x[i,v] for v in range(1,model.cardV+1)]) <= model.t_f[i])
#model.C5 = Constraint(model.indexN, rule=Timing_arrivee)



def Depart_unique(model,i): #tout colis ne part qu'au plus une fois
    return(sum([model.x[i,v] for v in range(1,model.cardV+1)]) <= 1)
model.C6 = Constraint(model.indexN, rule=Depart_unique)



def Gestion_palette(model, v, k): #satisfaire les demandes de position des colis
    return (sum(model.x[i,v]*model.s[i,k] for i in model.indexN) <= model.S_max[v,k])
#model.C7 = Constraint(model.indexV, model.indexK, rule=Gestion_palette)



def Perissable_radioactif(model,v): #ne pas avoir des denrées périssables en soute avec des objets radioactifs
    return (model.R[v]+model.P[v] <= 1)
model.C8 = Constraint(model.indexV, rule=Perissable_radioactif)



def Avion_radioactif(model,i,v): #permet de savoir si un avion transporte un colis périssable
    return(model.R[v] >= model.r[i]*model.x[i,v])
model.C9 = Constraint(model.indexN, model.indexV, rule=Avion_radioactif)



def Avion_perissable(model,i,v): #permet de savoir si un avion transporte un colis périssable
    return(model.P[v] >= model.p[i]*model.x[i,v] )
model.C10 = Constraint(model.indexV, rule=Avion_perissable)