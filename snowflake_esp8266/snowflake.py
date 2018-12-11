from machine import Pin
import neopixel
import random
from time import sleep_ms

npd=[
0x000000, 0x060000, 0x000000, 0x000000, 
0x000000, 0x000000, 0x000000, 0x000000, 
0x000000, 0x000000, 0x000000, 0x000000, 
0x0A0000, 0x060000, 0x000060, 0x000000, 
0x000000, 0x060000, 0x060060, 0x0A00A0, 
0x0F0000, 0x000000, 0x000000, 0x000000, 
0x000000, 0x000000, 0x0F0000, 0x0A00F0, 
0x0A00A0, 0x060060, 0x000060, 0x000000, 
0x024024, 0x060024, 0x060060, 0x0A00A0, 
0x0F00A0, 0x0F00F0, 0x000000, 0x000000, 
0x000000, 0x000000, 0x0F0000, 0x0A00F0, 
0x0A00A0, 0x060060, 0x000060, 0x000000, 
0x000000, 0x060000, 0x060060, 0x0A00A0, 
0x0F0000, 0x000000, 0x000000, 0x000000, 
0x000000, 0x000000, 0x000000, 0x000000, 
0x0A0000, 0x060000, 0x000060, 0x000000, 
0x000000, 0x060000, 0x000000, 0x000000, 
0x000000, 0x000000, 0x000000, 0x000000, 
0x000000, 0x000000, 0x000000, 0x000000, 
0x000000, 0x000000, 0x000000, 0x000000, 
0x000000, 0x000000, 0x000000, 0x000000, 
0x000000, 0x000000, 0x000000, 0x000000, 
0x000000, 0x000000, 0x000000, 0x000000, 
0x000000, 0x000000, 0x000000, 0x000000, 
0x000000, 0x000000, 0x000000, 0x000000, 
0x000000, 0x000000, 0x000000, 0x000000, 
0x000000, 0x000000, 0x000000, 0x000000, 
0x000000, 0x000000, 0x000000, 0x000000, 
0x000000, 0x000000, 0x000000, 0x000000, 
0x000000, 0x000000, 0x000000, 0x000000, 
0x000000, 0x000000, 0x000000, 0x000000, 
0x000000, 0x000000, 0x000000, 0x000000, 
]

class snowflake:
    def __init__(self, pin, npd, pileup=0, TH=32, perc=50, mpt=3, delay=50):
        self.np = neopixel.NeoPixel(pin, 256)
        self.img(npd)
        self.pileup = pileup
        self.TH = TH
        self.perc = perc
        self.mpt = mpt
        self.delay = delay
        self.snow = [] # 0: row, 1: col, 2:bright
        self.pile = [[0]*16,[0]*16,[0]*16,[0]*16,[TH]*16]
    
    def rand(self, n):
        return random.getrandbits(16)%n

    def clear(self):
        self.np.fill((0,0,0))
        self.np.write()

    def set(self, row, col, color):
        if col%2:
            self.np[col*16+15-row] = color
        else:
            self.np[col*16+row] = color

    def get(self, row, col):
        if col%2:
            return self.np[col*16+15-row]
        else:
            return self.np[col*16+row]

    def ColorOverlay(self, row, col, color, add):
        c = self.get(row, col)
        if add:
            self.set(row, col, [c[0]+color[0],c[1]+color[1],c[2]+color[2]])
        else:
            self.set(row, col, [c[0]-color[0],c[1]-color[1],c[2]-color[2]])

    def img(self,dat,pos=0,update=1):
        for x in range(16):
            for y in range(8):
                if ((x+pos)*8)>=len(dat):
                    self.np[x*16+y*2]=(0,0,0)
                    self.np[x*16+y*2+1]=(0,0,0)
                else:
                    t=dat[(x+pos)*8+y]
                    r=t%16
                    g=(t>>4)%16
                    b=(t>>8)%16
                    if pos%2:
                        self.np[x*16+y*2]=(r,g,b) 
                    else:
                        self.np[x*16+15-y*2]=(r,g,b)
                    r=(t>>12)%16
                    g=(t>>16)%16
                    b=(t>>20)%16
                    if pos%2:
                        self.np[x*16+y*2+1]=(r,g,b) 
                    else:
                        self.np[x*16+14-y*2]=(r,g,b)
        if update:
            self.np.write()

    def _line(self):
        for i in range(16):
            if self.pile[3][i]<self.TH:
                return
        for i in range(16):
            self.ColorOverlay(15,i,[16,0,0],1)
        self.np.write()
        sleep_ms(500)
        for i in range(16):
            self.ColorOverlay(15,i,[16,0,0],0)
        
        for j in range(3):
            for i in range(16):
                if self.pile[3-j][i]>=self.TH:
                    self.ColorOverlay(15-j,i,[8,8,8],0)
            self.np.write()
            sleep_ms(100)
            for i in range(16):
                self.pile[3-j][i]=self.pile[2-j][i]
                if self.pile[3-j][i]>=self.TH:
                    self.ColorOverlay(15-j,i,[8,8,8],1)
            self.np.write()
            sleep_ms(100)
        for i in range(16):
            if self.pile[0][i]>=self.TH:
                self.ColorOverlay(12,i,[8,8,8],0)
        self.pile[0]=[0]*16

    def _del(self):
        n = len(self.snow)
        if self.pileup:
            for i in range(n):
                c = self.snow[n-1-i]
                row = c[0]
                col = c[1]
                if row<12:
                    continue
                if col == 0:
                    a = 1
                    b = self.pile[row-11][col+1]>=self.TH
                elif col == 15:
                    a = self.pile[row-11][col-1]>=self.TH
                    b = 1
                else:
                    a = self.pile[row-11][col-1]>=self.TH
                    b = self.pile[row-11][col+1]>=self.TH
                if self.pile[row-11][col]>=self.TH:
                    self.ColorOverlay(c[0],c[1],[c[2],c[2],c[2]],0)
                    if a and b:
                        if self.pile[row-12][col]<self.TH:
                            self.pile[row-12][col]+=c[2]
                            if self.pile[row-12][col]>=self.TH:
                                self.ColorOverlay(c[0],c[1],[8,8,8],1)
                                self._line()
                    self.snow.pop(n-1-i)
        else:
            for i in range(n):
                c = self.snow[n-1-i]
                if c[0] > 14:
                    self.ColorOverlay(c[0],c[1],[c[2],c[2],c[2]],0)
                    self.snow.pop(n-1-i)

    def _new(self):
        if self.rand(100)<=self.perc:
            for i in range(self.mpt):
                self.snow.append([-1, self.rand(16), self.rand(15)+1])

    def _fall(self):
        for i in range(len(self.snow)):
            c=self.snow[i]
            if c[0]>-1:
                self.ColorOverlay(c[0],c[1],[c[2],c[2],c[2]],0)
            c[0] += 1
            c[1] += 1-self.rand(3)
            c[1]=max(0, min(c[1], 15))
            self.ColorOverlay(c[0],c[1],[c[2],c[2],c[2]],1)

    def start(self):
        while True:
            if len(self.snow) > 0:
                self._fall()
                self.np.write()
                self._del()

            self._new()
            sleep_ms(self.delay)


np = snowflake(Pin(2), npd, pileup=1)
np.start()
