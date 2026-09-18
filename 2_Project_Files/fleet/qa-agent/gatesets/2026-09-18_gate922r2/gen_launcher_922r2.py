#!/usr/bin/env python3
"""gen_launcher_922r2.py — derive launchers/launch_qa_secuura_922r2.sh from launchers/launch_qa_secuura_922.sh (the #922 round-1 launcher; that gate
returned GO WITH FINDINGS) by ASSERTED substitutions: every anchor must occur exactly as often as stated, or the generator refuses and writes nothing.

#922 ROUND 2 DELTA: 8664826e5 -> 30c773ee8, which the generator PROVES is a fast-forward of exactly one commit touching exactly three files. Pins are
RE-READ from the repo; the merged tree over the CURRENT develop 207716440 (#1037 landed since round 1) is RE-DERIVED read-only in a throwaway bare repo
whose objects/info/alternates points at the checkout (left in place; this drafter never deletes).

DIFFERENCES FROM THE ROUND-1 LAUNCHER, stated rather than implied:
 (a) SOURCE = the seat's READY mail, captured verbatim by message id from wednesday-agent@ (gatesets/2026-09-18_gate922r2/mail_922r2_ready.md).
 (b) MERGE AUTHORITY (exit 26, REWRITTEN): #922 does NOT merge on WEDNESDAY'S signed GO alone — Peter's 09-09 "not approving yet" is open and Kam rules
     on merging over it. The prompt must say so, name Kam and Peter, and must NOT carry round 1's "on WEDNESDAY'S signed GO naming the head ... and on
     nothing else" sentence. The Kam's-tap negative is dropped deliberately: naming Kam is now REQUIRED, not forbidden.
 (c) exit 15 now asserts ROUND 2 and the DELTA range; exit 27 asserts the seat's own words in the mail AND the prompt: '12/15 legs ran, 3 SKIPPED',
     'key_ is REFUSED', and "Peter's review is still open".
 (d) LANDED gains the round-1 blobs of the three changed files as well as the round-2 blobs: develop reading EITHER means #922 landed (exit 19).
 (e) env prefix QA922_ -> QA922R2_ so a round-1 override can never steer this launcher.
Usage: gen_launcher_922r2.py <template launcher> <output launcher>   Exit: 0 written · 1 anchor/control/pin disagreed · 2 residual token · 3 bash -n failed"""
import hashlib, os, re, shutil, subprocess, sys, tempfile
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_922r2', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))

REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
OLD = '8664826e53cc47d4dd69c784926c9c14af444cec'   # round-1 head
H   = '30c773ee8f869a7530a9c17521ba442d641aa757'   # round-2 head
MB  = 'f6669623ccae5ab445be6e0e73fb4f19ae2c89d1'   # merge-base with develop (unchanged)
DEV = '207716440e2a6282b90ed2a118614d9cf98bee1e'   # CURRENT develop (#1037), re-read 13:00:24 AEST
HT  = '7aa549d70e73df7d9660b4036498d5f191934806'   # head tree
MERGED = 'a1b4b6536d1d60fb2defca2886d36c9b9d0ec80e'  # merge-tree H x DEV, re-derived below
D = 'Blockchain/Dev/'
def git(*a): return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True)
rp = lambda x: git('rev-parse', '--verify', '-q', x).stdout.strip()
lines_of = lambda *a: git(*a).stdout.splitlines()   # NEWLINE split: two repo paths contain spaces

