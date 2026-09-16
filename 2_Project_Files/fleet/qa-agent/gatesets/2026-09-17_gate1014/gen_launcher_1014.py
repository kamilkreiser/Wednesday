#!/usr/bin/env python3
"""gen_launcher_1014.py — derive launch_qa_secuura_ks1176_1014.sh from launchers/launch_qa_secuura_ks999_1013.sh (the newest ROUND 1 tier-1 launcher of the
same generator family, with the ABSENT arm this PR's added test needs) by ASSERTED substitutions: every anchor must occur exactly as often as stated, or the
generator refuses and writes nothing. Re-points at #1014 616c766a5 / merge-base e0f41a8fa / develop 523f283c6 (#1011's squash, landed 06:10:46 AEST, NOT an
ancestor of the head: compare develop...head = merge_base e0f41a8fa ahead 1 behind 1 files 2); JUDGED 16 files; GUARDED = the api-gateway src tree and config,
the three other level-order copies' packages, the auth connector-JWT mint + internal route, the frontend copy, shared crypto, docs/openapi, eslint, the Dev
lockfile. Then a RESIDUAL GUARD (no #1013 / KS-999 token survives), output controls, heredoc apostrophe parity, no git write verb, no control bytes, bash -n.
Never overwrites an existing output (writes a .pre-* copy first if one exists).
Usage: gen_launcher_1014.py <template launcher> <output launcher>
Exit: 0 written · 1 an anchor/control count disagreed · 2 a residual token survived · 3 bash -n failed"""
import datetime, hashlib, os, re, shutil, subprocess, sys
TPL, OUT = sys.argv[1], sys.argv[2]
s = open(TPL).read()
print('gen_launcher_1014', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'), '| template sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))

def cut(start, end_incl):
    i = s.index(start); j = s.index(end_incl, i) + len(end_incl); return s[i:j]

HEADER_OLD = cut('# launch_qa_secuura_ks999_1013.sh', "# Exit: 0 launched (or guards passed under --check) · 2..23 a guard refused\n")
HEADER_NEW = """# launch_qa_secuura_ks1176_1014.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1014
# (KS-1176, Seat A) @ 616c766a57a51238450c99bbf1d59bb109e3841c — ONE commit on e0f41a8fa (#1013's squash), 2 files, both services/api-gateway:
# src/services/enforcement.ts +8 -1 (meetsVerificationLevel: an UNRECOGNISED user level ranks as 'none' — `userIdx === -1 ? 0 : userIdx`)
# and the NEW src/__tests__/ks1176-connector-key-level-ranks-as-none.test.ts (+363, 13 cells).
# TIER 1: it changes an AUTHORISATION decision on the gateway's document-creation path (POST /api/documents -> enforceDocumentTypeRules)
# and sits under the verifier gate of POST /api/documents/:id/verify (routes/verification.ts:557).
#
# THE SHAPE, as read 06:11-06:20 AEST 2026-09-17 (git ls-remote + the compare API agree): the PR parent = merge-base = e0f41a8fa; develop has
# since moved to 523f283c6 (#1011's squash, KS-871: middleware/audit.ts + three ks871 tests, landed 06:10:46), so develop is NOT an ancestor
# of the head: compare develop...head = merge_base e0f41a8fa, diverged, ahead 1, behind 1, files 2. The compare is asserted as
# merge_base + ahead + files (exit 10); `behind` is deliberately NOT asserted — the develop arm judges every move by CONTENT.
#
# The develop pin is judged by CONTENT, not bare: (a) SIXTEEN files by blob at the CURRENT develop — enforcement.ts (base 533cd309c;
# the PR's own 3e314ba11 -> exit 19 LANDED), the ks1176 test (ABSENT at base; the PR's own 5820520ae -> exit 19 LANDED), the two callers'
# router routes/verification.ts, middleware/auth.ts (the three principal producers), routes/admin.ts (SEED_DOCUMENT_TYPES), services/redis.ts
# (the catalogue), src/index.ts (the mounts), middleware/rateLimitEnforce.ts, middleware/audit.ts (a7be8626f before #1011 OR 052131de0 =
# #1011's squash — both clear), api-gateway package.json / vitest.config.ts / vitest.setup.ts / tsconfig.json, Dev eslint.config.mjs,
# packages/shared crypto/jwks.ts (the gateway's JWT verify) and docs/openapi/secuura-api.yaml — any blob nobody pinned -> exit 18;
# (b) if develop moved past 523f283c6, the compare pinned...develop REFUSES (exit 18) when the delta touches a GUARDED path —
# services/api-gateway/src/ and its config files, packages/shared/src/crypto/ + middleware/ + verification/, services/auth/src/services/jwt.ts
# + routes/internal.ts + middleware/authenticate.ts + types/index.ts, frontend/issuer/src/components/DocumentUpload.tsx, docs/openapi/,
# eslint.config.mjs, the Dev lockfile — or cannot be judged.
# DEV_CONTENT_ALLOWED is empty: dependabot #649/#575 touch api-gateway package.json and the Dev lockfile, seven more touch the lockfile,
# #922 touches docs/openapi/ — if one lands, re-pin deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate's R-6: a wholesale link can write through to the checkout's .vite).
# exit 23: the prompt must carry the exact verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# QA1014_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED refusals can be proven.
# A launch with any QA1014_* override set refuses (exit 16).
#
# Generated by gatesets/2026-09-17_gate1014/gen_launcher_1014.py from launch_qa_secuura_ks999_1013.sh (asserted substitutions + residual
# guard + output controls + bash -n): same guards and exit codes, re-pointed at #1014. Exit codes 2..23 (19 = LANDED).
#
# Usage: launch_qa_secuura_ks1176_1014.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..23 a guard refused
"""

