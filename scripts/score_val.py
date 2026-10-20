import sys; sys.path.insert(0,"scripts"); import lib, glob, re
gt={l.split("\t")[0]:l.rstrip("\n").split("\t",1)[1] for l in open("work/val1000/gt.tsv",encoding="utf8") if "\t" in l}
rows=[]
for f in sorted(glob.glob("work/val1000/lm_w*.txt"),key=lambda p:float(re.search(r"w([\d.]+)\.txt",p).group(1))):
    w=re.search(r"w([\d.]+)\.txt",f).group(1); h=lib.load_hyp(f)
    if len(h)<1000: print("vekt",w,"ufullstendig",len(h)); continue
    ce=cl=we=wl=0
    for i,r in gt.items():
        a,b=lib.edits(r,h.get(i,"")); c,d=lib.wedits(r,h.get(i,"")); ce+=a;cl+=b;we+=c;wl+=d
    rows.append((float(w),100*ce/cl,100*we/wl)); print("vekt %s  CER %.3f  WER %.3f"%(w,100*ce/cl,100*we/wl))
if rows: print("laveste CER:",min(rows,key=lambda r:r[1])[0])
