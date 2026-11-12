"""List every plate the catalog expects but src/plates doesn't have yet -> render/queue.json (+ a summary).
Usage: python3 tools/render_queue.py"""
import os,json,re,subprocess
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
js=subprocess.run(['node','-e',"global.window={};require(process.argv[1]);console.log(JSON.stringify(window.CATALOG))",os.path.join(ROOT,'src/catalog.js')],capture_output=True,text=True,check=True).stdout
C=json.loads(js); have=set(json.load(open(os.path.join(ROOT,'src/plates/index.json'))))
q=[]
for sc in C['scenes']:
    for L in C['lighting']:
        for O in C['optics']:
            for H in C['atmosphere']:
                k=f"{sc['id']}_{L}_{O}_{H}"
                if k not in have: q.append({'key':k,'scene':sc['id'],'L':L,'O':O,'H':H,'out':f"src/plates/{sc['id']}/{k}.webp"})
os.makedirs(os.path.join(ROOT,'render'),exist_ok=True)
json.dump(q,open(os.path.join(ROOT,'render/queue.json'),'w'),indent=0)
from collections import Counter
print(len(q),'plates to render'); print(' by scene:',dict(Counter(x['scene'] for x in q))); print(' by lighting:',dict(Counter(x['L'] for x in q)))
