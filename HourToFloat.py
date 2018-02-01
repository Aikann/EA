# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 14:26:46 2018

@author: guillaume.crognier
"""

def HourToFloat(x):
    a=x.split(":")
    h=float(a[0])
    m=float(a[1])/60
    return h+m