import sys,time,os
B=128
P=dict(zip('PNBRQKpnbrqk',range(12)))
V=[100,320,330,500,900,20000,-100,-320,-330,-500,-900,-20000]
S=b'0000000005050000051010050510202010100505102020101005051020201010050510202010100505102020101005051020201010050510202010100505102020101005051020201010050510202010100505102020101005051020201010050510202010100'
T=[c-48 for c in S]
K=(-16,-15,-17,-1,1,16,15,17)
N=(-33,-31,-18,-14,14,18,31,33)
R=(-16,-1,1,16)
Bd=(-15,-17,15,17)
nodes=0
def g(b,c):
 l=[]; o=16 if c<6 else -16
 for i in range(B):
  p=b[i]
  if p!=c: continue
  t=p%6
  if t==0:
   for d in (o,):
    j=i+d
    if j&128: continue
    if not b[j]:
     l+=[(i,j)]
     if (c<6 and i<16) or (c>5 and i>=112):
      j+=d
      if not j&128 and not b[j]: l+=[(i,j)]
   for d in (15,17) if c<6 else (-15,-17):
    j=i+d
    if j&128: continue
    if b[j] and (b[j]<6)!=(c<6): l+=[(i,j)]
  elif t==1:
   for d in N:
    j=i+d
    if j&128: continue
    if not b[j] or (b[j]<6)!=(c<6): l+=[(i,j)]
  elif t==2:
   for d in R:
    j=i+d
    while not j&128:
     if b[j]:
      if (b[j]<6)!=(c<6): l+=[(i,j)]
      break
     l+=[(i,j)]; j+=d
  elif t==3:
   for d in Bd:
    j=i+d
    while not j&128:
     if b[j]:
      if (b[j]<6)!=(c<6): l+=[(i,j)]
      break
     l+=[(i,j)]; j+=d
  elif t==4:
   for d in R+Bd:
    j=i+d
    while not j&128:
     if b[j]:
      if (b[j]<6)!=(c<6): l+=[(i,j)]
      break
     l+=[(i,j)]; j+=d
  else:
   for d in K:
    j=i+d
    if j&128: continue
    if not b[j] or (b[j]<6)!=(c<6): l+=[(i,j)]
 return l
def e(b,c):
 s=0
 for i in range(B):
  p=b[i]
  if p:
   v=V[p]
   s+= v+T[i] if p<6 else -v-T[127-i]
 return s if c<6 else -s
def q(b,c,a,b_,d):
 global nodes
 nodes+=1
 if d<=0: return e(b,c)
 s=e(b,c)
 if s>=b_: return s
 a=max(a,s)
 for f,t in g(b,c):
  p=b[f]; cp=b[t]
  if cp and (p<6)!=(cp<6):
   b[f]=0; b[t]=p
   s=-q(b,11-c,-b_,-a,d-1)
   b[f]=p; b[t]=cp
   if s>=b_: return s
   a=max(a,s)
 return a
def s(b,c,d,t0):
 global nodes
 nodes+=1
 if time.time()-t0>19 or nodes>2e6: raise TimeoutError
 if d<=0: return q(b,c,-10**9,10**9,3)
 a=-10**9
 l=g(b,c)
 l.sort(key=lambda m: (b[m[1]] and V[b[m[1]]]-V[b[m[0]]]*10,0))
 for f,t in l:
  p=b[f]; cp=b[t]; pr=0
  if p%6==0 and (t<16 or t>111): pr=4
  b[f]=0; b[t]=p|pr
  sc=-s(b,11-c,d-1,t0)
  b[f]=p; b[t]=cp
  if sc>a: a=sc
  if a>=10**9: break
 return a
def F(b,c,mt):
 global nodes
 t0=time.time(); bd=(0,0); nd=0
 for d in range(1,64):
  try:
   nodes=0
   a=-10**9
   l=g(b,c)
   l.sort(key=lambda m: (b[m[1]] and V[b[m[1]]]-V[b[m[0]]]*10,0))
   for f,t in l:
    p=b[f]; cp=b[t]; pr=0
    if p%6==0 and (t<16 or t>111): pr=4
    b[f]=0; b[t]=p|pr
    sc=-s(b,11-c,d-1,t0)
    b[f]=p; b[t]=cp
    if sc>a: a=sc; bd=(f,t)
    if a>=10**9: break
   nd=d
  except: break
  if time.time()-t0>mt-1: break
 return bd,nd
def main():
 b=[0]*B
 for i,r in enumerate(['RNBQKBNR','PPPPPPPP','........','........','........','........','pppppppp','rnbqkbnr']):
  for j,ch in enumerate(r):
   if ch!='.': b[i*16+j]=P[ch]
 c=0; t0=time.time()
 if os.getenv('MAKEFUN_ENV_URL'):
  for _ in range(10):
   mv,d=F(b,c,2)
   p=b[mv[0]]; b[mv[0]]=0; b[mv[1]]=p
   c=11-c
   print(f'{chr(97+(mv[0]&7))}{8-mv[0]//16}{chr(97+(mv[1]&7))}{8-mv[1]//16} d{d}')
   if time.time()-t0>5: break
if __name__=='__main__': main()