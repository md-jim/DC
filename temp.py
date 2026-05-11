import tkinter as tk
from tkinter import ttk
import numpy as np,matplotlib;matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- ENCODING ---
def nrz_l(b):return[1 if x=='1'else-1 for x in b]
def nrz_i(b):
 s,c=[],1
 for x in b:
  if x=='1':c=-c
  s.append(c)
 return s
def man(b):return sum([[-1,1]if x=='1'else[1,-1]for x in b],[])
def dman(b):
 s,c=[],1
 for x in b:
  if x=='0':c=-c
  s.append(c);c=-c;s.append(c)
 return s
def ami(b):
 s,l=[],1
 for x in b:
  if x=='0':s.append(0)
  else:s.append(l);l=-l
 return s

# --- ERROR DETECT ---
def vrc(d,t='even'):p='0'if(d.count('1')%2==0)==(t=='even')else'1';return p,d+p
def vchk(r,t='even'):return'OK'if(r.count('1')%2==0)==(t=='even')else'ERR'
def lrc(ds):
 rows=ds.split();n=max(len(r)for r in rows);rows=[r.zfill(n)for r in rows]
 res=['0']*n
 for r in rows:res=[str(int(res[i])^int(r[i]))for i in range(n)]
 return''.join(res),rows 
def lchk(ds,lv):
 rows=[r.zfill(len(lv))for r in ds.split()]+[lv];res=['0']*len(lv)
 for r in rows:res=[str(int(res[i])^int(r[i]))for i in range(len(lv))]
 return'OK'if all(b=='0'for b in res)else'ERR'
def xdiv(dd,dv):
 p=len(dv);t=list(dd[:p])
 while p<len(dd):
  if t[0]=='1':t=[str(int(t[i])^int(dv[i]))for i in range(len(dv))]
  t.pop(0);t.append(dd[p]);p+=1
 if t[0]=='1':t=[str(int(t[i])^int(dv[i]))for i in range(len(dv))]
 t.pop(0);return''.join(t)
def crc(d,dv):r=xdiv(d+'0'*(len(dv)-1),dv);return d+r,r
def cchk(rx,dv):r=xdiv(rx,dv);return'OK'if all(b=='0'for b in r)else'ERR='+r
def csenc(sg,b=8):
 t=sum(int(s,2)for s in sg);m=2**b
 while t>=m:t=(t&(m-1))+(t>>b)
 return format((~t)&(m-1),f'0{b}b')
def cschk(sg,cs,b=8):
 t=sum(int(s,2)for s in sg+[cs]);m=2**b
 while t>=m:t=(t&(m-1))+(t>>b)
 return'OK'if t==m-1 else'ERR'
def henc(d):
 m=len(d);r=0
 while 2**r<m+r+1:r+=1
 n=m+r;c=['0']*(n+1);j=0
 for i in range(1,n+1):
  if i&(i-1):c[i]=d[j];j+=1
 for i in range(r):
  pos=2**i;v=0
  for k in range(1,n+1):
   if k&pos:v^=int(c[k])
  c[pos]=str(v)
 return''.join(c[1:]),r
def hdec(rx):
 n=len(rx);c=['0']+list(rx);r=0
 while 2**r<=n:r+=1
 ep=0
 for i in range(r):
  pos=2**i;v=0
  for k in range(1,n+1):
   if k&pos:v^=int(c[k])
  if v:ep+=pos
 cor=list(c)
 if ep:cor[ep]='1'if c[ep]=='0'else'0'
 return ep,''.join(cor[1:]),''.join(cor[k]for k in range(1,n+1)if k&(k-1))

# --- GUI ---
def embed(fig,f):
 [w.destroy()for w in f.winfo_children()]
 cv=FigureCanvasTkAgg(fig,master=f);cv.draw();cv.get_tk_widget().pack(fill='both',expand=True);plt.close(fig)
def E(p,v,w=14):e=tk.Entry(p,width=w);e.insert(0,v);e.pack(side='left',padx=2);return e
def T(p):w=tk.Text(p,height=6,state='disabled');w.pack(fill='x',padx=4);return w
def wr(w,t):w.configure(state='normal');w.delete('1.0','end');w.insert('end',t);w.configure(state='disabled')
def LB(p,t):tk.Label(p,text=t).pack(side='left',padx=1)
def BT(p,t,c):tk.Button(p,text=t,command=c).pack(side='left',padx=2)
def ROW(p):r=tk.Frame(p);r.pack(fill='x',padx=2,pady=1);return r
def _ax(a,nm):a.axhline(0,lw=.8,ls='--',color='gray');a.set_ylabel(nm,fontsize=7,rotation=0,labelpad=40,va='center');a.tick_params(labelsize=6)

