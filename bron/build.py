import os
B=os.path.dirname(os.path.abspath(__file__))
import json, re
W=json.load(open(os.path.join(B,'words.json'),encoding='utf8'))
lijsten=[]
FIXA={('3.A','age / agrum'):'ager / agrum'}
EXTRA={}
FIXB={('2.A','mutat'):'(1.) (hij/zij/het) verandert / (2.) (hij/zij/het) verwisselt'}
for ch in sorted(W, key=lambda c:(int(c[0]),c[2])):
    lijsten.append({'id':ch,'naam':ch,'woorden':[[FIXA.get((ch,a),a), FIXB.get((ch,a),b)] for a,b in W[ch]['pairs']] + EXTRA.get(ch,[])})
Z=json.load(open(os.path.join(B,'zinnen.json'),encoding='utf8'))
zinnen=[{'id':ch,'naam':ch,'zinnen':Z[ch]} for ch in sorted(Z, key=lambda c:(int(c[0]),c[2]))]
D=json.load(open(os.path.join(B,'duits.json'),encoding='utf8'))
ko=lambda c:[int(x) for x in c.split('.')]
DL=[{'id':c,'naam':c,'woorden':D['woorden'][c]} for c in sorted(D['woorden'],key=ko) if D['woorden'][c]]
DZ=[{'id':c,'naam':c,'zinnen':D['zinnen'][c]} for c in sorted(D['zinnen'],key=ko) if D['zinnen'][c]]
data={'latijn':{'naam':'Latijn','bron':'Minerva deel 1, 1/2/3 vwo','lijsten':lijsten,'zinnen':zinnen,'voorrang':['2.A|'+w[0] for w in EXTRA.get('2.A',[])]},
      'duits':{'naam':'Duits','bron':'Na Klar! 1/2 vwo, 5e editie · Kapitel 4: Wien','code':'de','eenheid':'Lektion','richting':True,'lijsten':DL,'zinnen':DZ},'frans':{'naam':'Frans','bron':'','lijsten':[]},'engels':{'naam':'Engels','bron':'','lijsten':[]}}
t=open(os.path.join(B,'template.html'),encoding='utf8').read()
t=t.replace('/*DATA*/',json.dumps(data,ensure_ascii=False)).replace('/*MATCH*/',open(os.path.join(B,'match.js'),encoding='utf8').read())
t=t.replace("esc(w.chn) + '</span></div>'","eenh() + ' ' + esc(w.chn) + '</span></div>'",1)
t=t.replace("esc(CAT[R.from].n) + ' · ' + esc(w.chn)","esc(CAT[R.from].n) + ' · ' + eenh().toLowerCase() + ' ' + esc(w.chn)")
open(os.path.join(B,'..','claude-versie.html'),'w',encoding='utf8').write(t)
title=re.search(r'<title>.*?</title>',t,re.S).group(0); links=''.join(re.findall(r'<link [^>]*>\n?',t))
style=re.search(r'<style>.*?</style>',t,re.S).group(0).replace('* { box-sizing: border-box; }','html { color-scheme: light; }\n* { box-sizing: border-box; }\nbody { margin: 0; }',1)
rest=t[t.index('<div id="app"></div>'):]
open(os.path.join(B,'..','public','index.html'),'w',encoding='utf8').write(f'<!doctype html>\n<html lang="nl">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{title}\n{links}{style}\n</head>\n<body>\n{rest}\n</body>\n</html>\n')
print('gebouwd')