PIN = {  # develop 207716440 blobs; identical to round 1's develop pins (#1037 touched none of these paths) — re-read, not assumed
 'docs/openapi/secuura-api.yaml':                                  '122d3a2f84cf77bf2b7e2dc51489a0d5f823db1f',
 'packages/shared/src/__tests__/ks256-spec-example-contract.test.ts': 'adbe91dfb0f10752057cceec647b727edb186621',
 'packages/shared/src/openapi/examples/fixtures.ts':               'ca5d5eae163f492c6703e0017610ea7ece7b9583',
 'scripts/spec-examples/check/contract.mjs':                       '43a9c5dea27fc67bf0efc96489a1889833e2cbfd',
 'services/anchoring/src/anchoring.openapi.ts':                    '49b8b38da7764e071711ded751fa006ae21e808d',
 'scripts/spec-examples/check-spec-examples.mjs':                  'e9c14a4dedf103850dc1c93fb1c5c67b8489b2a3',
 'scripts/spec-examples/check/rules-example.mjs':                  '5d1e7ecaef021de85a12121af94871d86547dfcf',
 'scripts/spec-examples/check/rules-global.mjs':                   'f1b447b6d913b8700a47a2a1fff86e5fa18195e1',
 'scripts/spec-examples/check/allowlist.mjs':                      'a712f3c61d7ce570c709002ca0e217c8078af8c3',
 'scripts/spec-examples/check/collect.mjs':                        'a2da5a4dab146a70818a244033a4032fbd6ec3a6',
 'scripts/spec-examples/spec-example-allowlist.json':              '32bacbc4aa2c8764cc387c4d86919c2f1b08c223',
 'scripts/generate-openapi.ts':                                    'e84acdc9e1be073751fcd6a8bb95504e23688019',
 'packages/shared/package.json':                                   '3957692311221fbe87c4ab19447de8cec44aa19a',
 'packages/shared/vitest.config.ts':                               '2a226c0068faa65538cda8d43d03bb9bee2944f1',
 'packages/shared/tsconfig.json':                                  '1fd016cc28803cc8f36cc84db4628941a2af9c50',
 'services/anchoring/src/index.ts':                                'da4abd43292186da45c1533017fe042fa512bd43',
 'package.json':                                                   '773443a9faa0a2eb7caf01c313b880fbe3251922',
 'eslint.config.mjs':                                              '8c5374c6022eb0a3f449f41a570db61294aa63f1',
}
R1 = {  # round-1 head blobs of the five PR files
 'docs/openapi/secuura-api.yaml':                                  '16ac8aa78463849864fa6285e20c9946c027fb7b',
 'packages/shared/src/__tests__/ks256-spec-example-contract.test.ts': '72533d3b01a4941578b1f777f0def3f9ec9ea6f0',
 'packages/shared/src/openapi/examples/fixtures.ts':               'b54d26929c564d9cd4e2e2f27da12df6d6d85325',
 'scripts/spec-examples/check/contract.mjs':                       'db726db299f738e2bf6790b3612d917b4d1eb9fc',
 'services/anchoring/src/anchoring.openapi.ts':                    '29c089bb0abcd65d42fe8fca2d6beaff0368fa98',
}
R2 = {  # round-2 head blobs of the THREE files the delta changes
 'packages/shared/src/__tests__/ks256-spec-example-contract.test.ts': '4ef040f6f2fbbe6d73a76ff860caf71ac0bbe619',
 'packages/shared/src/openapi/examples/fixtures.ts':               '4416d7a586b1398793e1c15374d9cf45c318d832',
 'scripts/spec-examples/check/contract.mjs':                       '07d4e9ab6b2879e08acfd587c4575bfaac1d1071',
}
bad = []
for p, b in PIN.items():
    at_dev, at_h, at_o = rp(DEV + ':' + D + p), rp(H + ':' + D + p), rp(OLD + ':' + D + p)
    if at_dev != b: bad.append(('develop blob', p, b, at_dev))
    if p in R1 and at_o != R1[p]: bad.append(('round-1 head blob', p, R1[p], at_o))
    want_h = R2.get(p) or R1.get(p) or b
    if at_h != want_h: bad.append(('round-2 head blob', p, want_h, at_h))
# the delta: a fast-forward, one commit, three files
ff = git('merge-base', '--is-ancestor', OLD, H).returncode == 0
commits = lines_of('rev-list', OLD + '..' + H)
dfiles = sorted(lines_of('diff', '--name-only', OLD, H))
print('fast-forward %s..%s: %s | commits %d | parent %s | delta files %d' % (OLD[:9], H[:9], ff, len(commits), rp(H + '^1')[:9], len(dfiles)))
if not ff or len(commits) != 1 or rp(H + '^1') != OLD: bad.append(('not a one-commit fast-forward', ff, len(commits)))
if dfiles != sorted(D + p for p in R2): bad.append(('delta file list', dfiles))
if rp(H + '^{tree}') != HT: bad.append(('head tree', rp(H + '^{tree}'), HT))
mb = git('merge-base', DEV, H).stdout.strip()
if mb != MB: bad.append(('merge-base', mb, MB))
pr_files = sorted(lines_of('diff', '--name-only', MB, H)); dev_files = sorted(lines_of('diff', '--name-only', MB, DEV))
print('#922 files vs merge-base %d | develop delta since merge-base %d | overlap %d' % (len(pr_files), len(dev_files), len(set(pr_files) & set(dev_files))))
if sorted(D + p for p in R1) != pr_files or set(pr_files) & set(dev_files): bad.append(('PR files / overlap', pr_files))
print('pins re-read (develop %s for all %d; round-1 blobs for the 5 PR files; round-2 blobs for the 3 changed):' % (DEV[:9], len(PIN)), 'OK' if not bad else bad)
if bad: print('REFUSING: pins disagree with the repo; nothing written'); sys.exit(1)

