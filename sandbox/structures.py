import os
from collections import namedtuple
import pprint
from colorsys import hsv_to_rgb
import random
from time import sleep

import xtermcolor
from colorize import colorize

Pixel = namedtuple("Pixel",["r","g","b"])
class Strip():
    def __init__(self,length):
        self.pixels = [Pixel(0,0,0) for i in range(length)]
    def __setitem__(self, i, v):
        self.pixels[i] = v
class Section():
    def __init__(self,strip,start,end,fps=16,transitionFunc=lambda x:x):
        self.strip = strip
        self.fps =fps
        self.transitionFunc =transitionFunc
        self.end = end +1
        self.start =start
        self.length = end -start
    def __setitem__(self, i, v):
        self.strip[self.start+i] = v
    def __getitem__(self, i):
        return self.strip[self.start+i]
    def update(self):
        if globalFrameCounter % self.fps==0:
            self.strip.pixels[self.start:self.end] = list(map(self.transitionFunc,self.strip.pixels[self.start:self.end]))
        else:
            11==22
    def __str__(self):
        printPixel = lambda x:xtermcolor.colorize('a',ansi=int(16 + 36 * x.r + 6 * x.g + x.b))
        return ' '.join(map(printPixel,self.strip.pixels[self.start:self.end]))
    def __repr__(self):
        return self.__str__()
class SectionCollection():
    def __init__(self,strip,sectionCordsList=[[0,1]]):
        self.strip =strip
        self.sections=[]
        for num,sectionCords in enumerate(sectionCordsList):
            self.sections.append(Section(self.strip,sectionCords[0],sectionCords[1],fps=abs(6-num)+1))
            if num %2==0:
                self.sections[num].transitionFunc=blueCycleTransition
            else:
                self.sections[num].transitionFunc=redCycleTransition
    def update(self):
        for section in self.sections:
            section.update()
    def __str__(self):
        return '\n'.join([str(section) for section in self.sections])
    def __repr__(self):
        return self.__str__()



def transition(oldPixel):
    direction = 1 if random.randint(1,10) %2 ==0 else -1
    step = direction*random.random()/10
    NewPixel =Pixel(abs(round(oldPixel.r+step,2)),abs(round(oldPixel.g+step,2)),abs(round(oldPixel.b+step,2)),)
    return NewPixel
def redCycleTransition(oldPixel):
    NewPixel = Pixel((oldPixel.r+3)%5,oldPixel.b,oldPixel.g)
    return NewPixel
def blueCycleTransition(oldPixel):
    NewPixel = Pixel(oldPixel.r,(oldPixel.b +3)%5,oldPixel.g)
    return NewPixel

if __name__ =='__main__':

    globalFrameCounter =0
    size =30
    strip =Strip(30**2)
    sections =[[i,size+i] for i in range(0,size**2,size)]
    sc = SectionCollection(strip,sectionCordsList=sections)
    while 1==1:
        globalFrameCounter+=1
        sc.update()
        pprint.pprint(sc)
        sleep(.2)
        os.system('clear')
        pprint.pprint('')






