#!/usr/bin/env python3
"""gen_launcher_1012.py — derive launch_qa_secuura_ks745_1012.sh from tonight's #1010 TIER 1 launcher (launchers/launch_qa_secuura_ks1183_1010.sh — same
guard family: head on origin exit 6, compare exit 10/13, develop judged BY CONTENT exit 18/19, tier 7, round 15, thinking 8, brief path 9, head SHA 20, mail 12,
hook 11, memory 14, credential 17, per-ENTRY farm 22, exact subject 23, TTY 21, override-on-launch 16) by ASSERTED block replacements: every anchor must occur
exactly once, or the generator refuses and writes nothing. Changes: re-pointed at #1012; the JUDGED file set and GUARDED paths for the audit export +
the security list route + the shared authenticate/tenancy policy + the spec; a develop-ABSENT state (the new test file does not exist on develop — a
404 from the contents API is the expected base state, not unjudgeable); #1011's middleware/audit.ts blob accepted as a known develop move (a sibling lane,
content-adjacent: its EXCLUDED_PREFIXES list names /api/admin/audit). Then a RESIDUAL GUARD (no #1010-only token survives), output controls, no git
write verbs, bash -n. Never overwrites without a .pre-* copy.
Usage: gen_launcher_1012.py <template launcher> <output launcher>
Exit: 0 written · 1 an anchor count disagreed · 2 a residual token survived · 3 bash -n failed"""
import datetime, os, shutil, subprocess, sys
src_path, out_path = sys.argv[1], sys.argv[2]
s = open(src_path, encoding='utf-8').read()
def refuse(msg, code): print('REFUSING: ' + msg, file=sys.stderr); sys.exit(code)
def block(text, start, end, new, include_end=True):
    if text.count(start) != 1: refuse('start anchor count %d: %r' % (text.count(start), start[:60]), 1)
    i = text.index(start); j = text.find(end, i)
    if j < 0 or text.count(end, i) < 1: refuse('end anchor missing after start: %r' % end[:60], 1)
    j = j + len(end) if include_end else j
    return text[:i] + new + text[j:]
def sub(text, old, new, n=1):
    if text.count(old) != n: refuse('anchor count %d != %d: %r' % (text.count(old), n, old[:80]), 1)
    return text.replace(old, new)

HEADER = '''#!/bin/bash
# launch_qa_secuura_ks745_1012.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1012
# (KS-745, Seat A successor) @ e225a49480e16bb77251a5d7cbd16afdf2929550 — ONE commit on d067725ff (develop = #1009's squash), 2 files, both
# services/api-gateway: routes/audit-export.ts +4 -2 (the admin audit export fetches the security list route /api/audit, was /api/audit/logs
# which matched /api/audit/:id and 404'd, and reads data.data.logs) and the new ks745 test (+69). TIER 1 (Wednesday's ruling): before the PR
# the export 404'd and returned nothing; after it the export returns security audit-log entries — a NEW data path out of the audit store,
# and who can read which tenant's entries through it is the lead question.
#
# THE SHAPE, as read 04:13-04:21 AEST 2026-09-17 (git ls-remote + the PR and compare APIs agree): develop d067725ff IS the PR parent and the
# merge-base; compare develop...head = merge_base d067725ff, ahead 1, behind 0, files 2. The compare is asserted as merge_base + ahead + files
# (exit 10); `behind` is deliberately NOT asserted — the develop arm judges every move by CONTENT, and the gate builds the merged tree itself.
#
# The develop pin is judged by CONTENT, not bare: (a) FIFTEEN files by blob at the CURRENT develop — audit-export.ts (base a301f5e22; the PR's
# own d87c04979 -> exit 19 LANDED), the ks745 test (ABSENT on develop; the PR's own fb6a33957 -> exit 19 LANDED), api-gateway src/index.ts (the
# :801 mount), middleware/auth.ts, middleware/audit.ts (base a7be8626f OR #1011's f5a83ba2c — a known sibling lane), routes/admin.ts,
# package.json, vitest.config.ts, vitest.setup.ts, tsconfig.json, security src/index.ts (the list route :732-777), shared middleware/index.ts
# (authenticate), shared security/keyRevokePolicy.ts (isPlatformRole), docs/openapi/secuura-api.yaml (the export IS in the spec), Dev
# eslint.config.mjs — any blob nobody pinned -> exit 18; (b) if develop moved past d067725ff, the compare pinned...develop REFUSES (exit 18)
# when the delta touches a GUARDED path — those files, services/security/src/, packages/shared/src/middleware/, packages/shared/src/security/,
# docs/openapi/, the Dev lockfile — or cannot be judged; anything else proceeds and the gate re-derives the merged denominator.
# DEV_CONTENT_ALLOWED pins #1011's audit.ts blob only; dependabot #649/#575 touch api-gateway + security package.json and the lockfile — if one
# lands, re-pin deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate's R-6: a wholesale link can write through to the checkout's .vite).
# exit 23: the prompt must carry the exact verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# QA1012_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED refusals can be proven.
#
# Adapted from launch_qa_secuura_ks1183_1010.sh by gen_launcher_1012.py (asserted block replacements + residual guard + output
# controls + bash -n): same guards and exit codes, re-pointed at #1012. Exit codes 2..23 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks745_1012.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..23 a guard refused
'''
s = block(s, '#!/bin/bash\n', 'set -u\n', HEADER + 'set -u\n')

