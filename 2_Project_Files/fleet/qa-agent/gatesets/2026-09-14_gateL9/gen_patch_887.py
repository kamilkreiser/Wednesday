#!/usr/bin/env python3
"""gen_patch_887.py — extend gen_launcher_L9.py from three heads to FOUR (#887 KS-961 @ 3aee3deed) by asserted replacements
(each anchor must occur exactly as often as stated); nothing is written on a miss. Run once; idempotence is refused."""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
assert 'HEAD887' not in s, 'already patched'
def rep(old, new, n=1):
    global s
    c = s.count(old); assert c == n, (old[:90], c, n); s = s.replace(old, new)
rep("launch_qa_secuura_L9_940_941_942.sh", "launch_qa_secuura_L9_940_941_942_887.sh", 3)
rep("2026-09-14_secuura-L9-940-941-942-ks1075-1077-1078-tier2", "2026-09-14_secuura-L9-940-941-942-887-ks1075-1077-1078-961-tier2", 3)
rep("a loop over THREE heads", "a loop over FOUR heads")
rep("the merge-base guard -> the three GitHub compares", "the merge-base guard -> the four GitHub compares")
rep("# ci-workflows lane (Wednesday's ruling: one test pass proves the three; the verdict is PER PR; the MERGE of every\n# `.github/workflows` PR is Kam's — `kam-merges`):",
    "# ci-workflows lane PLUS its fourth PR #887 (Wednesday's rulings: one test pass proves the three; #887 added as a fourth\n# section 08:3x AEST; the verdict is PER PR; the MERGE of every `.github/workflows` PR is Kam's — `kam-merges`):")
rep("""#        103720115281 at M18: the same two, the same 27/2) — ATTRIBUTED to KS-1148, never graded against #942.
#""", """#        103720115281 at M18: the same two, the same 27/2) — ATTRIBUTED to KS-1148, never graded against #942.
#   #887 (KS-961) @ 3aee3deed — pr-platform-suites.yml: the `workspace-suites` advisory job (+97, continue-on-error: true,
#        the hunk Peter reviewed at cb7a3e3be — his COMMENTED review 5153400898 "the change I asked for is in… One re-run
#        before I approve"; his approval is HIS act; `mergeable: blocked` = his standing CHANGES_REQUESTED at bb0502c80 — the
#        gate states it, never chases him) + DEV-PROCESS.md (+50 -2 vs develop). This round = cb7a3e3be + de376a9f1 (a
#        clean --no-ff merge of develop M18; the workflow blob moves 8607f9bf2 -> fd5e8343c by develop's OWN +15 -2 hunk at
#        :314 on another job — no seat line) + 3aee3deed (ONE doc-only commit, DEV-PROCESS.md +15 -11 inside the PR's own
#        section: a second dated baseline column + the "cannot run today" sentence dated). develop is an ANCESTOR (0 behind /
#        5 ahead); the delta vs develop is exactly 2 files +147 -2. Peter's ONE re-run posted on the PR facts-only (comment
#        5656613944): at cb7a3e3be 40 s · 26 · 6 · exit 1 · 2 failing (anchoring 1/172, originate 2/515) — LANDS ON 2; at the
#        merged tree 58 s · 26 · 6 · exit 1 · 1 failing (anchoring 1/208; originate 0/588); OpenSSL 3.6.3. The push
#        preflight PASSED 11/14 (3/4/8 SKIP by HOLD; leg 14 29/29). Live: `pr` run 34786655660 / job `Workspace unit suites
#        (advisory, non-blocking)` 103803259738 — the job's FIRST execution anywhere: counts 26 / 6, npm ci green, step 6
#        Build FAILS on demo-overlay + outlook-addin (`Cannot find module @rollup/rollup-linux-x64-gnu` — the root lockfile
#        carries only rollup-darwin-arm64; npm/cli#4828), step 7 SKIPPED — a lockfile/platform defect, NOT #887's (advisory;
#        blocks nothing; Wednesday's filing call).
#""")
rep("The three heads by ls-remote (exit 6 for any that moved).", "The four heads by ls-remote (exit 6 for any that moved).")
rep("# The three GitHub compares (exit 10): develop...#940 and develop...#941 must read merge_base a1e49d151, ahead 1, files 1 / 2;\n# develop...#942 must read merge_base = the pinned develop, ahead 2, files 3. The three LIVE RUNS the brief names are the",
    "# The four GitHub compares (exit 10): develop...#940 and develop...#941 must read merge_base a1e49d151, ahead 1, files 1 / 2;\n# develop...#942 must read merge_base = the pinned develop, ahead 2, files 3; develop...#887 the pinned develop, ahead 5,\n# files 2. The four LIVE RUNS the brief names are the")
