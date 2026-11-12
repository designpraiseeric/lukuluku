"""Write plates/index.json: the list of rendered plates the app may load. Run after adding renders.
Usage: python3 tools/manifest.py [src_dir]"""
import os,sys,json
S=sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'src')
keys=sorted(f[:-5] for d in os.listdir(f'{S}/plates') if os.path.isdir(f'{S}/plates/{d}') for f in os.listdir(f'{S}/plates/{d}') if f.endswith('.webp'))
json.dump(keys,open(f'{S}/plates/index.json','w'),separators=(',',':'))
print(len(keys),'plates listed')
