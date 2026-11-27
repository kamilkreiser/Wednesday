# proposals_check.py — proposals 2 to 9 and FOR-KAM, each against a SCRATCH COPY of its real target. Nothing real is written.
import os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *
P = LANE + "/proposed"; SC = os.path.join(BASE, "proposals"); os.makedirs(SC, exist_ok=True)
applied = {}
print("## 1. every old block once, no new block applied, replacement applied to a scratch copy, shell targets parse")
for f in sorted(os.listdir(P)):
    if not re.match(r"(0[2-9]_.*|FOR-KAM.*)\.md$", f): continue
    s = open(os.path.join(P, f), encoding="utf-8").read()
    m = re.search(r"^TARGET: `([^`]+)`", s, re.M); tgt = m.group(1) if m else None
    olds = re.findall(r"```old\n(.*?)\n```", s, re.S); news = re.findall(r"```new\n(.*?)\n```", s, re.S)
    rb_ = re.findall(r"^ROLLBACK[^\n]*", s, re.M)
    line = "- %s -> %s | old blocks %d, new blocks %d, ROLLBACK lines %d" % (f, tgt, len(olds), len(news), len(rb_))
    if not tgt or not os.path.isfile(os.path.join(R, tgt)): print(line + " | NO TARGET (insert-style proposal)"); continue
    t = open(os.path.join(R, tgt), encoding="utf-8").read(); t2 = applied.get(tgt, t)
    cnt = [t.count(o) for o in olds]; already = [n in t for n in news]
    for o, n in zip(olds, news):
        if t2.count(o) == 1: t2 = t2.replace(o, n)
    if not olds and news: t2 = t2.rstrip("\n") + "\n" + news[0] + "\n"
    if not f.startswith("FOR-KAM") and not f.startswith("09_"): applied[tgt] = t2
    out = os.path.join(SC, f.replace(".md", "") + "__" + os.path.basename(tgt)); open(out, "w", encoding="utf-8").write(t2)
    extra = ""
    if tgt.endswith((".sh", ".command")):
        r = subprocess.run(["/bin/bash", "-n", out], stdout=subprocess.PIPE, stderr=subprocess.STDOUT); extra = " | /bin/bash -n rc %d %s" % (r.returncode, r.stdout.decode()[:100])
    seatwords = sorted(set(re.findall(r"\b(?:wednesday|tuesday|friday|Wednesday|Tuesday|Friday|WEDNESDAY|TUESDAY|FRIDAY)\b", "\n".join(news))))
    print(line + " | old found %s time(s); a new block already in the target: %s; seat names in the new text: %s%s" % (cnt, already, seatwords or "none", extra))

print("## 2. proposals 2, 3 and 6 applied TOGETHER to one scratch copy of each CLAUDE.md (they share root CLAUDE.md)")
for tgt in ("CLAUDE.md", "0_Brain/CLAUDE.md"):
    t = open(os.path.join(R, tgt), encoding="utf-8").read(); t2 = applied[tgt]
    import difflib
    sm = difflib.SequenceMatcher(None, t.split("\n"), t2.split("\n"), autojunk=False)
    ops = [op for op in sm.get_opcodes() if op[0] != "equal"]
    removed = [l for op in ops for l in t.split("\n")[op[1]:op[2]]]
    added = [l for op in ops for l in t2.split("\n")[op[3]:op[4]]]
    print("- %s: %d lines removed, %d lines added; removed lines:" % (tgt, len(removed), len(added)))
    for l in removed: print("      - " + l[:150])
    kam = "the full lesson load STAYS"; kam2 = "**All** of `learnings/`"
    k = kam if tgt == "CLAUDE.md" else kam2
    print("    Kam's sentence %r: in the original %d time(s), in the patched copy %d time(s); the whole numbered item byte-identical: %s"
          % (k, t.count(k), t2.count(k), (re.search(r"\n2\. Read ALL of.*?(?=\n3\. )", t, re.S).group(0) in t2) if tgt == "CLAUDE.md" else ("\n3. **All** of `learnings/` (this is deliberate — token cost accepted)\n" in t2)))
    open(os.path.join(SC, "ALL__" + os.path.basename(tgt) + ("_brain" if "0_Brain" in tgt else "_root")), "w", encoding="utf-8").write(t2)