CONST = '''QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA1012_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1012-ks745-tier1.md}"
PROMPT_FILE="${QA1012_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1012-ks745-tier1.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-745-ornith-audit-export-list-route'
HEAD_SHA="${QA1012_HEAD:-e225a49480e16bb77251a5d7cbd16afdf2929550}"
MERGE_BASE='d067725ff1c7f036dbf0f726b9bf12f4daefebe7'   # the merge-base of the head with develop = the PR parent d067725ff (#1009's squash) = develop at draft time (behind 0)
DEVELOP_SHA='d067725ff1c7f036dbf0f726b9bf12f4daefebe7'   # develop at draft time (git ls-remote 04:13:27, branches API 04:19:32 AEST)
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1012-ks745-tier1.md"
'''
s = block(s, "QA_DIR='", 'REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1010-ks1183-tier1.md"\n', CONST)

s = sub(s, '  echo "REFUSING: #1010 — $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2',
           '  echo "REFUSING: #1012 — $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2')
s = sub(s, '# develop...#1010 = f7c2f4acb ahead 1 files 2 (behind 1 at draft time; behind deliberately not asserted).',
           '# develop...#1012 = d067725ff ahead 1 files 2 (behind 0 at draft time; behind deliberately not asserted).')
s = sub(s, '''[ "$COMPARE" = "$MERGE_BASE ahead=1 files=2" ] || { echo "REFUSING: #1010 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=2'" >&2; exit 10; }''',
           '''[ "$COMPARE" = "$MERGE_BASE ahead=1 files=2" ] || { echo "REFUSING: #1012 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=2'" >&2; exit 10; }''')
s = sub(s, 'CUR_DEV="${QA1010_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"', 'CUR_DEV="${QA1012_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"')

JUDGED = '''# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the file does not exist at that develop (contents API 404)
JUDGED = {
  D + "services/api-gateway/src/routes/audit-export.ts":            ({"a301f5e22ceeb4adb37bd8b924eaade09e07394f": "base"}, {"d87c04979e2bbfb28505d4ba7c63d252f0fbe302": "#1012 own"}),
  D + "services/api-gateway/src/__tests__/ks745-audit-export-calls-the-list-route.test.ts": ({"ABSENT": "base, absent"}, {"fb6a33957d07256bef1d45d1a66d6f333233ba50": "#1012 own"}),
  D + "services/api-gateway/src/index.ts":                          ({"6f38c819e48162e3179aaf557085766f91beecc1": "base"}, {}),
  D + "services/api-gateway/src/middleware/auth.ts":                ({"20311010db0eb8ba097644ce105cf8df966ce456": "base"}, {}),
  D + "services/api-gateway/src/middleware/audit.ts":               ({"a7be8626ff1d79a0887fb8d31c44286472157644": "base", "f5a83ba2cde6c64eb5540976c55867d637e8f6eb": "#1011 KS-871 landed"}, {}),
  D + "services/api-gateway/src/routes/admin.ts":                   ({"f47dd6a655702ffbfc402ca920a33c4619d62c4b": "base"}, {}),
  D + "services/api-gateway/package.json":                          ({"841d8c6adcd71e885c01e65c22da9418daff276a": "base"}, {}),
  D + "services/api-gateway/vitest.config.ts":                      ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": "base"}, {}),
  D + "services/api-gateway/vitest.setup.ts":                       ({"22c1107683b8192df3bfd3e929aa94aff3dc7d45": "base"}, {}),
  D + "services/api-gateway/tsconfig.json":                         ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": "base"}, {}),
  D + "services/security/src/index.ts":                             ({"0903ce4380f219765ac63f5f9399d1bf0b4f230a": "base"}, {}),
  D + "packages/shared/src/middleware/index.ts":                    ({"3a67987a7be4a4c02f8326bf8a840a2c2b4efbf3": "base"}, {}),
  D + "packages/shared/src/security/keyRevokePolicy.ts":            ({"86b55405290f6337def1221c869fab68bdf7c2b2": "base"}, {}),
  D + "docs/openapi/secuura-api.yaml":                              ({"122d3a2f84cf77bf2b7e2dc51489a0d5f823db1f": "base"}, {}),
  D + "eslint.config.mjs":                                          ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": "base"}, {}),
}
'''
s = block(s, '# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})\n', '\n}\n', JUDGED)

