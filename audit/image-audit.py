import json, re, collections, difflib, os
SRC=['/root/.claude/projects/-home-user-manus/f9f720c1-823b-5cd8-aec8-e4501793ee60/tool-results/mcp-Shopify-graphql_query-1785985782078.txt',
     '/tmp/claude-0/-home-user-manus/f9f720c1-823b-5cd8-aec8-e4501793ee60/scratchpad/blobs/p1.json',
     '/tmp/claude-0/-home-user-manus/f9f720c1-823b-5cd8-aec8-e4501793ee60/scratchpad/blobs/p2.json',
     '/tmp/claude-0/-home-user-manus/f9f720c1-823b-5cd8-aec8-e4501793ee60/scratchpad/blobs/p3.json']
prods={}
for f in SRC:
    d=json.load(open(f))
    for e in d['data']['products']['edges']:
        n=e['node']
        imgs=[]
        for m in [x['node'] for x in n['media']['edges']]:
            u=(m.get('image') or {}).get('url')
            if not u: continue
            imgs.append({'mid':m.get('id'),'alt':m.get('alt') or '','file':u.split('/')[-1].split('?')[0]})
        prev=prods.get(n['id'])
        if prev and len(prev['imgs'])>=len(imgs): continue   # keep richest record
        prods[n['id']]={'title':n['title'],'handle':n['handle'],'status':n['status'],
                        'type':n.get('productType'),'imgs':imgs}

SUP=re.compile(r'^[0-9a-f]{32}\.png$')
sup=lambda f: bool(SUP.match(f))
act={k:v for k,v in prods.items() if v['status']=='ACTIVE'}
arc={k:v for k,v in prods.items() if v['status']=='ARCHIVED'}
print(f"products covered: {len(prods)}   ACTIVE {len(act)}   ARCHIVED {len(arc)}")

plan={}; tot=0
for pid,p in act.items():
    ai=[i for i in p['imgs'] if not sup(i['file'])]
    left=[i for i in p['imgs'] if sup(i['file'])]
    if ai:
        tot+=len(ai)
        plan[pid]={'title':p['title'],'handle':p['handle'],
                   'featured_is_fake': not sup(p['imgs'][0]['file']),
                   'remove_media_ids':[i['mid'] for i in ai],
                   'remove_files':[i['file'] for i in ai],
                   'real_photos_remaining':len(left)}
print(f"\n### FABRICATED IMAGERY: {len(plan)} active products, {tot} images")
nofeat=sum(1 for v in plan.values() if v['featured_is_fake'])
print(f"    of which featured/first image is fabricated: {nofeat}")
bad=[v for v in plan.values() if v['real_photos_remaining']<2]
print(f"    products left with <2 real photos after removal: {len(bad)}")
for v in bad: print('       ',v['real_photos_remaining'],v['title'])

print(f"\n### THIN IMAGERY: active products with <2 images")
for pid,p in act.items():
    if len(p['imgs'])<2: print(f"   {len(p['imgs'])} img  {p['title']}  /{p['handle']}  [{p['imgs'][0]['file'] if p['imgs'] else 'NONE'}]")

print(f"\n### DUPLICATE IMAGE FILES shared across products")
byf=collections.defaultdict(set)
for pid,p in prods.items():
    for i in p['imgs']: byf[i['file']].add(pid)
dd={f:v for f,v in byf.items() if len(v)>1}
print(f"   {len(dd)} shared files")
for f,v in dd.items():
    print('   ',f)
    for pid in v: print('        ',prods[pid]['status'],prods[pid]['title'])

print(f"\n### ALT TEXT naming a different product")
STOP={'hivolt','with','view','worn','model','front','back','detail','studio','life','candid','alternate','black','white','beige','gray','grey','apricot','light','static','blue','green','chest','thigh','bolt','mark','gym','leg','side'}
tk=lambda s:set(w for w in re.findall(r'[a-z0-9]+',s.lower()) if len(w)>3 and w not in STOP)
for pid,p in prods.items():
    t=tk(p['title'])
    for i in p['imgs']:
        if i['alt'] and t and tk(i['alt']) and not (tk(i['alt'])&t):
            print(f"   [{p['status']}] {p['title']}\n        alt : {i['alt']}\n        file: {i['file']}")

print(f"\n### ARCHIVED near-duplicates of ACTIVE titles")
norm=lambda s: re.sub(r'[^a-z0-9]','',s.lower().replace('’',"'"))
am={norm(v['title']):v for v in act.values()}
for v in arc.values():
    m=difflib.get_close_matches(norm(v['title']),list(am),n=1,cutoff=0.82)
    if m: print(f"   ARCHIVED {v['title']!r}  ~  ACTIVE {am[m[0]]['title']!r}")

json.dump(plan,open('/tmp/claude-0/-home-user-manus/f9f720c1-823b-5cd8-aec8-e4501793ee60/scratchpad/removal_plan.json','w'),indent=1)
print(f"\nmanifest -> removal_plan.json  ({len(plan)} products, {tot} media ids)")
