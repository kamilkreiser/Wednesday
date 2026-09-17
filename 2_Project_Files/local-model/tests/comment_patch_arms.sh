#!/bin/bash
# comment_patch_arms.sh — red-proof for the comment_patch tier (2026-09-17 19:5x, HARNESS_WIDEN_PROPOSAL_2026-09-17b §3):
# night/build_comment_input.sh, tasks/comment_patch/{checker.sh,cp_gates.py,token_equiv.cjs,prepare_clone.sh,task.md} and the
# night_run.sh RETRY-ONCE route. Every checker arm runs the REAL checker.sh end to end under sandbox-exec (off-host outbound
# denied) in ONE scratch clone made here exactly as night_run.sh makes it (`git clone --shared --no-checkout` + `checkout
# --detach <tip>` + the tier's prepare_clone.sh) under a mktemp -d. Goldens are the brief's own fence (the input's
# comment.brief_diff); mutants are the golden's AFTER image with one change, re-diffed against the tip (difflib, 3 context).
#
#   ARM0   golden KS-979                                   → RESULT PASS, apply_mode=strict
#   ARM0b  golden KS-1118-F3a (verification.ts)            → PASS          ARM0c golden KS-1118-F3b (ks1103 test) → PASS
#   ARM0d  KS-1118-F3a with the '-- no caller' line dropped → FAIL C7     ARM0e KS-1118-F3b + a test title edited → FAIL C4
#   ARM1a  OLD doc_patch checker on the KS-979 golden       → no PASS (cannot grade: no required sections)
#   ARM1b  OLD code_patch checker on the KS-979 golden      → no PASS (cannot grade: no service/test/red cell)
#   ARM1c  build_doc_input.sh on the KS-979 brief           → rc 2 REFUSED (no `## Required`)
#   ARM2a  golden + ORG_B→ORG_A in the org-less cell (:177) → FAIL C4 (identifier)
#   ARM2b  golden + that cell's it('…') title reworded      → FAIL C4 (a literal)
#   ARM2c  golden + a semicolon deleted (:176)              → FAIL C4 (punctuation)
#   ARM2d  golden + `===` → `==` (:102)                     → FAIL C4
#   ARM2e  golden + template TAIL text edited (:120)        → FAIL C4
#   ARM2i  INSTRUMENT: a `//` inside a template literal's text after `${}` edited — token_equiv.cjs says NOT equal, while a
#          bare ts.createScanner(skipTrivia) pass says EQUAL (why C4 walks parser leaves, not the raw scanner)
#   ARM3a  golden + `// @ts-expect-error` inserted inside the range → FAIL C4b (and C4 PASS)
#   ARM3b  a real `eslint-disable-next-line` rule edited (ks480-provenance.test.ts:19, range :19) → FAIL C4b only
#   ARM4   golden + a comment reworded OUTSIDE the range (:159)   → FAIL C5 only
#   ARM5   golden with the old :171 line kept beside the new lines → FAIL C6 only
#   ARM6a  golden with one brief '+' line dropped            → FAIL C7 only   ARM6b a '+' line indented +2 → FAIL C7 only
#   ARM7   golden + a second file (a provenance.ts comment)  → FAIL C3
#   ARM8a  two ```diff blocks → FAIL C1   ARM8b prose after the block → FAIL C1
#   ARM8c  a '-' line the file never had → FAIL C2   ARM8d fabricated context → PASS, C2 "ONLY REANCHORED" named
#   ARM8e  a miscounted hunk header → PASS, C2 "--recount" named   ARM8f the clone at the wrong SHA (input tip edited) → FAIL C0
#   ARM9   MUTATION KILL (checker copies): C4 short-circuited PASSes the ARM2a code change on a range widened over the
#          code lines (the real checker FAILs it at C4 only); C4b short-circuited PASSes ARM3a; C5 short-circuited PASSes ARM4
#   ARM10  builder refusals: R0 no premises · R0 a premise with no instrument · R1 a .sh product · R4 a range over the it(
#          line · R5 a '-' line one number off · R5 a '-' line not byte-unique (ks1103 banner rule :202 == :204) · R6 a
#          non-ASCII '+' · R7 a '+' code line · R7 a '+' line already at the tip · R8 a '+' `// @ts-expect-error` (C4b) ·
#          R8 a '+' unterminated `/*` (C4) · R9 a synthetic READY hunk 5 lines from the range · R10 Linear stub "In Progress" ·
#          R11 GitHub stub: an open PR changes the file · R11 GitHub unreachable (fail closed) · OK the real KS-979 build rc 0
#   ARM11  JS parity on scripts/audit/lock-discovery.mjs: a docblock reword → PASS; an import name changed → FAIL C4
#   RUNNER the NEW night_run.sh's own trigger + retry builder lines, cut from the file: ARM2a's FAIL C4 retries with a
#          `FAIL C4` verdict and the comment_patch sentence; the OLD runner does not retry it; ARM0 PASS and ARM8a FAIL C1
#          retry under neither
# Usage: bash comment_patch_arms.sh   (env CP_ARMS_KEEP_SCRATCH=1 keeps nothing special — nothing is ever deleted)
# rc 0 = every arm holds. Writes only under a mktemp -d. Never writes to the source checkout (read verbs + a --shared clone).
set -u
exec python3 - "$@" <<'PYARMS'
import difflib, http.server, json, os, re, shutil, socketserver, subprocess, sys, tempfile, threading, time

