#!/usr/bin/env python3
"""gen_launcher_922.py — derive launchers/launch_qa_secuura_922.sh from launchers/launch_qa_secuura_ks1101_1037.sh (the #1037 launcher, live in pane %99,
whose exit-18 guard caught develop moving mid-draft) by ASSERTED substitutions: every anchor must occur exactly as often as stated, or the generator refuses
and writes nothing. Pins are RE-READ from the repo, never copied from the coordinator's relay; the merged tree AND the seat's 234-file survival control are
RE-DERIVED here, read-only, in a throwaway bare repo that borrows the checkout's objects through objects/info/alternates (nothing is written into the
Secuura repo, and the throwaway is left in place for reading — this drafter does not delete).

#922 (KS-679) at head 8664826e5; merge-base / second parent f6669623c; CURRENT develop a105cd32b (#1034, api-gateway only — #922 is one develop-move
behind, 0 overlap, merge clean). A DIFFERENT service and suite from #1037: packages/shared vitest, the scripts/spec-examples guard, generate-openapi.
So the template's JUDGED set, GUARDED list and whole guard block are REPLACED as blocks (each block anchor asserted = 1), not edited line by line.

TIER 2 (through code), ruled by the drafter: no route, schema, status code, handler or mint path moves; the risk is a secret-detector guard (E7) being
widened, which is measured through code. The prompt file is therefore named -tier2 (the coordinator's commission named -tier1 and asked for a ruling).

DIFFERENCES FROM THE #1037 LAUNCHER, stated rather than implied:
 (a) NO seat READY mail at this head. BRIEF points at gatesets/2026-09-18_gate922/pr922_snapshot.md — the PR body + comments captured VERBATIM from the
     GitHub API at 00:45:15Z. Cross-document assertions kept, and real: the head SHA in both (exit 20; in the snapshot it is the API capture line), and
     exit 27 — the seat's OWN words for the three things this gate must not let pass as green ('12/15 legs ran, 3 SKIPPED', 'Closes KS-679', 'External
     consumers') in BOTH. The tier is asserted on the PROMPT alone (the seat never stated one) plus a NEGATIVE: no 'TIER 1 ROUND' / 'TIER 1 GATE' in it.
 (b) NEW exit 28: the prompt must forbid entering BOTH worktrees that hold this branch — the quarantined one the coordinator named AND seat A's
     worktrees/s-a9-ks679 (detached at the head), which the coordinator did not name and the drafter found in .git/worktrees.
 (c) No develop-ahead files: #1034 touched none of the eighteen judged paths. The template's 'eighteen files' develop comment is
     already true for #922 (18 pins), so it is deliberately NOT substituted — a substitution whose old equals its new is a silent no-op.
Usage: gen_launcher_922.py <template launcher> <output launcher>   Exit: 0 written · 1 anchor/control/pin disagreed · 2 residual token · 3 bash -n failed"""
import hashlib, os, re, shutil, subprocess, sys, tempfile
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
def now(f='+%Y-%m-%d %H:%M:%S %Z'): return subprocess.run(['date', f], capture_output=True, text=True).stdout.strip()
print('gen_launcher_922', now(), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))

REPO = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
H   = '8664826e53cc47d4dd69c784926c9c14af444cec'   # #922 head
MB  = 'f6669623ccae5ab445be6e0e73fb4f19ae2c89d1'   # merge-base = head second parent
DEV = 'a105cd32b1ed9c6927ae6e797f8259224d8480c6'   # CURRENT develop, re-read 10:37:46 AEST
HT  = '92224cca72ab50fd0ca882f0957b5b8f7cf79f0a'   # head tree
P1  = 'e60a24c5024d0adae3fae8966bbd4e243e8b581c'   # head first parent = the pre-merge head
OLDBASE = '852e1fff773bd358170c11334d59496f05fdd8a7'  # the branch base before this morning's merge
MERGED = '5c56e26fee8cffc3497eae5cc6433a81914d3931'   # merge-tree H x DEV, re-derived below
D = 'Blockchain/Dev/'
def git(*a, inp=None):
    return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True, input=inp)
