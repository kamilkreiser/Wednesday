"""QA-W-GATE-TEST-R2: byte scan of EVERY committed file at a commit for ids of the owner's test sessions.
usage: idscan.py <repo> <commit> <main-commit> [--detail]
Classes (bytes, case-insensitive hex): any UUID; session_id field value; transcript_path holding a UUID; prompt_id value;
toolu_ ids; event "uuid" field; request ids (req_...); msg_ ids.  A file is LANE if its blob differs from main's (or main lacks it)."""
import re, subprocess, sys, collections
repo, commit, main = sys.argv[1:4]
detail = "--detail" in sys.argv
def git(*a): return subprocess.run(["git", "-C", repo] + list(a), capture_output=True, check=True).stdout
def tree(c):
    out = {}
    for line in git("ls-tree", "-r", "-z", c).split(b"\0"):
        if not line: continue
        meta, path = line.split(b"\t", 1)
        out[path.decode()] = meta.split()[2].decode()
    return out
U = rb"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
CL = collections.OrderedDict([
 ("any UUID", re.compile(U)),
 ("session_id field w/ value", re.compile(rb'session_?[iI]d\\?"?\s*[:=]\s*\\?"?(' + U + rb')')),
 ("transcript_path w/ UUID", re.compile(rb'transcript_path[^\n]{0,400}?(' + U + rb')\.jsonl')),
 ("prompt_id w/ value", re.compile(rb'prompt_?[iI]d\\?"?\s*[:=]\s*\\?"(?!<prompt-id>)([^"\\<]{4,})')),
 ("toolu_ id", re.compile(rb'toolu_[A-Za-z0-9_]+')),
 ("event uuid field w/ value", re.compile(rb'"uuid"\s*:\s*"(?!<event-uuid>)([^"]+)"')),
 ("req_ id", re.compile(rb'\breq_[A-Za-z0-9]{12,}')),
 ("msg_ id", re.compile(rb'\bmsg_[A-Za-z0-9]{12,}')),
])
T = tree(commit); MT = tree(main)
tot = collections.Counter(); totlane = collections.Counter(); dist = collections.defaultdict(set); distlane = collections.defaultdict(set)
perfile = []
for path, sha in sorted(T.items()):
    b = git("cat-file", "blob", sha)
    lane = MT.get(path) != sha
    row = {}
    for name, rx in CL.items():
        ms = list(rx.finditer(b))
        if not ms: continue
        vals = [ (m.group(1) if m.groups() else m.group(0)).lower() for m in ms]
        row[name] = (len(ms), len(set(vals)), sorted(set(vals))[:3])
        tot[name] += len(ms); dist[name].update(vals)
        if lane: totlane[name] += len(ms); distlane[name].update(vals)
    if row: perfile.append((path, lane, row))
print("commit %s vs main %s: %d files, %d differ from main (LANE)" % (commit[:12], main[:12], len(T), sum(1 for p,s in T.items() if MT.get(p)!=s)))
print("%-28s %10s %10s %12s %12s" % ("class", "all:hits", "all:dist", "LANE:hits", "LANE:dist"))
for name in CL:
    print("%-28s %10d %10d %12d %12d" % (name, tot[name], len(dist[name]), totlane[name], len(distlane[name])))
print("-- LANE files with any hit (path: class=hits/distinct):")
for path, lane, row in perfile:
    if lane:
        print("  ", path, "; ".join("%s=%d/%d%s" % (k, v[0], v[1], (" e.g. " + repr(v[2][0][:40])) if detail else "") for k, v in row.items()))
print("-- files identical to main with any hit: %d (classes summed below)" % sum(1 for p,l,r in perfile if not l))
if detail:
    for path, lane, row in perfile:
        if not lane: print("   main:", path, "; ".join("%s=%d/%d" % (k, v[0], v[1]) for k, v in row.items()))
sess = set(distlane["session_id field w/ value"]) | set(distlane["transcript_path w/ UUID"])
print("DISTINCT SESSION IDS IN LANE FILES (session_id field or transcript_path):", len(sess))