rep("The develop pin is judged by CONTENT on the lane's two workflow files (GitHub contents", "The develop pin is judged by CONTENT on the lane's three workflow files (GitHub contents")
rep("# exit 18. Any OTHER file of a develop move under the GUARDED prefixes — .github/workflows/, Blockchain/Dev/.security/,\n# Blockchain/Dev/scripts/audit/, scripts/run-shell-suites.sh, systemTest/__tests__/manifest_quarantine.test.sh,\n# systemTest/__tests__/ (a new or moved shell suite changes the 27/2 of 29 ratio) — -> exit 18; otherwise the launcher",
    "# exit 18. pr-platform-suites.yml blob a509ad793 (M18) -> green; fd5e8343c (#887 landed) -> exit 19; other -> exit 18. Any\n# OTHER file of a develop move under the GUARDED prefixes — .github/workflows/, Blockchain/Dev/.security/,\n# Blockchain/Dev/scripts/audit/, scripts/run-shell-suites.sh, systemTest/__tests__/manifest_quarantine.test.sh,\n# systemTest/__tests__/ (a new or moved shell suite changes the 27/2 of 29 ratio), Blockchain/Dev/docs/DEV-PROCESS.md and\n# Blockchain/Dev/package-lock.json (#887's doc and the lockfile its live red rests on) — -> exit 18; otherwise the launcher")
rep("# no TTY), re-pointed at the three heads.", "# no TTY), re-pointed at the four heads.")
rep("""BRANCH942='refs/heads/feature/ks-1078-tsx-probe-capture'
""", """BRANCH942='refs/heads/feature/ks-1078-tsx-probe-capture'
BRANCH887='refs/heads/feature/ks-961-workspace-suites-advisory-on-pr'
""")
rep("""HEAD942="${QAL9_HEAD942:-53b9c3cc1a89f513620516c580a5de5bd60c64de}"
""", """HEAD942="${QAL9_HEAD942:-53b9c3cc1a89f513620516c580a5de5bd60c64de}"
HEAD887="${QAL9_HEAD887:-3aee3deed2e3ac557f0a52c0797c2a4a8df25f69}"
""")
rep("RUN940='34426409872'; RUN941='34427102258'; RUN942='34785721609'   # the live artefacts (Security Scanning / Security Scanning / PR Security Gates)",
    "RUN940='34426409872'; RUN941='34427102258'; RUN942='34785721609'; RUN887='34786655660'   # the live artefacts (Security Scanning ×2 / PR Security Gates / pr)")
rep("""GATES_BLOB_LANDED='eac30f09b461bd4fd270ba4da1d24423a53255c1'                                                              # #942 landed
""", """GATES_BLOB_LANDED='eac30f09b461bd4fd270ba4da1d24423a53255c1'                                                              # #942 landed
SUITES_FILE='.github/workflows/pr-platform-suites.yml'
SUITES_BLOB_OK='a509ad7934a50cd3f96c7241d9445b942c638cb7'                                                                 # M18
SUITES_BLOB_LANDED='fd5e8343c6392ec35b2abc5c38d305a945896b71'                                                             # #887 landed (its head's blob = the merged shape)
""")
rep('# THREE heads, one pass: every one must still be at its branch on origin (the verdict is per PR, on these SHAs).\nLSR="$(git -C "$REPO" ls-remote origin "$BRANCH940" "$BRANCH941" "$BRANCH942")"\nfor pair in "$HEAD940 $BRANCH940" "$HEAD941 $BRANCH941" "$HEAD942 $BRANCH942"; do',
    '# FOUR heads, one pass: every one must still be at its branch on origin (the verdict is per PR, on these SHAs).\nLSR="$(git -C "$REPO" ls-remote origin "$BRANCH940" "$BRANCH941" "$BRANCH942" "$BRANCH887")"\nfor pair in "$HEAD940 $BRANCH940" "$HEAD941 $BRANCH941" "$HEAD942 $BRANCH942" "$HEAD887 $BRANCH887"; do')
