import numpy as np
from gvid import GVid

f = open("nat2017.txt", "r")
lines = f.readlines()[1:]
data = np.array([line.split("\t") for line in lines])
dat = data[data[:,2].argsort()]

labels = np.unique(data[:,1])
times = np.unique(data[:,2])

def datai(annee):
    ind = np.where(dat[:,2] == str(annee))
    arr = dat[:,[1,3]][min(ind[0]):max(ind[0])]
    for i in arr:
        inde = np.where(labels==i[0])
        i[0] = inde[0][0]
    return arr.astype("int")


vid = GVid(labels, times, datai,  duration=29, fps=4, width=512, height=512, NbOfMax=20, rwidth=20)
vid.title("Top prénom en france par année")
vid.makeVid()
# or vid.makeGif()
