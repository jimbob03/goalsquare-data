import pandas as pd,glob
fs=glob.glob('afl/data/players/*_performance_details.csv')
out=[]
for f in fs:
    try: d=pd.read_csv(f,low_memory=False)
    except Exception: continue
    d=d[d['year']>=2012]
    if len(d): out.append(d)
p=pd.concat(out)
stats=['kicks','marks','handballs','disposals','goals','behinds','hit_outs','tackles','rebound_50s','inside_50s','clearances','clangers','free_kicks_for','free_kicks_against','contested_possessions','uncontested_possessions','contested_marks','marks_inside_50','one_percenters','bounces','goal_assist']
for s in stats: p[s]=pd.to_numeric(p[s],errors='coerce').fillna(0)
p['round']=p['round'].astype(str)
g=p.groupby(['year','round','team','opponent']).agg({**{s:'sum' for s in stats},'result':'first','jersey_num':'count'}).reset_index().rename(columns={'jersey_num':'players'})
print(g.shape, g.groupby('year').size().to_dict())
g.to_csv('team_games.csv',index=False)