JUDGED_OLD = cut('A = D + "services/auth/"\n', '  D + "docs/openapi/secuura-api.yaml":                              ({"122d3a2f84cf77bf2b7e2dc51489a0d5f823db1f": "base"}, {}),\n}\n')
JUDGED_NEW = '''G = D + "services/api-gateway/"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop
JUDGED = {
  G + "src/services/enforcement.ts":                                   ({"533cd309c56b8167ebe00b620744259b3cc186cc": "base"}, {"3e314ba116f85df0a8a37549272f8078c4c95ccd": "#1014 own"}),
  G + "src/__tests__/ks1176-connector-key-level-ranks-as-none.test.ts": ({"ABSENT": "base"}, {"5820520ae769aa5d118de2c1c5db4d1204d762e6": "#1014 own"}),
  G + "src/routes/verification.ts":                                    ({"04b3d980f657b13717060e9547d92970100b2557": "base"}, {}),
  G + "src/middleware/auth.ts":                                        ({"20311010db0eb8ba097644ce105cf8df966ce456": "base"}, {}),
  G + "src/routes/admin.ts":                                           ({"f47dd6a655702ffbfc402ca920a33c4619d62c4b": "base"}, {}),
  G + "src/services/redis.ts":                                         ({"47659ee9c9f06acf9ac64e09b2dc207113ba92ea": "base"}, {}),
  G + "src/index.ts":                                                  ({"6f38c819e48162e3179aaf557085766f91beecc1": "base"}, {}),
  G + "src/middleware/rateLimitEnforce.ts":                            ({"fc5c5a4d934384745565e730cd12c0a0fcfcaa70": "base"}, {}),
  G + "src/middleware/audit.ts":                                       ({"a7be8626ff1d79a0887fb8d31c44286472157644": "base", "052131de06c3f510e4bcaadc9b6831d0cca617c2": "#1011 squash"}, {}),
  G + "package.json":                                                  ({"841d8c6adcd71e885c01e65c22da9418daff276a": "base"}, {}),
  G + "vitest.config.ts":                                              ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": "base"}, {}),
  G + "vitest.setup.ts":                                               ({"22c1107683b8192df3bfd3e929aa94aff3dc7d45": "base"}, {}),
  G + "tsconfig.json":                                                 ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": "base"}, {}),
  D + "eslint.config.mjs":                                             ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": "base"}, {}),
  D + "packages/shared/src/crypto/jwks.ts":                            ({"a131d32caa3faf0f55ca9af1a4fcd889a1affa17": "base"}, {}),
  D + "docs/openapi/secuura-api.yaml":                                 ({"122d3a2f84cf77bf2b7e2dc51489a0d5f823db1f": "base"}, {}),
}
'''

GUARDED_OLD = cut('GUARDED = [A + "src/",\n', '           D + "package-lock.json"]\n')
GUARDED_NEW = '''GUARDED = [G + "src/",
           G + "package.json",
           G + "vitest.config.ts",
           G + "vitest.setup.ts",
           G + "tsconfig.json",
           D + "packages/shared/src/crypto/",
           D + "packages/shared/src/middleware/",
           D + "packages/shared/src/verification/",
           D + "services/auth/src/services/jwt.ts",
           D + "services/auth/src/routes/internal.ts",
           D + "services/auth/src/middleware/authenticate.ts",
           D + "services/auth/src/types/index.ts",
           D + "frontend/issuer/src/components/DocumentUpload.tsx",
           D + "docs/openapi/",
           D + "eslint.config.mjs",
           D + "package-lock.json"]
'''

