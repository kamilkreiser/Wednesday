#!/usr/bin/env python3
"""merged_sim.py — the DRAFTER's derivation (successor drafter, after develop moved to M20 = #903's SQUASH a53343502) of
every prediction the brief makes about the MERGED shapes onto live develop:
  M21   = #918 b54487216 merge-tree'd onto M20 (CLEAN, tree f089eaffe) committed as a scratch commit caf4aad15 (parent M20)
  END   = #925 5341b1dae onto M21 (CONFLICTS in preflight.sh — 3 blocks, ours 2 lines / theirs 78) resolved by taking
          #925's side -> the file is byte-identical to #925's head blob 28d3636c1 -> tree 364e44ca1 (= the alt-order end tree)
  924M  = #924 b85f1db24 onto M20 (CLEAN, tree 4641202fd; the one file = the head's blob 518bffeea)
Detached worktrees on scratch commits in the drafter's OWN shared clone (model/clone); nothing touches the Secuura checkout.
Predictions are written BELOW, before any run; every cell is scored EXACT / MISPREDICTED. HOLD-safe: no docker, no stack,
no push, no real 15-leg preflight (the verdict shape is re-derived in the suite's own fixture via probe_verdict.sh).
Usage: merged_sim.py <OUTPUT DIR>      Exit 0 = every prediction held · 1 = a misprediction or a precondition failed.
"""
import os, re, subprocess, sys, hashlib, datetime, time
G = sys.argv[1]
M = f"{G}/model"; CLONE = f"{M}/clone"; SIM = f"{G}/sim"; TMP = f"{SIM}/tmp"; os.makedirs(TMP, exist_ok=True)
M20 = 'a5334350221c819f54d4a20a3308daeb9ca09617'
T_M21 = 'f089eaffee03a552c78a55fd0472a38d9210a1d3'      # merge-tree M20 x b54487216 (mt_918_M20.out)
C_M21 = 'caf4aad1509fd08df9b9639f8b2c817da2e3cb1a'      # scratch commit of T_M21, parent M20 (mt_M21_read.out)
T_END = '364e44ca1923755e329c3a8407e011bd495d6dfc'      # #925 theirs-resolved onto M21 == alt order (mt_endstate_read.out)
T_924M = '4641202fd9163c246653456476b2ee8228004925'     # merge-tree M20 x b85f1db24 (mt_M20_read.out)
BASE_ENV = {k: v for k, v in os.environ.items() if k not in ('GH_TOKEN', 'LINEAR_API_KEY', 'AGENTMAIL_API_KEY', 'PREFLIGHT_STRICT_LEGS', 'GATEWAY_URL', 'HOOK_SH', 'CODE_GUARDS_SH', 'PREFLIGHT_DEPS_TEST_ROOT')}
BASE_ENV['TMPDIR'] = TMP; BASE_ENV['GIT_CONFIG_GLOBAL'] = '/dev/null'; BASE_ENV['GIT_CONFIG_SYSTEM'] = '/dev/null'
fails = 0
def ck(cond, msg):
    global fails
    print(("ok   " if cond else "FAIL ") + msg); fails += 0 if cond else 1
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
DET = dict(os.environ, GIT_AUTHOR_NAME='drafter', GIT_AUTHOR_EMAIL='drafter@none', GIT_COMMITTER_NAME='drafter', GIT_COMMITTER_EMAIL='drafter@none', GIT_AUTHOR_DATE='2026-09-14T10:40:00+1000', GIT_COMMITTER_DATE='2026-09-14T10:40:00+1000')
def git(*a): return subprocess.run(['git', '-C', CLONE, *a], capture_output=True, text=True, env=DET)   # deterministic scratch commits (re-runnable)
def run(cmd, cwd, env=None, timeout=900):
    e = dict(BASE_ENV); e.update(env or {}); t0 = time.time()
    r = subprocess.run(cmd, cwd=cwd, env=e, capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)
    return r.returncode, r.stdout + r.stderr, round(time.time() - t0, 1)
