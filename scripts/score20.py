import json,re,jiwer,statistics as st
meta=json.load(open("work/p20/meta.json")); hyp={}
for l in open("work/p20/lm.txt",encoding="utf8").read().split("\n"):
    if l and not l.startswith("#"): i,_,r=l.partition(" "); c,_,t=r.partition(" "); hyp[i]=(c,t)
R=[];H=[];tot=0;nf=0;ng=0;empty=0;short=0;pc=[];pw=[]
for b,m in meta.items():
    x=open(f"data/p20/test/page/{b}.xml",encoding="utf8").read()
    gt=[re.sub(r"\s+"," "," ".join(re.findall(r"<Unicode>(.*?)</Unicode>",tl,re.S))).strip() for tl in re.findall(r"<TextLine.*?</TextLine>",x,re.S)]
    ref=" ".join(g for g in gt if g); ng+=len(gt); nf+=m["n"]
    out=[hyp.get(i,("nan",""))[1].strip() for i in m["order"]]
    e=sum(1 for o in out if not o); empty+=e
    h=" ".join(o for o in out if o); R.append(ref);H.append(h)
    pc.append(jiwer.cer(ref,h)); pw.append(jiwer.wer(ref,h))
    print(b[-17:-5],"gt",len(gt),"found",m["n"],"empty",e,"CER %.1f WER %.1f"%(100*pc[-1],100*pw[-1]))
print("lines found",nf,"gt",ng,"empty",empty,"%.1f%%"%(100*empty/nf))
print("corpus CER %.2f WER %.2f | page-mean CER %.2f WER %.2f median CER %.2f"%(100*jiwer.cer(R,H),100*jiwer.wer(R,H),100*st.mean(pc),100*st.mean(pw),100*st.median(pc)))
json.dump({"R":R,"H":H},open("work/p20/pages.json","w"),ensure_ascii=False)
