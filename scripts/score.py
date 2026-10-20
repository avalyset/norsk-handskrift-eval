import sys, jiwer, re
def load(p):
    d={}
    for l in open(p,encoding="utf8").read().split("\n"):
        if not l or l.startswith("#"): continue
        i,_,rest=l.partition(" "); c,_,t=rest.partition(" "); d[i]=t
    return d
gt={l.split("\t")[0]:l.rstrip("\n").split("\t",1)[1] for l in open(sys.argv[1],encoding="utf8") if "\t" in l}
gt={f"t{int(k):04d}":v for k,v in gt.items()}
h=load(sys.argv[2]); ids=sorted(gt)
refs=[gt[i] for i in ids]; hyp=[h.get(i,"") for i in ids]
print("n",len(ids),"CER %.2f WER %.2f"%(100*jiwer.cer(refs,hyp),100*jiwer.wer(refs,hyp)))