print("## 3. FOR-KAM: are the sentences it quotes Kam's files' sentences, word for word?")
fk = open(os.path.join(P, "FOR-KAM_lesson-load-ruling.md"), encoding="utf-8").read()
root_t = open(R + "/CLAUDE.md", encoding="utf-8").read(); brain_t = open(R + "/0_Brain/CLAUDE.md", encoding="utf-8").read()
quotes = re.findall(r"^> (.*)$", fk, re.M)
norm = lambda x: re.sub(r"\s+", " ", x).strip()
for q in quotes:
    q1 = norm(q); hit_root = q1 in norm(root_t); hit_brain = q1 in norm(brain_t)
    if not (hit_root or hit_brain):
        hit_root = norm(re.sub(r"^\d+\. ", "", q1)) in norm(re.sub(r"\n\s+", " ", root_t))
    print("- quoted: %s... -> found word for word (whitespace folded) in root CLAUDE.md: %s, in 0_Brain/CLAUDE.md: %s" % (q1[:70], hit_root, hit_brain))
launcher = open(R + "/Launch_Wednesday.command", encoding="utf-8").read()
for words in ('go with a boot as you recommend', 'Do NOT read the individual lesson files at boot', 'Kam 2026-11-18, a trial on this seat', 'cost 34% of the window'):
    print("- the launcher holds the words FOR-KAM cites, %r: %d time(s)" % (words, launcher.count(words)))
import glob
ls = [p for p in glob.glob(R + "/0_Brain/learnings/*.md") if re.match(r"\d{4}-\d{2}-\d{2}_", os.path.basename(p))]
print("- FOR-KAM says '292 lesson files, 1,229,441 bytes': dated lesson files now %d, %d bytes (all .md in learnings/: %d)" % (len(ls), sum(os.path.getsize(p) for p in ls), len(glob.glob(R + "/0_Brain/learnings/*.md"))))
print("- words FOR-KAM attributes to Kam in quotation marks: %s" % re.findall(r'Kam[^|\n]{0,40}: "([^"]+)"', fk))

print("## 4. gitignore proposal, with a scratch excludes file (git check-ignore is a read)")
gi = re.findall(r"```new\n(.*?)\n```", open(os.path.join(P, "05_gitignore.md"), encoding="utf-8").read(), re.S)[0]
ex = os.path.join(SC, "excludes"); open(ex, "w").write(gi + "\n")
paths = ["0_Brain/wake/WAKE-wednesday.md", "0_Brain/wake/WAKE-wednesday.dropped.txt", "0_Brain/wake/WAKE-wednesday.md.tmp.123", "2_Project_Files/wake/out/WAKE-wednesday.md",
         "0_Brain/tasks/STATE-wednesday.md.tmp.123", "0_Brain/tasks/STATE-wednesday-archive.md.tmp.123", "0_Brain/tasks/STATE-wednesday.lock.d/owner",
         "0_Brain/tasks/STATE-wednesday.lock.d.stale-20261127-140000/owner", "0_Brain/tasks/STATE-wednesday.md", "0_Brain/tasks/STATE-wednesday-archive.md",
         "2_Project_Files/wake/out/STATUS_round1.md", "2_Project_Files/wake/out/tests_last_run.txt", "2_Project_Files/wake/handover.sh"]