s = sub(s, '''    try:
        blob = get("/contents/" + f + "?ref=" + cur)["sha"]
    except Exception as e:
        print("UNJUDGEABLE develop blob unreadable for " + f.split("/")[-1] + ": " + type(e).__name__); sys.exit(0)''',
'''    try:
        blob = get("/contents/" + f + "?ref=" + cur)["sha"]
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print("UNJUDGEABLE develop blob unreadable for " + f.split("/")[-1] + ": HTTP " + str(e.code)); sys.exit(0)
        blob = "ABSENT"
    except Exception as e:
        print("UNJUDGEABLE develop blob unreadable for " + f.split("/")[-1] + ": " + type(e).__name__); sys.exit(0)''')
s = sub(s, 'import json, os, sys, urllib.request\n', 'import json, os, sys, urllib.request, urllib.error\n')
s = sub(s, '''        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — #1010 has landed; this brief is stale"); sys.exit(0)''',
           '''        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — #1012 has landed; this brief is stale"); sys.exit(0)''')
s = sub(s, '''    print("OK " + state + " | origin develop still " + pinned + " (NOT an ancestor of the head: the gate builds the merged tree head + " + pinned[:9] + " in its own clone; git ls-remote)"); sys.exit(0)''',
           '''    print("OK " + state + " | origin develop still " + pinned + " (= the PR parent: merged tree = head while develop is unmoved; git ls-remote)"); sys.exit(0)''')

GUARDED = '''GUARDED = [D + "services/api-gateway/src/routes/audit-export.ts",
           D + "services/api-gateway/src/__tests__/ks745-audit-export-calls-the-list-route.test.ts",
           D + "services/api-gateway/src/index.ts",
           D + "services/api-gateway/src/middleware/auth.ts",
           D + "services/api-gateway/src/middleware/audit.ts",
           D + "services/api-gateway/src/routes/admin.ts",
           D + "services/api-gateway/package.json",
           D + "services/api-gateway/vitest.config.ts",
           D + "services/api-gateway/vitest.setup.ts",
           D + "services/api-gateway/tsconfig.json",
           D + "services/security/src/",
           D + "services/security/package.json",
           D + "packages/shared/src/middleware/",
           D + "packages/shared/src/security/",
           D + "docs/openapi/",
           D + "eslint.config.mjs",
           D + "package-lock.json"]
# SUFFIX-GUARDED: none for this gate (no proxy config is in the question; the export is gateway-answered).
GUARDED_SUFFIX = []'''
s = block(s, 'GUARDED = [D + "services/api-gateway/src/routes/verification.ts",', 'GUARDED_SUFFIX = ["/nginx.conf"]', GUARDED)

ALLOWED = '''# CONTENT-JUDGED allowlist: a hit under a GUARDED path clears ONLY if the per-file blob sha in the compare is EXACTLY one
# pinned here. ONE entry for this gate: #1011 (KS-871, 0a1f8900c, a sibling tier-1 lane) changes middleware/audit.ts to exactly
# f5a83ba2c — if it lands first the gate proceeds and must re-derive the merged tree with it (its EXCLUDED_PREFIXES names /api/admin/audit).
# Dependabot bumps of api-gateway or security package.json and the Dev lockfile must NOT clear silently — every other guarded hit is exit 18.
DEV_CONTENT_ALLOWED = {
  D + "services/api-gateway/src/middleware/audit.ts": "f5a83ba2cde6c64eb5540976c55867d637e8f6eb",
}'''
s = block(s, '# CONTENT-JUDGED allowlist:', 'DEV_CONTENT_ALLOWED = {\n}', ALLOWED)

