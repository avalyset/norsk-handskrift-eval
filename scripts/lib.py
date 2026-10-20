import re, json, random, xml.etree.ElementTree as ET
import numpy as np
def _loc(t): return t.rsplit("}",1)[-1]
def parse_gt(xmlpath):
    """-> list of (text, Nx2 int polygon) i filens rekkefølge (kun TextLine)"""
    out=[]
    for el in ET.parse(xmlpath).getroot().iter():
        if _loc(el.tag)!="TextLine": continue
        pts=None; txt=""
        for ch in el:
            if _loc(ch.tag)=="Coords" and pts is None: pts=np.array([[int(float(v)) for v in p.split(",")] for p in ch.get("points").split()],dtype=np.int32)
            if _loc(ch.tag)=="TextEquiv":
                for u in ch:
                    if _loc(u.tag)=="Unicode": txt=u.text or ""
        out.append((re.sub(r"\s+"," ",txt).strip(),pts))
    return out
def load_hyp(p):
    d={}
    for l in open(p,encoding="utf8").read().split("\n"):
        if not l or l.startswith("#"): continue
        i,_,r=l.partition(" "); c,_,t=r.partition(" "); d[i]=t.strip()
    return d
def edits(ref,hyp):
    """(char edits S+D+I, len(ref)) -- jiwer, rå tekst"""
    import jiwer
    if not ref: return len(hyp),0
    if not hyp: return len(ref),len(ref)
    o=jiwer.process_characters(ref,hyp); return o.substitutions+o.deletions+o.insertions,len(ref)
def wedits(ref,hyp):
    import jiwer
    r=ref.split(); h=hyp.split()
    if not r: return len(h),0
    if not h: return len(r),len(r)
    o=jiwer.process_words(ref,hyp); return o.substitutions+o.deletions+o.insertions,len(r)
def boot(errs,lens,B=2000,seed=20261020,units=None):
    """percentile bootstrap over enheter; returnerer (punkt, lo, hi) i %"""
    n=len(errs); rng=random.Random(seed); e=np.array(errs,float); l=np.array(lens,float); v=[]
    for _ in range(B):
        ix=[rng.randrange(n) for _ in range(n)]; v.append(100*e[ix].sum()/l[ix].sum())
    v.sort(); return 100*e.sum()/l.sum(), v[49], v[1949]
