"""Build the installable offline web app into www/ (GitHub Pages + Capacitor webDir).
Usage: python3 tools/build.py [src_dir]"""
import os,sys,json,shutil,hashlib,subprocess
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S=sys.argv[1] if len(sys.argv)>1 else os.path.join(ROOT,'src'); W=os.path.join(ROOT,'www'); A=os.path.join(ROOT,'assets')
subprocess.run([sys.executable,os.path.join(ROOT,'tools','manifest.py'),S],check=True)
shutil.rmtree(W,ignore_errors=True)
shutil.copytree(S,W,ignore=shutil.ignore_patterns('.*','*.md'))
os.makedirs(f'{W}/icons',exist_ok=True)
for f in ('pwa-192.png','pwa-512.png','pwa-maskable-512.png','apple-touch-icon.png','favicon.png'): shutil.copy(f'{A}/{f}',f'{W}/icons/{f}')
h=open(f'{W}/index.html',encoding='utf-8').read()
head='''<meta name="theme-color" content="#0e0e0f"><meta name="color-scheme" content="dark"><meta name="description" content="Lukuluku: a film look lab. See lighting, lenses, film stocks and grades on real faces before you shoot or prompt.">
<link rel="manifest" href="manifest.webmanifest"><link rel="icon" href="icons/favicon.png"><link rel="apple-touch-icon" href="icons/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"><meta name="apple-mobile-web-app-title" content="Lukuluku">'''
h=h.replace('<title>',head+'\n<title>',1); open(f'{W}/index.html','w',encoding='utf-8').write(h)
json.dump({"name":"Lukuluku: film look lab","short_name":"Lukuluku","description":"See lighting, lenses, atmosphere, film stocks and grades on real faces before you shoot or prompt.","start_url":"./","scope":"./","display":"standalone","orientation":"any","background_color":"#0e0e0f","theme_color":"#0e0e0f","categories":["photo","productivity","education"],
 "icons":[{"src":"icons/pwa-192.png","sizes":"192x192","type":"image/png"},{"src":"icons/pwa-512.png","sizes":"512x512","type":"image/png"},{"src":"icons/pwa-maskable-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]},open(f'{W}/manifest.webmanifest','w'),indent=1)
# service worker: app shell precached (versioned); plates and LUTs cached as they are opened (cache-first)
files=[];heavy=[]
for dp,_,fs in os.walk(W):
    for f in fs:
        rel=os.path.relpath(os.path.join(dp,f),W).replace(os.sep,'/')
        if rel=='sw.js': continue
        (heavy if rel.startswith(('plates/','luts/')) and rel not in ('plates/index.json','luts/luts.json') else files).append(rel)
def digest(lst):
    hs=hashlib.sha1()
    for f in sorted(lst): hs.update(f.encode()); hs.update(open(os.path.join(W,f),'rb').read())
    return hs.hexdigest()[:10]
shell,media=digest(files),digest(heavy)
open(f'{W}/sw.js','w').write(f'''const SHELL="lukuluku-shell-{shell}",MEDIA="lukuluku-media-{media}",FILES={json.dumps(["./"]+sorted(files))};
self.addEventListener("install",e=>{{e.waitUntil(caches.open(SHELL).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting()))}});
self.addEventListener("activate",e=>{{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==SHELL&&k!==MEDIA).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))}});
self.addEventListener("fetch",e=>{{const u=new URL(e.request.url);if(e.request.method!=="GET"||u.origin!==location.origin)return;
 const media=/\\/(plates|luts)\\/[^/]+(\\/[^/]+)?\\.(webp|bin)$/.test(u.pathname);
 e.respondWith(caches.match(e.request,{{ignoreSearch:true}}).then(r=>r||fetch(e.request).then(res=>{{if(media&&res.ok){{const c=res.clone();caches.open(MEDIA).then(x=>x.put(e.request,c))}}return res}}).catch(()=>new Response("",{{status:404}}))))}});
''')
open(f'{W}/.nojekyll','w').close()
tot=sum(os.path.getsize(os.path.join(W,f)) for f in files+heavy)
print(f'www: {len(files)} shell files + {len(heavy)} plates/LUTs, {tot/1e6:.1f} MB, shell {shell}, media {media}')