rep("# THIS GATE'S OWN GUARD: the three LIVE RUNS are the artefacts", "# THIS GATE'S OWN GUARD: the four LIVE RUNS are the artefacts")
rep('  RUN940="$RUN940" RUN941="$RUN941" RUN942="$RUN942" HEAD940="$HEAD940" HEAD941="$HEAD941" HEAD942="$HEAD942" python3 - <<\'PYR\'',
    '  RUN940="$RUN940" RUN941="$RUN941" RUN942="$RUN942" RUN887="$RUN887" HEAD940="$HEAD940" HEAD941="$HEAD941" HEAD942="$HEAD942" HEAD887="$HEAD887" python3 - <<\'PYR\'')
rep('(os.environ["RUN942"], os.environ["HEAD942"], "942")):', '(os.environ["RUN942"], os.environ["HEAD942"], "942"), (os.environ["RUN887"], os.environ["HEAD887"], "887")):')
rep("# The three compares: #940 and #941 sit on a1e49d151 (ONE commit each, 1 / 2 files); #942's merge-base is the pinned develop\n# itself (the head carries the --no-ff merge of M18: ahead 2, 3 files). A different merge-base or shape is a different PR.",
    "# The four compares: #940 and #941 sit on a1e49d151 (ONE commit each, 1 / 2 files); #942's and #887's merge-base is the pinned\n# develop itself (each head carries a --no-ff merge of M18: ahead 2 / 3 files, ahead 5 / 2 files). A different merge-base or\n# shape is a different PR.")
rep('  HEAD940="$HEAD940" HEAD941="$HEAD941" HEAD942="$HEAD942" python3 - <<\'PY\'', '  HEAD940="$HEAD940" HEAD941="$HEAD941" HEAD942="$HEAD942" HEAD887="$HEAD887" python3 - <<\'PY\'')
rep('for tag in ("940", "941", "942"):', 'for tag in ("940", "941", "942", "887"):')
rep('[ -n "$CMP_READ" ] || { echo "REFUSING: could not read the three compares from the GitHub compare API" >&2; exit 13; }', '[ -n "$CMP_READ" ] || { echo "REFUSING: could not read the four compares from the GitHub compare API" >&2; exit 13; }')
rep('CMP_WANT="#940 mb=$BASE_940_941 ahead=1 files=1 | #941 mb=$BASE_940_941 ahead=1 files=2 | #942 mb=$DEVELOP_SHA ahead=2 files=3"',
    'CMP_WANT="#940 mb=$BASE_940_941 ahead=1 files=1 | #941 mb=$BASE_940_941 ahead=1 files=2 | #942 mb=$DEVELOP_SHA ahead=2 files=3 | #887 mb=$DEVELOP_SHA ahead=5 files=2"')
rep('[ "$CMP_READ" = "$CMP_WANT" ] || { echo "REFUSING: the three compares do not read as the brief pins them', '[ "$CMP_READ" = "$CMP_WANT" ] || { echo "REFUSING: the four compares do not read as the brief pins them')
rep("# The develop pin, judged by CONTENT (see the header): the lane's two workflow files by blob on develop — a landing of #940,\n# #941 or #942 moves one of them",
    "# The develop pin, judged by CONTENT (see the header): the lane's three workflow files by blob on develop — a landing of #940,\n# #941, #942 or #887 moves one of them")
