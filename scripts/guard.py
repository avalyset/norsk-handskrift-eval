"""Heldout-vakt: avbryt hvis en reservert side-ID kommer inn. Importeres av alle skript som tar side-ID-er."""
import sys, re, os, hashlib
_H = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "work", "heldout-60.txt")
def heldout_ids():
    return {l.split("\t")[0] for l in open(_H, encoding="utf8") if l.strip() and not l.startswith("#")}
def _ok():
    """heldout tillates kun når prereg/run.py setter NORHAND_HELDOUT_OK = SHA256 av heldout-60.txt (bevisst handling, ikke tilfeldig)"""
    return os.environ.get("NORHAND_HELDOUT_OK") == hashlib.sha256(open(_H,"rb").read()).hexdigest()
def check(ids, allow_heldout=False):
    if allow_heldout or _ok(): return
    bad = sorted(set(re.sub(r"(__\d+)?(\.\w+)?$", "", str(i)).split("/")[-1] for i in ids) & heldout_ids())
    if bad:
        sys.exit("HELDOUT-VAKT: avbryter, reserverte sider i inndata: " + ", ".join(bad[:5]))

if __name__ == "__main__":   # brukes av scripts/dec.sh: guard.py <listefil med linje-ID-er>
    check([l.strip() for l in open(sys.argv[1]) if l.strip()])
