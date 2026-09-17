#!/usr/bin/env python3
"""repin_devpin_1034.py — develop MOVED during the re-pin: 3961c2add -> 34cdcfb26 (#1035 squash: verification.ts 28fb58343 -> f888e8cd0 + the ks1204 test;
0 #1034 files; merged tree e4624218b x 34cdcfb26 = f1c78bbb8, 0 conflicts; out_repin/devmove_34cdcfb26.out, out_repin/repin_merged.out). Re-pins the DEVELOP
pin only (the head, the merge-base 3961c2add and the compare guard are unchanged) in the launcher, brief, prompt and controls, by ASSERTED substitutions.
Snapshot of the 3961c2add-pinned set: *.repin-e4624218b-dev3961c2add (its --check rc 0 at 01:56:23)."""
import re, hashlib, subprocess, datetime
Q = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent'; GS = Q + '/gatesets/2026-09-17_gate1034'
L = Q + '/launchers/launch_qa_secuura_ks1215_1034.sh'; B = Q + '/briefs/2026-09-17_secuura-1034-ks1215-tier1.md'; P = Q + '/briefs/2026-09-17_secuura-1034-ks1215-tier1.prompt.txt'; K = GS + '/check_launcher_1034.sh'
N = '34cdcfb2663b9e4c31025044e6f842ad2c5a10a3'
STAMP = datetime.datetime.now().astimezone().strftime('%H:%M:%S')
def edit(path, pairs):
    s = open(path).read(); assert s == open(path + '.repin-e4624218b-dev3961c2add').read(), path
    for old, new, n in pairs:
        c = s.count(old); assert c == n, (path.split('/')[-1], old[:90], c, n); s = s.replace(old, new)
    return s