tmpr = tempfile.mkdtemp(prefix='gen922r2-mt-')
subprocess.run(['git', 'init', '--bare', '-q', tmpr], check=True)
open(os.path.join(tmpr, 'objects', 'info', 'alternates'), 'w').write(REPO + '/.git/objects\n')
for ref, sha in (('refs/heads/h', H), ('refs/heads/d', DEV)):
    subprocess.run(['git', '-C', tmpr, 'update-ref', ref, sha], check=True)
mt = subprocess.run(['git', '-C', tmpr, 'merge-tree', '--write-tree', '--name-only', 'd', 'h'], capture_output=True, text=True)
out = mt.stdout.strip().split('\n')
print('merge-tree rc', mt.returncode, '| merged tree', out[0], '| conflicted', max(0, len(out) - 1), '| scratch', tmpr)
if mt.returncode != 0 or len(out) != 1 or out[0] != MERGED:
    print('REFUSING: the merge against the CURRENT develop is not the clean %s it was measured to be' % MERGED[:9]); sys.exit(1)

def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:70], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]

WEDB = '$WED/2_Project_Files/fleet/qa-agent/'
MAIL = WEDB + 'gatesets/2026-09-18_gate922r2/mail_922r2_ready.md'
PROMPT = WEDB + 'briefs/2026-09-18_secuura-922r2-tier2-delta.prompt.txt'
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks679-922-30c773ee8-tier2-r2/'
PRIOR      = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks679-922-8664826e5-tier2-r1/'
SUBJECT = '[QA -> Wednesday] TIER 2 DELTA GATE #922 (KS-679) 30c773ee8'
DELTA = 'DELTA 8664826e5..30c773ee8'
assert os.path.isdir(PRIOR), 'prior (round-1) report dir missing'
mailf = MAIL.replace('$WED', '/Volumes/DevMASTER/WEDNESDAY'); promptf = PROMPT.replace('$WED', '/Volumes/DevMASTER/WEDNESDAY')
assert os.path.isfile(mailf) and H in open(mailf).read(), 'READY mail capture missing or does not carry the head'
assert os.path.isfile(promptf), 'prompt missing'

