#!/usr/bin/env python3
"""edit_gen_second_form.py — asserted edits turning gen_launcher_1014r2.py (first form, pin eb1051fd3) into the SECOND FORM (pin 7e89318bc, #1016 landed,
verification.ts judged by region content). Every anchor count asserted; nothing written unless all pass."""
import sys
P = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1014r2/gen_launcher_1014r2.py'
s = open(P).read()
E = []
def rep(label, old, new, want=1):
    global s
    c = s.count(old)
    if c != want: E.append((label, c, want)); return
    s = s.replace(old, new); print('  ok', label, c)

# ---- header: the shape and the develop pin
rep('hdr shape', """# THE SHAPE, as read 07:29-07:53 AEST 2026-09-17 (git ls-remote + the compare API agree): merge-base = the PR parent e0f41a8fa (#1013's squash);
# develop has moved to eb1051fd3 (#1015's squash, KS-1018: services/auth routes/users.ts + a ks1018 test, landed 07:12:51) on 523f283c6 (#1011's
# squash), so develop is NOT an ancestor of the head: compare develop...head = merge_base e0f41a8fa, diverged, ahead 2, behind 2, files 3. The""",
"""# THE SHAPE, as read 07:29-08:02 AEST 2026-09-17 (git ls-remote + the compare API agree): merge-base = the PR parent e0f41a8fa (#1013's squash);
# develop moved DURING drafting to 7e89318bc = #1016's squash (KS-1072, merged 07:57:19 AEST: routes/verification.ts @@ -298 makeFetchDocFromAnchorStore
# -> a7a6d4605 + a ks1072 test 4ad1cdcd1; tree e09ede17e = the drafter's own predicted merge-tree) on eb1051fd3 (#1015's squash, services/auth only) on
# 523f283c6 (#1011's), so develop is NOT an ancestor of the head: compare develop...head = merge_base e0f41a8fa, diverged, ahead 2, behind 3, files 3. The""")
rep('hdr judged', """# The develop pin is judged by CONTENT, not bare: (a) EIGHTEEN files by blob at the CURRENT develop — the three #1014 files (enforcement.ts base
# 533cd309c, ks1176 test ABSENT, verification.ts base 04b3d980f; their round-1 OR round-2 blobs -> exit 19 LANDED), verification.ts ALSO clearing at
# #1016's head blob a7a6d4605 and the ks1072 test clearing ABSENT or at #1016's 4ad1cdcd1 (#1016, KS-1072, is open and gating: its hunk is @@ -298 in
# makeFetchDocFromAnchorStore, ~900 lines from #1014's @@ -1213; drafter merge-tree #1014 x #1016 clean), middleware/auth.ts, routes/admin.ts,""",
"""# The develop pin is judged by CONTENT, not bare: (a) EIGHTEEN files by blob at the CURRENT develop — the three #1014 files (enforcement.ts
# 533cd309c, ks1176 test ABSENT, verification.ts a7a6d4605 = #1016's squash; their round-1 OR round-2 blobs, or verification.ts 28fb58343 = the drafter's
# merge of #1014 onto 7e89318bc -> exit 19 LANDED); routes/verification.ts at ANY OTHER blob is judged by CONTENT: it clears only if the #1014 hunk region
# (the connector allow-list block) and the verify-gate region hash to REGION_SHA (70426094413b = base = #1016's squash), so a move elsewhere in the file clears
# and a move INTO either region refuses (exit 18); the ks1072 test at 4ad1cdcd1, middleware/auth.ts, routes/admin.ts,""")
rep('hdr moved', """# eb1051fd3, the compare pinned...develop REFUSES (exit 18) when the delta touches a GUARDED path — services/api-gateway/src/ and its config files,""",
"""# 7e89318bc, the compare pinned...develop REFUSES (exit 18) when the delta touches a GUARDED path — services/api-gateway/src/ and its config files,""")
rep('hdr allow', """# routes/documents.ts, the frontend DocumentUpload copy, docs/openapi/, eslint.config.mjs, the Dev lockfile — unless the file's blob is EXACTLY
# #1016's (DEV_CONTENT_ALLOWED), or the move cannot be judged. The #1016-landed arm is proven only up to the blob loop (fixture N10: the JUDGED loop
# accepts a7a6d4605 / 4ad1cdcd1 and the compare then refuses a diverged develop); no develop containing #1016 existed at draft time.""",
"""# routes/documents.ts, the frontend DocumentUpload copy, docs/openapi/, eslint.config.mjs, the Dev lockfile — unless the hit is verification.ts and the
# region judgement cleared it (or a DEV_CONTENT_ALLOWED blob, EMPTY here), or the move cannot be judged. The first-form launcher (pin eb1051fd3, #1016's
# blobs pre-cleared) passed --check at 08:01:27 against the REAL landed develop 7e89318bc: that arm is proven on live data (check.first-run-*.out).""")
rep('hdr fixture', """# QA1014R2_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED refusals can be proven.""",
"""# QA1014R2_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED refusals can be proven.
# QA1014R2_VERIF_FILE (test fixture, --check only): a local file stands in for develop's routes/verification.ts (content AND git blob) so the region
# judgement's clear and refuse arms can be proven without a real develop commit.""")
rep('hdr exit16', "# A launch with any QA1014R2_* override set refuses (exit 16).", "# A launch with any QA1014R2_* override or fixture set refuses (exit 16).")
# ---- body pins
rep('develop sha', """("develop sha", "DEVELOP_SHA='523f283c6cd2550263ec9869dc5ee722be40df4e'""".replace('("develop sha", ', "('develop sha', "), """('develop sha', "DEVELOP_SHA='523f283c6cd2550263ec9869dc5ee722be40df4e'""", 1)
rep('develop sha new', """"DEVELOP_SHA='eb1051fd39fe3edab4e0b1d1967515b758d4ba3f'   # develop at draft time = #1015's squash on #1011's, NOT an ancestor of the head (git ls-remote 07:29:17, 07:34:32 and 07:51:52, branches API 07:33 AEST)\"""",
""""DEVELOP_SHA='7e89318bcedbc9a35757d4298ace54a6a23020bd'   # develop at draft close = #1016's squash on #1015's eb1051fd3, NOT an ancestor of the head (git ls-remote 08:02:10, branches API 08:02:14 AEST; re-pinned after #1016 landed 07:57:19)\"""")
rep('compare comment', "'# develop...#1014 = e0f41a8fa ahead 2 files 3 (behind 2 at draft time; behind deliberately not asserted).'", "'# develop...#1014 = e0f41a8fa ahead 2 files 3 (behind 3 at draft close; behind deliberately not asserted).'")
# ---- JUDGED
rep('judged verif', """  G + "src/routes/verification.ts":                                    ({"04b3d980f657b13717060e9547d92970100b2557": "base", "a7a6d46057a18b3460e7d08bbec5df12ab763a81": "#1016 head a226d94fe KS-1072, judged by content"}, {"6bd095f621183b2aaf7a3611222815b5bf1026a3": "#1014 round-2 own"}),
  G + "src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts": ({"ABSENT": "base", "4ad1cdcd1e45044efdbb0b8e4e6eaf358453d780": "#1016 head a226d94fe KS-1072"}, {}),""",
"""  G + "src/routes/verification.ts":                                    ({"a7a6d46057a18b3460e7d08bbec5df12ab763a81": "develop = #1016 squash 7e89318bc"}, {"6bd095f621183b2aaf7a3611222815b5bf1026a3": "#1014 round-2 own", "28fb5834308a502f5f7b806e3b49a77627601eff": "#1014 merged onto 7e89318bc, drafter merge"}),
  G + "src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts": ({"4ad1cdcd1e45044efdbb0b8e4e6eaf358453d780": "#1016 squash"}, {}),""")