rp = lambda x: git('rev-parse', '--verify', '-q', x).stdout.strip()

# path relative to Blockchain/Dev -> blob at the CURRENT develop a105cd32b. Re-read and asserted below.
PIN = {
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
LANDED = {  # the five #922 files -> blob AT THE HEAD (a develop that reads one of these means #922 landed: exit 19)
 'docs/openapi/secuura-api.yaml':                                  '16ac8aa78463849864fa6285e20c9946c027fb7b',
 'packages/shared/src/__tests__/ks256-spec-example-contract.test.ts': '72533d3b01a4941578b1f777f0def3f9ec9ea6f0',
 'packages/shared/src/openapi/examples/fixtures.ts':               'b54d26929c564d9cd4e2e2f27da12df6d6d85325',
 'scripts/spec-examples/check/contract.mjs':                       'db726db299f738e2bf6790b3612d917b4d1eb9fc',
 'services/anchoring/src/anchoring.openapi.ts':                    '29c089bb0abcd65d42fe8fca2d6beaff0368fa98',
}
bad = []
for p, b in PIN.items():
    at_dev, at_h = rp(DEV + ':' + D + p), rp(H + ':' + D + p)
    if at_dev != b: bad.append(('develop blob', p, b, at_dev))
    if p in LANDED:
        if at_h != LANDED[p]: bad.append(('landed blob at head', p, LANDED[p], at_h))
        if at_h == at_dev: bad.append(('PR file equals develop — #922 may have landed', p))
    elif at_h != b: bad.append(('head blob differs for an untouched file', p, b, at_h))
for k, want in (('^{tree}', HT), ('^1', P1), ('^2', MB)):
    if rp(H + k) != want: bad.append(('head' + k, rp(H + k), want))
mb = git('merge-base', DEV, H).stdout.strip()
print('merge-base(develop, head) re-read:', mb, '== MB', mb == MB)
if mb != MB: bad.append(('merge-base', mb, MB))
pr_files = sorted(git('diff', '--name-only', MB, H).stdout.splitlines())
dev_files = sorted(git('diff', '--name-only', MB, DEV).stdout.splitlines())
print('#922 files vs merge-base:', len(pr_files), '| develop delta since merge-base:', len(dev_files), '| overlap:', len(set(pr_files) & set(dev_files)))
if sorted(D + p for p in LANDED) != pr_files: bad.append(('PR file list', pr_files))
if set(pr_files) & set(dev_files): bad.append(('overlap with develop delta', sorted(set(pr_files) & set(dev_files))))
# The seat's survival control, RE-DERIVED: the merge brought exactly develop's delta, and KS-679's own delta is unchanged by it.
def pid(a, b):
    d = git('diff', a, b).stdout
    return subprocess.run(['git', 'patch-id', '--stable'], input=d, capture_output=True, text=True).stdout.split(' ')[0]
n_pre = len(git('diff', '--name-only', P1, H).stdout.splitlines()); n_dev = len(git('diff', '--name-only', OLDBASE, MB).stdout.splitlines())
names_eq = sorted(git('diff', '--name-only', P1, H).stdout.splitlines()) == sorted(git('diff', '--name-only', OLDBASE, MB).stdout.splitlines())
merge_pid_eq = pid(P1, H) == pid(OLDBASE, MB)
ks679_pid_eq = pid(OLDBASE, P1) == pid(MB, H)
print('survival control: pre-merge->head %d files, develop %s..%s %d files; names equal %s; patch-id equal %s; KS-679 delta patch-id equal %s'
      % (n_pre, OLDBASE[:9], MB[:9], n_dev, names_eq, merge_pid_eq, ks679_pid_eq))
if not (names_eq and merge_pid_eq and ks679_pid_eq and n_pre == 234): bad.append(('survival control', n_pre, n_dev, names_eq, merge_pid_eq, ks679_pid_eq))
print('pinned blobs re-read (develop %s for all %d; head = develop for the %d untouched; the %d PR files at the head):'
      % (DEV[:9], len(PIN), len(PIN) - len(LANDED), len(LANDED)), 'OK' if not bad else bad)
if bad: print('REFUSING: pins disagree with the repo; nothing written'); sys.exit(1)

tmpr = tempfile.mkdtemp(prefix='gen922-mt-')   # left in place: this drafter never deletes
subprocess.run(['git', 'init', '--bare', '-q', tmpr], check=True)
open(os.path.join(tmpr, 'objects', 'info', 'alternates'), 'w').write(REPO + '/.git/objects\n')
for ref, sha in (('refs/heads/h', H), ('refs/heads/d', DEV)):
    subprocess.run(['git', '-C', tmpr, 'update-ref', ref, sha], check=True)
mt = subprocess.run(['git', '-C', tmpr, 'merge-tree', '--write-tree', '--name-only', 'd', 'h'], capture_output=True, text=True)
lines = mt.stdout.strip().split('\n')
print('merge-tree rc', mt.returncode, '| merged tree', lines[0], '| conflicted paths', max(0, len(lines) - 1), '| scratch', tmpr)
if mt.returncode != 0 or len(lines) != 1 or lines[0] != MERGED:
    print('REFUSING: the merge against the CURRENT develop is not the clean %s it was measured to be — re-pin deliberately' % MERGED[:9]); sys.exit(1)

def cut(start, end_incl):
    assert s.count(start) == 1, ('cut start', start[:70], s.count(start))
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]