HEADER_OLD = cut('# launch_qa_secuura_922.sh', '# Exit: 0 launched (or guards passed under --check) · 2..28 a guard refused\n')
HEADER_NEW = """# launch_qa_secuura_922r2.sh — cross-project QA agent, ONE TIER 2 (through code) ROUND 2 DELTA gate over Secuura/Blockchain PR #922 (KS-679)
# DELTA 8664826e5..30c773ee8 — a ONE-COMMIT FAST-FORWARD (proved by the generator): "KS-679 round 2: bound the E7 <prefix>_<uuid> exemption to the minted
# form". Three files: contract.mjs (the round-1 /^[a-z]+_<uuid>$/i BENIGN_SHAPES entry -> PREFIXED_UUID_RE: 2-12 lower-case letters, lower-case v4 uuid
# with the RFC variant, anchored, no /i, secret-named prefixes refused), the ks256 test (36 -> 80 cells), fixtures.ts (comment only). Head tree 7aa549d70.
# Round 1 at 8664826e5 = GO WITH FINDINGS (F1-F8); this gate grades the fix delta and the merged tree, not the unchanged diff.
# TIER 2 DELTA: a test file, a CI guard regex and a comment; no route, schema, handler or mint path moves.
# MERGE AUTHORITY: #922 does NOT merge on WEDNESDAY'S signed GO alone — Peter's 09-09 "not approving yet" is open; Kam rules on merging over it (exit 26).
#
# THE SHAPE, re-read live 13:00:24-13:02:42 AEST 2026-09-18: head 30c773ee8 on origin (refs/pull/922/head and the branch agree). DEVELOP MOVED since
# round 1: a105cd32b -> 207716440 (#1037 KS-1101, api-gateway + frontend only). compare develop...head = merge_base f6669623c, diverged, ahead 5, files
# 5, behind 2 (ahead and files asserted, exit 10). 0 overlap; the read-only merge-tree of 30c773ee8 against 207716440 is CLEAN — merged tree
# a1b4b6536d1d60fb2defca2886d36c9b9d0ec80e, 0 conflicted paths. The checkout's local branch ref is stale at 2b5075e9f: the head is pinned from ORIGIN only.
#
# The develop pin is judged by CONTENT — the same EIGHTEEN paths as round 1, blobs re-read at 207716440 (unchanged: #1037 touched none). A develop blob
# equal to EITHER round's #922 blob -> exit 19 LANDED; any blob nobody pinned -> exit 18; a develop move touching a GUARDED path -> exit 18.
#
# SOURCE = gatesets/2026-09-18_gate922r2/mail_922r2_ready.md, the seat's READY mail captured verbatim by message id from wednesday-agent@ (03:02:05Z).
#
# exit 7:  the prompt must name TIER 2 and carry no 'TIER 1 ROUND' / 'TIER 1 GATE' line.
# exit 15: the prompt must name ROUND 2 and the DELTA range 8664826e5..30c773ee8.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate R-6: a wholesale link can write through to the checkout .vite).
# exit 23: the prompt must carry the exact #922 round-2 verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (round 1 of this PR) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM and require the per-finding CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must say the merge authority is NOT WEDNESDAY'S signed GO alone, name Kam and Peter, and must NOT carry round 1's
#          "... and on nothing else" signed-GO sentence.
# exit 27: the READY mail AND the prompt must BOTH carry the seat's own words: '12/15 legs ran, 3 SKIPPED' (not a pass), 'key_ is REFUSED' (a decision
#          the gate must verify) and "Peter's review is still open".
# exit 28: the prompt must forbid entering BOTH worktrees that hold this branch.
# QA922R2_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED refusals can be proven.
# QA922R2_CONTRACT_FILE (test fixture, --check only): a local file stands in for develop scripts/spec-examples/check/contract.mjs (its git blob).
# A launch with any QA922R2_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-18_gate922r2/gen_launcher_922r2.py from launch_qa_secuura_922.sh (asserted substitutions + pins re-read + a proved
# fast-forward + a re-derived merged tree + residual guard + output controls + bash -n).
#
# Usage: launch_qa_secuura_922r2.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..28 a guard refused
"""
VARS_OLD = cut('BRIEF="${QA922_BRIEF:-', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-18_gate922/pr922_snapshot.md"\n')
VARS_NEW = ('BRIEF="${QA922R2_BRIEF:-' + MAIL + '}"\n'
            'PROMPT_FILE="${QA922R2_PROMPT:-' + PROMPT + '}"\n'
            "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'\n"
            "SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'\n"
            "BRANCH='refs/heads/kamilkreiser/ks-679-anchor-id-format-false'   # read on ORIGIN only: the checkout's local ref of this name is stale at 2b5075e9f\n"
            'HEAD_SHA="${QA922R2_HEAD:-' + H + '}"\n'
            "MERGE_BASE='" + MB + "'   # the merge-base of the head with develop (unchanged from round 1; the delta is a fast-forward)\n"
            "DEVELOP_SHA='" + DEV + "'   # the pin = develop RE-READ at drafting, after #1037 landed (NOT the merge-base " + MB[:9] + "; moves judged by PATH BLOB and GUARDED paths: git ls-remote 13:00:24 AEST 2026-09-18)\n"
            "REPORT_DIR='" + REPORT_DIR + "'\n"
            "PRIOR_REPORT='" + PRIOR + "'\n"
            'REAL_BRIEF="' + MAIL + '"\n')

def landed_row(old_frag, blob_r2, blob_r1):
    return (old_frag, '{"' + blob_r2 + '": "#922 r2 own", "' + blob_r1 + '": "#922 r1 own"}')
T = 'packages/shared/src/__tests__/ks256-spec-example-contract.test.ts'; FXP = 'packages/shared/src/openapi/examples/fixtures.ts'; CM = 'scripts/spec-examples/check/contract.mjs'
OKPIN_OLD = cut('    print("OK " + state + " | origin develop still " + pinned + "', 'sys.exit(0)\n')
OKPIN_NEW = ('    print("OK " + state + " | origin develop still " + pinned + " (#1037 KS-1101, api-gateway and frontend only, 0 #922 files, NOT an ancestor of the head: '
             'merged tree ' + H[:9] + ' x ' + DEV[:9] + ' = ' + MERGED + ', 0 conflicts, drafter merge-tree 03:00:36Z; git ls-remote)"); sys.exit(0)\n')
TAIL_OLD = cut('tail = "the gate merges the then-current develop onto 8664826e5', '"\n')
TAIL_NEW = ('tail = "the gate merges the then-current develop onto ' + H[:9] + ' in its own clone, asserts the merged packages/shared/src, scripts/spec-examples, '
            'docs/openapi and services/anchoring/src subtrees equal the head, or re-runs the tamper table, the guard verdict diff and the suites on the MERGED tree; '
            'names the merged-tree OID, drafter ' + DEV[:9] + ' -> ' + MERGED[:9] + ' (prompt items 1, 2, 7)"\n')

GUARDS_OLD = cut("grep -q 'TIER 2' \"$PROMPT_FILE\"", '>&2; exit 28; }\n')
GUARDS_NEW = r'''grep -q 'TIER 2' "$PROMPT_FILE" && ! grep -qE 'TIER 1 (ROUND|GATE)' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name TIER 2, or still carries a TIER 1 ROUND / GATE line" >&2; exit 7; }
grep -q 'ROUND 2' "$PROMPT_FILE" && grep -qF '__DELTA__' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name ROUND 2 and the __DELTA__ range — a delta gate that does not name its delta regates the whole PR" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the seat's READY mail capture path" >&2; exit 9; }
grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" \
  || { echo "REFUSING: the READY mail or the prompt does not name the head SHA $HEAD_SHA — a gate about another SHA is another gate" >&2; exit 20; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict" >&2; exit 12; }
grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid pushing / running the hook in the real checkout" >&2; exit 11; }
grep -qi 'no memory maintenance' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid memory maintenance inside the gate session" >&2; exit 14; }
grep -qi 'NEVER print a credential value' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid printing a credential value" >&2; exit 17; }
grep -qi 'node_modules per ENTRY' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require node_modules farmed per ENTRY (a wholesale link can write through to the checkout .vite cache)" >&2; exit 22; }
grep -qF '__SUBJECT__' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact #922 round-2 verdict subject, the coagent@ sender and the wednesday-agent@ recipient" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT (round 1 of this PR) and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the MERGE ADDENDUM and the per-finding CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "NOT WEDNESDAY'S signed GO alone" "$PROMPT_FILE" && grep -qF 'Kam' "$PROMPT_FILE" && grep -qF 'Peter' "$PROMPT_FILE" && ! grep -qiF 'and on nothing else' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not say #922's merge authority is NOT WEDNESDAY'S signed GO alone (Kam rules on merging over Peter's open review), or still carries round 1's signed-GO-and-nothing-else sentence" >&2; exit 26; }
grep -qF '12/15 legs ran, 3 SKIPPED' "$PROMPT_FILE" && grep -qF 'key_ is REFUSED' "$PROMPT_FILE" && grep -qF "Peter's review is still open" "$PROMPT_FILE" \
  && grep -qF '12/15 legs ran, 3 SKIPPED' "$BRIEF" && grep -qF 'key_ is REFUSED' "$BRIEF" && grep -qF "Peter's review is still open" "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat's own words: 12/15 legs ran, 3 SKIPPED / key_ is REFUSED / Peter's review is still open" >&2; exit 27; }
grep -qF 'quarantine/2026-09-15-s233/worktree-ks679' "$PROMPT_FILE" && grep -qF 'worktrees/s-a9-ks679' "$PROMPT_FILE" && grep -qi 'DO NOT ENTER EITHER WORKTREE' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering BOTH worktrees that hold this branch (quarantine/2026-09-15-s233/worktree-ks679 and worktrees/s-a9-ks679)" >&2; exit 28; }
'''.replace('__SUBJECT__', SUBJECT).replace('__DELTA__', DELTA)
CHECK_OLD = cut('  echo "all guards pass:"\n', '  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"\n')
CHECK_NEW = '''  echo "all guards pass:"
  echo "  head on origin: #922 round 2 $HEAD_SHA at $BRANCH"
  echo "  compare (GitHub API): develop...#922 = $COMPARE"
  echo "  $DEV_NOTE"
  echo "  READY mail, prompt, QA project and repo all present"
  echo "  prompt names TIER 2 (no TIER 1 ROUND / GATE line), ROUND 2 and the DELTA 8664826e5..30c773ee8"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY mail and prompt both name the head SHA"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact #922 round-2 verdict subject, coagent@ sender, wednesday-agent@ recipient"
  echo "  prompt names the report directory, the round-1 PRIOR REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries the MERGE ADDENDUM and requires CLOSED / STILL OPEN / NEW per finding"
  echo "  prompt says the merge authority is NOT WEDNESDAY'S signed GO alone: Kam rules on merging over Peter's open review"
  echo "  READY mail and prompt BOTH carry: 12/15 legs ran, 3 SKIPPED / key_ is REFUSED / Peter's review is still open"
  echo "  prompt forbids entering both worktrees (the quarantined worktree-ks679 and seat A's s-a9-ks679)"
  [ -n "${QA922R2_CUR_DEV:-}" ] && echo "  (develop read from the QA922R2_CUR_DEV test override, not ls-remote)"
  [ -n "${QA922R2_CONTRACT_FILE:-}" ] && echo "  (develop scripts/spec-examples/check/contract.mjs read from the QA922R2_CONTRACT_FILE fixture, not the contents API)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
'''
REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('vars', VARS_OLD, VARS_NEW, 1),
 ('head refuse', 'REFUSING: #922 — $HEAD_SHA is not at', 'REFUSING: #922 round 2 — $HEAD_SHA is not at', 1),
 ('compare comment', '# develop...#922 = f6669623c ahead 4 files 5 (behind 1: develop moved to a105cd32b after the seat merged; behind deliberately NOT asserted). Compare API 00:37:52Z 2026-09-18.',
                     '# develop...#922 = f6669623c ahead 5 files 5 (behind 2: develop moved to a105cd32b then 207716440; behind deliberately NOT asserted). Compare API 03:02:42Z 2026-09-18.', 1),
 ('compare assert', '"$MERGE_BASE ahead=4 files=5"', '"$MERGE_BASE ahead=5 files=5"', 1),
 ('compare msg', "the gateset pins '$MERGE_BASE ahead=4 files=5'", "the gateset pins '$MERGE_BASE ahead=5 files=5'", 1),
 ('cur dev', 'CUR_DEV="${QA922_CUR_DEV:-', 'CUR_DEV="${QA922R2_CUR_DEV:-', 1),
 ('landed test', '{"' + R1[T] + '": "#922 own"}', landed_row(None, R2[T], R1[T])[1], 1),
 ('landed fixtures', '{"' + R1[FXP] + '": "#922 own"}', landed_row(None, R2[FXP], R1[FXP])[1], 1),
 ('landed contract', '{"' + R1[CM] + '": "#922 own"}', landed_row(None, R2[CM], R1[CM])[1], 1),
 ('fixture env', 'os.environ.get("QA922_CONTRACT_FILE", "")', 'os.environ.get("QA922R2_CONTRACT_FILE", "")', 1),
 ('ok pinned', OKPIN_OLD, OKPIN_NEW, 1),
 ('tail', TAIL_OLD, TAIL_NEW, 1),
 ('guards', GUARDS_OLD, GUARDS_NEW, 1),
 ('check block', CHECK_OLD, CHECK_NEW, 1),
 ('exit16', '[ -z "${QA922_BRIEF:-}${QA922_PROMPT:-}${QA922_HEAD:-}${QA922_CUR_DEV:-}${QA922_CONTRACT_FILE:-}" ]',
            '[ -z "${QA922R2_BRIEF:-}${QA922R2_PROMPT:-}${QA922R2_HEAD:-}${QA922R2_CUR_DEV:-}${QA922R2_CONTRACT_FILE:-}" ]', 1),
]
badn = 0
for label, old, new, want in REPL:
    n = s.count(old)
    if n != want: print('ANCHOR COUNT', label, n, '!=', want); badn += 1; continue
    s = s.replace(old, new); print('  ok', label, n)
