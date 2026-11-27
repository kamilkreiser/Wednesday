# n3_checks.py — round 4, N3's three lines: the ignore pattern, the doctor lock warning, on scratch only.
# The real repo is only READ (git check-ignore --no-index with a scratch excludes file); a throw-away repo under the scratch base
# is used to see what `git status` shows (that repo is mine; the real .git is never touched).
import os, re, shutil, subprocess, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "r3_copies"))
from qlib import *
P = LANE + "/proposed"; SC = os.path.join(BASE, "n3_%d" % os.getpid()); os.makedirs(SC)
gi = re.findall(r"```new\n(.*?)\n```", open(os.path.join(P, "05_gitignore.md"), encoding="utf-8").read(), re.S)[0]
print("## 1. proposal 5's lines:"); print("\n".join("    " + l for l in gi.split("\n")))
ex = os.path.join(SC, "excludes"); open(ex, "w").write(gi + "\n")
T_ = "0_Brain/tasks/"
want_ign = [T_ + "STATE-wednesday.lock.d", T_ + "STATE-wednesday.lock.d/owner", T_ + "STATE-wednesday.lock.d/archive.tmp.123-0a1b2c3d4e5f6071", T_ + "STATE-wednesday.lock.d/state.tmp.123-0a1b2c3d4e5f6071",
            T_ + "STATE-wednesday.lock.d.stale-20261127-181430", T_ + "STATE-wednesday.lock.d.stale-20261127-181430/owner", T_ + "STATE-wednesday.lock.d.stale-20261127-181430/state.tmp.123-0a1b",
            T_ + "STATE-wednesday.lock.d.stale-20261127-181430/STATE-wednesday.lock.d/owner", T_ + "STATE-tuesday.lock.d/owner", T_ + "STATE-friday.lock.d.stale-20261127-000000/owner",
            T_ + "STATE-wednesday.md.tmp.4242", T_ + "STATE-wednesday-archive.md.tmp.4242", "0_Brain/wake/WAKE-wednesday.md", "0_Brain/wake/WAKE-wednesday.md.tmp.99", "2_Project_Files/wake/out/WAKE-wednesday.md"]
want_not = [T_ + "STATE-wednesday.md", T_ + "STATE-wednesday-archive.md", T_ + "STATE-tuesday.md", T_ + "STATE-tuesday-archive.md", T_ + "STATE-friday.md", T_ + "STATE-friday-archive.md",
            T_ + "EXPIRING-GRANTS.md", T_ + "NEXT-PICKUP.md", "2_Project_Files/wake/out/STATUS_round3.md", "2_Project_Files/wake/handover.sh", "2_Project_Files/qa-checks/wake-r4/verdict.md"]
