import gizeh
import moviepy.editor as mpy
from random import random, randint
import numpy as np

class GVid():
    def __init__(self, labels, times, datafun, width=128, height=128, duration=2, fps=15, NbOfMax=10, rwidth=10, title=""):
        self.width = width
        self.height = height
        self.duration = duration
        self.fps = fps
        self.labels = labels
        self.times = times
        self.datafun = datafun
        self.changeColor()
        self.frame = 0
        self.NbOfMax = NbOfMax
        self.rwidth = rwidth
        self._title=title

    def make_frame(self, t):
        surface = gizeh.Surface(self.width,self.height)
        title = gizeh.text("{} ({})".format(self._title, self.times[self.frame] ), "Amiri", 20,fontweight='bold', xy=(self.width/2,self.height/10), fill=(0,1,0))
        title.draw(surface)
        bests = self.getNbest(self.frame, self.NbOfMax)

        for i in range(self.NbOfMax):
            nam, val = bests[i]
            rsize = int(val * self.width / bests[0][1]) - 20
            rect = gizeh.rectangle(lx=rsize, ly=self.rwidth, xy=(10+rsize/2,self.height/5+i*self.rwidth), fill=self.color[nam])
            rect.draw(surface)
            txt = gizeh.text(self.labels[nam], "Amiri", 10,fontweight='bold', xy=(10+rsize/2,self.height/5+i*self.rwidth), fill=(1,1,1))
            txt.draw(surface)
        self.frame += 1
        return surface.get_npimage()


    def getNbest(self, idtime, N=10):
        data = self.datafun(self.times[idtime])
        idmaxis = data[data[:,1].argsort()][-N:][::-1]
        # idmaxis = np.argpartition(data[:,1], -N)[-N:]
        # print(idmaxis)
        return idmaxis

    def changeColor(self):
        self.color = [(random()*0.8, random()*0.8, random()*0.8) for _ in self.labels]


    def makeGif(self, file="resultat.gif"):
        clip = mpy.VideoClip(self.make_frame, duration=self.duration)
        clip.write_gif(file,fps=self.fps, opt="OptimizePlus", fuzz=10)

    def makeVid(self, file="resultat.mp4"):
        clip = mpy.VideoClip(self.make_frame, duration=self.duration)
        clip.write_videofile(file, fps=self.fps, codec='libx264')

    def title(self, titl):
        self._title = titl

if __name__=="__main__":
    f = open("nat2017_txt/nat2017.txt", "r")
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
    vid.makeGif()
