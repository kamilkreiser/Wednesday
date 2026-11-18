STARTABLE: YES - the kit is complete, stamp_check.py exits 0 (51 claims, 51 measured), the frozen edits were applied and run in a scratch copy; four Tuesday questions below each carry a default that lets the seat start.

# Drafter report B1720 | SEAT-H183 | HPSM-POC | lane H-F: two docstrings (HPSMPOC-510)
Drafted 2026-11-18, `date` printed 23:09:00 at the first read and 23:19:18 at the last measure run. Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-18_B1720_SEAT-H183_hpsmpoc-lane-h-f-docstrings-510.md` (190 lines, 0 non-ASCII bytes, 8 lines holding a four-underscore run = 7 Stamp slots plus the last line, 0 `@TOKEN@`). Sidecar `.measured` beside it. Rules read whole first (`DRAFTER_RULES.md`; its paths say `/Volumes/Laptop-DEV`, this machine is `/Volumes/Datasec_DEV`, so the kit uses the latter).

## BLUF
- Two docstring corrections, nothing else: the `live_check` docstring in `scripts/deploy-package.py` (lines 536-537 at main) and the `plant` docstring in `infra/tests/test_deploy_hpsmpoc208.py` (line 460). Both texts are FROZEN in the kit, every word derived from printed code lines (78, 83, 84, 550, 561-562, 569-570; module docstring line 31 and comment 80-81 for "not tested").
- Main has moved since the sweep: `deef2d76` (the squash of #335). The sweep's line pointers (536-537, 460) still hold; the suite is now 332 tests (not B1705's 325/332).
- Proof is by program: a docdiff program (source in the kit, run from the extracted block) shows one hunk per file, inside the docstring, ASTs equal with the docstrings blanked, and FAILS on a planted code change; the infra suite by test id reads lost 0, added 0, changed 0; old phrase count 1 -> 0 with positive control.
- Model sonnet (`model-routing.md:82`, row L3; C2 line 92 only if the lane widens: STOP). Gate G3 (`model-routing.md:110`) with the builder's own red-proof; G2 (line 109) as the fallback (Q-1). Model id `claude-sonnet-5-5` at `models_latest.json:23`.
- Records (Jira comment or move, any clarifications entry) are not this lane's; the kit says so in the Authority section, PARTITION and HOLDS.

## Facts re-measured with instruments (sidecar ids are hashes; the kit's Sxx tags map as below)
- S01 Jira: HPSMPOC-510 read whole by the sweep's GET-only `jdesc.py` (token never printed); scope sentence and fix shape quoted in the kit; labels docs, follow-up; Backlog. The ticket's "Records: entry C-391" is the landed entry (B1712 STATUS: records PR 213 merged as f9ca1083); no C-392 exists at B1712 (see UNMEASURED).
- S02 `gh api -X GET` under the HPSM `GH_CONFIG_DIR`: main `deef2d768cdae5d765fe93a62b78bc8e342f923e` (23:09, 23:15, 23:19), 1 parent, files README, test file, script; open PRs 0; `heads/b1720` 0 (control `heads/b1639` 2); #335 merged 2026-11-18T01:05:53Z, #334 00:42:25Z; repo allows squash.
- S03 branches 350; pattern hits `b123/ci-deploy-package`, `b510/hpsmpoc-479-1-runner-env` (unrelated), `b1705/...` (merged work); `b1695/...` branch name still on origin, its change landed as #334.
- S04 `lsof 9900-9929` 0 (control 5000: 3); tmux: `tuesday`, `fleet-monitor`, one NexusAI seat, no HPSM pane. No server needed, so no port block assigned; the word-boundary port scan of today's SEAT kits was NOT run (listed in UNMEASURED); the `briefs/` listing showed no H183 or B1720 file before mine.
- S05/S06 blobs at main equal `git hash-object` of the tarball copy: script `cb540f1c`, test file `70d80f09`; awk NR pointers printed (above).
- S07-S08 old phrase `nothing else may be`: 1 file, 1 line (script:536) at main, control `ORYX_TARS` 4; plant phrase 1.
- S09 nothing reads the two docstrings (`__doc__` count 0 in both test files, 1 in the script at line 575 = the module docstring); ci.yml line 631 `run: bash infra/scripts/validate.sh`.
- S10 scratch run (git-initialised tarball copies, Python 3.14.10, BICEP set): base `Ran 332 tests` OK, head `Ran 332 tests` OK, byid lost 0 added 0 changed 0 (control lost 1); `validate.sh` rc 0, `ResourceWarnings: 0`, `Files still open: 0`; 208 file under 3.9.6 `Ran 42 tests` OK; 208 + test_deploy_package under 3.14 `Ran 86 tests` OK; docdiff OK on the pair, FAIL on the control; numstat `5 2` and `2 1`; kit's OLD/NEW blocks byte-equal to what I applied (OLD 1 at base, NEW 1 at head, 0 at base). Load1 5.46-6.83.
- S11 Pythons 3.14.10 and 3.9.6, bicep file exists, `.tools/b1705/scripts/{env.sh,byid.py}` exist; no `.tools/b1720`. S12 routing lines 80/82/92/109/110 by awk NR.

## D-decisions (mine)
- D-1: the docstring words are frozen in the kit (rule: freeze only if every word derives from printed code lines; they do), with a "reword only from printed lines and name it in STATUS" escape (Q-2).
- D-2: the `live_check` docstring names the Oryx names by constant (`SITE_ONLY_ALLOWED`, `FAVICON_ROUTE_CACHE`), not by the full path (the path is already in the module docstring), and says "the Oryx archive found there" because line 550 allows an archive only when it is the one found.
- D-3: the README is not touched (the ticket's "Done when": no other change to the three files of #335; README line 183-190 already says the pair).
- D-4: proof program written into the kit as a byte-for-byte block; AST-blanking plus difflib hunk spans beat eyes, and its control fails by design.
- D-5: no HELD line in `landing.txt` (the picomatch change landed as #334); hosted CI on the new PR is Tuesday's read.
- D-6: no ticket key in added lines; HPSMPOC-510 allowed in the commit message only.
- D-7: the old-phrase count and the plant-phrase counts carry positive controls.

## Q-questions for Tuesday (each with a default)
- Q-1: gate G3 (your instruction; default) or G2 for a change in a deploy tool's file? Default G3.
- Q-2: the frozen texts stand; may the builder reword from printed lines? Default: only from printed code lines, named in STATUS.
- Q-3: README untouched? Default yes.
- Q-4: lane pushes only, Tuesday opens the PR (the kit's Stamp default).

## UNMEASURED
- Hosted CI green on the new PR (Tuesday's read after it opens); whether a C-392 clarifications addendum exists today (the analysis repo's file is large; the local analysis clone at `.tools/b1701/analysis` is stale and read 0, not used as evidence); `git ls-remote` of the new branch (I used `gh api matching-refs` instead; the kit tells the seat to use `git ls-remote`).
- That a Sonnet seat applies the Edit hunks exactly (the kit gives a refusal if the old text does not occur once).
- The word-boundary scan of today's and yesterday's SEAT kits for the port block (not needed: no server).
- Whether any HPSM seat is started between drafting and stamp (re-read heads at the stamp).

## Inputs table (rule 4)
Step 0 makes `.tools/b1720/**`, the clone `head`, `main-tree`, `env.sh`, `byid.py` (copied from `.tools/b1705/scripts/`, exists at BASE) and `docdiff.py` (written from the kit block). Step 1 reads GitHub only. Step 2 reads `main-tree` (Step 0). Step 3 edits `head` (Step 0) and copies it to `scratch/ctl`; it needs `main-tree` and `docdiff.py`. Step 4 reads `out/base-infra-v.log` (Step 2). Step 5 reads the working tree and the commit; Step 6 needs 3-5.

## Outside-the-fences disclosure
- Wrote only: the kit, its `.measured` sidecar, this report, and scratch under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s291/d1720/` (the main tarball and extracted tree, scratch copies `g/base`, `g/head`, `g/ctl`, `g/nb` with scratch git inits and commits using a scratch identity, logs, `edit.py`, `docdiff.py`, `docdiff_kit.py`, `kit.md` draft). No project folder, repo, ref or Jira touched.
- Four Bash calls were refused by hooks (two for a typed `cd`, one for a zsh `=` word, one `git init` through a `$VAR` path, one `rm -rf` through a `$VAR`); nothing in a refused call ran, and each was re-issued without the fault. I read B1705's kit through the persisted tool-result copy of a refused-then-reissued `cat`.
- Jira: one GET of HPSMPOC-510 (the sweep's `jdesc.py`, credentials read in process, not printed). `gh api -X GET` only (commits, contents, tarball, branches, pulls, matching-refs, repo settings, dependabot count). No mail, no az, no hosted HTTP, no decision-queue use, no read of `briefs_staged`, `scoreboard.md`, the ledger or any WEDNESDAY/FRIDAY tree. Read of other lanes' briefs/STATUS: B1705 kit, sidecar, report and STATUS; B1712 and B1713 STATUS (grep); the sweep's H-F section.
