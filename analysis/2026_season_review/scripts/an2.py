import pandas as pd,numpy as np
m=pd.read_csv('matched.csv')
fo={'EF':30,'QF':30,'SF':31,'PF':32,'GF':33}
m['r']=m['round'].astype(str).map(lambda x: fo.get(x, None) or int(x))
m['margin']=m.score-m.o_score
S=['clearances','contested_possessions','uncontested_possessions','inside_50s','marks_inside_50','tackles','rebound_50s','hit_outs','disposals','kicks','marks','contested_marks','clangers','free_kicks_for','shots','goals']
for s in S: m['d_'+s]=m[s]-m['o_'+s]
m['acc']=m.goals/m.shots.replace(0,np.nan); m['d_acc']=m.acc-(m.o_goals/(m.o_shots.replace(0,np.nan)))
m['i50eff']=m.shots/m.inside_50s; m['d_i50eff']=m.i50eff-m.o_shots/m.o_inside_50s
F=['margin']+['d_'+s for s in S]+['d_acc','d_i50eff']
m=m.sort_values(['team','year','r'])
N=6
for f in F:
    # prior form: mean of previous N games (can span seasons? keep within-season + carry prior season). use across seasons, shift 1
    m['pf_'+f]=m.groupby('team')[f].transform(lambda x: x.shift(1).rolling(N,min_periods=3).mean())
# pair with opponent's pre-game form
key=['year','round','team','opponent']
pf=['pf_'+f for f in F]
opp=m[key+pf].rename(columns={'team':'opponent','opponent':'team',**{c:'o'+c for c in pf}})
x=m.merge(opp,on=key)
for f in F: x['X_'+f]=x['pf_'+f]-x['opf_'+f]
x=x.dropna(subset=['X_'+f for f in F])
x=x[x.year>=2013]
print('games with form',len(x))
y=x.margin.values; w=x.win.values
base=x.X_margin.values
b=np.polyfit(base,y,1); resid=y-np.polyval(b,base)
out=[]
for f in F:
    v=x['X_'+f].values
    r=np.corrcoef(v,y)[0,1]
    pr=np.corrcoef(v,resid)[0,1]
    tip=np.mean((v>0)==(w==1))
    out.append((f,round(r,3),round(pr,3),round(100*tip,1)))
t=pd.DataFrame(out,columns=['pre-game form (last 6, team minus opp)','corr w/ next margin','partial corr beyond margin form','tip% if you tip higher form']).sort_values('corr w/ next margin',ascending=False)
print(t.to_string(index=False))
# multivariate: margin form + i50 + clearances + cp + acc, out-of-sample (train <=2020, test 2021-24)
from numpy.linalg import lstsq
def fit(cols,tr,te):
    A=np.c_[tr[cols].values,np.ones(len(tr))]; c=lstsq(A,tr.margin.values,rcond=None)[0]
    p=np.c_[te[cols].values,np.ones(len(te))]@c
    return np.mean(np.abs(p-te.margin.values)), np.mean((p>0)==(te.win.values==1)), c
tr=x[x.year<=2020]; te=x[x.year>=2021]
for cols in [['X_margin'],['X_margin','X_d_inside_50s'],['X_margin','X_d_clearances'],['X_margin','X_d_contested_possessions'],['X_margin','X_d_acc'],['X_margin','X_d_shots'],['X_d_shots'],['X_margin','X_d_shots','X_d_acc'],['X_margin','X_d_inside_50s','X_d_clearances','X_d_contested_possessions','X_d_shots','X_d_acc','X_d_tackles','X_d_marks_inside_50']]:
    mae,tip,c=fit(cols,tr,te); print(f'OOS 2021-24 {"+".join(k[2:] for k in cols):80s} MAE {mae:5.2f} tips {100*tip:.1f}%  coefs {np.round(c,2)}')
x.to_csv('form.csv',index=False)
