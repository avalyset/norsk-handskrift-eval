import json, yaml, cv2, numpy as np, time, os
from doc_ufcn.main import DocUFCN
m="models/doc-ufcn-norhand-v1-line"; p=yaml.safe_load(open(m+"/parameters.yml"))["parameters"]
net=DocUFCN(3,p["input_size"],"cpu"); net.load(m+"/model.pth",p["mean"],p["std"],mode="eval")
os.makedirs("work/p20/lines",exist_ok=True); meta={}; ids=[]
for f in sorted(os.listdir("data/p20/test/images")):
    b=f[:-4]; im=cv2.cvtColor(cv2.imread("data/p20/test/images/"+f),cv2.COLOR_BGR2RGB)
    t=time.time(); polys,_,_,_=net.predict(im,min_cc=p["min_cc"]); dt=time.time()-t
    rows=[]
    for pl in polys.get(1,[]):
        pts=np.array(pl["polygon"],dtype=np.int32); x,y,w,h=cv2.boundingRect(pts)
        xs=pts[:,0]; lo=xs.min()+0.15*(xs.max()-xs.min()); ly=float(pts[xs<=lo][:,1].mean())
        rows.append((ly,x,y,w,h,pts))
    rows.sort(key=lambda r:(r[0],r[1]))  # y at the line's left end -> tolerant of slant
    meta[b]={"sec":dt,"n":len(rows),"order":[]}
    for i,(ly,x,y,w,h,pts) in enumerate(rows):
        mask=np.zeros(im.shape[:2],np.uint8); cv2.fillPoly(mask,[pts],255)
        crop=np.where(mask[y:y+h,x:x+w,None]>0,im[y:y+h,x:x+w],255).astype(np.uint8)
        crop=cv2.resize(crop,(max(1,round(w*128/max(h,1))),128),interpolation=cv2.INTER_AREA)
        lid=f"{b}__{i:03d}"; cv2.imwrite(f"work/p20/lines/{lid}.png",cv2.cvtColor(crop,cv2.COLOR_RGB2BGR)); ids.append(lid); meta[b]["order"].append(lid)
    print(b,len(rows),round(dt,2),flush=True)
open("work/p20/list.txt","w").write("\n".join(ids)+"\n"); json.dump(meta,open("work/p20/meta.json","w"))