# --- PLOTS ---
def pd2d(bits,f):
 n=len(bits);fig,ax=plt.subplots(5,1,figsize=(9,7),tight_layout=True)
 for a,(nm,sg)in zip(ax,[('NRZ-L',nrz_l(bits)),('NRZ-I',nrz_i(bits)),('Man',man(bits)),('DMn',dman(bits)),('AMI',ami(bits))]):
  _ax(a,nm)
  xs=np.linspace(0,n,len(sg)+1);a.step(xs,np.append(sg,sg[-1]),where='post',lw=1.5)
  a.set_xlim(0,n);a.set_ylim(-1.8,1.9);a.set_xticks(range(n+1))
  [a.text(i+.5,1.5,b,ha='center',fontsize=8)for i,b in enumerate(bits)]
 embed(fig,f)
def ppcm(fr,sr,bi,f):
 t=np.linspace(0,1,1000);ts=np.linspace(0,1,sr);an=np.sin(2*np.pi*fr*t);sm=np.sin(2*np.pi*fr*ts)
 qs=2/2**bi;qu=np.clip(np.floor((sm+1)/qs),0,2**bi-1).astype(int);enc=[format(v,f'0{bi}b')for v in qu]
 fig,ax=plt.subplots(3,1,figsize=(9,6),tight_layout=True)
 ax[0].plot(t,an,lw=1.5);ax[0].set_title('Analog',fontsize=8)
 ax[1].plot(t,an,alpha=.3);ax[1].stem(ts,sm,linefmt='C0',markerfmt='o',basefmt=' ')
 ax[1].step(ts,-1+qu*qs+qs/2,where='mid',lw=1.5);ax[1].set_title('Sampled',fontsize=8)
 ax[2].text(.5,.5,' '.join(enc[:14]),transform=ax[2].transAxes,ha='center',va='center',fontsize=9,fontfamily='monospace');ax[2].axis('off')
 embed(fig,f)
def pd2a(bits,f):
 fc,fs=5,500;t=np.linspace(0,len(bits),fs*len(bits));br=np.repeat(list(bits),fs)
 ask=np.array([int(b)*np.sin(2*np.pi*fc*ti)for b,ti in zip(br,t)])
 fsk=np.array([np.sin(2*np.pi*(fc if b=='1'else fc/2)*ti)for b,ti in zip(br,t)])
 psk=np.array([np.sin(2*np.pi*fc*ti+(np.pi if b=='0'else 0))for b,ti in zip(br,t)])
 fig,ax=plt.subplots(4,1,figsize=(9,7),tight_layout=True)
 for a,(nm,sg)in zip(ax,[('Dig',np.repeat([int(b)for b in bits],fs)),('ASK',ask),('FSK',fsk),('PSK',psk)]):
  _ax(a,nm);a.plot(t,sg,lw=1)
 embed(fig,f)
def pa2a(fm,fc,f):
 t=np.linspace(0,1,1000);msg=np.sin(2*np.pi*fm*t);car=np.sin(2*np.pi*fc*t)
 fig,ax=plt.subplots(5,1,figsize=(9,8),tight_layout=True)
 for a,(nm,sg)in zip(ax,[('Msg',msg),('Car',car),('AM',(1+.5*msg)*car),('FM',np.sin(2*np.pi*fc*t+2*np.pi*5*np.cumsum(msg)/1000)),('PM',np.sin(2*np.pi*fc*t+np.pi*msg))]):
  _ax(a,nm);a.plot(t,sg,lw=1)
 embed(fig,f)

