#!/usr/bin/env python3
"""gen_launcher_1015.py — derive launch_qa_secuura_ks1018_1015.sh from launch_qa_secuura_ks999_1013.sh by ASSERTED substitutions
(every anchor counted), a residual guard (no #1013 identifiers survive), output controls, and bash -n. Never runs the launcher."""
import subprocess, os, datetime, hashlib
L = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/'
SRC, DST = L + 'launch_qa_secuura_ks999_1013.sh', L + 'launch_qa_secuura_ks1018_1015.sh'
assert not os.path.exists(DST), 'refusing to overwrite ' + DST
s = open(SRC).read()
def sub(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:90], c, n); s = s.replace(a, b)
# 1. header block, wholesale between its asserted anchors
h0 = s.index('# launch_qa_secuura_ks999_1013.sh'); h1 = s.index('set -u\n')
assert s.count('# launch_qa_secuura_ks999_1013.sh') == 1 and s.count('set -u\n') == 1 and h0 < h1
HEADER = '''# launch_qa_secuura_ks1018_1015.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1015
# (KS-1018, Seat A) @ 77145ce84353534ba381688d5bbd16ff9ff27aef — TWO commits on 523f283c6 (#1011's squash): 6e30fe9f5 (a held local-model
# READY applied byte-equal + seat cells) and 77145ce84 (typing of the test, declared casts only). 2 files, all services/auth:
# src/routes/users.ts +14 -4 (getVerificationRequest / findPendingVerificationRequest / listUserVerificationRequests log `DB <fn> failed`
# {error, code} and rethrow an infrastructure DB error as 503) and the NEW src/__tests__/ks1018-security-correctness-three-verification-
# store-reads.test.ts (+216). TIER 1: auth-service error classification on routes whose base behaviour under a DB fault is a WRITE.
#
# THE SHAPE, as read 06:28-06:41 AEST 2026-09-17 (git ls-remote + the compare API agree): develop = 523f283c6 = the grandparent of the
# head; compare develop...head = merge_base 523f283c6, ahead 2, behind 0, files 2. The compare is asserted as merge_base + ahead + files
# (exit 10); `behind` is deliberately NOT asserted — the develop arm judges every move by CONTENT.
#
# The develop pin is judged by CONTENT, not bare: (a) EIGHTEEN files by blob at the CURRENT develop — users.ts (base 89da72df7; the PR's
# own 8ef9065e2 -> exit 19 LANDED), the ks1018 test (ABSENT at base; the PR's own 6723276d0 or its commit-1 0fb3e7197 -> exit 19 LANDED),
# middleware errorHandler.ts / authenticate.ts, repositories dbErrors.ts / userRepo.ts, db.ts, src/index.ts, auth.openapi.ts, auth
# package.json / vitest.config.ts / vitest.setup.ts / tsconfig.json, Dev eslint.config.mjs, docs/openapi/secuura-api.yaml and the three
# schema sources (migrations/001, docker/init/03, deployment/azure/migrate/init.sql) — any blob nobody pinned -> exit 18; (b) if develop
# moved past 523f283c6, the compare pinned...develop REFUSES (exit 18) when the delta touches a GUARDED path — services/auth/src/, the
# auth config files, packages/shared/src/, docs/openapi/, eslint.config.mjs, the Dev lockfile, migrations/, docker/init/,
# deployment/azure/migrate/ — or cannot be judged. An api-gateway-only move (#1014 KS-1176, A9 KS-1072) proceeds: the gate names it.
# DEV_CONTENT_ALLOWED is empty: dependabot #948/#649/#575 touch services/auth/package.json and the Dev lockfile — if one lands, re-pin deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate's R-6: a wholesale link can write through to the checkout's .vite).
# exit 23: the prompt must carry the exact verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# QA1015_BRIEF / QA1015_PROMPT / QA1015_HEAD / QA1015_CUR_DEV (test overrides, --check only): a launch with any set refuses (exit 16).
#
# Generated from launch_qa_secuura_ks999_1013.sh (the #1013 gate's launcher, verdict GO WITH FINDINGS) by gen_launcher_1015.py
# (asserted substitutions + residual guard + bash -n): same guards and exit codes, re-pointed at #1015. Exit codes 2..23 (19 = LANDED).
#
# Usage: launch_qa_secuura_ks1018_1015.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..23 a guard refused
'''
s = s[:h0] + HEADER + s[h1:]
# 2. variables
sub('QA1013_', 'QA1015_', 10)  # 10 after the header swap (the #1013 header named QA1013_CUR_DEV once)
sub("2026-09-17_secuura-1013-ks999-tier1", "2026-09-17_secuura-1015-ks1018-tier1", 3)
sub("BRANCH='refs/heads/feature/ks-999-ornith-getuserbyid-awaits-fromrow'", "BRANCH='refs/heads/feature/ks-1018-ornith-verification-store-reads-rethrow-infra'")
sub(":-5fbfb66a927ea50a8ad0531f344b58a33f7bd9c2}", ":-77145ce84353534ba381688d5bbd16ff9ff27aef}")
sub("MERGE_BASE='1125607e978d6ad637720c985e43e3d79fecdf88'   # the merge-base of the head with develop = the PR parent 1125607e9 (#1010's squash)",
    "MERGE_BASE='523f283c6cd2550263ec9869dc5ee722be40df4e'   # the merge-base of the head with develop = the parent of commit 1, 523f283c6 (#1011's squash)")