if badn: print('REFUSING: %d anchors disagreed; nothing written' % badn); sys.exit(1)

BODY = s.replace(HEADER_NEW, '')
RESID = ['QA922_', 'a105cd32b1ed9c6927ae6e797f8259224d8480c6', '5c56e26fe', 'pr922_snapshot', 'secuura-922-tier2.prompt', '2026-09-17-ks1211-1027', 'ROUND 1', 'ahead=4',
         'the TESTED grant) and on nothing else', 'PR snapshot', '#1034 KS-1215', '00:37:52Z', '10:37:46', '"#922 own"}, {"' ]
res = {t: BODY.count(t) for t in RESID if t in BODY}
# the two unchanged PR files keep their single "#922 own" label — count it exactly instead of banning it
if BODY.count('"#922 own"') != 2: res['"#922 own" (want 2)'] = BODY.count('"#922 own"')
if res: print('REFUSING: residual tokens in the body', res); sys.exit(2)

CTL = {H: None, DEV: 1, MERGED: 2, REPORT_DIR: 1, PRIOR: 1, 'ahead=5 files=5': 2, 'QA922R2_CONTRACT_FILE': 5, 'QA922R2_CUR_DEV': 5,
       ': DV}': 18, '"#922 r2 own"': 3, '"#922 r1 own"': 3, "grep -q 'ROUND 2'": 1, DELTA: None, SUBJECT: 1, "NOT WEDNESDAY'S signed GO alone": None,
       'key_ is REFUSED': None, "Peter's review is still open": None, 'gatesets/2026-09-18_gate922r2/mail_922r2_ready.md': None,
       'briefs/2026-09-18_secuura-922r2-tier2-delta.prompt.txt': 1, '[ -t 0 ]': 1, 'exec claude --dangerously-skip-permissions --model opus': 1,
       'exit 26': None, 'exit 27': None, 'exit 28': None, 'exit 19': None, 'exit 16': None, 'DEV_CONTENT_ALLOWED = {}': 1}
