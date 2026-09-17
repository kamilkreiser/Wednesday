#!/usr/bin/env python3
"""repin_brief_prompt.py — re-pin the #1022 brief + prompt from head 58684e653 / develop 581c9db0d to head ff49d0242 / develop 81ee4b729.
Asserted replacements (each anchor's count must match) on the files in place; .pre-repin-ff49d0242 copies were taken first.
After: residual scan for the old head pin in operative positions (every surviving 58684e653 mention must be a labelled history line)."""
import re, sys
Q = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1022-ks1211-hono-tier1'
def apply(path, subs):
    s = open(path, encoding='utf-8').read()
    for old, new, n in subs:
        c = s.count(old)
        if c != n: print('REFUSING %s: anchor %r count %d expected %d' % (path.rsplit('/', 1)[1], old[:80], c, n)); sys.exit(1)
        s = s.replace(old, new)
    return s

REPIN = '''## RE-PIN (read this before anything below)

**This brief was re-pinned at 18:3x AEST from head `58684e653` to head `ff49d0242a8ae764155d427232b15647c6bfa849`.** Seat B merged develop in after #1021 (colord) landed; no gate had run on `58684e653`. The HEAD MOVED mail, saved verbatim with its Authentication-Results header (spf, dkim, dmarc pass): `GS/mail_1022_head_moved.md` (08:31:17Z). Drafter re-derivation: `GS/drafter_repin.py` → `GS/drafter_repin.out` (18:34:19–18:34:42), raw gate runs in `GS/out_repin/`.

- **New head** `ff49d0242` = a `--no-ff` MERGE commit, parents `58684e653` (the hono commit) + `81ee4b729` (develop). Tree **`1b03e6951f447a28c60bf69d2ebbed426a272697`** = the drafter's second-merge prediction = the seat's `merge-tree` prediction. `merge-tree --write-tree 81ee4b729 ff49d0242` = the same tree (develop is an ancestor).
- **New develop** `81ee4b729e86a645fc9098aafa1aaf39035a9950` = #1021's squash on `581c9db0d`: `audit-baseline.json` `c73fcebed` (37 rows) + `systemTest/akto` and `systemTest/api-explorer` locks. It is now the head's **merge-base and parent**. Compare `develop...ff49d0242` (API 18:34): **status ahead, ahead 2, behind 0, files 4** — the same 4 files.
- **What the merge commit brought (`58684e653..ff49d0242`):** #1019's 3 api-gateway files, #1021's 2 systemTest locks, and the baseline. **The 3 PR lock blobs are UNCHANGED** — root `99db3e7c2`, mcp-server `f942d659b`, originate `d91d746ef` — and so are every audit script, preflight script, both service Dockerfiles, the three `package.json` and mcp-server `src/{http-server,index}.ts` (18 blobs, `GS/drafter_repin.out` §2). **Therefore every runtime-reach prediction (D1–D3) and the clean-room prediction (D6) carry over unchanged**: they read only unchanged blobs. The "base" tree for runtime and clean-room is now `81ee4b729`, whose 3 lock blobs and mcp-server source equal `f8c7aaa39`'s.
- **What changed:** `audit-baseline.json` `b78691b4c` (35) → **`45ef8220f` (34 rows)** = develop's 37 minus exactly the 3 hono rows, 0 added, 0 altered, key order kept, `$comment` equal; the file is byte-identical to `json.dumps(develop's baseline minus the 3 rows, indent=2)` + newline (drafter-measured; control: a planted `reason` change → 1 altered).
- **Scope by parse vs the NEW three-dot base `81ee4b729`:** mcp-server 312/312 and originate 655/655 — only `node_modules/hono` 4.13.0 → 4.13.8, 0 other; root 1970/1970 — hono + the 12 ruled flag entries, 0 unexpected, 0 version fields; each with a planted-version control that fires.
- **Gates at the new head (`GS/out_repin/`):**

  | run | tree | baseline | audit-gate | audit-locks |
  |---|---|---|---|---|
  | H1 | ff49d0242 | real (34) | **rc 0**, "33 distinct advisories reported, 34 baselined.", 0 CLEANUP | **rc 0**, 43 standalone lockfiles, 0 CLEANUP |
  | H2 control | ff49d0242 | develop 81ee4b729 copy (37) | rc 0, CLEANUP exactly the 3 hono ids | rc 0, no CLEANUP |
  | B0 control | 81ee4b729 | real (37) | rc 0, "36 reported, 37 baselined" | rc 0 |
  | B1 negative | 81ee4b729 | head copy (34) | **rc 1**, FAIL exactly the 3 | **rc 1**, FAIL exactly the 3 |

- **Linear/GitHub at 18:34:** PR API head `ff49d0242`, 2 commits, 4 files; 0 closing phrases in title, body, and both commit messages (the merge commit's is "Merge develop 81ee4b729 into feature/ks-1211-bump-hono"); `attachmentsForURL(pull/1022)` = KS-1211 In Progress, `completedAt` null, `contributes`.
- **Overlap now:** #1021 is MERGED (it is develop), so the "second merge" question is answered by the head itself; no open PR other than the Dependabot set touches the root lock (not re-read after 17:57).
- **In the sections below, the original 58684e653 measurements are kept as history.** Where a number differs, THIS section wins: baseline **34** (not 35), develop **`81ee4b729`** (not `581c9db0d`), merged-tree target **`1b03e6951`** (not `b475cfbe1`), three-dot base **`81ee4b729`** (not `f8c7aaa39`), gate B0 "36 reported, **37** baselined".

'''