for pth in paths:
    r = subprocess.run(["git", "-C", R, "-c", "core.excludesFile=" + ex, "check-ignore", "-v", "--no-index", pth], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    src = r.stdout.decode().strip().split("\t")[0]
    print("- %-66s %s" % (pth, ("IGNORED by " + (src.split(":", 2)[-1] if src else "?") + (" (the scratch excludes file)" if ex in src else " (ALREADY by the tree's own .gitignore)")) if r.returncode == 0 else "not ignored"))

print("## 5. the doctor snippet: inserted where proposal 4 says, on a scratch copy of doctor.sh (never run); then the snippet alone in a stub harness")
doc = open(R + "/2_Project_Files/doctor.sh", encoding="utf-8").read().split("\n")
a = [i for i, l in enumerate(doc) if l.startswith('RC="$PROJECT_DIR/2_Project_Files/tools/rules_card.py"')]
snip = open(os.path.join(P, "doctor_check_snippet.sh"), encoding="utf-8").read()
if len(a) == 1:
    e = next(i for i in range(a[0], len(doc)) if doc[i] == "fi")
    nxt = [l for l in doc[e + 1:e + 6] if l.strip()][:1]
    new = doc[:e + 1] + snip.rstrip("\n").split("\n") + doc[e + 1:]
    t7 = open(os.path.join(P, "07_doctor_pickup_warning.md"), encoding="utf-8").read()
    o7 = re.search(r"```old\n(.*?)\n```", t7, re.S).group(1); n7 = re.search(r"```new\n(.*?)\n```", t7, re.S).group(1)
    both = "\n".join(new).replace(o7, n7)
    out = os.path.join(SC, "doctor_with_4_and_7.sh"); open(out, "w", encoding="utf-8").write(both)
    r = subprocess.run(["/bin/bash", "-n", out], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print("- anchor found once at line %d, block closes at line %d, next text: %r; proposals 4 + 7 together: /bin/bash -n rc %d %s" % (a[0] + 1, e + 1, nxt, r.returncode, r.stdout.decode()[:120]))
    names = sorted(set(re.findall(r"^\s*([A-Z_]+)=", snip, re.M)))
    doct = "\n".join(doc)
    print("- names the snippet assigns: %s; already used in doctor.sh: %s (positive control: RC used %d times)" % (names, [n for n in names if re.search(r"\b%s\b" % n, doct)] or "none", len(re.findall(r"\bRC\b", doct))))
    print("- doctor.sh options line: %s; the snippet's `2>/dev/null` count: %d; `2>&1` count: %d" % ([l for l in doc if l.startswith("set -")], snip.count("2>/dev/null"), snip.count("2>&1")))
HARN = 'set -uo pipefail\nPROJECT_DIR="$1"\nok()   { printf \'OK: %s\\n\' "$1"; }\nwarn() { printf \'WARN: %s | %s\\n\' "$1" "${2:-}"; }\n' + snip
hp = os.path.join(SC, "doctor_harness.sh"); open(hp, "w").write(HARN)
def doc_run(root, env=None):
    r = subprocess.run(["/bin/bash", hp, root], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=ENV(env)); return r.returncode, r.stdout.decode(), r.stderr.decode()
for folder in ("TUESDAY", "FRIDAY"):
    r_ = mk("doc_" + folder, "proposals_doc", folder=folder)
    rc, o, e = doc_run(r_); print("- a %s tree before its own cut-over (tools present, no state, no pack): rc %d, stdout %r, stderr %r" % (folder, rc, o, e))
    open(os.path.join(T(r_), "STATE-wednesday.md"), "w").write("the Wednesday seat's state, synced by git\n"); os.makedirs(os.path.join(r_, "0_Brain/wake")); open(os.path.join(r_, "0_Brain/wake/WAKE-wednesday.md"), "w").write("x\n")
    rc, o, e = doc_run(r_); print("    the same tree holding the WEDNESDAY seat's state file and pack: rc %d, stdout %r, stderr %r" % (rc, o, e))
    rc, o, e = doc_run(r_, {"WED_AGENT": folder.lower()}); print("    with WED_AGENT=%s as its launcher exports it: rc %d, stdout %r" % (folder.lower(), rc, o))
rw = mk_real("doc_wed", "proposals_doc")
rc, o, e = doc_run(rw); print("- a WEDNESDAY tree before cut-over: rc %d, stdout %r, stderr %r" % (rc, o, e))
ho(rw, "write", "--stdin", data=blk("CUT"))
rc, o, e = doc_run(rw); print("- cut over, no pack: %s" % o.strip().replace("\n", " // ")[:330])
wp(rw); rc, o, e = doc_run(rw); print("- cut over, pack built BEFORE... (the pack was built after the state write): %s" % o.strip().replace("\n", " // ")[:330])
os.mkdir(lockd(rw)); open(os.path.join(lockd(rw), "owner"), "w").write("pid: 1\nhost: nowhere\n")
rc, o, e = doc_run(rw); print("- the same with a STALE LOCK directory left by a dead writer: does doctor say anything about the lock? %s | %s" % ("lock" in o.lower(), o.strip().replace("\n", " // ")[:200]))

print("## 6. proposal 8 and other readers of the legacy pickup that the cut-over freezes")
ns = open(R + "/2_Project_Files/scheduler/nas_staleness.sh", encoding="utf-8").read()
print("- nas_staleness.sh: the old line occurs %d time(s); lines naming a per-seat file there: %s" % (ns.count("$SEAT_DIR/0_Brain/tasks/NEXT-PICKUP.md"), [l for l in ns.split("\n") if "$SEAT_DIR/0_Brain/" in l][:8]))
for rel in ("2_Project_Files/tools/stuart_weekly/stuart_weekly.sh", "2_Project_Files/scheduler/nas_sync.sh", "2_Project_Files/fleet/cockpit/wednesday_rotate.sh"):
    t = open(os.path.join(R, rel), encoding="utf-8", errors="replace").read()
    hits = [(i + 1, l.strip()[:150]) for i, l in enumerate(t.split("\n")) if "NEXT-PICKUP" in l and not l.lstrip().startswith("#")]
    named = any(rel.split("/")[-1] in open(os.path.join(P, f), encoding="utf-8").read() for f in os.listdir(P) if f.endswith(".md"))
    print("- %s: code lines reading NEXT-PICKUP: %s; named anywhere in proposed/*.md: %s" % (rel, hits or "none", named))
