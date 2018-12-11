from microbit import pin1, sleep, reset
from neopixel import NeoPixel
from random import randint
import gc

pileup=1
TH=2
perc=50
mpt=1
snow = []
pile = [[0]*16,[0]*16,[0]*16,[0]*16,[TH]*16]

np = NeoPixel(pin1, 256)

def rand(n):
  return randint(0,n-1)

def set(row, col, color):
  if col%2:
    np[col*16+15-row] = color
  else:
    np[col*16+row] = color

def get(row, col):
  if col%2:
    return np[col*16+15-row]
  else:
    return np[col*16+row]

def ColorOverlay(row, col, color, add):
  c = get(row, col)
  if add:
    set(row, col, [c[0]+color[0],c[1]+color[1],c[2]+color[2]])
  else:
    set(row, col, [c[0]-color[0],c[1]-color[1],c[2]-color[2]])

def showimg(dat):
  for x in range(9):
    for y in range(8):
      t=dat[x*8+y]
      r=t%16
      g=(t>>4)%16
      b=(t>>8)%16
      np[x*16+15-y*2]=(r,g,b)
      r=(t>>12)%16
      g=(t>>16)%16
      b=(t>>20)%16
      np[x*16+14-y*2]=(r,g,b)

def _line():
  for i in range(16):
    if pile[3][i]<TH:
      return

  for i in range(16):
    ColorOverlay(15,i,[16,0,0],1)
  np.show()
  sleep(300)
  for i in range(16):
    ColorOverlay(15,i,[16,0,0],0)

  for j in range(3):
    for i in range(16):
      if pile[3-j][i]>=TH:
        ColorOverlay(15-j,i,[8,8,8],0)
      pile[3-j][i]=pile[2-j][i]
      if pile[3-j][i]>=TH:
        ColorOverlay(15-j,i,[8,8,8],1)
  for i in range(16):
    if pile[0][i]>=TH:
      ColorOverlay(12,i,[8,8,8],0)
  pile[0]=[0]*16

def _del():
  n = len(snow)
  if pileup:
    for i in range(n):
      c = snow[n-1-i]
      row = c[0]
      col = c[1]
      if row<12:
        continue
      if col == 0:
        a = 1
        b = pile[row-11][col+1]>=TH
      elif col == 15:
        a = pile[row-11][col-1]>=TH
        b = 1
      else:
        a = pile[row-11][col-1]>=TH
        b = pile[row-11][col+1]>=TH
      if pile[row-11][col]>=TH:
        ColorOverlay(c[0],c[1],[c[2],c[2],c[2]],0)
        if a and b:
          if pile[row-12][col]<TH:
            pile[row-12][col]+=c[2]
            if pile[row-12][col]>=TH:
              ColorOverlay(c[0],c[1],[8,8,8],1)
              _line()
        snow.pop(n-1-i)
  else:
    for i in range(n):
      c = snow[n-1-i]
      if c[0] > 14:
        ColorOverlay(c[0],c[1],[c[2],c[2],c[2]],0)
        snow.pop(n-1-i)

def _new():
  if rand(100)<=perc:
    for i in range(mpt):
      snow.append([-1, rand(16), rand(15)+1])

def _fall():
  for i in range(len(snow)):
    c=snow[i]
    if c[0]>-1:
      ColorOverlay(c[0],c[1],[c[2],c[2],c[2]],0)
    c[0] += 1
    c[1] += 1-rand(3)
    c[1]=max(0, min(c[1], 15))
    ColorOverlay(c[0],c[1],[c[2],c[2],c[2]],1)

def snowflake():
  while True:
    if len(snow)>0:
      _fall()
      np.show()
      _del()
    _new()
    sleep(50)
    gc.collect()

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
]

showimg(npd)
del npd
del showimg
gc.collect()

try:
  snowflake()
except:
  reset()