# ---- launcher
l = edit(L, [
 ("# behind 0, files 3 (auth.ts, platform.ts, the ks1215 test) (asserted, exit 10; behind NOT asserted). (Drafted at fd81a75f0: 27e53ec3a ahead 2 files 2.)\n",
  "# behind 0, files 3 (auth.ts, platform.ts, the ks1215 test) (asserted, exit 10; behind NOT asserted). (Drafted at fd81a75f0: 27e53ec3a ahead 2 files 2.)\n"
  "# DEVELOP MOVED during the re-pin (02:02:48 ls-remote): 3961c2add -> 34cdcfb26 (#1035 squash: routes/verification.ts 28fb58343 -> f888e8cd0 + the ks1204\n"
  "# test; 0 #1034 files). The DEVELOP pin (not the merge-base, not the compare) was re-pinned to 34cdcfb26 with verification.ts f888e8cd0 JUDGED; merged tree\n"
  "# e4624218b x 34cdcfb26 = f1c78bbb8 (0 conflicts) != the head tree. Compare develop...head still reads merge_base 3961c2add ahead 4 files 3 (behind 1).\n", 1),
 ("DEVELOP_SHA='3961c2add8e1637b32e638f8f0952c328c00833e'   # the pin = the merge-base = develop at the re-pin (moves judged by PATH BLOB and GUARDED paths, never by this SHA: git ls-remote 01:38:08 + 01:40:22; compare API 01:38:38 AEST 2026-09-18)",
  "DEVELOP_SHA='" + N + "'   # the pin = develop after #1035 landed mid-re-pin (NOT the merge-base 3961c2add; moves judged by PATH BLOB and GUARDED paths: git ls-remote 02:02:48 AEST 2026-09-18)", 1),
 ('  A + "src/routes/verification.ts":                                      ({"28fb5834308a502f5f7b806e3b49a77627601eff": DV}, {}),',
  '  A + "src/routes/verification.ts":                                      ({"f888e8cd0": DV}, {}),', 1),
 ('    print("OK " + state + " | origin develop still " + pinned + " (= the head merge-base, an ANCESTOR of the head: merged tree = the head tree 6f912843b54cdcbcc7e6398d6766398f0e0c5ca9; git ls-remote)"); sys.exit(0)',
  '    print("OK " + state + " | origin develop still " + pinned + " (#1035 squash on the head merge-base 3961c2add, NOT an ancestor of the head: merged tree e4624218b x 34cdcfb26 = f1c78bbb888f5c0f875a7ab11ee09d810126f72a, 0 conflicts, re-pinner; git ls-remote)"); sys.exit(0)', 1),
 ('names the merged-tree OID, re-pinner 3961c2add -> 6f912843b = the head tree (brief items 1, 3, 5, 6)"',
  'names the merged-tree OID, re-pinner 34cdcfb26 -> f1c78bbb8 (brief items 1, 3, 5, 6)"', 1),
])
# the verification.ts blob must be the FULL sha the contents API returns
full = subprocess.run(['git', '-C', '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files', 'rev-parse', N + ':Blockchain/Dev/services/api-gateway/src/routes/verification.ts'], capture_output=True, text=True).stdout.strip()
assert full.startswith('f888e8cd0') and len(full) == 40, full
assert l.count('{"f888e8cd0": DV}') == 1; l = l.replace('{"f888e8cd0": DV}', '{"' + full + '": DV}')
print('launcher sha256', hashlib.sha256(l.encode()).hexdigest()[:16], '| verification.ts pinned', full)
# ---- brief
b = edit(B, [
 ("**RE-PINNED 2026-09-18 01:38–02:xx AEST to `e4624218b`**", "**RE-PINNED 2026-09-18 01:38–" + STAMP + " AEST to `e4624218b`** (develop re-pinned to `34cdcfb26` when #1035 landed mid-re-pin)", 1),
 ("**Merged tree over the current develop = `merge-tree e4624218b × 3961c2add` = `6f912843b` = the head tree** (develop is an ancestor): merged = head.",
  "**Merged tree over `3961c2add` = `6f912843b` = the head tree** (develop was an ancestor) — **SUPERSEDED at 02:02:48, see the next bullet.**", 1),
 ("- **Checks (re-pinner, MEASURED 01:40:56",
  "- **DEVELOP MOVED DURING THE RE-PIN (ls-remote 02:02:48): `3961c2add` → `34cdcfb2663b9e4c31025044e6f842ad2c5a10a3`** = the #1035 squash (KS-1204): `routes/verification.ts` `28fb58343` → `f888e8cd0` and the ks1204 test ABSENT → `f1f9840ed`; **0 #1034 files** (`out_repin/devmove_34cdcfb26.out`). `merge-tree e4624218b × 34cdcfb26` (clone) = **`f1c78bbb888f5c0f875a7ab11ee09d810126f72a`, 0 conflicts**; merged vs head differs in exactly those 2 files, every blob = develop's; `auth.ts` / `platform.ts` / ks1215 test in merged = head. **Merged ≠ head now: api-gateway `src` subtree head `1b2f0fd79`, merged `533185eaf`.** Re-pinner MEASURED on it (`out_repin/repin_merged.out`, 02:03:43–02:04:18, vitest 4.1.11, load 12–14): develop `34cdcfb26` **58 / 565** default and 60 s (ks1204 9 / 9); **merged `f1c78bbb8` 59 / 585** both ways, 0 failed, ks1215 20 / 20 + ks1204 9 / 9; project tsc rc 0 both. The launcher's DEVELOP pin is now `34cdcfb26` (verification.ts `f888e8cd0` JUDGED); the merge-base and the compare guard (`3961c2add` ahead 4 files 3) are unchanged (behind is now 1, not asserted). **The census, tampers and HANG on the merged tree were NOT run by the re-pinner:** #1035 changes the connector document-create path (`verification.ts`), which the census drives (`POST /api/documents`) — item 1 and L0 on the merged tree are the gate's.\n"
  "- **Checks (re-pinner, MEASURED 01:40:56", 1),
 ("develop / merge-base **`3961c2add`**, compare **ahead 4 files 3**, suites **57 / 556 → 58 / 576**, ks1215 **20** cells, merged tree **= head**,",
  "merge-base **`3961c2add`**, develop **`34cdcfb26`**, compare **ahead 4 files 3**, suites **57 / 556 (3961c2add) · 58 / 565 (34cdcfb26) → 58 / 576 (head) → 59 / 585 (merged)**, ks1215 **20** cells, merged tree **`f1c78bbb8`**,", 1),
 ("on **develop `3961c2add`** and **head `e4624218b`**; merged = head (tree-equal).",
  "on **develop `34cdcfb26`** (or `3961c2add`), **head `e4624218b`** and **merged `f1c78bbb8`** (#1035's verification.ts is on the census's `POST /api/documents` path: the merged tree is not head-equal).", 1),
 ("squash e4624218b onto develop <then-current; 3961c2add = the merge-base at the re-pin> (merged tree <OID>; re-pinner 6f912843b = the head tree over 3961c2add);",
  "squash e4624218b onto develop <then-current; 34cdcfb26 at the re-pin close, merge-base 3961c2add> (merged tree <OID>; re-pinner f1c78bbb8 over 34cdcfb26);", 1),
 ("api-gateway 57/556 at 3961c2add -> 58/576 at head", "api-gateway 58/565 at 34cdcfb26 -> 58/576 at head", 1),
])
assert "WEDNESDAY'S signed GO" in b and not re.search(r"waits for Kam.s tap|on Kam.s tap only", b) and '02:xx' not in b
print('brief bytes', len(b.encode()), 'sha256', hashlib.sha256(b.encode()).hexdigest()[:16])
# ---- prompt
p = edit(P, [
 ("""  auth.ts 6e1668362 -> bf09d315a; platform.ts 4550401f8 -> b80a8cd8d; ks1215 test absent -> 75006b5cf. Merged tree over 3961c2add = the head tree
  6f912843b (develop is an ancestor), and develop's api-gateway + shared subtrees equal 27e53ec3a's. If develop moves, merge it onto e4624218b in YOUR
  clone, name the OID, judge the move by content, and re-run items 1, 3 and 6 on the merged tree if it touches services/api-gateway/ or packages/shared/src/.""",
  """  auth.ts 6e1668362 -> bf09d315a; platform.ts 4550401f8 -> b80a8cd8d; ks1215 test absent -> 75006b5cf. develop then MOVED (02:02:48) to 34cdcfb26
  (#1035: verification.ts f888e8cd0 + ks1204 test; 0 #1034 files): re-pinner merged tree e4624218b x 34cdcfb26 = f1c78bbb8, 0 conflicts, NOT head-equal,
  59/585. Merge the then-current develop onto e4624218b in YOUR clone, name the OID, and run L0 and items 1, 3 and 6 on the merged tree too.""", 1),
 ("(develop 3961c2add, head e4624218b; merged = head).", "(develop 34cdcfb26, head e4624218b, merged f1c78bbb8).", 1),
 ("Merged tree over the CURRENT develop (re-pinner: = head tree 6f912843b).", "Merged tree over the CURRENT develop (re-pinner: f1c78bbb8 over 34cdcfb26).", 1),
 ("as the delta over develop 3961c2add, AND on the", "as the delta over develop 3961c2add, AND on the", 1),
 ("""squash e4624218b onto develop <then-current; 3961c2add at
re-pin> (merged tree <OID>; re-pinner 6f912843b = head tree);""", """squash e4624218b onto develop <then-current; 34cdcfb26 at
re-pin close> (merged tree <OID>; re-pinner f1c78bbb8);""", 1),
 ("api-gateway 57/556 at develop -> 58/576 at head", "api-gateway 58/565 at 34cdcfb26 -> 58/576 at head", 1),
 ("""attachmentsForURL(pull/1034) = KS-1215 contributes only (controls pull/1028 -> KS-744;
   pull/99999 -> 0); 0 closing phrases in title, body and both commit messages (planted controls);""", """attachmentsForURL(pull/1034) = KS-1215 contributes only (controls
   pull/1028, pull/99999); 0 closing phrases in title, body and all 4 commit messages (planted controls);""", 1),
 ("""- zsh: no PIPESTATUS (`cmd > out 2>&1; rc=$?`), no timeout on macOS, `set -- $var` does not word-split, `"$VAR:path"` applies history modifiers
  (write `"${VAR}:path"`), never begin a line with `=====`.""", """- zsh: no PIPESTATUS, no timeout, `set -- $var` does not word-split, write `"${VAR}:path"`, never begin a line with `=====`.""", 1),
])
assert "WEDNESDAY'S signed GO naming the head" in p and not re.search(r"waits for Kam.s tap|on Kam.s tap only", p) and '\x00' not in p
n = len(p.encode()); print('prompt bytes', n, 'sha256', hashlib.sha256(p.encode()).hexdigest()[:16]); assert n <= 19800
# ---- controls
k = edit(K, [
 ("ctl 0  QA1034_CUR_DEV=3961c2add8e1637b32e638f8f0952c328c00833e\nctl 0  QA1034_CUR_DEV=4306726977b55171a7c8c0eb5e42de078587a725\n",
  "ctl 0  QA1034_CUR_DEV=34cdcfb2663b9e4c31025044e6f842ad2c5a10a3\nctl 18 QA1034_CUR_DEV=3961c2add8e1637b32e638f8f0952c328c00833e\nctl 18 QA1034_CUR_DEV=4306726977b55171a7c8c0eb5e42de078587a725\n", 1),
])
open(L, 'w').write(l); open(B, 'w').write(b); open(P, 'w').write(p); open(K, 'w').write(k)
print('ALL FOUR WRITTEN (after every assert) | launcher bash -n rc', subprocess.run(['bash', '-n', L]).returncode, '| controls re-aimed; stamp', STAMP)
