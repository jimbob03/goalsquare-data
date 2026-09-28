import pandas as pd,numpy as np
g=pd.read_csv('team_games.csv'); g=g[g.year<=2024]
g['score']=g.goals*6+g.behinds
g['shots']=g.goals+g.behinds
g['frees_diff_raw']=g.free_kicks_for
S=['clearances','contested_possessions','uncontested_possessions','inside_50s','marks_inside_50','tackles','rebound_50s','hit_outs','disposals','kicks','handballs','marks','contested_marks','clangers','free_kicks_for','one_percenters','shots','goals']
o=g.rename(columns={c:'o_'+c for c in S+['score','team','opponent','result','players']})
m=g.merge(o,left_on=['year','round','team','opponent'],right_on=['year','round','o_opponent','o_team'])
m=m[m.result.isin(['W','L'])]
m['win']=(m.result=='W').astype(int)
print('team-games',len(m),'matches',len(m)//2, 'player count check',m.players.describe()[['min','mean']].to_dict())
print('score check corr(player-sum score diff vs win)', np.corrcoef(m.score-m.o_score, m.win)[0,1].round(3))
rows=[]
for s in S:
    d=m[s]-m['o_'+s]
    won=m[d>0]; lost=m[d<0]
    rows.append((s, round(100*won.win.mean(),1), round(100*(d==0).mean(),1), round(np.corrcoef(d,m.win)[0,1],3), round(d.abs().mean(),1)))
t=pd.DataFrame(rows,columns=['stat','win% when you win the stat','% tied','corr w/ win','avg |diff|']).sort_values('win% when you win the stat',ascending=False)
print(t.to_string(index=False))
# clearances buckets
d=m.clearances-m.o_clearances
for lo,hi in [(-99,-10),(-10,-5),(-5,0),(1,5),(5,10),(10,99)]:
    sel=m[(d>=lo)&(d<hi)] if lo<0 else m[(d>=lo)&(d<hi)]
    print(f'clearance diff [{lo},{hi}) n={len(sel)} win%={100*sel.win.mean():.1f}')
m.to_csv('matched.csv',index=False)