REPL = [
  # (label, old, new, expected count)
  ('header', HEADER_OLD, HEADER_NEW, 1),
  ('brief path', 'briefs/2026-09-17_secuura-1013-ks999-tier1.md', 'briefs/2026-09-17_secuura-1014-ks1176-tier1.md', 2),
  ('prompt path', 'briefs/2026-09-17_secuura-1013-ks999-tier1.prompt.txt', 'briefs/2026-09-17_secuura-1014-ks1176-tier1.prompt.txt', 1),
  ('override prefix', 'QA1013_', 'QA1014_', 10),
  ('branch', "BRANCH='refs/heads/feature/ks-999-ornith-getuserbyid-awaits-fromrow'", "BRANCH='refs/heads/feature/ks-1176-connector-key-level-ranks-as-none'", 1),
  ('head sha', '5fbfb66a927ea50a8ad0531f344b58a33f7bd9c2', '616c766a57a51238450c99bbf1d59bb109e3841c', 1),
  ('merge base', "MERGE_BASE='1125607e978d6ad637720c985e43e3d79fecdf88'   # the merge-base of the head with develop = the PR parent 1125607e9 (#1010's squash)",
                 "MERGE_BASE='e0f41a8fafd64fa31524390cfeab320e822f3d15'   # the merge-base of the head with develop = the PR parent e0f41a8fa (#1013's squash)", 1),
  ('develop sha', "DEVELOP_SHA='1125607e978d6ad637720c985e43e3d79fecdf88'   # develop at draft time = the PR parent (git ls-remote 04:44:09, branches API 04:48:55 AEST)",
                  "DEVELOP_SHA='523f283c6cd2550263ec9869dc5ee722be40df4e'   # develop at draft time = #1011's squash on the PR parent, NOT an ancestor of the head (git ls-remote 06:11:56 and 06:22:44, branches API 06:20 AEST)", 1),
  ('head refuse', 'REFUSING: #1013 — $HEAD_SHA', 'REFUSING: #1014 — $HEAD_SHA', 1),
  ('compare comment', '# develop...#1013 = 1125607e9 ahead 1 files 3 (behind 0 at draft time; behind deliberately not asserted).', '# develop...#1014 = e0f41a8fa ahead 1 files 2 (behind 1 at draft time; behind deliberately not asserted).', 1),
  ('compare assert', '''[ "$COMPARE" = "$MERGE_BASE ahead=1 files=3" ] || { echo "REFUSING: #1013 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=3'" >&2; exit 10; }''',
                     '''[ "$COMPARE" = "$MERGE_BASE ahead=1 files=2" ] || { echo "REFUSING: #1014 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=2'" >&2; exit 10; }''', 1),
  ('count comment', 'twenty-one files by blob at the CURRENT develop', 'sixteen files by blob at the CURRENT develop', 1),
  ('judged', JUDGED_OLD, JUDGED_NEW, 1),
  ('landed msg', '#1013 has landed; this brief is stale', '#1014 has landed; this brief is stale', 1),
  ('ok same', '(= the PR parent: the merged tree is content-identical to the head until develop moves; git ls-remote)',
              '(= #1011 squash on the PR parent e0f41a8fa, NOT an ancestor of the head: the gate merges it; drafter merged tree 8589933267963afda8fc352279c4b694ed5bb3de; git ls-remote)', 1),
  ('guarded', GUARDED_OLD, GUARDED_NEW, 1),
  ('allow comment', '''pinned here. EMPTY for this gate: at draft time 04:48 AEST the open PRs touching a guarded path were dependabot bumps of
# services/auth/package.json and the Dev lockfile, which must NOT clear silently — every guarded hit falls through to GUARDED and exit 18.''',
                    '''pinned here. EMPTY for this gate: at draft time 06:20 AEST the open PRs touching a guarded path were dependabot bumps of
# services/api-gateway/package.json and the Dev lockfile, and #922 on docs/openapi, which must NOT clear silently — every guarded hit falls through to exit 18.''', 1),
  ('tail', 'the gate merges the then-current develop onto 5fbfb66a9 in its own clone, rebuilds the shared dist there, runs the auth suite and the route probe on the MERGED tree beside the base and head trees, names the delta and re-derives every count, above all the auth denominator (brief items 1, 6 and 11)',
           'the gate merges the then-current develop onto 616c766a5 in its own clone, rebuilds the shared dist there, runs the api-gateway suite and the principal census on the MERGED tree beside the base and head trees, names the merged-tree OID and re-derives every count, above all the api-gateway denominator (brief items 1, 7, 9)', 1),
  ('ok moved', 'disjoint from the GUARDED list (services/auth/src/ + the auth config files, packages/shared/src/crypto/, docs/openapi/, eslint.config.mjs, the Dev lockfile)',
               'disjoint from the GUARDED list (services/api-gateway/src/ + its config files, packages/shared/src/crypto|middleware|verification/, the auth connector-JWT mint + internal route + authenticate + types, the frontend DocumentUpload copy, docs/openapi/, eslint.config.mjs, the Dev lockfile)', 1),
  ('subject', "'[QA -> Wednesday] TIER 1 GATE #1013 (KS-999) 5fbfb66a9'", "'[QA -> Wednesday] TIER 1 GATE #1014 (KS-1176) 616c766a5'", 1),
  ('check head', 'echo "  head on origin: #1013 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1014 $HEAD_SHA at $BRANCH"', 1),
  ('check compare', 'echo "  compare (GitHub API): develop...#1013 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1014 = $COMPARE"', 1),
]
bad = 0
for label, old, new, want in REPL:
    n = s.count(old)
    if n != want:
        print('ANCHOR COUNT', label, n, '!=', want); bad += 1; continue
    s = s.replace(old, new); print('  ok', label, n)
