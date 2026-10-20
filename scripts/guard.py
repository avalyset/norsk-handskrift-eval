"""Heldout-vakt: avbryt hvis en reservert side-ID kommer inn. Importeres av alle skript som tar side-ID-er."""
import sys, re, os
_H = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "heldout-60.txt")
def heldout_ids():
    return {l.split("\t")[0] for l in open(_H, encoding="utf8") if l.strip() and not l.startswith("#")}
def check(ids, allow_heldout=False):
    if allow_heldout: return
    bad = sorted(set(re.sub(r"(__\d+)?(\.\w+)?$", "", str(i)).split("/")[-1] for i in ids) & heldout_ids())
    if bad:
        sys.exit("HELDOUT-VAKT: avbryter, reserverte sider i inndata: " + ", ".join(bad[:5]))
