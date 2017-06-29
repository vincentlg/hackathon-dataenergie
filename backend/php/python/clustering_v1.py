
# coding: utf-8

# In[1]:

import pandas as pd
import random
import math
import json
import sys

from sklearn.cluster import KMeans
from sklearn.externals import joblib

args = sys.argv
userLat, userLong = float(args[1]),float(args[2])
print(userLat, userLong)
# In[2]:

# Fonction de calcul de distance entre deux coordonnees gps
def calc_dist(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1))         * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d


# In[3]:

# Recupere les coordonnees des Pr
lDPr = joblib.load("/var/www/python/Prospective.pkl")
postes = []

for i in lDPr:
    postes.append((i["lat"],i["lng"]))


# In[4]:

# definition d'une zone dans laquelle les votes utilisateurs seront concentres
topLeft = (48.902559, 2.255868)
botLeft = (48.820147, 2.255868)
topRight = (48.902559, 2.423716)
botRight = (48.820147, 2.423716)


# In[5]:

# Creation d un jeu de donnees de votes simules
userdemand = []

for i in range(100):
    lat = round(random.uniform(48.820147, 48.902559),6)
    long = round(random.uniform(2.255868, 2.423716),6)
    #nbVote = random.randint(1,10)
    coord = (lat,long)
    d = 100000
    for poste in postes:
        dist = calc_dist(poste, coord)
        if dist < d:
            d = round(dist,4)
            postePP = poste
    #r = (lat,long, nbVote, postePP[0],postePP[1], d)
    r = (lat,long)
    userdemand.append(r)

userdemand.append((userLat, userLong))

df = pd.DataFrame(userdemand, columns=["latUser","longUser"])


# In[6]:

# Jeu d'entrainement
X_train = []
for ind, row in df.iterrows():
    X_train.append(row)

# Creation et entrainement d un model de clustering sur les votes
model = KMeans()

a = model.fit(X_train)


# In[7]:

# Correspondance entre cluster et vote utilisateur
lc = []

for ind , row in df.iterrows():
    pr = a.cluster_centers_[a.predict(row.values.reshape(1,-1))[0]]
    lc.append((pr[0],pr[1]))
# ajout de la correspondance de chaque point a chaque cluster dans le jeu de donnees
df["cluster"] = lc


# In[8]:

# Trouver le pr la plus proche des clusters

lCLuterPP = []

for i in a.cluster_centers_:
    coord = (i[0],i[1])
    d = 100000
    clusterPP = (0,0)
    for poste in postes:
        dist = calc_dist(poste, coord)
        if dist < d:
            d = round(dist,4)
            clusterPP = poste
    lCLuterPP.append((coord, clusterPP))
    
clusterPr = pd.DataFrame(lCLuterPP, columns=["cluster","pr"])


# In[9]:

# Creation d'un jeu de donnees qui fait le lien entre pr le plus proche et le vote

lpr = []
for ind, row in df.iterrows():
#     print(row["latUser"],row["longUser"],row["cluster"])
#     print(row["cluster"])
    pr = clusterPr.loc[clusterPr["cluster"] == row["cluster"]]
    i = pr.index[0]
    lpr.append(pr["pr"][i])
#print(len(lpr))

dff = df.copy()
del dff["cluster"]
dff["pr"] = lpr


# In[10]:

# Creation d un dict de sortie
dUserPr = {}
for ind, row in clusterPr.iterrows():
    o = dff.loc[dff.pr == row["pr"]]
    #print(o)
    dUserPr[row["pr"]] = []
    for i, r in o.iterrows():
        dUserPr[row["pr"]].append((r["latUser"], r["longUser"]))
print(dUserPr)