sub("DEVELOP_SHA='1125607e978d6ad637720c985e43e3d79fecdf88'   # develop at draft time = the PR parent (git ls-remote 04:44:09, branches API 04:48:55 AEST)",
    "DEVELOP_SHA='523f283c6cd2550263ec9869dc5ee722be40df4e'   # develop at draft time = the merge-base (git ls-remote 06:28:52 and 06:40:55, branches API 06:31:06 AEST)")
sub('echo "REFUSING: #1013 — $HEAD_SHA', 'echo "REFUSING: #1015 — $HEAD_SHA')
sub("# develop...#1013 = 1125607e9 ahead 1 files 3 (behind 0 at draft time; behind deliberately not asserted).", "# develop...#1015 = 523f283c6 ahead 2 files 2 (behind 0 at draft time; behind deliberately not asserted).")
sub('[ "$COMPARE" = "$MERGE_BASE ahead=1 files=3" ] || { echo "REFUSING: #1013 develop...head reads \'$COMPARE\', brief pins \'$MERGE_BASE ahead=1 files=3\'" >&2; exit 10; }',
    '[ "$COMPARE" = "$MERGE_BASE ahead=2 files=2" ] || { echo "REFUSING: #1015 develop...head reads \'$COMPARE\', brief pins \'$MERGE_BASE ahead=2 files=2\'" >&2; exit 10; }')
sub("# The develop pin, judged by CONTENT (see the header): twenty-one files by blob", "# The develop pin, judged by CONTENT (see the header): eighteen files by blob")
# 3. JUDGED block, wholesale between asserted anchors
j0 = s.index('JUDGED = {\n'); j1 = s.index('}\nstate = []\n')
assert s.count('JUDGED = {\n') == 1 and s.count('}\nstate = []\n') == 1 and j0 < j1
JUDGED = '''JUDGED = {
  A + "src/routes/users.ts":                                                         ({"89da72df7bfab2275550de0868288b7958ea059c": "base"}, {"8ef9065e2fb24308daeb41820a227a4ee1d6ecc9": "#1015 own"}),
  A + "src/__tests__/ks1018-security-correctness-three-verification-store-reads.test.ts": ({"ABSENT": "base"}, {"6723276d016e4d6cf4ead8cb4f511ce5dad5ce53": "#1015 own", "0fb3e7197d5195608ff7decece9a4b766215095e": "#1015 commit-1 own"}),
  A + "src/middleware/errorHandler.ts":                                              ({"1cf66e74cd2bbe1d56f53c6f7ef5200e1835ee3c": "base"}, {}),
  A + "src/repositories/dbErrors.ts":                                                ({"f94faf0d3d3540990f8626fcb65c746737202ac4": "base"}, {}),
  A + "src/repositories/userRepo.ts":                                                ({"9060b308e6d6a82c8a79be7387032d2a18c4ac22": "base"}, {}),
  A + "src/db.ts":                                                                   ({"cf0ee130bb5228214a41e163b3be766b8aebbb72": "base"}, {}),
  A + "src/middleware/authenticate.ts":                                              ({"be7102929b44f7567b0cab4ec1c82f84d04bc58e": "base"}, {}),
  A + "src/index.ts":                                                                ({"edabbf87182311241662b20ac71d7244e923b5a3": "base"}, {}),
  A + "src/auth.openapi.ts":                                                         ({"2c356c3c7877add99f5e1a3c437d04ac8be3dc76": "base"}, {}),
  A + "package.json":                                                                ({"814e88419470b811f26f1593984071bb317608d8": "base"}, {}),
  A + "vitest.config.ts":                                                            ({"8bb96293a0f11a14d90e7c7893f32a053277bbdb": "base"}, {}),
  A + "vitest.setup.ts":                                                             ({"bc18c18755cb00f96e3e228ca34d99fd1266c20f": "base"}, {}),
  A + "tsconfig.json":                                                               ({"a7952bdeaf16e933432bb0e7136f484bb7288a40": "base"}, {}),
  D + "eslint.config.mjs":                                                           ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": "base"}, {}),
  D + "docs/openapi/secuura-api.yaml":                                               ({"122d3a2f84cf77bf2b7e2dc51489a0d5f823db1f": "base"}, {}),
  D + "migrations/001_initial-schema.sql":                                           ({"271c42237e70f0fa9664ccdb5151a276e8b89157": "base"}, {}),
  D + "docker/init/03-service-tables.sql":                                           ({"9a6394ceb9389a17c9e177b3182b7612286f3c54": "base"}, {}),
  D + "deployment/azure/migrate/init.sql":                                           ({"f06d1882fcd23ce3d945c7ea16e5423b57279f0f": "base"}, {}),
'''
s = s[:j0] + JUDGED + s[j1:]
sub('" — #1013 has landed; this brief is stale"', '" — #1015 has landed; this brief is stale"')
sub('" (= the PR parent: the merged tree is content-identical to the head until develop moves; git ls-remote)"', '" (= the merge-base: the merged tree is content-identical to the head until develop moves; git ls-remote)"')
g0 = s.index('GUARDED = [A + "src/",'); g1 = s.index('           D + "package-lock.json"]\n')
assert s.count('GUARDED = [A + "src/",') == 1 and s.count('           D + "package-lock.json"]\n') == 1 and g0 < g1
GUARDED = '''GUARDED = [A + "src/",
           A + "package.json",
           A + "vitest.config.ts",
           A + "vitest.setup.ts",
           A + "tsconfig.json",
           D + "packages/shared/src/",
           D + "docs/openapi/",
           D + "eslint.config.mjs",
           D + "migrations/",
           D + "docker/init/",
           D + "deployment/azure/migrate/",
'''
s = s[:g0] + GUARDED + s[g1:]
sub("# pinned here. EMPTY for this gate: at draft time 04:48 AEST the open PRs touching a guarded path were dependabot bumps of",
    "# pinned here. EMPTY for this gate: at draft time 06:31 AEST the open PRs touching a guarded path were dependabot bumps of")