WEDB = '$WED/2_Project_Files/fleet/qa-agent/'
SNAP = WEDB + 'gatesets/2026-09-18_gate922/pr922_snapshot.md'
PROMPT = WEDB + 'briefs/2026-09-18_secuura-922-tier2.prompt.txt'
REPORT_DIR = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks679-922-8664826e5-tier2-r1/'
PRIOR      = '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1211-1027-d7fc6cc55-tier2-r1/'
QUAR = 'quarantine/2026-09-15-s233/worktree-ks679'; SEATWT = 'worktrees/s-a9-ks679'
SUBJECT = '[QA -> Wednesday] TIER 2 GATE #922 (KS-679) 8664826e5'
assert os.path.isdir(PRIOR), 'prior report dir missing'
snapf = SNAP.replace('$WED', '/Volumes/DevMASTER/WEDNESDAY'); promptf = PROMPT.replace('$WED', '/Volumes/DevMASTER/WEDNESDAY')
assert os.path.isfile(snapf) and H in open(snapf).read(), 'snapshot missing or does not carry the head'
assert os.path.isfile(promptf), 'prompt missing'
for q in (QUAR, SEATWT):
    assert os.path.isdir('/Volumes/DevMASTER/!CODING/Secuura/Blockchain/' + ('5_Project_History/' if q == QUAR else '') + q), 'worktree path not found: ' + q

