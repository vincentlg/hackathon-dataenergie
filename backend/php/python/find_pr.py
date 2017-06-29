
# coding: utf-8

# In[1]:

import pandas as pd
import random
import math
import json

from sklearn.cluster import KMeans
from sklearn.externals import joblib


# In[2]:

# Les emplacements des PR sont remplaces par les emplacement des autolibs
dfBornesElec = pd.read_csv("IRVE-201605.csv")
dfBornesElecParis = dfBornesElec[dfBornesElec['adresse_station'].str.contains("PARIS") == True]
dfBornesElecParis.reset_index(drop=True, inplace=True)

latitude = list(dfBornesElecParis['latitude'])
longitude = list(dfBornesElecParis['longitude'])
# On considere que seulement 10 bornes sont utilisees
la = latitude[10:20]
lo = longitude[10:20]
postes = []
lDPr = []
for i,j in zip(la,lo):
    dPr = {}
    dPr["lat"] = round(float(i),6)
    dPr["lng"] = round(float(j),6)
    postes.append((round(float(i),6),round(float(j),6)))
    lDPr.append(dPr)

st = json.dumps(lDPr)


# In[3]:

# sauvegarde le json des Pr
with open("../php/resources/assets/json/Prospective.json", 'w') as f:
    f.write(st)
print(st)

joblib.dump(lDPr, "Prospective.pkl")