got = {k: s.count(k) for k in CTL}
print('output controls', {(k[:26] + '…' if len(k) > 26 else k): v for k, v in got.items()})
for k, v in CTL.items():
    if (v is not None and got[k] != v) or got[k] == 0: print('CONTROL DISAGREED', k, got[k], v); sys.exit(1)
for pth, b_ in PIN.items():
    if s.count(b_) != 1: print('CONTROL DISAGREED develop pin', pth, s.count(b_)); sys.exit(1)
for pth, b_ in list(R1.items()) + list(R2.items()):
    if s.count(b_) != 1: print('CONTROL DISAGREED landed pin', pth, b_[:9], s.count(b_)); sys.exit(1)
for tag in ("<<'PY'\n", "<<'PYJ'\n"):
    i = s.index(tag); j = s.index('\nPY' + ('J' if 'PYJ' in tag else '') + '\n', i); blk = s[i:j]
    print('heredoc', tag.strip(), 'apostrophes', blk.count("'") - 2, 'parens (', blk.count('('), ')', blk.count(')'))
    if (blk.count("'") - 2) % 2 or blk.count('(') != blk.count(')'): print('REFUSING: heredoc parity'); sys.exit(1)
if re.search(r'git -C "\$REPO" (fetch|push|checkout|merge|reset|worktree|commit|switch|pull|merge-tree)\b', s): print('REFUSING: git write verb'); sys.exit(1)
if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', s): print('REFUSING: control bytes'); sys.exit(1)
tmp = OUT + '.gen-tmp'; open(tmp, 'w').write(s)
p = subprocess.run(['bash', '-n', tmp], capture_output=True, text=True); print('bash -n rc', p.returncode, p.stderr.strip()[:300])
if p.returncode: print('REFUSING: bash -n; the tmp file is left for reading at', tmp); sys.exit(3)
if os.path.exists(OUT):
    pre = OUT + '.pre-' + now('+%H%M%S'); shutil.copyfile(OUT, pre); print('existing output copied to', pre)
os.replace(tmp, OUT); os.chmod(OUT, 0o755)
print('written', OUT, 'mode', oct(os.stat(OUT).st_mode & 0o777), 'sha256', hashlib.sha256(open(OUT, 'rb').read()).hexdigest()[:16], 'lines', s.count('\n'))
