"""Generate app icons + splash into assets/: a sphere lit by a warm key and a cool rim (lighting on a form)."""
import os,numpy as np
from PIL import Image,ImageDraw
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','assets'); os.makedirs(OUT,exist_ok=True)
BG=(14,14,15)
def mark(S,bg=True,scale=1.0):
    n=1024; y,x=np.mgrid[0:n,0:n].astype(np.float32); c=n/2; R=n*0.34*scale
    dx,dy=(x-c)/R,(y-c)/R; r2=dx*dx+dy*dy; inside=r2<=1; nz=np.sqrt(np.clip(1-r2,0,1))
    N=np.stack([dx,-dy,nz],-1)
    def lam(v): v=np.array(v,np.float32); v/=np.linalg.norm(v); return np.clip((N*v).sum(-1),0,1)
    key=lam([-0.75,0.45,0.55])**1.4; rim=lam([0.95,0.1,-0.25])**3.0
    col=key[...,None]*np.array([236,170,72])+rim[...,None]*np.array([70,170,205])*1.1+np.array([10,9,9])
    col=np.clip(col,0,255)
    img=np.zeros((n,n,4),np.float32); img[...,:3]=BG; img[...,3]=255 if bg else 0
    edge=np.clip((1-np.sqrt(r2))*R/1.5,0,1)  # anti-aliased edge
    a=edge*inside
    img[...,:3]=img[...,:3]*(1-a[...,None])+col*a[...,None]
    if not bg: img[...,3]=a*255
    im=Image.fromarray(img.astype(np.uint8),'RGBA')
    d=ImageDraw.Draw(im); rr=n*0.43*scale; w=max(2,int(n*0.012*scale))
    d.ellipse((c-rr,c-rr,c+rr,c+rr),outline=(217,164,65,255),width=w)   # the lens ring
    return im.resize((S,S),Image.LANCZOS)
mark(1024).save(f'{OUT}/icon-only.png')
mark(1024,bg=False,scale=0.7).save(f'{OUT}/icon-foreground.png')
Image.new('RGBA',(1024,1024),BG+(255,)).save(f'{OUT}/icon-background.png')
sp=Image.new('RGBA',(2732,2732),BG+(255,)); sp.alpha_composite(mark(900,bg=False),(916,916)); sp.save(f'{OUT}/splash.png'); sp.save(f'{OUT}/splash-dark.png')
for s in (192,512): mark(s).save(f'{OUT}/pwa-{s}.png')
mark(512,scale=0.78).save(f'{OUT}/pwa-maskable-512.png')
mark(180).convert('RGB').save(f'{OUT}/apple-touch-icon.png')
mark(64).save(f'{OUT}/favicon.png'); print('icons ok')