brief = apply(Q + '.md', [
    ('— TIER 1, ROUND 1\n', '— TIER 1, ROUND 1 — RE-PINNED to head ff49d0242a8ae764155d427232b15647c6bfa849 (merge of develop 81ee4b729)\n', 1),
    ('Drafted 2026-09-17 17:57–18:2x AEST (from `date`; origin re-read 18:11:01: head `58684e653` and develop `581c9db0d` unchanged)',
     'Drafted 2026-09-17 17:57–18:2x AEST against head `58684e653`, **re-pinned 18:33–18:4x AEST to head `ff49d0242` / develop `81ee4b729`** (origin re-read 18:33:06 and 18:34:19)', 1),
    ('## WHY TIER 1, AND HOW MUCH\n', REPIN + '## WHY TIER 1, AND HOW MUCH\n', 1),
    ('`git ls-remote origin refs/heads/feature/ks-1211-bump-hono refs/pull/1022/head`, plus the PR API\'s `head.sha`.',
     '`git ls-remote origin refs/heads/feature/ks-1211-bump-hono refs/pull/1022/head`, plus the PR API\'s `head.sha`, must read **`ff49d0242a8ae764155d427232b15647c6bfa849`**.', 1),
    ('| head | **`58684e6534b4d420c9fb9ea246d3a32c70c70828`** (ls-remote 17:57:05, 17:58:35, 18:11:01; PR API 17:57:27), tree `4863c729c` |',
     '| head | **`ff49d0242a8ae764155d427232b15647c6bfa849`** (ls-remote 18:33:06, 18:34:19; PR API 18:34), tree **`1b03e6951`**; a merge commit, parents `58684e653` (the hono commit, tree `4863c729c`, the original pin) + `81ee4b729` (develop) |', 1),
    ('| parent = merge-base | `f8c7aaa39dabfe6a3916e5be55d9ccd752e7d8ed` (the #1020 merge). Compare `develop...head` 17:57:27: **status diverged, ahead 1, behind 1, files 4** |',
     '| merge-base = develop | **`81ee4b729e86a645fc9098aafa1aaf39035a9950`** (#1021 squash). Compare `develop...head` 18:34: **status ahead, ahead 2, behind 0, files 4**. (History: `58684e653`\'s parent was `f8c7aaa39`; compare at 17:57:27 was diverged, ahead 1, behind 1, files 4) |', 1),
    ('| **develop moved** | origin develop = **`581c9db0db4201c42cbbf702f339b750989acdb1`** (#1019, KS-1187, Seat A; tree `99df1503e`), 3 files,',
     '| **develop moved twice** | now **`81ee4b729`** (#1021 colord: `audit-baseline.json` `03d1680e3` → `c73fcebed`, 38 → 37, and the two systemTest locks), on top of `581c9db0db4201c42cbbf702f339b750989acdb1` (#1019, KS-1187, Seat A; tree `99df1503e`), 3 files,', 1),
    ('`Blockchain/Dev/scripts/audit/audit-baseline.json` `03d1680e3` → `b78691b4c` (+0 −21);',
     '`Blockchain/Dev/scripts/audit/audit-baseline.json` develop `c73fcebed` → head **`45ef8220f`** (+0 −21; at `58684e653` it was `03d1680e3` → `b78691b4c`);', 1),
    ('| open-PR overlap | **#1021** (KS-1211 colord, Seat B, `742e1c608`) shares `audit-baseline.json` (a different row).',
     '| open-PR overlap | **#1021** (KS-1211 colord) is now MERGED into develop and merged into this head; it shared `audit-baseline.json` (a different row).', 1),
    ('| head locks + head baseline (35 rows) | audit-gate rc 0 "33 distinct advisories reported, 35 baselined"',
     '| head locks + head baseline (34 rows) | audit-gate rc 0 "33 distinct advisories reported, 34 baselined"', 1),
    ('| head locks + develop baseline (38) |', '| head locks + develop baseline (37) |', 1),
    ('| base locks (4.13.0) + baseline without the 3 rows |', '| develop 81ee4b729 locks (4.13.0) + the head baseline (34) |', 1),
    ('11. **The heredoc slip**', '12. **HEAD MOVED (08:31:17Z, `GS/mail_1022_head_moved.md`):** `git merge --no-ff 81ee4b729` rc 0, no conflict; tree `1b03e6951` = the prediction; the 3 lock blobs identical to `58684e653`; baseline `b78691b4c` → `45ef8220f`, 34 rows = the branch\'s 35 minus colord = develop\'s minus the 3 hono rows. Re-measured 08:23:59Z: audit-gate rc 0 "33 reported, 34 baselined", 0 CLEANUP; audit-locks rc 0 "32 match, 32 baselined, 0 CLEANUP" (the drafter\'s audit-locks first line reads "43 standalone lockfiles"; the gate reads the whole output and reconciles "32 match" — RECORD); control (develop\'s 37-row baseline) gate CLEANUP exactly the 3; negative control rc 1 / rc 1 exactly the 3. **Suites NOT re-run** (claims originate 637/637 and shared 851/851 "stand from 58684e653"). Push rc 0 fast-forward; in-hook preflight 12/15, 3 SKIPPED, leg 6 "33 reported, 34 baselined" OK, leg 7 OK; 4 stubs ended by pid. It also raises a source discrepancy about systemTest quality gates for PR-3 — not this gate\'s subject.\n11. **The heredoc slip**', 1),
    ('4. **develop moved after the READY** (#1019). PREDICTION: merged == `b475cfbe1`, no interaction with the 4 files; the audit inputs on the merged tree are blob-identical to head.',
     '4. **develop moved twice after the READY** (#1019, then #1021) and the head merged it in. PREDICTION: head tree == merged tree == `1b03e6951`; merging the then-current develop again (if still `81ee4b729`) is a no-op by tree hash.\n5. **The suites were not re-run on `ff49d0242`** (HEAD MOVED). The merge brought api-gateway source (#1019) into the head\'s tree. PREDICTION: RECORD — no hoisted-tree byte the originate and shared suites read moved (root lock blob unchanged), so the 58684e653 numbers stand for those two; the gate may re-run if the root install fits.', 1),
    ('head + real baseline → audit-gate rc 0 (33 / 35) and audit-locks rc 0 (43), 0 CLEANUP; head + develop\'s baseline',
     'head `ff49d0242` + real baseline → audit-gate rc 0 (33 / **34**) and audit-locks rc 0 (43), 0 CLEANUP; head + develop `81ee4b729`\'s baseline (37)', 1),
    ('base + head\'s baseline → both **rc 1**', 'develop `81ee4b729` + head\'s baseline (34) → both **rc 1**', 1),
    ('Per lock, base vs head `packages` maps:', 'Per lock, develop `81ee4b729` vs head `ff49d0242` `packages` maps (and head vs `58684e653`: the 3 lock blobs must be identical):', 1),
    ('Baseline conservation: 35 rows, only the 3 hono ids removed, 0 added, 0 altered, `$comment` identical, with a planted-alteration control. 1 commit, 4 files, `git diff -w` numstat equals the plain one.',
     'Baseline conservation: **34 rows** = develop `81ee4b729`\'s 37 minus only the 3 hono ids, 0 added, 0 altered, `$comment` identical, with a planted-alteration control; and vs `58684e653`\'s 35, only `GHSA-2wm5-q62r-hmrv` (colord) gone. Three-dot vs develop: 4 files, 2 commits (the hono commit + the develop merge); prove the merge commit brought no byte into the 3 PR locks; `git diff -w` numstat equals the plain one.', 1),
    ('(drafter and seat: `b475cfbe1` over `581c9db0d`)', '(drafter and seat: head tree `1b03e6951` over `81ee4b729`; history: `b475cfbe1` over `581c9db0d` for `58684e653`)', 1),
    ('**Overlap with #1021:** predict the result of merging either PR second (drafter: `1b03e6951` both ways, clean, 34 rows) and state what the second PR must re-measure.',
     '**Overlap with #1021:** it merged first; confirm the head\'s merge of it matches the drafter\'s pre-merge prediction (`1b03e6951`, clean, 34 rows) and that Seat B\'s re-measure covered what the second PR owed.', 1),
    ('reports/2026-09-17-ks1211-1022-58684e653-tier1-r1/', 'reports/2026-09-17-ks1211-1022-ff49d0242-tier1-r1/', 1),
    ('`[QA -> Wednesday] TIER 1 GATE #1022 (KS-1211) 58684e653 — <GO | GO WITH FINDINGS | NO GO>`', '`[QA -> Wednesday] TIER 1 GATE #1022 (KS-1211) ff49d0242 — <GO | GO WITH FINDINGS | NO GO>`', 1),
    ('"squash `58684e653` onto develop `<then-current SHA>` (merged tree `<OID>`; drafter and seat `b475cfbe1` over `581c9db0d`); overlap: #1021 edits `audit-baseline.json` (different row) — whichever merges second merges develop in and is re-measured (drafter\'s prediction: clean either way, tree `1b03e6951`, 34 rows);',
     '"squash `ff49d0242` onto develop `<then-current SHA>` (merged tree `<OID>`; drafter and seat `1b03e6951` = the head tree over `81ee4b729`); #1021 already merged and merged in;', 1),
    ('`audit-baseline.json` `b78691b4c` (35 rows)', '`audit-baseline.json` `45ef8220f` (34 rows)', 1),
    ('audit-gate rc 0 33/35 and audit-locks rc 0 43 scanned (re-measure)', 'audit-gate rc 0 33/34 and audit-locks rc 0 43 scanned (re-measure)', 1),
    ('- **#1021 and its gate**,', '- **#1021 and its gate** (merged),', 1),
    ('## DRAFTER-MEASURED INPUTS (re-derive them; a wrong one is Wednesday\'s error, so report it as one)', '## DRAFTER-MEASURED INPUTS — measured at head 58684e653 (history; the RE-PIN section above carries what changed at ff49d0242) (re-derive them; a wrong one is Wednesday\'s error, so report it as one)', 1),
])