HEADER_OLD = cut('# launch_qa_secuura_ks1101_1037.sh', '# Exit: 0 launched (or guards passed under --check) · 2..27 a guard refused\n')
HEADER_NEW = """# launch_qa_secuura_922.sh — cross-project QA agent, ONE TIER 2 (through code) ROUND 1 gate over Secuura/Blockchain PR #922 (KS-679, Seat A)
# @ 8664826e53cc47d4dd69c784926c9c14af444cec — the published example Anchor.id becomes the shape anchoring actually mints (anchor_<uuid>, was anc_…, which
# E8 CERTIFIED because it sat in the fixture set), and the spec-example secret detector E7 is WIDENED: BENIGN_SHAPES gains /^[a-z]+_<exact uuid>$/i.
# Five files, four commits: 2b5075e9f (the change) -> a7d9e2943 (develop 852e1fff7 in) -> e60a24c50 (the seven-case E7 control) -> 8664826e5 (develop
# f6669623c in, this morning). Head tree 92224cca7. anchoring.openapi.ts is +3 COMMENT lines.
# TIER 2, drafter-ruled: no route, schema, status code, handler or mint path moves; the risk is a guard being loosened, measured through code. A GO is a
# gate verdict: #922 merges on WEDNESDAY'S signed GO naming the head (the TESTED grant) and on nothing else (exit 26 guards it).
#
# THE SHAPE, re-read live 10:37:46-10:45:15 AEST 2026-09-18 (git ls-remote + the GitHub PR and compare APIs agree): the head is 8664826e5 on origin, as
# relayed. #922 is ALREADY ONE DEVELOP-MOVE BEHIND: develop a105cd32b = #1034 (KS-1215), three files, all services/api-gateway. compare develop...head =
# merge_base f6669623c, status diverged, ahead 4, files 5, behind 1 (ahead and files asserted, exit 10; behind NOT asserted). MEASURED: 0 shared files,
# and the read-only merge-tree of 8664826e5 against a105cd32b is CLEAN — merged tree 5c56e26fee8cffc3497eae5cc6433a81914d3931, 0 conflicted paths.
# The seat's survival control is RE-DERIVED by the generator: e60a24c50..8664826e5 = develop 852e1fff7..f6669623c by name (234 = 234) AND by patch-id,
# and KS-679's own delta is patch-id-equal before and after the merge.
# THE LOCAL BRANCH REF IS STALE (refs/heads/kamilkreiser/ks-679-anchor-id-format-false = 2b5075e9f in the checkout): the head is pinned from ORIGIN only.
#
# The develop pin is judged by CONTENT — PATH BLOBS — never by develop's SHA: (a) EIGHTEEN files by blob at the CURRENT develop: the PR five
# (secuura-api.yaml 122d3a2f8, the ks256 test adbe91dfb, fixtures.ts ca5d5eae1, contract.mjs 43a9c5dea, anchoring.openapi.ts 49b8b38da; at a #922 blob ->
# exit 19 LANDED) and what the gate runs: the spec-example guard (check-spec-examples.mjs, rules-example / rules-global / allowlist / collect .mjs, the
# allowlist json), scripts/generate-openapi.ts, packages/shared package.json / vitest.config.ts / tsconfig.json, anchoring index.ts (the mint sites),
# the Dev package.json (check:openapi) and eslint.config.mjs — any blob nobody pinned -> exit 18; (b) if develop moves past a105cd32b, the compare
# pinned...develop REFUSES (exit 18) when the delta touches a GUARDED path — packages/shared/src/ and its package.json / vitest.config.ts /
# tsconfig.json, scripts/spec-examples/, scripts/generate-openapi.ts, docs/openapi/, services/anchoring/src/, the Dev package.json, eslint.config.mjs.
# NOTE: #1036 (KS-763, READY, ungated) rewrites packages/shared/package.json — if it lands first this REFUSES by design: re-pin deliberately.
# Lockfiles are not guarded: the gate names the vitest version it ran. DEV_CONTENT_ALLOWED is EMPTY.
#
# NO SEAT READY MAIL at this head. BRIEF = gatesets/2026-09-18_gate922/pr922_snapshot.md, the PR body + comments captured verbatim from the GitHub API
# (00:45:15Z). Its Test Evidence and PREFLIGHT line are from the 2026-09-14 push at e60a24c50, not this head — the prompt says so.
#
# exit 7:  the prompt must name TIER 2 and must NOT carry a 'TIER 1 ROUND' / 'TIER 1 GATE' line (the seat stated no tier; the drafter ruled it).
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate R-6: a wholesale link can write through to the checkout .vite).
# exit 23: the prompt must carry the exact #922 verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (#1027, the tier 2 method bar) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM and require the per-finding CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as #922's merge authority and carry no copied Kam's-tap merge condition.
# exit 27: the PR snapshot AND the prompt must BOTH carry the seat's own words for what must not pass as green: '12/15 legs ran, 3 SKIPPED' (the
#          incomplete preflight), 'Closes KS-679' (a closing phrase) and 'External consumers' (unmeasured).
# exit 28: the prompt must forbid entering BOTH worktrees that hold this branch: 5_Project_History/quarantine/2026-09-15-s233/worktree-ks679 and
#          worktrees/s-a9-ks679 (seat A's, detached at the head).
# QA922_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED refusals can be proven.
# QA922_CONTRACT_FILE (test fixture, --check only): a local file stands in for develop scripts/spec-examples/check/contract.mjs (its git blob).
# A launch with any QA922_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-18_gate922/gen_launcher_922.py from launch_qa_secuura_ks1101_1037.sh (asserted block substitutions + pins re-read from the
# repo + a re-derived merged tree + a re-derived survival control + residual guard + output controls + bash -n).
#
# Usage: launch_qa_secuura_922.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..28 a guard refused
"""

