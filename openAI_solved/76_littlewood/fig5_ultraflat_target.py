import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
N=256
rng=np.random.default_rng(1)
def rs(n):
    a=[1];b=[1]
    while len(a)<n: a,b=a+b,a+[-x for x in b]
    return np.array(a[:n])
seqs={"Random ±1 signs":rng.choice([-1,1],N),"Rudin–Shapiro signs\n(flat within ×√2, not ultraflat)":rs(N)}
th=np.linspace(0,2*np.pi,4000)
z=np.exp(1j*th)
fig,ax=plt.subplots(1,3,figsize=(15,5.4),subplot_kw={"projection":"polar"})
for a,(t,c) in zip(ax,seqs.items()):
    h=np.abs(np.polyval(c[::-1],z)) if False else np.abs(sum(c[k]*z**k for k in range(N)))
    a.plot(th,h/np.sqrt(N),lw=1);a.plot(th,np.ones_like(th),"k--",lw=.8)
    a.set_ylim(0,3);a.set_title(t,fontsize=10)
a=ax[2];a.plot(th,np.ones_like(th),lw=2,color="C2");a.plot(th,np.ones_like(th),"k--",lw=.8)
a.set_ylim(0,3);a.set_title("Ultraflat (the theorem): height → √N\neverywhere = a perfect circle",fontsize=10)
fig.suptitle("Distance from center = |P(z)|/√N at angle θ around the unit circle (dashed = 1)")
plt.tight_layout();plt.savefig("fig5_ultraflat_target.png",dpi=110)
