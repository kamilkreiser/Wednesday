# launcher_harness.py — the launcher proposal on a SCRATCH COPY. The launcher is never run: three regions are lifted from the copy
# (the seat-files block; hunk A when present; everything from SEAT_HOST= to the line before `clear`, which holds the prompt and, patched,
# hunk B) and evaluated by /bin/bash (3.2) under `set -u` with IDENTICAL dummy variables for the original and the patched copy.
# The step-5 backtick pair of the existing prompt runs a STUB note_entry.sh in a scratch cwd. python3 is the real one except where stated.
import hashlib, os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qlib import *
D = os.path.join(BASE, "launcher"); os.makedirs(D, exist_ok=True)
ORIG = os.path.join(D, "orig.command"); PAT = os.path.join(D, "patched.command")
shutil.copy(R + "/Launch_Wednesday.command", ORIG); shutil.copy(ORIG, PAT)
DIFF = LANE + "/proposed/01_launcher_boot_prompt.diff"
p = subprocess.run(["patch", "-s", PAT, DIFF], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print("## 0. apply and parse")
print("patch on the scratch copy: rc %d %s" % (p.returncode, p.stdout.decode().strip()))
for f in (ORIG, PAT):
    r = subprocess.run(["/bin/bash", "-n", f], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print("/bin/bash -n %s: rc %d %s" % (os.path.basename(f), r.returncode, r.stdout.decode().strip()[:200]))
v = subprocess.run(["/bin/bash", "--version"], stdout=subprocess.PIPE).stdout.decode().split("\n")[0]; print("shell: " + v)
REV = os.path.join(D, "patched_then_reversed.command"); shutil.copy(PAT, REV)
r = subprocess.run(["patch", "-s", "-R", REV, DIFF], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
print("rollback line (patch -R) on the patched copy: rc %d; byte-identical to the original again: %s" % (r.returncode, rd(REV) == rd(ORIG)))
o = open(ORIG, encoding="utf-8").read().split("\n"); pt = open(PAT, encoding="utf-8").read().split("\n")
import difflib
ops = [op for op in difflib.SequenceMatcher(None, o, pt, autojunk=False).get_opcodes() if op[0] != "equal"]
print("line-level difference original -> patched: %s (inserted lines %d, deleted %d, replaced %d)"
      % ([(op[0], op[1] + 1, op[3] + 1, op[4]) for op in ops], sum(op[4] - op[3] for op in ops if op[0] == "insert"),
         sum(op[2] - op[1] for op in ops if op[0] == "delete"), sum(1 for op in ops if op[0] == "replace")))
added = [l for op in ops for l in pt[op[3]:op[4]]]
code = [l for l in added if l.strip() and not l.lstrip().startswith("#")]
names = sorted(set(re.findall(r"\b(WAKE_[A-Z0-9_]+)=", "\n".join(added))))
orig_text = "\n".join(o)
print("names the added lines assign (%d): %s" % (len(names), " ".join(names)))
print("  of those, already used in the ORIGINAL launcher (whole word): %s (positive control: WAKE_MODE_FILE occurs %d times)"
      % ([n for n in names if re.search(r"\b%s\b" % n, orig_text)] or "none", len(re.findall(r"\bWAKE_MODE_FILE\b", orig_text))))
print("in the added lines (comments excluded): backticks %d; '$(' %d; eval %d; 'set -e' %d; 'exit' %d; 'rm ' %d; 'export' %d; bash-4-only forms %d (positive control: 'if [' %d)"
      % (sum(l.count("`") for l in code), sum(l.count("$(") for l in code), sum(len(re.findall(r"\beval\b", l)) for l in code),
         sum(l.count("set -e") for l in code), sum(len(re.findall(r"\bexit\b", l)) for l in code), sum(len(re.findall(r"\brm\s", l)) for l in code),
         sum(len(re.findall(r"\bexport\b", l)) for l in code),
         sum(len(re.findall(r"declare -A|mapfile|readarray|\$\{[A-Za-z_]+(,,|\^\^)|&>>|\|&|coproc", l)) for l in code), sum(l.count("if [") for l in code)))
for l in code:
    if "$(" in l: print("    the '$(' lines: " + l.strip()[:150])
# (run 1 of this script walked difflib's inserted lines, whose first line is the rules-card block's own `fi`: the depth count was off by one
# and listed guarded lines as outside. Instrument error, kept in raw/launcher_harness_run1_instrument_error.txt. Now the two hunk FILES are walked,
# after checking that the patched copy contains each of them verbatim.)
hunks = [open(LANE + "/proposed/launcher_hunk_%s.sh" % x, encoding="utf-8").read() for x in "AB"]
print("the patched copy contains hunk A and hunk B verbatim: %s; their line count %d == inserted lines %d"
      % (all(hk in "\n".join(pt) for hk in hunks), sum(len(hk.split("\n")) - 1 for hk in hunks), len(added)))
outside = []
depth = 0
for l in "".join(hunks).split("\n"):
    s = l.strip()
    if not s or s.startswith("#"): continue
    if depth == 0 and not l.startswith('if [ "$AGENT" = "wednesday" ]; then'):
        outside.append(l)
    if re.match(r"^\s*if\b", l) : depth += 1
    if s == "fi": depth -= 1
print("added statements OUTSIDE an `if AGENT = wednesday` block: %s" % outside)


def region(path):
    L = open(path, encoding="utf-8").read().split("\n")
    def find(pred, start=0):
        for i in range(start, len(L)):
            if pred(L[i]): return i
        raise SystemExit("anchor not found in " + path)
    a = find(lambda l: l == 'if [ "$AGENT" = "tuesday" ]; then' ); b = find(lambda l: l == "fi", a)
    assert "PICKUP_FILE=" in L[a + 1]
    hunkA = []
    hs = [i for i, l in enumerate(L) if l.startswith("# --- Wake pack (WED-170 step 1; Kam")]
    if hs:
        e = find(lambda l: l.startswith("# ── Arm panel_sync"), hs[0]); hunkA = L[hs[0]:e]
    c = find(lambda l: l.startswith('SEAT_HOST="$(hostname')); pe = find(lambda l: l == "clear", c)
    return L[a:b + 1], hunkA, L[c:pe]


STUBBIN = os.path.join(D, "bin_nopython"); os.makedirs(STUBBIN, exist_ok=True)
for tool in ("/usr/bin/tail", "/bin/cat", "/usr/bin/sed", "/usr/bin/head", "/usr/bin/tr"):
    if not os.path.exists(os.path.join(STUBBIN, os.path.basename(tool))): os.symlink(tool, os.path.join(STUBBIN, os.path.basename(tool)))


def run_seat(path, seat, root, tag, path_env=None, trace=False):
    seatmap, hunkA, body = region(path)
    cwd = os.path.join(D, "cwd_" + tag); os.makedirs(os.path.join(cwd, "2_Project_Files/tools"), exist_ok=True)
    open(os.path.join(cwd, "2_Project_Files/tools/note_entry.sh"), "w").write("#!/bin/bash\necho STUB-NOTE-ENTRY-WHERE\n")
    pre = ["set -u", "hostname() { echo stubhost; }", "AGENT=%s" % seat, "AGENT_UPPER=%s" % seat.upper(), 'PROJECT_DIR="%s"' % root,
           'BRAIN_DIR="$PROJECT_DIR/0_Brain"', "DEVMASTER='<<DEVMASTER>>'", "DEVMASTER_STATE='<<DEVMASTER_STATE>>'", "DEVMASTER_VAULT='<<DEVMASTER_VAULT>>'",
           "DASH_URL='<<DASH_URL>>'", "DASH_STATE='<<DASH_STATE>>'", "RULES_CARD_NOTE='<<RULES_CARD_NOTE>> '"]
    if trace: pre.insert(1, "PS4='+T '; set -x")
    out = os.path.join(D, "prompt_%s.txt" % tag)
    if os.path.exists(out): os.rename(out, out + ".prev.%d" % len(os.listdir(D)))
    script = "\n".join(pre + seatmap + hunkA + body) + "\nset +x\nprintf '%s' \"$INITIAL_PROMPT\" > \"" + out + "\"\n"
    hp = os.path.join(D, "harness_%s.sh" % tag); open(hp, "w").write(script)
    env = {"PATH": path_env or (os.path.dirname(sys.executable) + ":/usr/bin:/bin"), "HOME": cwd, "PYTHONDONTWRITEBYTECODE": "1", "LANG": "en_AU.UTF-8"}
    r = subprocess.run(["/bin/bash", hp], cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    return r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace"), rd(out)


def h(b): return hashlib.sha256(b).hexdigest()[:16] if b is not None else "NONE"


print("## 1. tuesday and friday: the prompt before and after, identical dummy variables")
for seat in ("tuesday", "friday"):
    root = mk_real("t_" + seat, "launcher_trees")       # a tree that even holds a working wake_pack.py and sources: the patched region must not use them
    rc0, o0, e0, p0 = run_seat(ORIG, seat, root, seat + "_orig")
    rc1, o1, e1, p1 = run_seat(PAT, seat, root, seat + "_patched")
    print("- %s: original rc %d, %d bytes, sha %s | patched rc %d, %d bytes, sha %s | BYTE-IDENTICAL %s | stdout identical %s (%r) | stderr identical %s (%r) | a wake directory was created: %s"
          % (seat, rc0, len(p0 or b""), h(p0), rc1, len(p1 or b""), h(p1), p0 is not None and p0 == p1, o0 == o1, o1[:60], e0 == e1, e1[:80],
             os.path.exists(os.path.join(root, "0_Brain/wake"))))
    print("    control (the prompts are the seats' own, not empty stubs): %s; 'WAKE' occurs %d times in the patched prompt"
          % ([x for x in (b"NEXT-PICKUP-TUESDAY", b"NEXT-PICKUP-FRIDAY", b"_ledger_laptop_datasec", b"_ledger_friday", b"STUB-NOTE-ENTRY-WHERE") if x in (p0 or b"")], (p1 or b"").count(b"WAKE")))
print("## 2. wednesday: the original prompt, then each build outcome on the patched copy")
rootw = mk_real("w_ok", "launcher_trees")
rc0, o0, e0, pw = run_seat(ORIG, "wednesday", rootw, "wed_orig")
print("- original: rc %d, %d bytes, sha %s; stderr %r" % (rc0, len(pw), h(pw), e0[:80]))
U = b"ultrathink\n\n"


def describe(label, rc, so, se, p, root, expect):
    # (run 1 compared every case with the ORIGINAL prompt of another tree, so the paths differed and every fallback read as OTHER:
    # instrument error. The original prompt is now evaluated for the SAME tree and PATH as the case.)
    global pw
    _rc, _o, _e, pw = run_seat(ORIG, "wednesday", root, "wed_origfor_" + os.path.basename(os.path.dirname(root)), path_env=describe.penv)
    kind = "OTHER"
    notice_first = False; why = ""
    if p is not None and b"FIRST ACTIONS (WAKE PACK boot" in p: kind = "PACK PROMPT"
    elif p is not None and p.startswith(U) and p.endswith(b"\n" + pw[len(U):]):
        mid = p[len(U):len(p) - len(pw[len(U):])].decode("utf-8", "replace")
        kind = "LEGACY whole (byte-identical below the notice)" if mid else "LEGACY, NO NOTICE"
        notice_first = mid.startswith("\U0001F534\U0001F534 THE WAKE PACK FAILED AT THIS LAUNCH")
        why = (mid.split("Why: ", 1)[1].split("\n")[0] if "Why: " in mid else "")[:210]
    elif p == pw: kind = "LEGACY, NO NOTICE"
    ok = (kind == "PACK PROMPT") if expect == "pack" else (kind.startswith("LEGACY whole") and notice_first)
    print("- %-62s rc %d -> %s; notice is the FIRST text after 'ultrathink': %s; %s\n      why: %s\n      stdout: %s | stderr: %r"
          % (label, rc, kind, notice_first, "as expected" if ok else "<<< NOT AS EXPECTED", why or "-", so.strip().replace("\n", " / ")[:200], se[:120]))
    return ok


rc, so, se, pn = run_seat(PAT, "wednesday", rootw, "wed_ok", trace=False)
describe.penv = None
ok_pack = describe("the pack builds (real wake_pack.py on a scratch copy of the real sources)", rc, so, se, pn, rootw, "pack")
packp = os.path.join(rootw, "0_Brain/wake/WAKE-wednesday.md")
print("      the prompt names the pack path: %s; the pack file exists: %s (%s bytes)" % (packp.encode() in (pn or b""), os.path.isfile(packp), os.path.getsize(packp) if os.path.isfile(packp) else "-"))
cases = []
r_missing = mk_real("w_notool", "launcher_trees"); os.rename(os.path.join(r_missing, "2_Project_Files/wake/wake_pack.py"), os.path.join(r_missing, "2_Project_Files/wake/wake_pack.py.gone_qa"))
cases.append(("the pack tool is missing", r_missing, None))
r_rc = mk_real("w_rc", "launcher_trees"); os.rename(os.path.join(r_rc, "0_Brain/tasks/EXPIRING-GRANTS.md"), os.path.join(r_rc, "grants.gone_qa"))
cases.append(("build rc non-zero (the grants file is missing)", r_rc, None))
r_stale = mk_real("w_stale", "launcher_trees"); wp(r_stale); os.rename(os.path.join(r_stale, "0_Brain/learnings/_ledger.md"), os.path.join(r_stale, "ledger.gone_qa"))
cases.append(("build rc non-zero while an OLDER pack from a previous launch is on disk", r_stale, None))
r_empty = mk_real("w_empty", "launcher_trees"); open(os.path.join(r_empty, "2_Project_Files/wake/wake_pack.py"), "w").write(
    "import os,sys\nd=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','0_Brain','wake'); os.makedirs(d,exist_ok=True); open(os.path.join(d,'WAKE-wednesday.md'),'w').close()\nprint('x  bytes: 0')\n")
cases.append(("exit 0 with an EMPTY pack file", r_empty, None))
r_nopack = mk_real("w_nopack", "launcher_trees"); open(os.path.join(r_nopack, "2_Project_Files/wake/wake_pack.py"), "w").write("print('pretend  bytes: 1  ~tokens: 1 of 60000')\n")
cases.append(("exit 0 with NO pack file", r_nopack, None))
r_nopy = mk_real("w_nopython", "launcher_trees")
cases.append(("python3 is not on the PATH (rc 127)", r_nopy, STUBBIN + ":/bin"))
r_budget = mk_real("w_budget", "launcher_trees"); open(os.path.join(r_budget, "0_Brain/learnings/_ledger.md"), "a").write("".join("\n| 2026-11-26 | **BIG-%d** %s Rule: %s. | c | 1 | - | - |\n" % (i, "x" * 200, "y " * 330) for i in range(700)))
cases.append(("over budget (a huge ledger)", r_budget, None))
r_host = mk_real("w_hostile", "launcher_trees"); open(os.path.join(r_host, "2_Project_Files/wake/wake_pack.py"), "w").write(
    "import sys\nsys.stderr.write('wake_pack: FAILED \\u2014 `touch \"$PROJECT_DIR/PWNED_BACKTICK\"` $(touch \"$PROJECT_DIR/PWNED_DOLLAR\") \"; touch \"$PROJECT_DIR/PWNED_QUOTE\"; echo \" ${PROJECT_DIR} \\\\$(id) %s\\n')\nsys.exit(2)\n")
cases.append(("build fails with a HOSTILE last line (backticks, $( ), quotes)", r_host, None))
r_host2 = mk_real("w_hostile_ok", "launcher_trees"); open(os.path.join(r_host2, "2_Project_Files/wake/wake_pack.py"), "w").write(
    "import os,sys\nd=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','0_Brain','wake'); os.makedirs(d,exist_ok=True); open(os.path.join(d,'WAKE-wednesday.md'),'w').write('PACK\\n')\nprint('x  bytes: 1 `touch \"$PROJECT_DIR/PWNED_BACKTICK\"` $(touch \"$PROJECT_DIR/PWNED_DOLLAR\") \"; touch \"$PROJECT_DIR/PWNED_QUOTE\"; echo \" ${PROJECT_DIR}')\n")
all_ok = ok_pack
for label, root, penv in cases:
    rc, so, se, p = run_seat(PAT, "wednesday", root, "wed_" + os.path.basename(os.path.dirname(root)), path_env=penv)
    describe.penv = penv
    all_ok = describe(label, rc, so, se, p, root, "legacy") and all_ok
    if "HOSTILE" in label:
        print("      files named PWNED* in the tree: %s; the hostile text is in the prompt literally: %s" % ([f for f in os.listdir(root) if f.startswith("PWNED")], b"`touch" in p and b"$(touch" in p))
    if "OLDER pack" in label:
        print("      the older pack is still on disk: %s; the prompt names it: %s" % (os.path.isfile(os.path.join(root, "0_Brain/wake/WAKE-wednesday.md")), b"WAKE-wednesday.md WHOLE" in p))
describe.penv = None
rc, so, se, p = run_seat(PAT, "wednesday", r_host2, "wed_hostile_ok")
describe("the build SUCCEEDS with a hostile summary line", rc, so, se, p, r_host2, "pack")
print("      files named PWNED* in the tree: %s; the hostile text is in the prompt literally: %s" % ([f for f in os.listdir(r_host2) if f.startswith("PWNED")], b"`touch" in p and b"$(touch" in p))
print("every wednesday case as expected: %s" % all_ok)

print("## 3. the new wednesday prompt against the legacy one")
_rc, _o, _e, pw = run_seat(ORIG, "wednesday", rootw, "wed_orig_again")
i = pn.find(b"FIRST ACTIONS"); j = pw.find(b"FIRST ACTIONS"); k = pn.find(b"\n5. Read yesterday's and today's notes"); m = pw.find(b"\n5. Read yesterday's and today's notes")
print("head before FIRST ACTIONS identical: %s (%d bytes); tail from step 5 identical: %s (%d bytes); steps 1 to 4: legacy %d bytes -> new %d bytes"
      % (pn[:i] == pw[:j], i, pn[k:] == pw[m:], len(pn) - k, m - j, k - i))
mid = pn[i:k]
print("in the new steps 1 to 4: unexpanded '${' %d; '$WAKE' %d; '<<' sentinels %s; backticks %d; '$(' %d; STUB-NOTE-ENTRY-WHERE new/legacy %d/%d"
      % (mid.count(b"${"), mid.count(b"$WAKE"), sorted(set(re.findall(rb"<<([A-Z_]+)>>", mid))), mid.count(b"`"), mid.count(b"$("), pn.count(b"STUB-NOTE-ENTRY-WHERE"), pw.count(b"STUB-NOTE-ENTRY-WHERE")))
open(os.path.join(D, "prompt_wednesday_new.txt"), "wb").write(pn); open(os.path.join(D, "prompt_wednesday_legacy.txt"), "wb").write(pw)
print("## 4. does anything in the ADDED text execute? (xtrace: a command substitution shows as a '++T' line)")
for tag, path, root in (("orig", ORIG, rootw), ("patched_ok", PAT, rootw), ("patched_fail", PAT, r_rc)):
    rc, so, se, p = run_seat(path, "wednesday", root, "trace_" + tag, trace=True)
    nested = [l for l in se.split("\n") if l.startswith("++T")]
    cmds = sorted(set(re.sub(r"\s.*", "", l[4:].strip()) for l in nested))
    print("- %-13s rc %d; command substitutions executed: %d; the commands: %s" % (tag, rc, len(nested), cmds))
