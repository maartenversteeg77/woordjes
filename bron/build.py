import os
B=os.path.dirname(os.path.abspath(__file__))
import json, re
W=json.load(open(os.path.join(B,'words.json'),encoding='utf8'))
lijsten=[]
FIXA={('3.A','age / agrum'):'ager / agrum'}
FIXB={('2.A','mutat'):'(1.) (hij/zij/het) verandert / (2.) (hij/zij/het) verwisselt'}
for ch in sorted(W, key=lambda c:(int(c[0]),c[2])):
    lijsten.append({'id':ch,'naam':ch,'woorden':[[FIXA.get((ch,a),a), FIXB.get((ch,a),b)] for a,b in W[ch]['pairs']]})
data={'latijn':{'naam':'Latijn','bron':'Minerva deel 1, 1/2/3 vwo','lijsten':lijsten},
      'duits':{'naam':'Duits','bron':'','lijsten':[]},'frans':{'naam':'Frans','bron':'','lijsten':[]},'engels':{'naam':'Engels','bron':'','lijsten':[]}}
t=open(os.path.join(B,'template.html'),encoding='utf8').read()
t=t.replace('/*DATA*/',json.dumps(data,ensure_ascii=False)).replace('/*MATCH*/',open(os.path.join(B,'match.js'),encoding='utf8').read())
t=t.replace("esc(w.chn) + '</span></div>'","'Hoofdstuk ' + esc(w.chn) + '</span></div>'",1)
t=t.replace("esc(CAT[R.from].n) + ' · ' + esc(w.chn)","esc(CAT[R.from].n) + ' · hoofdstuk ' + esc(w.chn)")
open(os.path.join(B,'..','claude-versie.html'),'w',encoding='utf8').write(t)
title=re.search(r'<title>.*?</title>',t,re.S).group(0); links=''.join(re.findall(r'<link [^>]*>\n?',t))
style=re.search(r'<style>.*?</style>',t,re.S).group(0).replace('* { box-sizing: border-box; }','html { color-scheme: light; }\n* { box-sizing: border-box; }\nbody { margin: 0; }',1)
rest=t[t.index('<div id="app"></div>'):]
open(os.path.join(B,'..','public','index.html'),'w',encoding='utf8').write(f'<!doctype html>\n<html lang="nl">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n{title}\n{links}{style}\n</head>\n<body>\n{rest}\n</body>\n</html>\n')
print('gebouwd')
