"""Encode Blender renders (scene-linear EXR, Rec.709 primaries) into Lukuluku plates:
LogC3 (EI 800) curve, 1536x768 WebP, named <scene>_<L>_<O>_<H>.webp, then refresh plates/index.json.
Usage: python3 tools/encode_plates.py <folder_of_exrs> [--quality 92]
Each EXR must be named like the plate key, e.g. S4_L1_O1_H1.exr."""
import os,sys,glob,subprocess
import numpy as np, OpenEXR
from PIL import Image
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Same LogC3 constants as the app's decoder (LOGF in index.html) - keep them in sync.
A,B,C,D,E,F,CUT=5.555556,0.052272,0.247190,0.385537,5.367655,0.092809,0.010591
def lin2log(x): return np.where(x>CUT, C*np.log10(A*np.maximum(x,1e-6)+B)+D, E*x+F)
def read_exr(p):
    with OpenEXR.File(p) as f:
        ch=f.channels()
        if 'RGB' in ch: rgb=ch['RGB'].pixels
        else: rgb=np.stack([ch[k].pixels for k in ('R','G','B')],-1)
    return np.asarray(rgb,np.float32)[...,:3]
def main():
    src=sys.argv[1]; q=int(sys.argv[sys.argv.index('--quality')+1]) if '--quality' in sys.argv else 92; n=0
    for p in sorted(glob.glob(os.path.join(src,'*.exr'))):
        key=os.path.splitext(os.path.basename(p))[0]; sc=key.split('_')[0]
        log=np.clip(lin2log(np.maximum(read_exr(p),0)),0,1)
        im=Image.fromarray((log*255+.5).astype(np.uint8),'RGB')
        if im.size!=(1536,768): im=im.resize((1536,768),Image.LANCZOS)
        os.makedirs(f'{ROOT}/src/plates/{sc}',exist_ok=True); im.save(f'{ROOT}/src/plates/{sc}/{key}.webp','WEBP',quality=q,method=6); n+=1
    print(n,'plates encoded'); subprocess.run([sys.executable,os.path.join(ROOT,'tools/manifest.py')],check=True)
if __name__=='__main__': main()