rep('  DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" SCAN_FILE="$SCAN_FILE" GATES_FILE="$GATES_FILE" \\\\\n  SCAN_BLOB_OK="$SCAN_BLOB_OK" SCAN_BLOBS_LANDED="$SCAN_BLOBS_LANDED" GATES_BLOB_OK="$GATES_BLOB_OK" GATES_BLOB_LANDED="$GATES_BLOB_LANDED" python3 - <<\'PYJ\'',
    '  DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" SCAN_FILE="$SCAN_FILE" GATES_FILE="$GATES_FILE" SUITES_FILE="$SUITES_FILE" \\\\\n  SCAN_BLOB_OK="$SCAN_BLOB_OK" SCAN_BLOBS_LANDED="$SCAN_BLOBS_LANDED" GATES_BLOB_OK="$GATES_BLOB_OK" GATES_BLOB_LANDED="$GATES_BLOB_LANDED" \\\\\n  SUITES_BLOB_OK="$SUITES_BLOB_OK" SUITES_BLOB_LANDED="$SUITES_BLOB_LANDED" python3 - <<\'PYJ\'')
rep('scan_f = os.environ["SCAN_FILE"]; gates_f = os.environ["GATES_FILE"]\n', 'scan_f = os.environ["SCAN_FILE"]; gates_f = os.environ["GATES_FILE"]; suites_f = os.environ["SUITES_FILE"]\n')
rep('    gates_blob = get("/contents/" + gates_f + "?ref=" + cur)["sha"]\n', '    gates_blob = get("/contents/" + gates_f + "?ref=" + cur)["sha"]\n    suites_blob = get("/contents/" + suites_f + "?ref=" + cur)["sha"]\n')
rep('gates_state = "M18" if gates_blob == os.environ["GATES_BLOB_OK"] else ("LANDED #942" if gates_blob == os.environ["GATES_BLOB_LANDED"] else "OTHER")\n',
    'gates_state = "M18" if gates_blob == os.environ["GATES_BLOB_OK"] else ("LANDED #942" if gates_blob == os.environ["GATES_BLOB_LANDED"] else "OTHER")\nsuites_state = "M18" if suites_blob == os.environ["SUITES_BLOB_OK"] else ("LANDED #887" if suites_blob == os.environ["SUITES_BLOB_LANDED"] else "OTHER")\n')
rep('if scan_state.startswith("LANDED") or gates_state.startswith("LANDED"):\n    print("LANDEDL9 develop\'s security-scan.yml blob " + scan_blob[:9] + " (" + scan_state + ") / pr-security-gates.yml blob " + gates_blob[:9] + " (" + gates_state + ") — a PR of this pass has landed; its section is moot"); sys.exit(0)\nif scan_state == "OTHER" or gates_state == "OTHER":\n    print("GUARDED develop\'s security-scan.yml blob " + scan_blob[:9] + " (" + scan_state + ") / pr-security-gates.yml blob " + gates_blob[:9] + " (" + gates_state + ") — a version nobody pinned"); sys.exit(0)\nstate = "develop\'s security-scan.yml blob " + scan_blob[:9] + " = M18; pr-security-gates.yml blob " + gates_blob[:9] + " = M18 (the three heads\' base copies)"',
    'trio = "security-scan.yml blob " + scan_blob[:9] + " (" + scan_state + ") / pr-security-gates.yml blob " + gates_blob[:9] + " (" + gates_state + ") / pr-platform-suites.yml blob " + suites_blob[:9] + " (" + suites_state + ")"\nif scan_state.startswith("LANDED") or gates_state.startswith("LANDED") or suites_state.startswith("LANDED"):\n    print("LANDEDL9 develop\'s " + trio + " — a PR of this pass has landed; its section is moot"); sys.exit(0)\nif scan_state == "OTHER" or gates_state == "OTHER" or suites_state == "OTHER":\n    print("GUARDED develop\'s " + trio + " — a version nobody pinned"); sys.exit(0)\nstate = "develop\'s " + trio + " = the four heads\' base copies"')