LM = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model"
SRC = "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files"
CP = f"{LM}/tasks/comment_patch"
CK = f"{CP}/checker.sh"
SB = f"{LM}/tests/fixtures/a3b_line/nonet.sb"
BUILDER = f"{LM}/night/build_comment_input.sh"
IN979 = f"{LM}/night/inputs/comment_979.json"
IN1118A = f"{LM}/night/inputs/comment_1118F3a.json"
IN1118B = f"{LM}/night/inputs/comment_1118F3b.json"
NEW_RUNNER = f"{LM}/night/night_run.sh"
OLD_RUNNER = f"{LM}/night/night_run.sh.pre-0917-commentpatch"
sys.path.insert(0, CP)
import cp_gates as G

for f in (CK, SB, BUILDER, IN979, IN1118A, IN1118B, NEW_RUNNER, OLD_RUNNER, f"{LM}/tasks/doc_patch/checker.sh", f"{LM}/tasks/code_patch/checker.sh"):
    if not os.path.exists(f):
        print(f"FATAL: missing {f}"); sys.exit(2)
W = tempfile.mkdtemp(prefix="cp_arms.")
print(f"comment_patch arms {time.strftime('%F %T')} · scratch {W}")
RESULTS = []
def arm(name, ok, detail):
    RESULTS.append((name, ok)); print(f"{'PASS' if ok else 'FAIL'} {name} — {detail}")
def run(cmd, env=None, timeout=600):
    e = dict(os.environ); e.update(env or {})
    # own process group, so a timeout kills the whole tree (an old checker's npm/vitest children included)
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=e, start_new_session=True)
    try:
        so, _ = pr.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        import signal
        os.killpg(pr.pid, signal.SIGKILL); so, _ = pr.communicate()
        return 124, (so or "") + f"\nTIMEOUT after {timeout}s (process group killed)"
    return pr.returncode, so

inp979 = json.load(open(IN979, encoding="utf-8"))
TIP = inp979["tip"]
for p in (IN1118A, IN1118B):
    assert json.load(open(p))["tip"] == TIP, f"{p} is not at {TIP}"
# grep positive control (the arms read verdict lines with re; control that the reader finds a known line)
assert re.search(r"^RESULT:", "x\nRESULT: PASS (9/9)\n", re.M)

# ---------------------------------------------------------------- the clone (as night_run.sh makes it)
CLONE = os.path.join(W, "clone")
rc, o = run(["git", "clone", "--shared", "--no-checkout", SRC, CLONE])
rc2, o2 = run(["git", "-C", CLONE, "checkout", "--detach", TIP])
rc3, o3 = run(["bash", f"{CP}/prepare_clone.sh", IN979, CLONE])
head = run(["git", "-C", CLONE, "rev-parse", "HEAD"])[1].strip()
print(f"clone rc={rc} checkout rc={rc2} prepare rc={rc3} HEAD={head} :: {o3.strip().splitlines()[-1] if o3.strip() else ''}")
if head != TIP or rc3 != 0:
    print("FATAL: clone not prepared"); sys.exit(2)
src_dirty0 = run(["git", "-C", SRC, "status", "--porcelain", "--untracked-files=no"])[1]

def tip_text(path):
    return run(["git", "-C", SRC, "show", f"{TIP}:{path}"])[1]

def fence(diff_text, extra=""):
    return "```diff\n" + diff_text.rstrip("\n") + "\n```\n" + extra

def mkdiff(path, before_lines, after_lines):
    d = list(difflib.unified_diff([l + "\n" for l in before_lines], [l + "\n" for l in after_lines], f"a/{path}", f"b/{path}", n=3))
    return "".join(d)

def golden_after(inp):
    path = inp["product_file"]; tl = G.split_lines(inp["files"][path])
    secs = G.parse_diff_sections(inp["comment"]["brief_diff"])
    after, minus, plus, err = G.strict_apply(tl, secs[0]["hunks"])
    assert err is None, err
    return tl, after

