import sys; sys.path.insert(0,"scripts"); import lib
gt={f"t{int(l.split(chr(9))[0]):04d}":l.rstrip("\n").split("\t",1)[1] for l in open("work/hf_gt.tsv",encoding="utf8")}
ids=sorted(gt)
for name,card in (("nolm",(7.52,22.99)),("lm",(6.36,18.11))):
    h=lib.load_hyp(f"work/hf_{name}.txt"); ce=[];cl=[];we=[];wl=[]
    for i in ids:
        a,b=lib.edits(gt[i],h.get(i,"")); c,d=lib.wedits(gt[i],h.get(i,"")); ce.append(a);cl.append(b);we.append(c);wl.append(d)
    c=lib.boot(ce,cl); w=lib.boot(we,wl)
    print(f"{name}: CER {c[0]:.2f} [{c[1]:.2f}, {c[2]:.2f}] kort {card[0]} {'INNE' if c[1]<=card[0]<=c[2] else 'UTE'} | WER {w[0]:.2f} [{w[1]:.2f}, {w[2]:.2f}] kort {card[1]} {'INNE' if w[1]<=card[1]<=w[2] else 'UTE'}")