print("## 1a. the REAL repo, read-only: git check-ignore -v --no-index with the scratch excludes file (the pattern that decides is named)")
bad = 0
for pth, want in [(p, True) for p in want_ign] + [(p, False) for p in want_not]:
    r = subprocess.run(["git", "-C", R, "-c", "core.excludesFile=" + ex, "check-ignore", "-v", "--no-index", pth], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    src = r.stdout.decode().strip().split("\t")[0]
    ign = r.returncode == 0
    by = ("proposal 5" if ex in src else "ALREADY by the tree's own rules: " + src) if ign else "-"
    ok = ign == want
    bad += not ok
    print("- %-88s %-11s %s%s" % (pth, "IGNORED" if ign else "not ignored", by, "" if ok else "   <<< NOT AS EXPECTED"))
print("   not as expected: %d of %d" % (bad, len(want_ign) + len(want_not)))
print("## 1b. a throw-away repo holding ONLY proposal 5's lines as .gitignore: what `git status --porcelain --untracked-files=all` lists")
g = os.path.join(SC, "repo"); os.makedirs(g)
def git(*a): return subprocess.run(["git", "-C", g] + list(a), stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode()
git("init", "-q"); open(os.path.join(g, ".gitignore"), "w").write(gi + "\n"); git("add", ".gitignore"); git("-c", "user.name=qa", "-c", "user.email=qa@example.invalid", "commit", "-q", "-m", "x")
for pth in want_ign + want_not[:6]:   # (instrument fix: run 1 made the two bare lock-directory paths as FILES and then could not make files inside them)
    if any(q.startswith(pth + "/") for q in want_ign): continue
    os.makedirs(os.path.dirname(os.path.join(g, pth)), exist_ok=True)
    if not os.path.exists(os.path.join(g, pth)): open(os.path.join(g, pth), "w").write("x\n")
st_ = git("status", "--porcelain", "--untracked-files=all").strip().split("\n")
print("   listed as untracked (%d): %s" % (len(st_), [l[3:] for l in st_]))
print("   expected exactly the six STATE files: %s" % (sorted(l[3:] for l in st_) == sorted(want_not[:6])))

print("## 2. the doctor snippet in a stub harness (ok/warn stubbed; doctor.sh itself is not run)")
snip = open(os.path.join(P, "doctor_check_snippet.sh"), encoding="utf-8").read()
hp = os.path.join(SC, "doctor_harness.sh")
open(hp, "w").write('set -uo pipefail\nPROJECT_DIR="$1"\nok()   { printf \'OK: %s\\n\' "$1"; }\nwarn() { printf \'WARN: %s | %s\\n\' "$1" "${2:-}"; }\n' + snip)
def doc(root):
    r = subprocess.run(["/bin/bash", hp, root], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV(), cwd=SC); return r.returncode, r.stdout.decode(), r.stderr.decode()
def tree(name):
    r = mk(name, "n3doc_%d" % os.getpid()); return r
def lockwarn(o): return [l for l in o.split("\n") if "write lock is standing" in l]
dead = subprocess.Popen([sys.executable, "-c", "pass"]); dead.wait()
import socket
host = socket.gethostname()
cases = [("no lock at all (control: silent)", lambda r: None, 0),
         ("a lock dir with an owner file (dead pid here)", lambda r: (os.mkdir(lockd(r)), open(os.path.join(lockd(r), "owner"), "w").write("pid: %d\nhost: %s\nstarted: 2026-11-27 10:00:00 AEDT\nepoch: 1\ntoken: t\n" % (dead.pid, host))), 1),
         ("a lock dir with NO owner file", lambda r: os.mkdir(lockd(r)), 1),
         ("the lock path is a regular FILE", lambda r: open(lockd(r), "w").write("x"), 1),
         ("the lock path is a dangling symlink", lambda r: os.symlink(os.path.join(r, "nowhere"), lockd(r)), 1),
         ("ANOTHER seat's lock dir in this tree (STATE-tuesday.lock.d)", lambda r: os.mkdir(lockd(r, "tuesday")), 1),
         ("two locks (wednesday and friday)", lambda r: (os.mkdir(lockd(r)), os.mkdir(lockd(r, "friday"))), 2),
         ("ONLY a set-aside directory (.stale-<stamp>) (control: silent)", lambda r: os.mkdir(lockd(r) + ".stale-20261127-101500"), 0),
         ("a set-aside directory AND a live lock", lambda r: (os.mkdir(lockd(r) + ".stale-20261127-101500"), os.mkdir(lockd(r))), 1),
         ("an owner file holding hostile text (backticks, $( ), quotes)", lambda r: (os.mkdir(lockd(r)), open(os.path.join(lockd(r), "owner"), "w").write("pid: `touch %s/PWNED_BT` $(touch %s/PWNED_DS) \"; touch %s/PWNED_Q; echo \"\nhost: x' ; touch %s/PWNED_SQ ; '\n" % (r, r, r, r))), 1)]
for label, make, want in cases:
    r = tree(re.sub(r"\W+", "_", label)[:36]); make(r)
    rc, o, e = doc(r); lw = lockwarn(o)
    rec = re.findall(r"mv -n '[^']*' '[^']*'", "\n".join(lw))
    okline = all(re.fullmatch(r"mv -n '(.+\.lock\.d)' '\1\.stale-\d{8}-\d{6}'", x) for x in rec) and len(rec) == len(lw)
    pw = [f for f in os.listdir(r) if f.startswith("PWNED")] + [f for f in os.listdir(SC) if f.startswith("PWNED")]
    ran = "-"
    if rec and "hostile" not in label:
        assert all(x.count(BASE) == 2 for x in rec)
        ran = [subprocess.run(["/bin/sh", "-c", x], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).returncode for x in rec]
        rc2, o2, e2 = doc(r); after = len(lockwarn(o2))
    else: after = "-"
    print("- %-62s rc %d; lock warnings %d (expected %d) %s; each carries one exact `mv -n` line %s; says the seat may run it %s; names pgrep %s; stderr %r; PWNED files %s | the line(s) run: %s; warnings afterwards: %s"
          % (label, rc, len(lw), want, "ok" if len(lw) == want else "<<< NOT AS EXPECTED", okline if lw else "-", all("the seat may run this itself" in x for x in lw) if lw else "-",
             all("pgrep -fl handover_core.py" in x for x in lw) if lw else "-", e[:80], pw or "none", ran, after))
    if "hostile" in label: print("      the warning text: " + lw[0][:330])
# the doctor line against the tool's own line
r = tree("same_line"); ho(r, "write", "--stdin", data=blk("S0")); os.mkdir(lockd(r)); open(os.path.join(lockd(r), "owner"), "w").write("pid: %d\nhost: %s\nstarted: x\ntoken: t\n" % (dead.pid, host))
rc, o, e = doc(r); rct, ot, et = ho(r, "write", "--stdin", data=blk("A"), env={"HANDOVER_LOCK_WAIT": "1"})
strip = lambda s: re.sub(r"stale-\d{8}-\d{6}", "stale-<stamp>", s)
dl = strip(re.findall(r"mv -n '[^']*' '[^']*'", o)[0]); tl = strip([l.strip() for l in et.split("\n") if l.strip().startswith("mv -n '")][0])
print("- doctor's recovery line == the line the tool itself prints for the same lock (stamp aside): %s; the tool said %s" % (dl == tl, "STALE LOCK" if "STALE LOCK" in et else "LOCK BUSY"))
print("  doctor's whole output for that tree: " + o.strip().replace("\n", " // ")[:700])
print("## 2b. the snippet inserted where proposal 4 says, on a scratch copy of doctor.sh, with proposal 7: /bin/bash -n")
doc_l = open(R + "/2_Project_Files/doctor.sh", encoding="utf-8").read().split("\n")
a = [i for i, l in enumerate(doc_l) if l.startswith('RC="$PROJECT_DIR/2_Project_Files/tools/rules_card.py"')]
e_ = next(i for i in range(a[0], len(doc_l)) if doc_l[i] == "fi")
new = doc_l[:e_ + 1] + snip.rstrip("\n").split("\n") + doc_l[e_ + 1:]
t7 = open(os.path.join(P, "07_doctor_pickup_warning.md"), encoding="utf-8").read()
o7 = re.search(r"```old\n(.*?)\n```", t7, re.S).group(1); n7 = re.search(r"```new\n(.*?)\n```", t7, re.S).group(1)
out = os.path.join(SC, "doctor_with_4_and_7.sh"); open(out, "w", encoding="utf-8").write("\n".join(new).replace(o7, n7))
rr = subprocess.run(["/bin/bash", "-n", out], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
names = sorted(set(re.findall(r"^\s*(?:for\s+)?([A-Z_]+)(?:=|\s+in\b)", snip, re.M)))
print("- anchor found %d time(s) at line %d; /bin/bash -n rc %d %s; names the snippet assigns %s; of them already used in doctor.sh: %s; `2>/dev/null` in the snippet %d (control: `2>&1` %d)"
      % (len(a), a[0] + 1, rr.returncode, rr.stdout.decode()[:100], names, [n for n in names if re.search(r"\b%s\b" % n, "\n".join(doc_l))] or "none", snip.count("2>/dev/null"), snip.count("2>&1")))