# ---- ALLOW
rep('allow', """ALLOW_NEW = '''# pinned here. For this gate: the two files of #1016 KS-1072 at its head a226d94fe, judged by content at draft time 07:5x AEST: verification.ts
# hunk -298 in makeFetchDocFromAnchorStore only, 0 lines in POST /api/documents or the verify gate, merge-tree with #1014 clean in the drafter clone.
# Any other version of either file, and every other guarded hit, falls through to exit 18 — dependabot #649 / #575, the lockfile PRs and #922 included.
DEV_CONTENT_ALLOWED = {
  G + "src/routes/verification.ts": "a7a6d46057a18b3460e7d08bbec5df12ab763a81",
  G + "src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts": "4ad1cdcd1e45044efdbb0b8e4e6eaf358453d780",
}
'''""",
"""ALLOW_NEW = '''# pinned here. EMPTY for this gate: routes/verification.ts is judged by its REGION content above, not by a blob here; every other guarded hit
# falls through to exit 18 — dependabot #649 / #575, the lockfile PRs and #922 docs/openapi included. Re-pin deliberately.
DEV_CONTENT_ALLOWED = {
}
'''""")
# ---- region judgement code in the PYJ block
rep('repl list head', "REPL = [\n", """REGION_SHA = '70426094413b2ca8506d656f252061f61040b1eef5c93eb99578c8318b9f0f1c'
PYJ_IMPORT_OLD = 'import json, os, sys, urllib.request, urllib.error\\n'
PYJ_IMPORT_NEW = 'import hashlib, json, os, sys, urllib.request, urllib.error\\n'
LOOP_OLD = '''state = []
for f, (ok, landed) in JUDGED.items():
    try:
        blob = get("/contents/" + f + "?ref=" + cur)["sha"]
'''
LOOP_NEW = '''# REGION judgement for routes/verification.ts (brief items 1-3 stand on these two regions): the connector allow-list block and the verify gate.
REGIONS = [["// --- Connector scope and document type enforcement ---", "// --- Workflow gate: check if approval workflow is required ---"],
           ["// Enforce verifierVerificationLevel from the document", "requiredLevel: verifierLevel,"]]
REGION_SHA = "''' + REGION_SHA + '''"
VERIF = G + "src/routes/verification.ts"
FIXTURE = os.environ.get("QA1014R2_VERIF_FILE", "")
def raw(path, ref):
    return urllib.request.urlopen(urllib.request.Request(api + "/contents/" + path + "?ref=" + ref, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github.raw"}), timeout=60).read().decode("utf-8")
def region_sha(text):
    parts = []
    for a, b in REGIONS:
        if text.count(a) != 1:
            return "anchor-count-" + str(text.count(a))
        i = text.index(a); j = text.find(b, i)
        if j < 0:
            return "end-anchor-missing"
        parts.append(text[i:j + len(b)])
    return hashlib.sha256("\\\\n----\\\\n".join(parts).encode()).hexdigest()
content_cleared = set()
state = []
for f, (ok, landed) in JUDGED.items():
    try:
        if f == VERIF and FIXTURE:
            data = open(FIXTURE, "rb").read()
            blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\\\\0" + data).hexdigest()
        else:
            blob = get("/contents/" + f + "?ref=" + cur)["sha"]
'''
NOTOK_OLD = '''    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
'''
NOTOK_NEW = '''    if blob not in ok and f == VERIF:
        try:
            text = open(FIXTURE).read() if FIXTURE else raw(f, cur)
        except Exception as e:
            print("UNJUDGEABLE develop verification.ts content unreadable: " + type(e).__name__); sys.exit(0)
        rs = region_sha(text)
        if rs != REGION_SHA:
            print("GUARDED develop " + short + " blob " + blob[:9] + " — the #1014 hunk region or the verify gate changed: region " + rs[:16] + " vs pinned " + REGION_SHA[:16]); sys.exit(0)
        content_cleared.add(f)
        state.append(f.split("/")[-1] + " " + blob[:9] + " = moved OUTSIDE the #1014 hunk region and the verify gate, judged by content: region " + rs[:12])
        continue
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
'''
CLEARED_OLD = 'cleared = sorted(h for h in hits if h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") == DEV_CONTENT_ALLOWED[h])\\n'
CLEARED_NEW = 'cleared = sorted(h for h in hits if (h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") == DEV_CONTENT_ALLOWED[h]) or h in content_cleared)\\n'

REPL = [
""")
rep('repl entries', "  ('judged', JUDGED_OLD, JUDGED_NEW, 1),\n",
"""  ('judged', JUDGED_OLD, JUDGED_NEW, 1),
  ('pyj import', PYJ_IMPORT_OLD, PYJ_IMPORT_NEW, 1),
  ('region loop', LOOP_OLD, LOOP_NEW, 1),
  ('region not-ok', NOTOK_OLD, NOTOK_NEW, 1),
  ('region cleared', CLEARED_OLD, CLEARED_NEW, 1),
""")
rep('ok same', """'(= #1015 squash on #1011 squash, NOT an ancestor of the head: the gate merges it; drafter merged tree 1372b3b66b6749e6fd9458db37b672ca753e28d7; #1016 still open; git ls-remote)'""",
"""'(= #1016 squash on #1015 squash, NOT an ancestor of the head: the gate merges it; drafter merged tree 5748a1d68318ed2e310a360fb79e7a1ebc63c785; git ls-remote)'""")
rep('ok moved', "or cleared at the exact #1016 head blobs'", "or verification.ts cleared by its region judgement'")
rep('exit16 override', """  ('check compare', 'echo "  compare (GitHub API): develop...#1014 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1014 ROUND 2 = $COMPARE"', 1),
]""",
"""  ('check compare', 'echo "  compare (GitHub API): develop...#1014 = $COMPARE"', 'echo "  compare (GitHub API): develop...#1014 ROUND 2 = $COMPARE"', 1),
  ('exit16 fixture', '[ -z "${QA1014R2_BRIEF:-}${QA1014R2_PROMPT:-}${QA1014R2_HEAD:-}${QA1014R2_CUR_DEV:-}" ]', '[ -z "${QA1014R2_BRIEF:-}${QA1014R2_PROMPT:-}${QA1014R2_HEAD:-}${QA1014R2_CUR_DEV:-}${QA1014R2_VERIF_FILE:-}" ]', 1),
  ('check fixture echo', '  [ -n "${QA1014R2_CUR_DEV:-}" ] && echo "  (develop read from the QA1014R2_CUR_DEV test override, not ls-remote)"\\n',
   '  [ -n "${QA1014R2_CUR_DEV:-}" ] && echo "  (develop read from the QA1014R2_CUR_DEV test override, not ls-remote)"\\n  [ -n "${QA1014R2_VERIF_FILE:-}" ] && echo "  (develop verification.ts read from the QA1014R2_VERIF_FILE fixture, not the contents API)"\\n', 1),
]""")
rep('resid', "RESID = ['QA1014_', 'ROUND 1', 'sixteen', '8589933267', '523f283c6cd2550263ec9869dc5ee722be40df4e', 'ahead=1 files=2', '616c766a57a51238450c99bbf1d59bb109e3841c', 'principal census', 'tier1-r1/', 'launch_qa_secuura_ks1176_1014.sh']",
"RESID = ['QA1014_', 'ROUND 1', 'sixteen', '8589933267', '523f283c6cd2550263ec9869dc5ee722be40df4e', 'eb1051fd39fe3edab4e0b1d1967515b758d4ba3f', '1372b3b66b67', 'ahead=1 files=2', '616c766a57a51238450c99bbf1d59bb109e3841c', 'principal census', 'tier1-r1/', 'launch_qa_secuura_ks1176_1014.sh', 'still open', 'open and gating', 'a226d94fe']")
rep('ctl', "'eb1051fd39fe3edab4e0b1d1967515b758d4ba3f': 1,", "'7e89318bcedbc9a35757d4298ace54a6a23020bd': 1, REGION_SHA: 1, 'QA1014R2_VERIF_FILE': None, 'content_cleared': 3, '28fb5834308a502f5f7b806e3b49a77627601eff': 1,")
rep('ctl blobs', "'a7a6d46057a18b3460e7d08bbec5df12ab763a81': 2, '4ad1cdcd1e45044efdbb0b8e4e6eaf358453d780': 2,", "'a7a6d46057a18b3460e7d08bbec5df12ab763a81': 1, '4ad1cdcd1e45044efdbb0b8e4e6eaf358453d780': 1,")
rep('ctl qa', "'QA1014R2_': 12,", "'QA1014R2_': None,")
if E:
    print('REFUSING: anchors disagreed', E); sys.exit(1)
open(P, 'w').write(s); print('second form written', P)
