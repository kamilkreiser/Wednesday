STARTABLE: YES (with Q-1 to Q-3 decided by you at the stamp; none blocks the launch)

# B1228 drafter report (kit: SEAT-G325, HPSM-POC tier-1 gate, round 4 on class R)

Window: reads 2026-11-03 19:09:57 to 19:12:49 AEDT (`date`), kit written about 19:25. Kit 52 lines (long lines; the 70-line target holds by count). Slot count 8 (7 slots plus the last line; `grep -c` 8, the REFUSE control says 8). At-sign placeholders 0. Non-ASCII lines 1 (the footer's real text `Prototype · sample data only`; kit only).

## BLUF
Kit is the B1198 shape re-aimed at head `58ac1077...` (merged with main `f464376b`, 5 ahead / 6 behind, 10 paths). It re-measures the jump (frames (a) and (b)), the nudge (25 cells), the footer (open and collapsed, `:has()` rule in the built CSS and its browser support), the band (pair of PNGs, smaller = Note, larger = Major), the page-height waiver, the ring against `-pre` (full 1752 grid at landing and `-pre`), the CI chain, the plants (round 3 set plus pm1-3, ph1-3, m6, m7), axe at 1440/390 is added in step 4H only if an axe package is already installed, else NOT RUN (see Q-3). A NO GO is a card (`residue.md` + `card-input.txt`), not a round 5.

## Facts re-measured with instruments (all by program, `gh api -X GET` unless stated)
- Branch ref = `58ac10775f1d3cde07a3f37918c1976e900e86d2` (`git/ref/heads/...`; the `git ls-remote` over SSH failed "Repository not found" from this shell: global ssh config, not a ref problem), main = `f464376b...` (`git/ref/heads/main` and `commits/main`), open PRs 0 (`pulls?state=open` length 0), `matching-refs/heads/b1228` 0.
- `compare f39ac80...58ac107`: ahead 1 behind 0; files `shell-sidebar.spec.ts +100 -2`, `globals.css +2 -2`, `layout.tsx +1 -1`, `Sidebar.tsx +1 -1` (matches your numbers). `compare main...58ac107`: diverged, ahead 5, behind 6, merge base `c14573495e51...`, 10 files. Commit tree `fb32841377345aef...`, `verified false`, `Co-Authored-By` count 1.
- Blob equality at pin vs main: `package-lock.json` `81393fd77c36`, `playwright.config.ts` `bf42f0291518`, `scripts/e2e.mjs` `53879b96371f`, `ci.yml` `0176b4915d69` (all equal).
- Pointers printed by `grep -n`/`awk NR` over raw files at the pin: `Sidebar.tsx:68` (tokens printed, `lg:-mb-16` present), `layout.tsx:18/:26/:28`, `globals.css:93/:96/:90`, `AppShell.tsx:163/:164/:166`, `FeedbackPill.module.css:41-42`, spec `:554 :590 :651 :659 :715 :721 :734 :735 :741 :751 :752 :770`, `e2e.mjs:52`, CI lines (371 395 396 409 413 426 450 478 483 515 526), `package.json:20` (next 16.4.2). Control for the has/browserslist counts: `browserslist` in `package.json` 0 vs `"next"` 1; repo-root `.browserslistrc` 404; `web/` listing 0.
- Model: `model-routing.md:108` G1, `:111` G-cap (awk NR printed); `models_latest.json:17` `claude-opus-5-5`.
- Round counts: line 1 of B1109, B1130, B1198 STATUS each `grep -c -i -F ' NO GO '` 1; absent-string control 0 on all three.
- Landing rule: `CLARIFICATIONS.md:3617` is the first line starting "The landing form is a head-pinned squash" (awk NR==3617 printed it); 99 lines mention it; file is 5491 lines now (B1198 read 5477).
- Ports 9110-9119: `lsof` 0; word-bounded scan over 153 non-`.pre-` SEAT kits of 11-02 and 11-03: 0 files; controls in the same loop `966[0-9]` 4, `964[0-9]` 3 (a first pass with an unsplit zsh variable gave false zeros; I redid it with `${=K}`). Your avoid-list blocks untouched. `lsof` over 9600-9999: 0 listeners.
- Panes 19:09: `tuesday`, `Datasec/HPSM-POC-G324`, `Datasec/NexusAI-G323`, `fleet-monitor`. G324's 36 files vs main (`compare main...f0000f54`): property regex over shell/globals/layout/shell-sidebar 0 (control, a planted `layout.tsx` line, 1); `FeedbackPill` 0. `df` 217858484 KiB; load1 21.10 at 19:12.
- `.tools/b1228` absent; `.tools/b1198/repo`, `.tools/wt-b1198-head/web/node_modules`, `node24`, `ms-playwright` present; `.tools/b1218` exists (control).

## D-decisions (mine, for you to keep or strike)
- D-1 The waiver is written as a PROPERTY (never taller than `-pre`; shorter by at most 62 px), and >62 px is a Major with a question in `residue.md`.
- D-2 Band: larger than `-pre` at any of 12 cells = Major; smaller = Note (as you said); one PNG pair (4 PNGs max).
- D-3 Ring: full 1752 grid at landing AND `-pre`, graded cell-for-cell against `-pre`; main's figures are B1198's (RELAYED) with the 3.1 control cells re-fired. Saves 16 chunks.
- D-4 B-4 is a verdict input again (Major), B1198-3 closes only on x3-alone reads.
- D-5 `:has()` support: gate reads Next's default targets and Tailwind's floor from `node_modules`; a declared target lacking `:has()` = Major (question to the product owner); I wrote my recollection of the versions as UNMEASURED.
- D-6 Added controls B1198 lacked: reach control (`html{overflow:hidden}` must read false), element-outline equality in step 2, footer on routes with no menu.
- D-7 Port block 9110-9119; trees `base/pre/head/mut`; `-pre` = round-3 landing tree (id `21327280e6cd...`, two sources).

## Q-questions for Tuesday (each with a default)
- Q-1 **The builder reads page height shorter by 57 or 64 px in 6 of 12 cells; the waiver you relayed is 35 to 62 px.** 64 is outside. Default (kit): Major + question in the card. Alternative: you tell the seat the waiver means "about 35 to 64".
- Q-2 The builder's PM plant (40 px margin) leaves its own E4 green and says so. Default: not a gap; the gate's m5 is red on `:653` and the E5 rows. No action.
- Q-3 You asked for "axe at 1440 and 390". B1198 has no axe step and I found no axe script in its instruments, so the kit says: use an axe package only if already in `web/node_modules`, else NOT RUN, no install. I did not verify whether axe is installed (UNMEASURED). Default stands unless you want an install authorised.
- Q-4 The kit has no outer-bound clock (S5 default 180/270 minutes); with load1 21 at drafting the waiter may delay launch. Default: use `launch_when_cool.sh`.

## UNMEASURED
Built stylesheet text of the `:has()` rule; Next's actual default browser list; whether axe is installed; the page-height and band figures (all builder claims); the 25 `b4cells.json` cells (file read only by name); whether a footer row can pass vacuously at 1024; load at launch; hosted CI, CodeQL.

## Outside the fences, disclosed
No project-repo git verbs except `git ls-remote` (failed, harmless read). `gh` only `-X GET` under the project's `GH_CONFIG_DIR`; no card read, no Jira, no `decision_queue.sh`. Read-only `ls`/`sed -n` of `.tools/b1198/` file headers (first 8 lines each) and `ls` of `.tools/b1198/data`; no instrument invoked. Raw file fetches via `gh api` were saved in the session scratchpad. No cd typed. The `date` stamped times are mine; no slot filled.