# --- APP ---
class App(tk.Tk):
 def __init__(self):
  super().__init__();self.title("DCL");self.geometry("1100x720")
  nb=ttk.Notebook(self);nb.pack(fill='both',expand=True,padx=2,pady=2)
  for i in range(1,10):getattr(self,f'_l{i}')(nb)
 def _pt(self,nb,ti):
  t=ttk.Frame(nb);nb.add(t,text=ti);tp=tk.Frame(t);tp.pack(fill='x')
  pf=tk.Frame(t);pf.pack(fill='both',expand=True);return tp,pf
 def _st(self,nb,ti):
  t=ttk.Frame(nb);nb.add(t,text=ti);return t
 def _l1(self,nb):
  tp,pf=self._pt(nb,'L1:D→D');r=ROW(tp);LB(r,'Bits:');e=E(r,'10110010',18)
  BT(r,'Plot',lambda:pd2d(e.get().strip(),pf));self.after(400,lambda:pd2d('10110010',pf))
 def _l2(self,nb):
  tp,pf=self._pt(nb,'L2:PCM');r=ROW(tp);LB(r,'Fr:');fe=E(r,'2',4);LB(r,'Smp:');se=E(r,'32',4);LB(r,'Bits:');be=E(r,'3',3)
  BT(r,'Run',lambda:ppcm(float(fe.get()),int(se.get()),int(be.get()),pf));self.after(400,lambda:ppcm(2,32,3,pf))
 def _l3(self,nb):
  tp,pf=self._pt(nb,'L3:D→A');r=ROW(tp);LB(r,'Bits:');e=E(r,'1011',12)
  BT(r,'Plot',lambda:pd2a(e.get().strip(),pf));self.after(400,lambda:pd2a('1011',pf))
 def _l4(self,nb):
  tp,pf=self._pt(nb,'L4:A→A');r=ROW(tp);LB(r,'Msg:');me=E(r,'2',4);LB(r,'Car:');ce=E(r,'20',4)
  BT(r,'Plot',lambda:pa2a(float(me.get()),float(ce.get()),pf));self.after(400,lambda:pa2a(2,20,pf))
 def _l5(self,nb):
  f=self._st(nb,'L5:VRC');r=ROW(f);LB(r,'Data:');de=E(r,'1010001',14)
  pv=tk.StringVar(value='even');tk.OptionMenu(r,pv,'even','odd').pack(side='left');ot=T(f)
  def _r():
   d=de.get().strip();p,tx=vrc(d,pv.get());bad=tx[:-1]+('0'if tx[-1]=='1'else'1')
   wr(ot,f"TX:{tx} P:{p} {vchk(tx,pv.get())}\nRX:{bad} {vchk(bad,pv.get())}")
  BT(r,'Run',_r)
 def _l6(self,nb):
  f=self._st(nb,'L6:LRC');r=ROW(f);LB(r,'Rows:');de=E(r,'1010 1100 0110',22);ot=T(f)
  def _r():
   s=de.get().strip();lv,rows=lrc(s);r2=rows[:];r2[0]=('1'if r2[0][0]=='0'else'0')+r2[0][1:]
   wr(ot,'\n'.join(f"R{i+1}:{rw}"for i,rw in enumerate(rows))+f"\nLRC:{lv} {lchk(s,lv)}\nErr:{' '.join(r2)} {lchk(' '.join(r2),lv)}")
  BT(r,'Run',_r)
 def _l7(self,nb):
  f=self._st(nb,'L7:CRC');r=ROW(f);LB(r,'Data:');de=E(r,'1101011011',14);LB(r,'Gen:');ge=E(r,'10011',8);ot=T(f)
  def _r():
   d,dv=de.get().strip(),ge.get().strip();tx,rem=crc(d,dv);bad=tx[:-1]+('1'if tx[-1]=='0'else'0')
   wr(ot,f"TX:{tx} Rem:{rem} {cchk(tx,dv)}\nErr:{bad} {cchk(bad,dv)}")
  BT(r,'Run',_r)
 def _l8(self,nb):
  f=self._st(nb,'L8:CSum');r=ROW(f);LB(r,'Segs:');de=E(r,'10101001 00111001',24);ot=T(f)
  def _r():
   sg=de.get().strip().split();cs=csenc(sg);bad=('1'if cs[0]=='0'else'0')+cs[1:]
   wr(ot,f"CS:{cs} {cschk(sg,cs)}\nBad:{bad} {cschk(sg,bad)}")
  BT(r,'Run',_r)
 def _l9(self,nb):
  f=self._st(nb,'L9:Ham');r=ROW(f);LB(r,'Data:');de=E(r,'1011',10);LB(r,'ErrPos:');ep=E(r,'3',4);ot=T(f)
  def _r():
   d=de.get().strip();pos=int(ep.get());enc,rr=henc(d);rv=list(enc)
   if pos and 1<=pos<=len(rv):rv[pos-1]='1'if rv[pos-1]=='0'else'0'
   rx=''.join(rv);ep2,cor,rec=hdec(rx)
   wr(ot,f"Enc:{enc} r={rr}\nRX:{rx}\nSyn:{'@'+str(ep2)if ep2 else'OK'} Cor:{cor}\nRec:{rec} {'OK'if rec==d else'FAIL'}")
  BT(r,'Run',_r)

App().mainloop()