if bad: print('REFUSING: %d anchors disagreed; nothing written' % bad); sys.exit(1)
RESID = ['1013', 'KS-999', 'ks999', '5fbfb66a9', '1125607e9', 'userRepo', 'fromRow', 'services/auth/package.json', 'auth suite', 'A + ']
PERMITTED = {"e0f41a8fa (#1013's squash)": 2, 'from launch_qa_secuura_ks999_1013.sh': 1}  # the PR parent's provenance and the template-name mention
stripped = s
for k, v in PERMITTED.items():
    assert stripped.count(k) == v, ('PERMITTED count', k, stripped.count(k)); stripped = stripped.replace(k, '')
res = {t: stripped.count(t) for t in RESID if t in stripped}
if res: print('REFUSING: residual tokens', res); sys.exit(2)
CTL = {'#1014': None, '616c766a57a51238450c99bbf1d59bb109e3841c': 2, 'e0f41a8fafd64fa31524390cfeab320e822f3d15': 1, '523f283c6cd2550263ec9869dc5ee722be40df4e': 1, 'QA1014_': 12, '"ABSENT"': None, 'exit 19': None, 'exit 22': None, 'exit 23': None, 'exit 21': None, 'exit 16': None, 'KS-1176': None}
got = {k: s.count(k) for k in CTL}
print('output controls', got)
for k, v in CTL.items():
    if (v is not None and got[k] != v) or got[k] == 0: print('CONTROL DISAGREED', k, got[k], v); sys.exit(1)
for tag in ("<<'PY'\n", "<<'PYJ'\n"):
    i = s.index(tag); j = s.index('\nPY' + ('J' if 'PYJ' in tag else '') + '\n', i); blk = s[i:j]
    print('heredoc', tag.strip(), "apostrophes", blk.count("'") - 2, 'parens (', blk.count('('), ')', blk.count(')'))
    if (blk.count("'") - 2) % 2 or blk.count('(') != blk.count(')'): print('REFUSING: heredoc parity'); sys.exit(1)
if re.search(r'git -C "\$REPO" (fetch|push|checkout|merge|reset|worktree|commit|switch|pull)\b', s): print('REFUSING: git write verb'); sys.exit(1)
if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', s): print('REFUSING: control bytes'); sys.exit(1)
if os.path.exists(OUT):
    pre = OUT + '.pre-' + datetime.datetime.now().strftime('%H%M%S'); shutil.copyfile(OUT, pre); print('existing output copied to', pre)
open(OUT, 'w').write(s); os.chmod(OUT, 0o755)
p = subprocess.run(['bash', '-n', OUT], capture_output=True, text=True)
print('bash -n rc', p.returncode, p.stderr.strip()[:300])
if p.returncode: sys.exit(3)
print('written', OUT, 'sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'lines', s.count('\n'))
