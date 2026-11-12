"""One-off: convert the legacy data/*.js bundles (base64 plates + LUTs) into plain files.
Usage: python3 -I tools/split_legacy.py <legacy_data_dir> <src_dir>"""
import os,re,sys,json,base64
D,S=sys.argv[1],sys.argv[2]
n=0
for f in sorted(os.listdir(D)):
    if not re.match(r'S\w+\.js$',f): continue
    s=open(os.path.join(D,f)).read()
    for key,b64 in re.findall(r'PLATES\["([^"]+)"\]="data:image/webp;base64,([^"]+)"',s):
        sc=key.split('_')[0]; os.makedirs(f'{S}/plates/{sc}',exist_ok=True)
        open(f'{S}/plates/{sc}/{key}.webp','wb').write(base64.b64decode(b64)); n+=1
s=open(os.path.join(D,'luts.js')).read(); L=json.loads(s[s.index('{'):s.rindex('}')+1]); meta={}
for k,v in L.items():
    open(f'{S}/luts/{k}.bin','wb').write(base64.b64decode(v['data'])); meta[k]={'file':v['file'],'size':v['size']}
json.dump(meta,open(f'{S}/luts/luts.json','w'),indent=1)
print(n,'plates,',len(meta),'luts')