VARS_OLD = cut('BRIEF="${QA1037_BRIEF:-', 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-18_gate1037/mail_1037_ready.md"\n')
VARS_NEW = ('BRIEF="${QA922_BRIEF:-' + SNAP + '}"\n'
            'PROMPT_FILE="${QA922_PROMPT:-' + PROMPT + '}"\n'
            "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'\n"
            "SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'\n"
            "BRANCH='refs/heads/kamilkreiser/ks-679-anchor-id-format-false'   # read on ORIGIN only: the checkout's local ref of this name is stale at 2b5075e9f\n"
            'HEAD_SHA="${QA922_HEAD:-' + H + '}"\n'
            "MERGE_BASE='" + MB + "'   # the merge-base of the head with develop = the head second parent (develop when the seat merged it in, NOT develop now)\n"
            "DEVELOP_SHA='" + DEV + "'   # the pin = develop RE-READ at drafting, after #1034 landed (NOT the merge-base " + MB[:9] + "; moves judged by PATH BLOB and GUARDED paths: git ls-remote 10:37:46 AEST 2026-09-18)\n"
            "REPORT_DIR='" + REPORT_DIR + "'\n"
            "PRIOR_REPORT='" + PRIOR + "'\n"
            'REAL_BRIEF="' + SNAP + '"\n')

JUDGED_OLD = cut('A = D + "services/api-gateway/"\n', 'content_cleared = set()\n')
def key(p_):
    if p_.startswith('packages/shared/'): return 'A + "' + p_[len('packages/shared/'):] + '"'
    if p_.startswith('scripts/spec-examples/'): return 'X + "' + p_[len('scripts/spec-examples/'):] + '"'
    return 'D + "' + p_ + '"'
rows = []
for p_, b_ in PIN.items():
    k = 'CONTRACT' if p_ == 'scripts/spec-examples/check/contract.mjs' else key(p_)
    landed = ('{"' + LANDED[p_] + '": "#922 own"}') if p_ in LANDED else '{}'
    rows.append('  %s:%s({"%s": DV}, %s),' % (k, ' ' * max(1, 66 - len(k)), b_, landed))
JUDGED_NEW = ('A = D + "packages/shared/"\nX = D + "scripts/spec-examples/"\nCONTRACT = X + "check/contract.mjs"\nDV = "develop"\n'
              '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop\nJUDGED = {\n'
              + '\n'.join(rows) +
              '\n}\n# No REGION judgement: every file is judged by exact blob (a develop move of any judged file refuses, exit 18; a #922 blob, exit 19).\n'
              'content_cleared = set()\n')

OKPIN_OLD = cut('    print("OK " + state + " | origin develop still " + pinned + "', 'sys.exit(0)\n')
OKPIN_NEW = ('    print("OK " + state + " | origin develop still " + pinned + " (#1034 KS-1215, services/api-gateway only, 0 #922 files, NOT an ancestor of the head: '
             'merged tree ' + H[:9] + ' x ' + DEV[:9] + ' = ' + MERGED + ', 0 conflicts, drafter merge-tree 00:38:43Z; git ls-remote)"); sys.exit(0)\n')

GUARD_OLD = cut('GUARDED = [A + "src/",\n', 'DEV_CONTENT_ALLOWED = {}\n')
GUARD_NEW = '''GUARDED = [A + "src/",
           A + "package.json",
           A + "vitest.config.ts",
           A + "tsconfig.json",
           X,
           D + "scripts/generate-openapi.ts",
           D + "docs/openapi/",
           D + "services/anchoring/src/",
           D + "package.json",
           D + "eslint.config.mjs"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: EMPTY. No lockfile is guarded: the gate names the vitest version it ran against develops lock. Re-pin deliberately.
# A pending PR that rewrites packages/shared/package.json would refuse here if it lands first. That is by design: re-pin deliberately.
DEV_CONTENT_ALLOWED = {}
'''
TAIL_OLD = cut('tail = "the gate merges the then-current develop onto f87506f47', '"\n')
TAIL_NEW = ('tail = "the gate merges the then-current develop onto ' + H[:9] + ' in its own clone, asserts the merged packages/shared/src, scripts/spec-examples, '
            'docs/openapi and services/anchoring/src subtrees equal the head, or re-runs the E7 census, the guard verdict diff, the tamper table and the suites on the '
            'MERGED tree; names the merged-tree OID, drafter ' + DEV[:9] + ' -> ' + MERGED[:9] + ' (prompt L0 and items 1-3, 5, 6)"\n')
OKMOVED_OLD = cut('print("OK " + state + " | origin develop MOVED %s -> %s', 'sys.exit(0)\n')
OKMOVED_NEW = ('print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d — disjoint from the GUARDED list '
               '(packages/shared/src/ + its package.json / vitest.config.ts / tsconfig.json, scripts/spec-examples/, scripts/generate-openapi.ts, docs/openapi/, '
               'services/anchoring/src/, the Dev package.json, eslint.config.mjs); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), tail)); sys.exit(0)\n')

GUARDS_OLD = cut("grep -q 'TIER 1' \"$BRIEF\" && grep -q 'TIER 1' \"$PROMPT_FILE\"", '>&2; exit 27; }\n')
GUARDS_NEW = r'''grep -q 'TIER 2' "$PROMPT_FILE" && ! grep -qE 'TIER 1 (ROUND|GATE)' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name TIER 2, or still carries a TIER 1 ROUND / GATE line — the drafter ruled tier 2; the seat stated none" >&2; exit 7; }
grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: prompt does not name ROUND 1 — this gate has no seat READY mail; its source is the PR snapshot, which carries no round" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the PR snapshot path" >&2; exit 9; }
grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" \
  || { echo "REFUSING: the PR snapshot or the prompt does not name the head SHA $HEAD_SHA — a gate about another SHA is another gate" >&2; exit 20; }
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
  || { echo "REFUSING: prompt does not carry the exact #922 verdict subject, the coagent@ sender and the wednesday-agent@ recipient" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT (#1027, the tier 2 method bar) and NOT-TESTED.written-first.md — the QA agent has no inbox" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the MERGE ADDENDUM and the per-finding CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO as the #922 merge authority, or a copied Kam's-tap merge condition survives" >&2; exit 26; }
grep -qF '12/15 legs ran, 3 SKIPPED' "$PROMPT_FILE" && grep -qF 'Closes KS-679' "$PROMPT_FILE" && grep -qiF 'External consumers' "$PROMPT_FILE" \
  && grep -qF '12/15 legs ran, 3 SKIPPED' "$BRIEF" && grep -qF 'Closes KS-679' "$BRIEF" && grep -qiF 'External consumers' "$BRIEF" \
  || { echo "REFUSING: the PR snapshot and the prompt do not BOTH carry the seat's own words for the incomplete preflight (12/15 legs ran, 3 SKIPPED), the closing phrase (Closes KS-679) and the unmeasured External consumers — the gate must not let them pass as green" >&2; exit 27; }
grep -qF '__QUAR__' "$PROMPT_FILE" && grep -qF '__SEATWT__' "$PROMPT_FILE" && grep -qi 'DO NOT ENTER EITHER WORKTREE' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering BOTH worktrees that hold this branch (__QUAR__ and __SEATWT__)" >&2; exit 28; }
'''.replace('__SUBJECT__', SUBJECT).replace('__QUAR__', QUAR).replace('__SEATWT__', SEATWT)

CHECK_OLD = cut('  echo "all guards pass:"\n', '  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"\n')
CHECK_NEW = '''  echo "all guards pass:"
  echo "  head on origin: #922 $HEAD_SHA at $BRANCH"
  echo "  compare (GitHub API): develop...#922 = $COMPARE"
  echo "  $DEV_NOTE"
  echo "  PR snapshot, prompt, QA project and repo all present"
  echo "  prompt names TIER 2 and carries no TIER 1 ROUND / GATE line; prompt names ROUND 1"
  echo "  prompt opens with the thinking directive and names the PR snapshot"
  echo "  PR snapshot and prompt both name the head SHA"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact #922 verdict subject, coagent@ sender, wednesday-agent@ recipient"
  echo "  prompt names the report directory, the #1027 PRIOR REPORT (tier 2 method bar) and NOT-TESTED.written-first.md"
  echo "  prompt carries the MERGE ADDENDUM and requires CLOSED / STILL OPEN / NEW per finding"
  echo "  prompt names WEDNESDAY'S signed GO as the merge authority; no copied Kam's-tap merge condition survives"
  echo "  PR snapshot and prompt BOTH carry: 12/15 legs ran, 3 SKIPPED / Closes KS-679 / External consumers"
  echo "  prompt forbids entering both worktrees (the quarantined worktree-ks679 and seat A's s-a9-ks679)"
  [ -n "${QA922_CUR_DEV:-}" ] && echo "  (develop read from the QA922_CUR_DEV test override, not ls-remote)"
  [ -n "${QA922_CONTRACT_FILE:-}" ] && echo "  (develop scripts/spec-examples/check/contract.mjs read from the QA922_CONTRACT_FILE fixture, not the contents API)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
'''

REPL = [
 ('header', HEADER_OLD, HEADER_NEW, 1),
 ('vars', VARS_OLD, VARS_NEW, 1),
 ('head refuse', 'REFUSING: #1037 — $HEAD_SHA is not at $BRANCH on origin', 'REFUSING: #922 — $HEAD_SHA is not at $BRANCH on origin', 1),
 ('compare comment', '# develop...#1037 = 34cdcfb26 ahead 3 files 6 (behind 2: develop moved to f6669623c then a105cd32b after the seat pushed; behind deliberately NOT asserted). Compare API 00:25:55Z 2026-09-18.',
                     '# develop...#922 = f6669623c ahead 4 files 5 (behind 1: develop moved to a105cd32b after the seat merged; behind deliberately NOT asserted). Compare API 00:37:52Z 2026-09-18.', 1),
 ('compare assert', '''[ "$COMPARE" = "$MERGE_BASE ahead=3 files=6" ] || { echo "REFUSING: #1037 develop...head reads '$COMPARE', the gateset pins '$MERGE_BASE ahead=3 files=6'" >&2; exit 10; }''',
                    '''[ "$COMPARE" = "$MERGE_BASE ahead=4 files=5" ] || { echo "REFUSING: #922 develop...head reads '$COMPARE', the gateset pins '$MERGE_BASE ahead=4 files=5'" >&2; exit 10; }''', 1),
 ('cur dev', 'CUR_DEV="${QA1037_CUR_DEV:-', 'CUR_DEV="${QA922_CUR_DEV:-', 1),
 ('judged', JUDGED_OLD, JUDGED_NEW, 1),
 ('fixture env', '    fixture = os.environ.get("QA1037_HEALTH_FILE", "") if f == HEALTHTS else ""\n',
                 '    fixture = os.environ.get("QA922_CONTRACT_FILE", "") if f == CONTRACT else ""\n', 1),
 ('landed msg', '" — #1037 has landed; this gateset is stale"', '" — #922 has landed; this gateset is stale"', 1),
 ('ok pinned', OKPIN_OLD, OKPIN_NEW, 1),
 ('guarded', GUARD_OLD, GUARD_NEW, 1),
 ('tail', TAIL_OLD, TAIL_NEW, 1),
 ('ok moved', OKMOVED_OLD, OKMOVED_NEW, 1),
 ('guards', GUARDS_OLD, GUARDS_NEW, 1),
 ('check block', CHECK_OLD, CHECK_NEW, 1),
 ('exit16', '[ -z "${QA1037_BRIEF:-}${QA1037_PROMPT:-}${QA1037_HEAD:-}${QA1037_CUR_DEV:-}${QA1037_HEALTH_FILE:-}" ]',
            '[ -z "${QA922_BRIEF:-}${QA922_PROMPT:-}${QA922_HEAD:-}${QA922_CUR_DEV:-}${QA922_CONTRACT_FILE:-}" ]', 1),
]
badn = 0
for label, old, new, want in REPL:
    n = s.count(old)
    if n != want: print('ANCHOR COUNT', label, n, '!=', want); badn += 1; continue
    s = s.replace(old, new); print('  ok', label, n)
if badn: print('REFUSING: %d anchors disagreed; nothing written' % badn); sys.exit(1)

BODY = s.replace(HEADER_NEW, '')
RESID = ['QA1037_', '#1037', 'KS-1101', 'ks1101', 'f87506f47', '34cdcfb26', '6e8e62231', 'HEALTHTS', 'health', 'api-gateway', 'smoke-test',
         'frontend', 'READY mail and', 'READY mail path', 'the READY mail or', 'mail_1037', 'secuura-1037', 'TIER 1 GATE #', 'ks-1101', '#1034 PRIOR']
res = {t[:30]: BODY.count(t) for t in RESID if t in BODY and t not in ('api-gateway',)}
# api-gateway may survive ONLY inside the ok-pinned line naming #1034's own service; count it exactly.
if BODY.count('api-gateway') != 1: res['api-gateway (want 1)'] = BODY.count('api-gateway')
if res:
    print('REFUSING: residual tokens in the body', res, [l[:140] for l in BODY.splitlines() if any(t in l for t in ('QA1037_', '#1037', 'health', 'TIER 1', 'frontend', 'smoke'))][:8]); sys.exit(2)

CTL = {H: None, MB: None, DEV: 1, MERGED: 2, REPORT_DIR: 1, PRIOR: 1, '"$PRIOR_REPORT"': 1, 'ahead=4 files=5': 2, 'QA922_CONTRACT_FILE': 5,
       'QA922_CUR_DEV': 5, ': DV}': 18, '"#922 own"': 5, "grep -q 'ROUND 1'": 1, "grep -q 'TIER 2'": 1, 'content_cleared': 2,
       'DEV_CONTENT_ALLOWED = {}': 1, SUBJECT: 1, '12/15 legs ran, 3 SKIPPED': None, 'Closes KS-679': None, QUAR: None, SEATWT: None,
       'gatesets/2026-09-18_gate922/pr922_snapshot.md': None, 'briefs/2026-09-18_secuura-922-tier2.prompt.txt': 1, '[ -t 0 ]': 1,
       'exec claude --dangerously-skip-permissions --model opus': 1, 'CLOSED / STILL OPEN / NEW': None, 'MERGE ADDENDUM': None,
       'NOT-TESTED.written-first.md': None, 'exit 28': None, 'exit 27': None, 'exit 26': None, 'exit 19': None, 'exit 16': None,
       'CONTRACT': None, 'X = D + "scripts/spec-examples/"': 1, 'A = D + "packages/shared/"': 1}
got = {k: s.count(k) for k in CTL}
print('output controls', {(k[:26] + '…' if len(k) > 26 else k): v for k, v in got.items()})
for k, v in CTL.items():
    if (v is not None and got[k] != v) or got[k] == 0: print('CONTROL DISAGREED', k, got[k], v); sys.exit(1)
for pth, b_ in list(PIN.items()) + list(LANDED.items()):
    if s.count(b_) != 1: print('CONTROL DISAGREED pin', pth, b_, s.count(b_)); sys.exit(1)
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
