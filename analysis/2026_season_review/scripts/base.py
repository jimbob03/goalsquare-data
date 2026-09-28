import json,collections,re,statistics as st
import numpy as np
fp=json.load(open('final_preds.json'))
H=json.load(open('/home/user/goalsquare-data/prediction_history.json'))
norm=lambda t:{'Greater Western Sydney':'GWS Giants'}.get(t,t)
res={(g['round'],norm(g['home_team']),norm(g['away_team'])):g for g in H}
PAT=re.compile(r'(?:Squiggle[^:]{0,40}|[Ww]eighted consensus|WEIGHTED consensus)[:]?\s*(HOME|AWAY|[A-Z]{3})\s+by\s+([\d.]+)')
rows=[];nob=0
for v in fp.values():
    if v['round']==1: continue
    k=(v['round'],norm(v['home_team']),norm(v['away_team'])); r=res.get(k)
    if not r: continue
    kf=v.get('key_factors','')
    m=PAT.search(kf)
    if not m: nob+=1; continue
    side,val=m.group(1),float(m.group(2))
    if side in('HOME',v['home_code']): base=val
    elif side in('AWAY',v['away_code']): base=-val
    else: nob+=1; continue
    gs=v['predicted_margin']*(1 if v['predicted_winner']==v['home_team'] else -1)
    act=r['actual_home_score']-r['actual_away_score']
    rows.append(dict(k=k,rnd=v['round'],base=base,gs=gs,act=act,tier=v['tier'],prob=v['win_probability'],kf=kf,home=k[1],away=k[2],venue=v.get('venue')))
print('rows',len(rows),'unparsed',nob)
json.dump(rows,open('rows.json','w'))
