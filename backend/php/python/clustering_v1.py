
# coding: utf-8

# In[1]:

import pandas as pd
import math
import json

from sklearn.cluster import KMeans
from sklearn.externals import joblib

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
#lDPr = joblib.load("Prospective.pkl")
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
with open("www/resources/assets/json/Users.json", 'r') as f:
    st = f.read()

newstr = st.replace("[", "")
nn1 = newstr.replace("]", "")
nn2 = nn1.replace("{", "")
nn = nn2.replace("}", "")
nnn = nn.split("}")

n4 = nnn[0].split(",")

latList = []
longList = []
i=0
while i < len(n4):
    latList.append(float(n4[i].replace('"lat": ', "")))
    longList.append(float(n4[i+1].replace('"lng": ', "")))
    i += 2

df = pd.DataFrame()
df["latUser"] = latList
df["longUser"] = longList

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
    pr = clusterPr.loc[clusterPr["cluster"] == row["cluster"]]
    i = pr.index[0]
    lpr.append(pr["pr"][i])

dff = df.copy()
del dff["cluster"]
dff["pr"] = lpr


# In[10]:

lUserPr = []
for ind, row in clusterPr.iterrows():
    dUserPr = {}
    o = dff.loc[dff.pr == row["pr"]]
    dUserPr['"lat"'] = row["pr"][0]
    dUserPr['"lng"'] = row["pr"][1]
    dUserPr['"points"'] = []
    for i, r in o.iterrows():
        dd = {}
        dd['"lat"'] = r["latUser"]
        dd['"lng"'] = r["longUser"]
        dUserPr['"points"'].append(dd)
    lUserPr.append(dUserPr)
print(lUserPr)