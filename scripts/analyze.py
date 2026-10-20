"""usage: analyze.py <segdir> <hypfil> [json-ut]  -- side-CER/WER (rekkefølge) + IoU-parede mål. Kun pilotsider (guard)."""
import sys; sys.path.insert(0,"scripts"); import guard, lib, json, statistics as st
import numpy as np
from shapely.geometry import Polygon
from scipy.optimize import linear_sum_assignment
segdir,hypf=sys.argv[1:3]; meta=json.load(open(segdir+"/meta.json")); guard.check(meta.keys())
hyp=lib.load_hyp(hypf); res={"pages":{}}
def poly(p):
    g=Polygon(p); return g if g.is_valid else g.buffer(0)
pe=[];pl=[];we=[];wl=[];rows=[]
IOUS=[0.3,0.5,0.7]; agg={t:dict(mat=0,ung=0,unp=0,ed=0,split=0,merge=0,gtn=0,predn=0) for t in IOUS}; chars=0; empty=0; nfound=0
for b,m in sorted(meta.items()):
    gt=lib.parse_gt(f"data/p20/test/page/{b}.xml"); gtext=[t for t,_ in gt]; chars+=sum(len(t) for t in gtext)
    out=[hyp.get(i,"") for i in m["order"]]; nfound+=len(out); empty+=sum(1 for o in out if not o)
    ref=" ".join(t for t in gtext if t); h=" ".join(o for o in out if o)
    a,c=lib.edits(ref,h); d,e=lib.wedits(ref,h); pe.append(a);pl.append(c);we.append(d);wl.append(e)
    res["pages"][b]=dict(cer=100*a/max(c,1),gt=len(gt),found=len(out))
    if "polys" not in m: continue
    G=[poly(p) for _,p in gt]; P=[poly(p) for p in m["polys"]]
    I=np.zeros((len(G),len(P))); cg=np.zeros_like(I); cp=np.zeros_like(I)
    for i,g in enumerate(G):
        for j,p in enumerate(P):
            if g.intersects(p):
                x=g.intersection(p).area; I[i,j]=x/(g.area+p.area-x+1e-9); cg[i,j]=x/(g.area+1e-9); cp[i,j]=x/(p.area+1e-9)
    ri,ci=linear_sum_assignment(-I) if I.size else ([],[])
    for t in IOUS:
        A=agg[t]; pairs=[(i,j) for i,j in zip(ri,ci) if I[i,j]>=t]; mg={i for i,_ in pairs}; mp={j for _,j in pairs}
        A["mat"]+=len(pairs); A["ung"]+=len(G)-len(mg); A["unp"]+=len(P)-len(mp); A["gtn"]+=len(G); A["predn"]+=len(P)
        A["ed"]+=sum(lib.edits(gtext[i],out[j])[0] for i,j in pairs)
        A["ed"]+=sum(len(gtext[i]) for i in range(len(G)) if i not in mg)+sum(len(out[j]) for j in range(len(P)) if j not in mp)
        A["split"]+=int(sum(1 for i in range(len(G)) if (cp[i]>=0.5).sum()>=2)); A["merge"]+=int(sum(1 for j in range(len(P)) if (cg[:,j]>=0.5).sum()>=2))
res["lines"]=dict(found=nfound,gt=sum(r["gt"] for r in res["pages"].values()),empty=empty)
res["corpus_cer"]=100*sum(pe)/sum(pl); res["corpus_wer"]=100*sum(we)/sum(wl)
pc=[100*a/max(c,1) for a,c in zip(pe,pl)]; res["mean_cer"]=st.mean(pc); res["median_cer"]=st.median(pc); res["mean_wer"]=st.mean(100*a/max(c,1) for a,c in zip(we,wl))
res["cer_ci_pages"]=lib.boot(pe,pl); res["wer_ci_pages"]=lib.boot(we,wl)
if "polys" in next(iter(meta.values())):
    res["iou"]={str(t):dict(A,order_free_cer=100*A["ed"]/chars,matched_frac_gt=A["mat"]/A["gtn"]) for t,A in agg.items()}
print(json.dumps(res,indent=1,ensure_ascii=False))
if len(sys.argv)>3: json.dump(res,open(sys.argv[3],"w"),ensure_ascii=False,indent=1)