rep('           "systemTest/__tests__/"]\n', '           "systemTest/__tests__/",\n           "Blockchain/Dev/docs/DEV-PROCESS.md",\n           "Blockchain/Dev/package-lock.json"]\n')
rep("— disjoint from the two judged files (by blob) and the six GUARDED prefixes; the gate re-reads develop at start and end, re-derives #942's merged shape onto the then-current tip in its own clone",
    "— disjoint from the three judged files (by blob) and the eight GUARDED paths; the gate re-reads develop at start and end, re-derives #942's and #887's merged shapes onto the then-current tip in its own clone")
rep("# 7. the exit-20 guard: all three heads in both files", "# 7. the exit-20 guard: all four heads in both files")
rep('for h in "$HEAD940" "$HEAD941" "$HEAD942"; do', 'for h in "$HEAD940" "$HEAD941" "$HEAD942" "$HEAD887"; do')
rep('  echo "  heads $HEAD940 / $HEAD941 / $HEAD942 present at their branches on origin"\\n', '  echo "  heads $HEAD940 / $HEAD941 / $HEAD942 / $HEAD887 present at their branches on origin"\\n')
rep('  echo "  brief and prompt both name all three head SHAs"\\n', '  echo "  brief and prompt both name all four head SHAs"\\n')
rep('[ -z "${QAL9_BRIEF:-}${QAL9_PROMPT:-}${QAL9_HEAD940:-}${QAL9_HEAD941:-}${QAL9_HEAD942:-}" ]', '[ -z "${QAL9_BRIEF:-}${QAL9_PROMPT:-}${QAL9_HEAD940:-}${QAL9_HEAD941:-}${QAL9_HEAD942:-}${QAL9_HEAD887:-}" ]', 1)
rep('("2026-09-14_secuura-L9-940-941-942-887-ks1075-1077-1078-961-tier2.md", 2), ("2026-09-14_secuura-L9-940-941-942-887-ks1075-1077-1078-961-tier2.prompt.txt", 1),',
    '("2026-09-14_secuura-L9-940-941-942-887-ks1075-1077-1078-961-tier2.md", 2), ("2026-09-14_secuura-L9-940-941-942-887-ks1075-1077-1078-961-tier2.prompt.txt", 1),\n    ("3aee3deed2e3ac557f0a52c0797c2a4a8df25f69", 1), ("a509ad7934a50cd3f96c7241d9445b942c638cb7", 1), ("fd5e8343c6392ec35b2abc5c38d305a945896b71", 1), ("34786655660", 2), ("QAL9_HEAD887", 2),\n    ("refs/heads/feature/ks-961-workspace-suites-advisory-on-pr", 1), ("SUITES_FILE", 4), ("SUITES_BLOB_OK", 4), ("SUITES_BLOB_LANDED", 4), ("KS-961", 1), ("Blockchain/Dev/docs/DEV-PROCESS.md", 2), ("Blockchain/Dev/package-lock.json", 2), ("rollup-linux-x64-gnu", 1),')
rep('("brief and prompt both name all three head SHAs", 1)', '("brief and prompt both name all four head SHAs", 1)')
rep('("34427102258", 3), ("34785721609", 2), ("34755906436", 1),', '("34427102258", 3), ("34785721609", 2), ("34755906436", 1), ("5656613944", 1), ("5153400898", 1),')
rep('("GUARDED", 7),', '("GUARDED", 8),')
rep('("CMP_WANT", 3), ("CMP_READ", 5),', '("CMP_WANT", 3), ("CMP_READ", 5), ("ahead=5 files=2", 2),')
rep('("head_sha", 4),', '("head_sha", 4), ("HEAD887", 9),')
rep('4 block replacements + the exit-20 loop + the echo block + the override line;', '4 block replacements + the exit-20 loop + the echo block + the override line (four heads);')
open(p, 'w', encoding='utf-8').write(s)
print('generator patched for the fourth head')