def check(label, inp, out_text, checker=CK, sandbox=True, timeout=600):
    d = os.path.join(W, label); os.makedirs(d, exist_ok=True)
    ip = os.path.join(d, "input.json"); json.dump(inp, open(ip, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    op = os.path.join(d, "out.md"); open(op, "w", encoding="utf-8").write(out_text)
    cmd = (["sandbox-exec", "-f", SB] if sandbox else []) + ["bash", checker, ip, op, CLONE]
    rc, o = run(cmd, timeout=timeout)
    open(os.path.join(d, "checker.out"), "w", encoding="utf-8").write(o)
    fails = re.findall(r"^FAIL (C\d+b?)\b", o, re.M)
    res = (re.search(r"^RESULT:.*$", o, re.M) or [None])
    res = res.group(0) if hasattr(res, "group") else "NO RESULT"
    clean = run(["git", "-C", CLONE, "status", "--porcelain", "--", inp.get("product_file", "")])[1].strip() == ""
    return rc, o, fails, res, clean

def only(fails, gate):
    return fails == [gate]

P979 = inp979["product_file"]
tl979, ga979 = golden_after(inp979)
G979 = fence(inp979["comment"]["brief_diff"])

# ---------------------------------------------------------------- ARM0
rc, o, fails, res, clean = check("ARM0", inp979, G979)
arm("ARM0 golden KS-979 → PASS strict", rc == 0 and res.startswith("RESULT: PASS") and "apply_mode=strict" in res and clean, f"rc={rc} {res} clone-clean={clean}")
ARM0_DIR = os.path.join(W, "ARM0")
for lbl, p in (("ARM0b", IN1118A), ("ARM0c", IN1118B)):
    ii = json.load(open(p, encoding="utf-8"))
    rc, o, fails, res, clean = check(lbl, ii, fence(ii["comment"]["brief_diff"]))
    arm(f"{lbl} golden {ii['ticket']['identifier']} → PASS", rc == 0 and res.startswith("RESULT: PASS") and clean, f"rc={rc} {res}")
iiA = json.load(open(IN1118A, encoding="utf-8")); tlA, gaA = golden_after(iiA)
mut = [l for l in gaA if "takes the hash strategy, as v2 already does -- no caller" not in l]
assert len(mut) == len(gaA) - 1
rc, o, fails, res, clean = check("ARM0d", iiA, fence(mkdiff(iiA["product_file"], tlA, mut)))
arm("ARM0d KS-1118-F3a, one brief '+' line dropped → FAIL C7", rc != 0 and only(fails, "C7"), f"fails={fails} {res}")
iiB = json.load(open(IN1118B, encoding="utf-8")); tlB, gaB = golden_after(iiB)
k = [i for i, l in enumerate(gaB) if "it('C1 {contentHash} with no rows answers 200 verified:false from one lookup'" in l]
assert len(k) == 1
mut = list(gaB); mut[k[0]] = mut[k[0]].replace("from one lookup", "from a single lookup")
rc, o, fails, res, clean = check("ARM0e", iiB, fence(mkdiff(iiB["product_file"], tlB, mut)))
arm("ARM0e KS-1118-F3b + a test title edited → FAIL C4", rc != 0 and "C4" in fails and fails[0] == "C4", f"fails={fails} {res}")

# ---------------------------------------------------------------- ARM1 negative controls (the old harness)
rc, o, fails, res, clean = check("ARM1a", inp979, G979, checker=f"{LM}/tasks/doc_patch/checker.sh")
arm("ARM1a OLD doc_patch checker on the golden → cannot grade (D0-D3 pass, then KeyError on defect_line; no PASS)", rc != 0 and "RESULT: PASS" not in o and "KeyError: 'defect_line'" in o, f"rc={rc} last: {o.strip().splitlines()[-1][:160] if o.strip() else ''}")
# the old code_patch checker cannot read its own contract from this input (no service_dir / test_dir / reference test), then
# falls through to a whole-subdir `npx vitest` baseline that cannot resolve offline — bounded at 90 s, process group killed
rc, o, fails, res, clean = check("ARM1b", inp979, G979, checker=f"{LM}/tasks/code_patch/checker.sh", timeout=90)
arm("ARM1b OLD code_patch checker on the golden → cannot grade (KeyError on its contract fields; no PASS)", rc != 0 and "RESULT: PASS" not in o and "KeyError: 'service_dir'" in o,
    f"rc={rc} KeyError(service_dir)={'yes' if chr(39)+'service_dir'+chr(39) in o else 'no'} KeyError(test_dir)={'yes' if chr(39)+'test_dir'+chr(39) in o else 'no'} last: {o.strip().splitlines()[-1][:120] if o.strip() else ''}")
rc, o = run(["bash", f"{LM}/tasks/doc_patch/build_doc_input.sh", "KS-979", os.path.join(W, "ARM1c.json"), f"{LM}/night/briefs/KS-979.md", f"product={P979}"])
arm("ARM1c build_doc_input.sh on the KS-979 brief → REFUSED", rc == 2 and "REFUSED" in o and not os.path.exists(os.path.join(W, "ARM1c.json")), f"rc={rc} {o.strip()[-160:]}")

# ---------------------------------------------------------------- ARM2 C4
def idx(lines, needle, after_idx=0):
    ks = [i for i, l in enumerate(lines) if needle in l and i >= after_idx]
    return ks
t_orgless = idx(ga979, "it('does NOT 403 an org-less caller")
assert len(t_orgless) == 1; t0 = t_orgless[0]
def mutate(label, fn, desc, expect):
    m = list(ga979); fn(m)
    assert m != ga979, label
    rc, o, fails, res, clean = check(label, inp979, fence(mkdiff(P979, tl979, m)))
    ok = rc != 0 and expect(fails) and clean
    arm(f"{label} {desc}", ok, f"fails={fails} {res} :: {next((l for l in o.splitlines() if l.startswith('FAIL ' + (fails[0] if fails else 'X'))), '')[:200]}")
    return o
def m2a(m):
    assert "organizationUuid: ORG_B" in m[t0 + 2]; m[t0 + 2] = m[t0 + 2].replace("ORG_B", "ORG_A")
ARM2A_OUT = mutate("ARM2a", m2a, "ORG_B→ORG_A in the org-less cell → FAIL C4", lambda f: f and f[0] == "C4")
mutate("ARM2b", lambda m: m.__setitem__(t0, m[t0].replace("org-less caller", "orgless caller")), "it() title reworded → FAIL C4", lambda f: f and f[0] == "C4")
def m2c(m):
    assert m[t0 + 1].rstrip().endswith("};"); m[t0 + 1] = m[t0 + 1].rstrip()[:-1]
mutate("ARM2c", m2c, "a semicolon deleted → FAIL C4", lambda f: f and f[0] == "C4")
k = idx(ga979, "typeof address === 'object'"); assert len(k) == 1
mutate("ARM2d", lambda m: m.__setitem__(k[0], m[k[0]].replace("===", "==")), "=== → == → FAIL C4", lambda f: f and f[0] == "C4")
k2 = idx(ga979, "`${baseUrl}/api/documents`"); assert len(k2) == 1
mutate("ARM2e", lambda m: m.__setitem__(k2[0], m[k2[0]].replace("/api/documents`", "/api/document`")), "template tail text edited → FAIL C4", lambda f: f and f[0] == "C4")
# ARM2i instrument
TS = os.path.join(CLONE, "Blockchain/Dev/node_modules/typescript")
ta = os.path.join(W, "trick_a.ts"); tb = os.path.join(W, "trick_b.ts")
open(ta, "w").write("const a = `x ${1} y // not a comment ${2} z`;\nconst r = /\\/\\*/g; // real comment\n")
open(tb, "w").write("const a = `x ${1} y // NOT a comment ${2} z`;\nconst r = /\\/\\*/g; // real comment\n")
jq, err = G.node_json(["compare", TS, ta, tb, "t.ts"])
bare = os.path.join(W, "bare_scanner.cjs")
open(bare, "w").write("const ts=require(process.argv[2]);const fs=require('fs');function t(f){const s=ts.createScanner(ts.ScriptTarget.Latest,true,ts.LanguageVariant.Standard,fs.readFileSync(f,'utf8'));const o=[];let k;while((k=s.scan())!==ts.SyntaxKind.EndOfFileToken)o.push(k+':'+s.getTokenText());return o;}console.log(JSON.stringify(t(process.argv[3]))===JSON.stringify(t(process.argv[4]))?'EQUAL':'DIFFER');\n")
brc, bo = run([G.NODE, bare, TS, ta, tb])
arm("ARM2i instrument: template-text `//` edit → token_equiv NOT equal; bare scanner EQUAL", jq is not None and jq["equal"] is False and bo.strip() == "EQUAL",
    f"token_equiv equal={jq and jq['equal']} first_diff={jq and jq['first_diff']} · bare scanner: {bo.strip()}")

# ---------------------------------------------------------------- ARM3 C4b
k3 = idx(ga979, "SUBJECT, not the org-less caller)"); assert len(k3) == 1
m = list(ga979); m.insert(k3[0] + 1, "  // @ts-expect-error arm: a directive slipped into a comment edit")
rc, o, fails, res, clean = check("ARM3a", inp979, fence(mkdiff(P979, tl979, m)))
arm("ARM3a golden + `// @ts-expect-error` inside the range → FAIL C4b only", rc != 0 and only(fails, "C4b") and "PASS C4 " in o, f"fails={fails} {res}")
P480 = "Blockchain/Dev/services/originate/src/__tests__/ks480-provenance.test.ts"
t480 = tip_text(P480); tl480 = G.split_lines(t480)
assert tl480[18].startswith("// eslint-disable-next-line @typescript-eslint/no-var-requires"), tl480[18]
new19 = tl480[18].replace("no-var-requires", "no-require-imports")
m480 = list(tl480); m480[18] = new19
inp480 = {"ticket": {"identifier": "ARM3b", "title": "arm", "description": "arm"}, "repo": {"source_checkout": SRC, "tip": TIP}, "tip": TIP,
          "task_type": "comment_patch", "product_file": P480, "repo_subdir": "Blockchain/Dev",
          "comment": {"ranges": [[19, 19]], "must_remove": [{"line": 19, "text": tl480[18]}], "expected_plus": [new19], "brief_diff": ""}, "files": {P480: t480}}
rc, o, fails, res, clean = check("ARM3b", inp480, fence(mkdiff(P480, tl480, m480)))
arm("ARM3b real eslint-disable rule edited (ks480:19) → FAIL C4b only", rc != 0 and only(fails, "C4b"), f"fails={fails} {res}")

# ---------------------------------------------------------------- ARM4..ARM7
k4 = idx(ga979, "// provenance.ts:128-129 / QA F-4: both sides go through"); assert len(k4) == 1
m = list(ga979); m[k4[0]] = m[k4[0]].replace("both sides go through", "the two sides go through")
rc, o, fails, res, clean = check("ARM4", inp979, fence(mkdiff(P979, tl979, m)))
arm("ARM4 a comment reworded OUTSIDE the range (:159) → FAIL C5 only", rc != 0 and only(fails, "C5"), f"fails={fails} {res}")
ARM4_DIFF = mkdiff(P979, tl979, m)
k5 = idx(ga979, '// provenance.ts:109 gives the reason'); assert len(k5) == 1
m = list(ga979); m.insert(k5[0], tl979[170])
rc, o, fails, res, clean = check("ARM5", inp979, fence(mkdiff(P979, tl979, m)))
arm("ARM5 old :171 kept beside the new lines → FAIL C6 only", rc != 0 and only(fails, "C6"), f"fails={fails} {res}")
k6 = idx(ga979, 'to validate against", so resolving'); assert len(k6) == 1
m = list(ga979); del m[k6[0]]
rc, o, fails, res, clean = check("ARM6a", inp979, fence(mkdiff(P979, tl979, m)))
arm("ARM6a one brief '+' line dropped → FAIL C7 only", rc != 0 and only(fails, "C7"), f"fails={fails} {res}")
m = list(ga979); m[k6[0]] = "  " + m[k6[0]]
rc, o, fails, res, clean = check("ARM6b", inp979, fence(mkdiff(P979, tl979, m)))
arm("ARM6b a '+' line indented +2 → FAIL C7 only", rc != 0 and only(fails, "C7"), f"fails={fails} {res}")
PPROV = "Blockchain/Dev/services/originate/src/services/provenance.ts"
tpv = G.split_lines(tip_text(PPROV)); mpv = list(tpv); assert "Store verbatim instead" in mpv[106]
mpv[106] = mpv[106].replace("Store verbatim instead", "Store it verbatim instead")
rc, o, fails, res, clean = check("ARM7", inp979, fence(inp979["comment"]["brief_diff"].rstrip("\n") + "\n" + mkdiff(PPROV, tpv, mpv)))
arm("ARM7 golden + a second file → FAIL C3", rc != 0 and fails == ["C3"] and "stopped at C3" in res and run(["git", "-C", CLONE, "status", "--porcelain", "--", PPROV])[1].strip() == "", f"fails={fails} {res}")

# ---------------------------------------------------------------- ARM8 C1 / C2 / C0
rc, o, fails, res, clean = check("ARM8a", inp979, G979 + "\n" + G979)
arm("ARM8a two ```diff blocks → FAIL C1", rc != 0 and fails == ["C1"], f"fails={fails} {res}")
ARM8A_DIR = os.path.join(W, "ARM8a")
rc, o, fails, res, clean = check("ARM8b", inp979, G979 + "\nThis changes only comments.\n")
arm("ARM8b prose after the block → FAIL C1", rc != 0 and fails == ["C1"], f"fails={fails} {res}")
g = inp979["comment"]["brief_diff"]
assert g.count("-  // svc_api_keys.organization_id for admin-issued keys.") == 1
rc, o, fails, res, clean = check("ARM8c", inp979, fence(g.replace("-  // svc_api_keys.organization_id for admin-issued keys.", "-  // svc_api_keys.organization_id for admin issued keys.")))
arm("ARM8c a '-' line the file never had → FAIL C2", rc != 0 and fails == ["C2"], f"fails={fails} {res}")
glines = g.split("\n"); ci = next(i for i, l in enumerate(glines) if l == "   });")
fab = list(glines); fab[ci] = "   }); // invented context"
rc, o, fails, res, clean = check("ARM8d", inp979, fence("\n".join(fab)))
arm("ARM8d fabricated context → PASS with C2 ONLY REANCHORED named", rc == 0 and "ONLY REANCHORED" in o and res.startswith("RESULT: PASS") and "apply_mode=reanchored" in res, f"{res} :: {next((l for l in o.splitlines() if l.startswith('PASS C2')), '')[:160]}")
assert g.count("@@ -169,8 +169,12 @@") == 1
rc, o, fails, res, clean = check("ARM8e", inp979, fence(g.replace("@@ -169,8 +169,12 @@", "@@ -169,8 +169,13 @@")))
arm("ARM8e miscounted header → PASS with C2 --recount named", rc == 0 and "--recount" in o and "apply_mode=recount" in res, f"{res}")
wrong = json.loads(json.dumps(inp979)); wrong["tip"] = "efaaa6034f036dd9538ee35b189217b1d08b90a9"; wrong["repo"]["tip"] = wrong["tip"]
rc, o, fails, res, clean = check("ARM8f", wrong, G979)
arm("ARM8f clone at the wrong SHA → FAIL C0", rc != 0 and fails == ["C0"], f"fails={fails} {res}")

# ---------------------------------------------------------------- ARM9 mutation kill
def mutant_checker(name, old, new):
    d = os.path.join(W, name, "tasks"); os.makedirs(os.path.join(d, "comment_patch"), exist_ok=True)
    for f in ("checker.sh", "token_equiv.cjs"):
        shutil.copy2(f"{CP}/{f}", os.path.join(d, "comment_patch", f))
    os.symlink(f"{LM}/tasks/code_patch", os.path.join(d, "code_patch"))
    t = open(f"{CP}/cp_gates.py", encoding="utf-8").read(); assert t.count(old) == 1, old
    open(os.path.join(d, "comment_patch", "cp_gates.py"), "w", encoding="utf-8").write(t.replace(old, new))
    return os.path.join(d, "comment_patch", "checker.sh")
wide = json.loads(json.dumps(inp979)); wide["comment"]["ranges"] = [[169, 181]]
m = list(ga979); m2a(m); D2A = fence(mkdiff(P979, tl979, m))
rc_r, o_r, f_r, res_r, _ = check("ARM9a_real", wide, D2A)
ck4 = mutant_checker("mut_c4", "    res, _ = gate_c4(before_path, after_path, ts_dir, name)\n",
                     "    res = [x for x in gate_c4(before_path, after_path, ts_dir, name)[0] if x[1] != 'C4'] + [('PASS', 'C4', 'SHORT-CIRCUITED (mutant)')]\n")
rc_m, o_m, f_m, res_m, _ = check("ARM9a_mut", wide, D2A, checker=ck4)
arm("ARM9a C4 load-bearing: widened range, ORG_B→ORG_A — real FAIL C4 only; C4-short-circuited PASS", only(f_r, "C4") and rc_m == 0 and res_m.startswith("RESULT: PASS"), f"real fails={f_r} · mutant {res_m}")
m = list(ga979); m.insert(k3[0] + 1, "  // @ts-expect-error arm: a directive slipped into a comment edit"); D3A = fence(mkdiff(P979, tl979, m))
ck4b = mutant_checker("mut_c4b", "    if j[\"directives_equal\"]:\n", "    if True:\n")
rc_m, o_m, f_m, res_m, _ = check("ARM9b_mut", inp979, D3A, checker=ck4b)
arm("ARM9b C4b load-bearing: ARM3a under a C4b-short-circuited checker → PASS", rc_m == 0 and res_m.startswith("RESULT: PASS"), f"mutant {res_m}")
ck5 = mutant_checker("mut_c5", "    res += gate_c5(before, after, ranges)\n", "    res += [('PASS', 'C5', 'SHORT-CIRCUITED (mutant)')]\n")
rc_m, o_m, f_m, res_m, _ = check("ARM9c_mut", inp979, fence(ARM4_DIFF), checker=ck5)
arm("ARM9c C5 load-bearing: ARM4 under a C5-short-circuited checker → PASS", rc_m == 0 and res_m.startswith("RESULT: PASS"), f"mutant {res_m}")

# ---------------------------------------------------------------- ARM11 .mjs parity
PMJS = "Blockchain/Dev/scripts/audit/lock-discovery.mjs"
tmj = tip_text(PMJS); tlm = G.split_lines(tmj)
assert tlm[54] == "/** Repo root via git, so the corpus does not depend on the caller's cwd. */", tlm[54]
assert tlm[51].startswith("import { isIsoDate, isLapsed }"), tlm[51]
new55 = "/** Repo root via git, so the corpus never depends on the caller's cwd. */"
mm = list(tlm); mm[54] = new55
imj = {"ticket": {"identifier": "ARM11", "title": "arm", "description": "arm"}, "repo": {"source_checkout": SRC, "tip": TIP}, "tip": TIP,
       "task_type": "comment_patch", "product_file": PMJS, "repo_subdir": "Blockchain/Dev",
       "comment": {"ranges": [[50, 55]], "must_remove": [{"line": 55, "text": tlm[54]}], "expected_plus": [new55], "brief_diff": ""}, "files": {PMJS: tmj}}
rc, o, fails, res, clean = check("ARM11a", imj, fence(mkdiff(PMJS, tlm, mm)))
arm("ARM11a .mjs docblock reword → PASS", rc == 0 and res.startswith("RESULT: PASS"), f"{res}")
mm2 = list(mm); mm2[51] = mm2[51].replace("isLapsed }", "isLapsed as lapsed }")
rc, o, fails, res, clean = check("ARM11b", imj, fence(mkdiff(PMJS, tlm, mm2)))
arm("ARM11b .mjs import changed inside the range → FAIL C4", rc != 0 and only(fails, "C4"), f"fails={fails} {res}")

# ---------------------------------------------------------------- RUNNER route
def cut_runner(path):
    t = open(path, encoding="utf-8").read()
    i = t.index('  if [ "${NIGHT_RETRY_ON_PARTIAL:-1}" = "1" ]'); j = t.index("; then\n", i)
    cond = t[i:j].strip()
    p0 = t.index("<<'PYR'\n") + len("<<'PYR'\n"); p1 = t.index("\nPYR\n", p0)
    assert t.count("<<'PYR'\n") == 1 and t.count('  if [ "${NIGHT_RETRY_ON_PARTIAL:-1}" = "1" ]') == 1
    return cond, t[p0:p1]
def runner_decision(path, run_dir):
    cond, pyr = cut_runner(path)
    verdict = next((l for l in open(os.path.join(run_dir, "checker.out"), encoding="utf-8").read().splitlines() if l.startswith("RESULT:")), "")[:120]
    sh = os.path.join(W, "runner_cond.sh"); open(sh, "w").write(cond + "; then echo RETRY; else echo NORETRY; fi\n")
    rc, o = run(["bash", sh], env={"VERDICT": verdict, "RUN": run_dir, "RETRY_DONE": "", "NIGHT_RETRY_ON_PARTIAL": "1"})
    fb = None
    if o.strip() == "RETRY":
        py = os.path.join(W, "runner_pyr.py"); open(py, "w").write(pyr)
        outj = os.path.join(run_dir, "retry_input." + os.path.basename(path) + ".json")
        r2, o2 = run(["python3", py, os.path.join(run_dir, "input.json"), os.path.join(run_dir, "checker.out"), outj])
        fb = json.load(open(outj)) ["retry_feedback"] if r2 == 0 else {"error": o2}
    return o.strip(), fb
A2 = os.path.join(W, "ARM2a")
dn, fbn = runner_decision(NEW_RUNNER, A2)
do, fbo = runner_decision(OLD_RUNNER, A2)
arm("RUNNER-a ARM2a FAIL C4: NEW retries with a FAIL C4 verdict + the comment_patch sentence; OLD does not",
    dn == "RETRY" and fbn and fbn.get("verdict", "").startswith("FAIL C4") and "This is a comment_patch task" in fbn.get("instruction", "") and do == "NORETRY",
    f"new={dn} verdict={(fbn or {}).get('verdict', '')[:90]!r} · old={do}")
dp, _ = runner_decision(NEW_RUNNER, ARM0_DIR); dp_o, _ = runner_decision(OLD_RUNNER, ARM0_DIR)
arm("RUNNER-b ARM0 PASS retries under neither runner", dp == "NORETRY" and dp_o == "NORETRY", f"new={dp} old={dp_o}")
dc, _ = runner_decision(NEW_RUNNER, ARM8A_DIR)
arm("RUNNER-c ARM8a FAIL C1 does not retry (C0/C1 are not sample failures of the C2-C7 kind)", dc == "NORETRY", f"new={dc}")

# ---------------------------------------------------------------- ARM10 builder refusals
brief979 = open(f"{LM}/night/briefs/KS-979.md", encoding="utf-8").read()
def build(label, brief_text, product=P979, env=None, ticket="KS-979"):
    d = os.path.join(W, "b_" + label); os.makedirs(d, exist_ok=True)
    bp = os.path.join(d, "brief.md"); open(bp, "w", encoding="utf-8").write(brief_text)
    outp = os.path.join(d, "input.json")
    rc, o = run(["bash", BUILDER, ticket, outp, bp, f"product={product}"], env=env)
    open(os.path.join(d, "build.out"), "w").write(o)
    code = re.search(r"REFUSED (R\d+)", o)
    return rc, o, (code.group(1) if code else None), os.path.exists(outp)
def refusal(label, text, want, **kw):
    rc, o, code, wrote = build(label, text, **kw)
    arm(f"ARM10 {label} → REFUSED {want}", rc == 2 and code == want and not wrote, f"rc={rc} code={code} :: {(re.search(r'REFUSED.*', o) or [''])[0][:190] if re.search(r'REFUSED.*', o) else o.strip()[-150:]}")
def sub(old, new, text=brief979, count=1):
    assert text.count(old) >= 1, old[:60]
    return text.replace(old, new, count)
refusal("R0-missing", re.sub(r"## Premises \(measured\)", "## Premises", brief979), "R0")
refusal("R0-noinstrument", sub("- P7 KS-979 is Backlog, unassigned, 0 comments, 0 attachments — instrument: Linear GraphQL read", "- P7 KS-979 is Backlog, unassigned, 0 comments, 0 attachments — read from Linear"), "R0")
refusal("R1-sh", brief979, "R1", product="Blockchain/Dev/scripts/run-shell-suites.sh")
refusal("R4-code-line", sub(":171-174", ":171-175"), "R4")
refusal("R5-off-by-one", sub("@@ -169,8 +169,12 @@", "@@ -170,8 +170,12 @@"), "R5")
# R5 not byte-unique: the ks1103 banner rule appears at :202 and :204
P1103 = "Blockchain/Dev/services/originate/src/__tests__/ks1103-verify-hash-field.test.ts"
tl1103 = G.split_lines(tip_text(P1103)); assert tl1103[201] == tl1103[203] and tl1103[201].strip().startswith("// ----")
b_dup = brief979.split("## Lines")[0] + f"## Lines\n- `{P1103}`:202-204\n\n## The exact change\n\n```diff\n--- a/{P1103}\n+++ b/{P1103}\n@@ -201,3 +201,3 @@\n {tl1103[200]}\n-{tl1103[201]}\n+  // ======== arm ========\n {tl1103[202]}\n```\n"
refusal("R5-not-unique", b_dup, "R5", product=P1103)
refusal("R6-nonascii", sub("+  // org-less keys is the migration's stated reason, not a per-key condition.", "+  // org-less keys is the migration's stated reason — not a per-key condition."), "R6")
refusal("R7-code-plus", sub("+  // SUBJECT, not the org-less caller). So the org-less caller is", "+  // SUBJECT, not the org-less caller). So the org-less caller is\n+  const armCode = 1;").replace("@@ -169,8 +169,12 @@", "@@ -169,8 +169,13 @@"), "R7")
# R7 already-at-tip needs an ASCII tip line inside the range: :173 text re-added
refusal("R7-already-at-tip", sub("+  // SUBJECT, not the org-less caller). So the org-less caller is", "+  // SUBJECT, not the org-less caller). So the org-less caller is\n+" + tl979[172]).replace("@@ -169,8 +169,12 @@", "@@ -169,8 +169,13 @@"), "R7")
refusal("R8-directive", sub("+  // SUBJECT, not the org-less caller). So the org-less caller is", "+  // SUBJECT, not the org-less caller). So the org-less caller is\n+  // @ts-expect-error arm").replace("@@ -169,8 +169,12 @@", "@@ -169,8 +169,13 @@"), "R8")
refusal("R8-unterminated", sub("+  // SUBJECT, not the org-less caller). So the org-less caller is", "+  // SUBJECT, not the org-less caller). So the org-less caller is\n+  /* arm: an unterminated block comment").replace("@@ -169,8 +169,12 @@", "@@ -169,8 +169,13 @@"), "R8")
rd = os.path.join(W, "ready"); os.makedirs(rd, exist_ok=True)
open(os.path.join(rd, "READY_KS-0000_arm.diff.md"), "w").write("# arm\n```diff\n--- a/services/originate/src/__tests__/ks597-issuer-org-bind.test.ts\n+++ b/services/originate/src/__tests__/ks597-issuer-org-bind.test.ts\n@@ -179,3 +179,3 @@\n```\n")
refusal("R9-ready-near", brief979, "R9", env={"NIGHT_READY_DIR": rd})
# stubs for R10/R11 (localhost; the builder's http(s) seams)
class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, obj):
        b = json.dumps(obj).encode(); self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        self.rfile.read(int(self.headers.get("Content-Length", 0)))
        st = ("In Progress", "started") if "/inprogress" in self.path else ("Backlog", "backlog")
        self._send({"data": {"issues": {"nodes": [{"identifier": "KS-979", "title": "stub", "archivedAt": None, "state": {"name": st[0], "type": st[1]}, "assignee": None, "attachments": {"nodes": []}}]}}})
    def do_GET(self):
        if "/files" in self.path:
            self._send([{"filename": P979}] if self.path.startswith("/hit/") else [])
        elif "/pulls" in self.path:
            self._send([{"number": 999}] if self.path.startswith("/hit/") else [])
        else:
            self._send({"message": "Not Found"})
srv = socketserver.TCPServer(("127.0.0.1", 0), H); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
refusal("R10-linear-inprogress", brief979, "R10", env={"NIGHT_LINEAR_API": f"http://127.0.0.1:{port}/inprogress"})
refusal("R11-open-pr-on-file", brief979, "R11", env={"NIGHT_LINEAR_API": f"http://127.0.0.1:{port}/backlog", "NIGHT_GITHUB_API": f"http://127.0.0.1:{port}/hit"})
refusal("R11-github-unreachable", brief979, "R11", env={"NIGHT_LINEAR_API": f"http://127.0.0.1:{port}/backlog", "NIGHT_GITHUB_API": "http://127.0.0.1:9"})
rc, o, code, wrote = build("OK-stub-clean", brief979, env={"NIGHT_LINEAR_API": f"http://127.0.0.1:{port}/backlog", "NIGHT_GITHUB_API": f"http://127.0.0.1:{port}/clean"})
arm("ARM10 OK-stub-clean (same brief, clean stubs) → rc 0 (the refusals above are the stub, not the brief)", rc == 0 and wrote, f"rc={rc} {o.strip().splitlines()[-1][:160] if o.strip() else ''}")
rc, o, code, wrote = build("OK-real", brief979)
same = wrote and json.load(open(os.path.join(W, "b_OK-real", "input.json")))["comment"] == inp979["comment"]
arm("ARM10 OK-real KS-979 build (real Linear + GitHub) → rc 0, comment block == night/inputs/comment_979.json", rc == 0 and same, f"rc={rc} same={same} {o.strip().splitlines()[-1][:140] if o.strip() else ''}")
srv.shutdown()

src_dirty1 = run(["git", "-C", SRC, "status", "--porcelain", "--untracked-files=no"])[1]
arm("SOURCE checkout tracked state unchanged across the arms", src_dirty0 == src_dirty1, f"before={len(src_dirty0.splitlines())} after={len(src_dirty1.splitlines())} lines")
n_ok = sum(1 for _, ok in RESULTS if ok)
print(f"SUMMARY {n_ok}/{len(RESULTS)} arms hold · scratch {W}")
sys.exit(0 if n_ok == len(RESULTS) else 1)
PYARMS
