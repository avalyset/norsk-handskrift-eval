import sys; sys.path.insert(0,"scripts"); import guard, lib
import cv2, numpy as np, os, json
imgdir,xmldir,out=sys.argv[1:4]
files=sorted(f for f in os.listdir(imgdir) if f.endswith(".jpg")); guard.check(files); os.makedirs(out+"/lines",exist_ok=True); ids=[]; meta={}
for f in files:
    b=f[:-4]; im=cv2.cvtColor(cv2.imread(f"{imgdir}/{f}"),cv2.COLOR_BGR2RGB); meta[b]={"order":[]}
    for i,(txt,pts) in enumerate(lib.parse_gt(f"{xmldir}/{b}.xml")):
        x,y,w,h=cv2.boundingRect(pts); mask=np.zeros(im.shape[:2],np.uint8); cv2.fillPoly(mask,[pts],255)
        crop=np.where(mask[y:y+h,x:x+w,None]>0,im[y:y+h,x:x+w],255).astype(np.uint8)
        crop=cv2.resize(crop,(max(1,round(w*128/max(h,1))),128),interpolation=cv2.INTER_AREA)
        lid=f"{b}__{i:03d}"; cv2.imwrite(f"{out}/lines/{lid}.png",cv2.cvtColor(crop,cv2.COLOR_RGB2BGR)); ids.append(lid); meta[b]["order"].append(lid)
open(out+"/list.txt","w").write("\n".join(ids)+"\n"); json.dump(meta,open(out+"/meta.json","w")); print(len(ids))