sub('tail = "the gate merges the then-current develop onto 5fbfb66a9 in its own clone, rebuilds the shared dist there, runs the auth suite and the route probe on the MERGED tree beside the base and head trees, names the delta and re-derives every count, above all the auth denominator (brief items 1, 6 and 11)"',
    'tail = "the gate merges the then-current develop onto 77145ce84 in its own clone, rebuilds the shared dist there, runs the auth suite and the route probe on the MERGED tree beside the base and head trees, names the delta and re-derives every count, above all the auth denominator (brief items 1, 7 and 10)"')
sub('disjoint from the GUARDED list (services/auth/src/ + the auth config files, packages/shared/src/crypto/, docs/openapi/, eslint.config.mjs, the Dev lockfile)',
    'disjoint from the GUARDED list (services/auth/src/ + the auth config files, packages/shared/src/, docs/openapi/, eslint.config.mjs, the Dev lockfile, migrations/, docker/init/, deployment/azure/migrate/)')
sub("grep -qF '[QA -> Wednesday] TIER 1 GATE #1013 (KS-999) 5fbfb66a9' \"$PROMPT_FILE\"", "grep -qF '[QA -> Wednesday] TIER 1 GATE #1015 (KS-1018) 77145ce84' \"$PROMPT_FILE\"")
sub('echo "  head on origin: #1013 $HEAD_SHA at $BRANCH"', 'echo "  head on origin: #1015 $HEAD_SHA at $BRANCH"')
sub('echo "  compare (GitHub API): develop...#1013 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1015 = $COMPARE"')
# 4. residual guard
for bad in ('1013', '5fbfb66a9', '1125607e9', 'KS-999', 'ks999', 'twenty-one', 'crypto/"', '04:4'):
    body = '\n'.join(l for l in s.split('\n') if not l.startswith('# Generated from launch_qa_secuura_ks999_1013.sh'))  # the one intended provenance line
    assert bad not in body, (bad, [l for l in body.split('\n') if bad in l][:3])
# 5. output controls
for need in ("MERGE_BASE='523f283c6cd2550263ec9869dc5ee722be40df4e'", 'ahead=2 files=2', "TIER 1 GATE #1015 (KS-1018) 77145ce84", "grep -q 'ROUND 1'", "[ -t 0 ]", 'exit 21', 'exit 22', 'exit 23', 'exit 20', 'exit 19', 'exit 18', 'exit 16', '"ABSENT"', 'node_modules per ENTRY', 'MAIL YOUR VERDICT'):
    assert need in s, need
open(DST, 'w').write(s); os.chmod(DST, 0o755)
p = subprocess.run(['bash', '-n', DST], capture_output=True, text=True)
j = s[s.index("<<'PYJ'"):s.index('\nPYJ\n')]
print('gen_launcher_1015', datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z'))
print('wrote', DST, 'lines', s.count('\n'), 'sha256', hashlib.sha256(s.encode()).hexdigest()[:16], 'mode', oct(os.stat(DST).st_mode & 0o777))
print('bash -n rc', p.returncode, p.stderr.strip())
print('PYJ heredoc apostrophes', j.count("'"), '| parens', j.count('('), j.count(')'))
