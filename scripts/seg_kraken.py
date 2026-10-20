"""usage: seg_kraken.py <bildedir> <utdir> -- Kraken blla standardmodell, samme utklipp/sortering som seg_generic. Heldout-vakt."""
import sys; sys.path.insert(0,"scripts"); import guard
import json, cv2, numpy as np, time, os
from PIL import Image
from kraken import blla
imgdir,out=sys.argv[1:3]
files=sorted(f for f in os.listdir(imgdir) if f.endswith(".jpg")); guard.check(files)
os.makedirs(out+"/lines",exist_ok=True); meta={}; ids=[]
for f in files:
    b=f[:-4]; pil=Image.open(f"{imgdir}/{f}").convert("RGB"); im=np.array(pil)
    t=time.time(); rows=[]; err=None
    try: seg=blla.segment(pil); lines=seg.lines
    except Exception as e: err=repr(e)[:200]; lines=[]   # krasj: siden beholdes med 0 linjer og feilmelding
    dt=time.time()-t
    for ln in lines:
        pts=np.array(ln.boundary if ln.boundary else ln.baseline,dtype=np.int32)
        if len(pts)<3: continue
        x,y,w,h=cv2.boundingRect(pts); xs=pts[:,0]; lo=xs.min()+0.15*(xs.max()-xs.min()); ly=float(pts[xs<=lo][:,1].mean()); rows.append((ly,x,y,w,h,pts))
    rows.sort(key=lambda r:(r[0],r[1])); meta[b]={"sec":dt,"n":len(rows),"order":[],"polys":[]}
    if err: meta[b]["error"]=err
    for i,(ly,x,y,w,h,pts) in enumerate(rows):
        mask=np.zeros(im.shape[:2],np.uint8); cv2.fillPoly(mask,[pts],255)
        crop=np.where(mask[y:y+h,x:x+w,None]>0,im[y:y+h,x:x+w],255).astype(np.uint8)
        crop=cv2.resize(crop,(max(1,round(w*128/max(h,1))),128),interpolation=cv2.INTER_AREA)
        lid=f"{b}__{i:03d}"; cv2.imwrite(f"{out}/lines/{lid}.png",cv2.cvtColor(crop,cv2.COLOR_RGB2BGR)); ids.append(lid)
        meta[b]["order"].append(lid); meta[b]["polys"].append(pts.tolist())
    print(b,len(rows),round(dt,2),flush=True)
open(out+"/list.txt","w").write("\n".join(ids)+"\n"); json.dump(meta,open(out+"/meta.json","w"))