s = sub(s, '''tail = "the gate merges the then-current develop onto c3213b04e in its own clone, rebuilds the shared dist there, runs the api-gateway suite and the outcome probe on the MERGED tree beside the base and head trees, names the delta and re-derives every count, above all the api-gateway denominator (brief items 1, 8 and 9)"''',
           '''tail = "the gate merges the then-current develop onto e225a4948 in its own clone, rebuilds the shared dist there, runs the api-gateway suite, the tenant probe and the real-app reach rows on the MERGED tree beside the base and head trees, names the delta and re-derives every count (brief items 1, 7, 8 and 10)"''')
old_ok = s[s.index('print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — disjoint from the GUARDED list'):]
old_ok = old_ok[:old_ok.index('\n')]
s = sub(s, old_ok, '''print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — disjoint from the GUARDED list (api-gateway audit-export.ts + the ks745 test + index.ts + auth.ts + audit.ts + admin.ts + package.json + vitest config/setup + tsconfig, services/security/src/ + package.json, packages/shared/src/middleware/ + security/, docs/openapi/, eslint.config.mjs, the Dev lockfile); %s" % (pinned, cur, c["ahead_by"], len(files), tail)); sys.exit(0)''')
s = sub(s, "grep -qF '[QA -> Wednesday] TIER 1 GATE #1010 (KS-1183) c3213b04e' \"$PROMPT_FILE\"", "grep -qF '[QA -> Wednesday] TIER 1 GATE #1012 (KS-745) e225a4948' \"$PROMPT_FILE\"")
s = sub(s, '  echo "  head on origin: #1010 $HEAD_SHA at $BRANCH"', '  echo "  head on origin: #1012 $HEAD_SHA at $BRANCH"')
s = sub(s, '  echo "  compare (GitHub API): develop...#1010 = $COMPARE"', '  echo "  compare (GitHub API): develop...#1012 = $COMPARE"')
s = sub(s, '  [ -n "${QA1010_CUR_DEV:-}" ] && echo "  (develop read from the QA1010_CUR_DEV test override, not ls-remote)"', '  [ -n "${QA1012_CUR_DEV:-}" ] && echo "  (develop read from the QA1012_CUR_DEV test override, not ls-remote)"')
s = sub(s, '[ -z "${QA1010_BRIEF:-}${QA1010_PROMPT:-}${QA1010_HEAD:-}${QA1010_CUR_DEV:-}" ]', '[ -z "${QA1012_BRIEF:-}${QA1012_PROMPT:-}${QA1012_HEAD:-}${QA1012_CUR_DEV:-}" ]')

# RESIDUAL GUARD: after stripping the one permitted template-name mention in the header
probe = s.replace('launch_qa_secuura_ks1183_1010.sh', '')
for tok in ('#1010', 'QA1010', '1010.sh', '-1010-', 'KS-1183', 'ks1183',  # bare '1010' is inside the auth.ts blob 20311010d — measured, first run
             'c3213b04e', 'f7c2f4acb', 'verification.ts', 'originate', 'nginx.conf', 'ks1087', 'KS-1087'):
    if tok in probe: refuse('residual token %r survived (%d): %s' % (tok, probe.count(tok), [l[:160] for l in probe.splitlines() if tok in l]), 2)
for want, n in (('e225a49480e16bb77251a5d7cbd16afdf2929550', 2), ('exit 21', 2), ('exit 22', 2), ('exit 23', 2), ('QA1012_CUR_DEV', 4)):
    got = s.count(want)
    if got < n: refuse('output control %r count %d < %d' % (want, got, n), 1)
for verb in (' push', ' commit ', ' checkout ', ' reset ', ' worktree add', ' merge '):
    for line in s.splitlines():
        if line.lstrip().startswith('#'): continue
        if ('git ' in line and verb in line): refuse('git write verb in a code line: ' + line[:100], 1)
if os.path.exists(out_path):
    shutil.copyfile(out_path, out_path + '.pre-' + datetime.datetime.now().strftime('%H%M%S'))
open(out_path, 'w', encoding='utf-8').write(s); os.chmod(out_path, 0o755)
p = subprocess.run(['/bin/bash', '-n', out_path], capture_output=True, text=True)
print('written', out_path, 'lines', s.count('\n'), 'bash -n rc', p.returncode, p.stderr.strip()[:300])
sys.exit(3 if p.returncode else 0)
