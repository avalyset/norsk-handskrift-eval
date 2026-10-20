import sys, json, yaml, cv2, numpy as np, time
from doc_ufcn.main import DocUFCN
m="models/doc-ufcn-norhand-v1-line"; p=yaml.safe_load(open(m+"/parameters.yml"))["parameters"]
img=sys.argv[1]; out=sys.argv[2]
net=DocUFCN(3,p["input_size"],"cpu"); net.load(m+"/model.pth",p["mean"],p["std"],mode="eval")
im=cv2.cvtColor(cv2.imread(img),cv2.COLOR_BGR2RGB); t=time.time()
polys,_,_,_=net.predict(im,min_cc=p["min_cc"]); print("predict s",round(time.time()-t,2))
print({k:len(v) for k,v in polys.items()})
res=[]
for cls in (1,):
    for pl in polys.get(cls,[]):
        pts=np.array(pl["polygon"],dtype=np.int32); x,y,w,h=cv2.boundingRect(pts)
        res.append((y,x,w,h,pts))
res.sort(key=lambda r:(r[0]))
for i,(y,x,w,h,pts) in enumerate(res):
    mask=np.zeros(im.shape[:2],np.uint8); cv2.fillPoly(mask,[pts],255)
    crop=np.where(mask[y:y+h,x:x+w,None]>0,im[y:y+h,x:x+w],255).astype(np.uint8)
    cv2.imwrite(f"{out}/line_{i:03d}.png",cv2.cvtColor(crop,cv2.COLOR_RGB2BGR))
json.dump([[int(a) for a in r[:4]] for r in res],open(out+"/boxes.json","w"))
print("horizontal lines",len(res), "image",im.shape)
