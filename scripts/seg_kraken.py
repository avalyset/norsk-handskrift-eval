"""usage: seg_kraken.py <bildedir> <utdir> -- Kraken blla standardmodell, samme utklipp/sortering som seg_generic. Heldout-vakt.
Krasj per side (åpning, segmentering, maskering, skalering, skriving) fanges: siden får n=0, tom liste og feilmelding i meta.json; kjøringen fortsetter.
Skrivefeil: cv2.imwrite kaster ikke, men returnerer False; returverdien sjekkes og False gir RuntimeError, slik at siden tas av unntaksgrenen."""
import sys; sys.path.insert(0,"scripts"); import guard
import json, cv2, numpy as np, time, os
from PIL import Image
from kraken import blla
imgdir,out=sys.argv[1:3]
files=sorted(f for f in os.listdir(imgdir) if f.endswith(".jpg")); guard.check(files)
os.makedirs(out+"/lines",exist_ok=True); meta={}; ids=[]
for f in files:
    b=f[:-4]; t=time.time(); written=[]
    try:
        pil=Image.open(f"{imgdir}/{f}").convert("RGB"); im=np.array(pil); rows=[]
        for ln in blla.segment(pil).lines:
            pts=np.array(ln.boundary if ln.boundary else ln.baseline,dtype=np.int32)
            if len(pts)<3: continue
            x,y,w,h=cv2.boundingRect(pts); xs=pts[:,0]; lo=xs.min()+0.15*(xs.max()-xs.min()); ly=float(pts[xs<=lo][:,1].mean()); rows.append((ly,x,y,w,h,pts))
        rows.sort(key=lambda r:(r[0],r[1])); m={"sec":0,"n":len(rows),"order":[],"polys":[]}
        for i,(ly,x,y,w,h,pts) in enumerate(rows):
            mask=np.zeros(im.shape[:2],np.uint8); cv2.fillPoly(mask,[pts],255)
            crop=np.where(mask[y:y+h,x:x+w,None]>0,im[y:y+h,x:x+w],255).astype(np.uint8)
            crop=cv2.resize(crop,(max(1,round(w*128/max(h,1))),128),interpolation=cv2.INTER_AREA)
            lid=f"{b}__{i:03d}"; fn=f"{out}/lines/{lid}.png"; written.append(fn)
            if not cv2.imwrite(fn,cv2.cvtColor(crop,cv2.COLOR_RGB2BGR)): raise RuntimeError(f"cv2.imwrite feilet: {lid}.png")   # imwrite kaster ikke, returnerer False
            m["order"].append(lid); m["polys"].append(pts.tolist())
        m["sec"]=time.time()-t
    except Exception as e:
        for fn in written:
            if os.path.exists(fn): os.remove(fn)    # kun filer dette skriptet nettopp skrev for denne siden
        m={"sec":time.time()-t,"n":0,"order":[],"polys":[],"error":repr(e)[:200]}
    meta[b]=m; ids+=m["order"]; print(b,m["n"],round(m["sec"],2),"FEIL "+m["error"] if "error" in m else "",flush=True)
open(out+"/list.txt","w").write("\n".join(ids)+"\n"); json.dump(meta,open(out+"/meta.json","w"))