prompt = apply(Q + '.prompt.txt', [
    ('Tier 1 because hono ships at runtime,', 'RE-PINNED: the head is now a merge of develop 81ee4b729 (#1021) into the hono commit 58684e653 — read the brief\'s RE-PIN section first. Tier 1 because hono ships at runtime,', 1),
    ('Then the charter it names, the READY and its correction (gatesets/2026-09-17_gate1022/mail_1022_ready.md, mail_1022_ready_correction.md)',
     'Then the charter it names, the READY, its correction and the HEAD MOVED mail (gatesets/2026-09-17_gate1022/mail_1022_ready.md, mail_1022_ready_correction.md, mail_1022_head_moved.md)', 1),
    ('Subject: PR #1022 (KS-1211) @ 58684e6534b4d420c9fb9ea246d3a32c70c70828, one commit on f8c7aaa39dabfe6a3916e5be55d9ccd752e7d8ed, four files, no manifest:',
     'Subject: PR #1022 (KS-1211) @ ff49d0242a8ae764155d427232b15647c6bfa849, a --no-ff merge (parents 58684e6534b4d420c9fb9ea246d3a32c70c70828 + develop 81ee4b729e86a645fc9098aafa1aaf39035a9950), tree 1b03e6951; three-dot vs develop 81ee4b729: two commits, four files, no manifest:', 1),
    ('- Blockchain/Dev/scripts/audit/audit-baseline.json: GHSA-gqvv-2mrq-wpjv, GHSA-g6gw-c38x-mqfc, GHSA-crvj-82cr-hjcx removed (38 -> 35).',
     '- Blockchain/Dev/scripts/audit/audit-baseline.json: GHSA-gqvv-2mrq-wpjv, GHSA-g6gw-c38x-mqfc, GHSA-crvj-82cr-hjcx removed (develop 37 -> 34; colord already gone with #1021).', 1),
    ('origin develop MOVED after the READY: 581c9db0db4201c42cbbf702f339b750989acdb1 (#1019, 3 api-gateway files). Seat and drafter both predict merge-tree over it = b475cfbe1c7e7864adf0eb81bdcf829dd5637e06. #1021 (colord, same ticket) edits audit-baseline.json too, a different row.',
     'origin develop is 81ee4b729 (#1021 colord merged, on #1019 581c9db0d) and is the head\'s merge-base. The 3 lock blobs and every audit/preflight/Dockerfile/mcp-server-src input are byte-identical to 58684e653, so the runtime and clean-room predictions carry over; the baseline is now 34 rows.', 1),
    ('   Drafter: hono resolved 0 times', '   Drafter (measured at 58684e653 vs f8c7aaa39; the same lock and source blobs as ff49d0242 vs 81ee4b729): hono resolved 0 times', 1),
    ('head + real baseline -> audit-gate rc 0 (33 reported, 35 baselined) and audit-locks rc 0 (43), 0 CLEANUP; head + develop\'s baseline -> audit-gate CLEANUP naming exactly the 3, audit-locks none; base + head\'s baseline -> both rc 1 naming exactly the 3',
     'head ff49d0242 + real baseline -> audit-gate rc 0 (33 reported, 34 baselined) and audit-locks rc 0 (43), 0 CLEANUP; head + develop 81ee4b729\'s baseline (37) -> audit-gate CLEANUP naming exactly the 3, audit-locks none; develop 81ee4b729 + head\'s baseline (34) -> both rc 1 naming exactly the 3', 1),
    ('3. Scope by parse: exactly node_modules/hono moves in each lock;', '3. Scope by parse, develop 81ee4b729 vs head (and the 3 lock blobs identical to 58684e653, so the merge commit brought nothing into them): exactly node_modules/hono moves in each lock;', 1),
    ('baseline 35 rows, only the 3 removed, 0 added, 0 altered, with a planted-alteration control.',
     'baseline 34 rows = develop\'s 37 minus only the 3, 0 added, 0 altered, with a planted-alteration control.', 1),
    ('at head and base with a control that must FAIL', 'at head and develop 81ee4b729 with a control that must FAIL', 1),
    ('5. Merge: re-derive the merged tree over the THEN-CURRENT develop in your own clone (drafter b475cfbe1 over 581c9db0d), prove the audit inputs blob-identical to head or re-run item 2 there; predict merging #1021 or #1022 second (drafter: clean both ways, tree 1b03e6951, 34 rows).',
     '5. Merge: re-derive the merged tree over the THEN-CURRENT develop in your own clone (drafter: head tree 1b03e6951 over 81ee4b729, a no-op merge), prove the audit inputs blob-identical to head or re-run item 2 there; confirm #1021-then-#1022 landed as predicted (1b03e6951, clean, 34 rows) and that the seat\'s HEAD MOVED re-measure covered what the second PR owed (it did NOT re-run the suites: rule it).', 1),
    ('/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1211-1022-58684e653-tier1-r1/',
     '/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1211-1022-ff49d0242-tier1-r1/', 1),
    ('Verdict: GO, GO WITH FINDINGS, or NO GO, on 58684e6534b4d420c9fb9ea246d3a32c70c70828 and on the merged tree',
     'Verdict: GO, GO WITH FINDINGS, or NO GO, on ff49d0242a8ae764155d427232b15647c6bfa849 and on the merged tree', 1),
    ('[QA -> Wednesday] TIER 1 GATE #1022 (KS-1211) 58684e653 — <GO | GO WITH FINDINGS | NO GO>', '[QA -> Wednesday] TIER 1 GATE #1022 (KS-1211) ff49d0242 — <GO | GO WITH FINDINGS | NO GO>', 1),
])
# residual: the old pin may survive only in history/labelled lines
for name, text in (('brief', brief), ('prompt', prompt)):
    bad = [l for l in text.splitlines() if '58684e653' in l and not re.search(r'(?i)history|re-pin|parents|merge commit|hono commit|original pin|58684e653\.\.ff49d0242|measured at 58684e653|vs `58684e653`|to 58684e653|58684e653\'s|as `58684e653`|from 58684e653|RE-PINNED', l)]
    for l in bad: print('RESIDUAL old-pin line in %s: %s' % (name, l[:200]))
    print(name, 'mentions of 58684e653:', text.count('58684e653'), '| unlabelled:', len(bad), '| ff49d0242 mentions:', text.count('ff49d0242'))
if '--write' in sys.argv:
    open(Q + '.md', 'w', encoding='utf-8').write(brief); open(Q + '.prompt.txt', 'w', encoding='utf-8').write(prompt)
    print('written; prompt bytes', len(prompt.encode()), 'brief bytes', len(brief.encode()))