def keep(name, out): open(f"{SIM}/run.{name}.out", 'w', encoding='utf-8').write(out)
def porcelain(wt): return subprocess.run(['git', '-C', wt, 'status', '--porcelain'], capture_output=True, text=True).stdout.count('\n')
def tally(out):
    m = re.search(r'(\d+) passed, (\d+) failed', out); return (int(m.group(1)), int(m.group(2))) if m else (-1, -1)
print("merged_sim at", datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
print("bash:", subprocess.run(['/bin/bash', '--version'], capture_output=True, text=True).stdout.splitlines()[0], "| node:", subprocess.run(['node', '--version'], capture_output=True, text=True).stdout.strip())

# ---- 0. the trees are what the merge-tree reads said; scratch commits for END and 924M; three worktrees --------------------
ck(git('rev-parse', C_M21 + '^{tree}').stdout.strip() == T_M21, f"scratch M21 {C_M21[:9]} has tree {T_M21[:9]}")
ck(git('rev-parse', C_M21 + '^').stdout.strip() == M20, f"scratch M21's parent is M20 {M20[:9]}")
C_END = git('commit-tree', T_END, '-p', C_M21, '-m', 'SCRATCH END: #925 theirs-resolved onto M21 (drafter simulation)').stdout.strip()
C_924M = git('commit-tree', T_924M, '-p', M20, '-m', 'SCRATCH 924M: #924 onto M20 (drafter simulation)').stdout.strip()
ck(len(C_END) == 40 and len(C_924M) == 40, f"scratch commits END {C_END[:9]} (parent M21) and 924M {C_924M[:9]} (parent M20)")
WT = {}
for name, c in [('wtM21', C_M21), ('wtEND', C_END), ('wt924M20', C_924M)]:
    p = f"{M}/{name}"; WT[name] = p
    if not os.path.isdir(p):
        r = subprocess.run(['git', '-C', CLONE, 'worktree', 'add', '--detach', p, c], capture_output=True, text=True)
        ck(r.returncode == 0, f"worktree {name} @ {c[:9]} rc={r.returncode} {r.stderr.strip()[:80]}")
    h = subprocess.run(['git', '-C', p, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    ck(h == c and porcelain(p) == 0, f"{name} HEAD {h[:9]} porcelain {porcelain(p)}")
RCG = 'Blockchain/Dev/scripts/run-code-guards.sh'; RCT = 'Blockchain/Dev/scripts/__tests__/run_code_guards.test.sh'
PF = 'Blockchain/Dev/scripts/preflight/preflight.sh'; PFD = 'Blockchain/Dev/scripts/__tests__/preflight_deps.test.sh'
LC = 'Blockchain/Dev/scripts/preflight/lockfile-cleanroom.sh'; RSS = 'Blockchain/Dev/scripts/run-shell-suites.sh'
HOOK = '.githooks/pre-push'; PPT = 'Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh'
# the bytes: M21 carries #918's four files at #918's blobs EXCEPT preflight.sh (= #918's + #903's env_fail +24); END carries #925's six
PINS = {f"{WT['wtM21']}/{RCG}": 'b0a951a444455d83', f"{WT['wtM21']}/{RCT}": '4b9b66c62359e03a', f"{WT['wtM21']}/{PFD}": 'ec344d954dc89a0c',
        f"{WT['wtEND']}/{PF}": 'a65577f0176b5394', f"{WT['wtEND']}/{PFD}": 'f4c0ece2c398d41e', f"{WT['wtEND']}/{RCG}": 'b0a951a444455d83',
        f"{WT['wtEND']}/{HOOK}": '92abd8e9b30e8d19', f"{WT['wtEND']}/{PPT}": '6dabbb516e92e5cf', f"{WT['wt924M20']}/{LC}": '4f0522fe0c72ab4b'}
for p, want in PINS.items():
    ck(sha(p) == want, f"{p.replace(M + '/', '')} sha256 {sha(p)} (pinned {want})")
m21pf = f"{WT['wtM21']}/{PF}"
ck(sha(m21pf) == sha(f"{M}/preflight.sh.918-onto-M20"), f"wtM21 preflight.sh sha256 {sha(m21pf)} = model/preflight.sh.918-onto-M20 (NOT #918's 6e128baf: +24 env_fail from M20)")
for p in [m21pf, f"{WT['wtEND']}/{PF}", f"{WT['wtEND']}/{PFD}", f"{WT['wt924M20']}/{LC}"]:
    rc, out, _ = run(['/bin/bash', '-n', p], G); ck(rc == 0, f"/bin/bash -n {p.replace(M + '/', '')} rc={rc}")
# static shape of M21's preflight.sh: 15 /15 headers, env_fail x3, the plain PASSED echo once, 0 '/13 |/14 ' (control develop's 14)
txt = open(m21pf, encoding='utf-8').read()
nh = len(re.findall(r'^step "\d+/15', txt, re.M)); ck(nh == 15, f"M21 preflight.sh step headers /15: {nh} (predicted 15)")
ck(txt.count('env_fail') == 3, f"M21 preflight.sh 'env_fail' x{txt.count('env_fail')} (predicted 3 — #903's arm rode in from M20)")
npe = len(re.findall(r'^echo "PREFLIGHT PASSED\."', txt, re.M)); ck(npe == 1, f"M21 preflight.sh plain PASSED echo x{npe} (predicted 1 — #918 keeps develop's plain verdict)")
ck(len(re.findall(r'/13 |/14 ', txt)) == 0, f"M21 preflight.sh '/13 |/14 ' x{len(re.findall(r'/13 |/14 ', txt))} (predicted 0)")
dev = open(f"{M}/preflight.sh.8861e6216", encoding='utf-8').read(); ck(len(re.findall(r'/13 |/14 ', dev)) == 14, f"control: develop M18's preflight.sh '/13 |/14 ' x{len(re.findall(r'/13 |/14 ', dev))} (14)")
endpf = open(f"{WT['wtEND']}/{PF}", encoding='utf-8').read()
ck(len(re.findall(r'^<<<<<<<|^=======|^>>>>>>>', endpf, re.M)) == 0, "END preflight.sh conflict markers 0")
ck(len(re.findall(r'^<<<<<<<|^=======|^>>>>>>>', open(f"{M}/preflight.sh.CONFLICT-925-onto-M21", encoding='utf-8').read(), re.M)) == 9, "control: the CONFLICT copy carries 9 marker lines (3 blocks)")
# tracked counts
def count(tree, pat): return len([l for l in git('ls-tree', '-r', '--name-only', tree).stdout.splitlines() if re.search(pat, l)])
TS = r'\.test\.sh$'; CK = r'Blockchain/Dev/scripts/check-[^/]*\.sh$'
ck(count(T_M21, TS) == 30 and count(T_M21, CK) == 21, f"M21 tracked *.test.sh {count(T_M21, TS)} (30) / check-*.sh {count(T_M21, CK)} (21)")
ck(count(T_END, TS) == 30 and count(T_END, CK) == 21, f"END tracked *.test.sh {count(T_END, TS)} (30) / check-*.sh {count(T_END, CK)} (21)")
ck(count(M20, TS) == 29 and count(T_924M, TS) == 29, f"control: M20 *.test.sh {count(M20, TS)} (29); 924M {count(T_924M, TS)} (29)")

# ---- 1. M21 (#918 on M20): the five lines ---------------------------------------------------------------------------------
print("\n== PREDICTIONS (M21 = #918 on M20): --list 13/4/4 · census rc 0 'OK — all 21 tracked guards accounted for (21 buckets entries).' · run rc 0 'OK — 13 code guards passed.' 0 FAILED · run_code_guards.test.sh 15/0 · preflight_deps 55/0")
dev21 = f"{WT['wtM21']}/Blockchain/Dev"
rc, out, dt = run(['/bin/bash', 'scripts/run-code-guards.sh', '--list'], dev21); keep('M21.list', out)
ck(rc == 0 and 'WIRED HERE (13):' in out and 'HOMED ELSEWHERE (4):' in out and 'DEFERRED, with reason (4):' in out, f"M21 --list rc={rc} 13/4/4 ({dt}s)")
rc, out, dt = run(['/bin/bash', 'scripts/run-code-guards.sh', '--check-unreached'], dev21); keep('M21.census', out)
ck(rc == 0 and 'OK — all 21 tracked guards accounted for (21 buckets entries).' in out, f"M21 --check-unreached rc={rc}: {out.strip().splitlines()[-1][:90]} ({dt}s)")
rc, out, dt = run(['/bin/bash', 'scripts/run-code-guards.sh'], dev21); keep('M21.run', out)
ck(rc == 0 and 'OK — 13 code guards passed.' in out and '^ FAILED' not in out, f"M21 run rc={rc}: {out.strip().splitlines()[-1][:90]} FAILED lines {out.count('^ FAILED')} ({dt}s)")
rc, out, dt = run(['/bin/bash', 'scripts/__tests__/run_code_guards.test.sh'], dev21); keep('M21.suite', out)
ck(rc == 0 and tally(out) == (15, 0), f"M21 run_code_guards.test.sh rc={rc} tally {tally(out)} (15, 0) ({dt}s)")
rc, out, dt = run(['/bin/bash', 'scripts/__tests__/preflight_deps.test.sh'], dev21); keep('M21.pfd', out)
ck(rc == 0 and tally(out) == (55, 0), f"M21 preflight_deps.test.sh rc={rc} tally {tally(out)} (55, 0) ({dt}s)")
# the verdict shape of M21's preflight.sh (the #918-on-M20 file) in the suite's own fixture: plain PASSED (no ratio), 3 stack SKIPs, rc 0
rc, out, dt = run(['/bin/bash', f"{G}/probe_verdict.sh", m21pf, f"{WT['wtM21']}/{RSS}", '0', 'M21'], G); keep('M21.verdict', out)
def probe(out): m = re.search(r'rc=(\d+)\s+step banners=(\d+)\s+SKIP-stack lines=(\d+)', out); return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else (-1, -1, -1)
ck(probe(out) == (0, 16, 3) and '| PREFLIGHT PASSED.' in out and 'legs ran' not in out, f"M21 verdict in the fixture: plain 'PREFLIGHT PASSED.' (no ratio), nested rc/banners/stack-SKIPs {probe(out)} (0, 16, 3) ({dt}s)")

# ---- 2. END (#925 resolved onto M21): the fixture suite plain + STRICT, the census, the verdict shape ------------------------
print("\n== PREDICTIONS (END = #925 theirs-resolved onto M21): preflight_deps 56/0 plain AND under PREFLIGHT_STRICT_LEGS=1 · census OK all 21 · run_code_guards 15/0 · pre_push_hook_base 28/0 · verdict 'PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.' rc 0 / STRICT rc 1 with the refusal line")
devE = f"{WT['wtEND']}/Blockchain/Dev"
rc, out, dt = run(['/bin/bash', 'scripts/__tests__/preflight_deps.test.sh'], devE); keep('END.pfd', out)
ck(rc == 0 and tally(out) == (56, 0) and re.search(r'^ok\s+F-925-3', out, re.M), f"END preflight_deps.test.sh plain rc={rc} tally {tally(out)} (56, 0), F-925-3 cell ok ({dt}s)")
rc, out, dt = run(['/bin/bash', 'scripts/__tests__/preflight_deps.test.sh'], devE, env={'PREFLIGHT_STRICT_LEGS': '1'}); keep('END.pfd.strict', out)
ck(rc == 0 and tally(out) == (56, 0), f"END preflight_deps.test.sh under STRICT rc={rc} tally {tally(out)} (56, 0) ({dt}s)")
rc, out, dt = run(['/bin/bash', 'scripts/run-code-guards.sh', '--check-unreached'], devE); keep('END.census', out)
ck(rc == 0 and 'OK — all 21 tracked guards accounted for (21 buckets entries).' in out, f"END --check-unreached rc={rc}: {out.strip().splitlines()[-1][:90]}")
rc, out, dt = run(['/bin/bash', 'scripts/__tests__/run_code_guards.test.sh'], devE); keep('END.suite', out)
ck(rc == 0 and tally(out) == (15, 0), f"END run_code_guards.test.sh rc={rc} tally {tally(out)} (15, 0) ({dt}s)")
rc, out, dt = run(['/bin/bash', 'scripts/__tests__/pre_push_hook_base.test.sh'], devE); keep('END.pphb', out)
ck(rc == 0 and tally(out) == (28, 0), f"END pre_push_hook_base.test.sh rc={rc} tally {tally(out)} (28, 0 — #903's suite on M20's hook) ({dt}s)")
rc, out, dt = run(['/bin/bash', f"{G}/probe_verdict.sh", f"{WT['wtEND']}/{PF}", f"{WT['wtEND']}/{RSS}", '0', 'END'], G); keep('END.verdict', out)
ck(probe(out) == (0, 16, 3) and 'PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.' in out, f"END verdict plain: INCOMPLETE 12/15, nested rc/banners/stack-SKIPs {probe(out)} (0, 16, 3) ({dt}s)")
rc, out, dt = run(['/bin/bash', f"{G}/probe_verdict.sh", f"{WT['wtEND']}/{PF}", f"{WT['wtEND']}/{RSS}", '1', 'END-strict'], G); keep('END.verdict.strict', out)
ck(probe(out)[0] == 1 and 'PREFLIGHT_STRICT_LEGS=1 — refusing to pass on legs that did not run.' in out, f"END verdict STRICT: refusal line, nested rc={probe(out)[0]} (1) ({dt}s)")

# ---- 3. 924M (#924 on M20): the corpus ---------------------------------------------------------------------------------------
print("\n== PREDICTIONS (924M = #924 on M20): lockfile-cleanroom rc 0 'All 35 standalone lock(s) pass clean-room npm ci.' incl. 'OK    services/mcp-server', 0 FAIL, 0 SKIP; find = 35")
dev924 = f"{WT['wt924M20']}/Blockchain/Dev"
n = int(run(['/bin/bash', '-c', 'find services packages frontend scripts -maxdepth 2 -name package-lock.json | wc -l'], dev924)[1].strip())
ck(n == 35, f"924M standalone locks by find: {n} (35)")
rc, out, dt = run(['/bin/bash', 'scripts/preflight/lockfile-cleanroom.sh'], dev924); keep('924M.corpus', out)
ck(rc == 0 and 'All 35 standalone lock(s) pass clean-room npm ci.' in out and 'OK    services/mcp-server' in out and len(re.findall(r'^FAIL ', out, re.M)) == 0 and len(re.findall(r'^SKIP', out, re.M)) == 0, f"924M corpus rc={rc}: All 35, mcp-server OK, FAIL {len(re.findall(r'^FAIL ', out, re.M))}, SKIP {len(re.findall(r'^SKIP', out, re.M))} ({dt}s)")

# ---- 4. after: worktrees porcelain 0, pinned shas unchanged --------------------------------------------------------------------
for name, p in WT.items(): ck(porcelain(p) == 0, f"after: {name} porcelain {porcelain(p)}")
for p, want in PINS.items(): ck(sha(p) == want, f"after: {p.replace(M + '/', '')} sha256 unchanged")
print(f"\nmerged_sim: FAILS={fails}\ndone at", datetime.datetime.now().astimezone().strftime('%H:%M:%S %Z'))
sys.exit(1 if fails else 0)
