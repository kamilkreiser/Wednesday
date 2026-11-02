STARTABLE: YES, once Tuesday stamps the 9 four-underscore lines (8 slots and the last line) and answers Q-1 to Q-6 below. No STOP found at drafting. State at 03:52-03:59 AEDT 2026-11-03 (clock `date`): branch `63fe0b9e`, main `01bc16e4`, open PRs 113/91/86/85, no Composer pane, `.tools/composer-heavy.lock` absent, load1 2.10. The kit tells the gate to re-read all of it at launch.

# B1173 drafter report (kit B1173 / SEAT-G304, tier-1 Opus gate, ROUND 1 OF 2 on class "Composer: Route B completeness check (0021) header-key rule", branch `b1170/composer-pcomp115-116-db-typecheck-awk` @ `63fe0b9e`, PCOMP-116 only)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-03_B1173_SEAT-G304_composer-pcomp116-route-b-check-gate-tier1.md`, 51.8 KB (`wc -c`), 9 lines with the four-underscore pattern (`grep -c` 9; every other line 0), 0 non-ASCII bytes (`LC_ALL=C grep -c '[^ -~]'` 0), 0 hits for the owner's name, no decision-card id. Launch line carries `BRIEF_SEAT_LEVEL=opus` inside the quotes (G1 `model-routing.md:108`; G-cap `:111`; C8 `:98`; `claude-opus-5-5` at `models_latest.json:17`).

## BLUF
A gate that independently (1) re-derives the claim that the new `DEPLOY.md:203` differs from main's in nothing else (one hunk), (2) regenerates the earlier gate's 899 cut files with its `cutter.py` and proves them byte-equal to `c3-files-sha256.tsv` (899 lines) before using them, then runs old vs new on the three engines (CI-image mawk, macOS BWK awk 20200816 under bash 3.2.57, busybox in `node:24-alpine`) and builds the flip table itself, with a hand-up STOP for any refused-to-accepted cell (this line guards a `DROP FUNCTION` single-transaction restore); (3) adds its own cell families Y1-Y4 (header shapes, trio positions, degenerate files, engine edges) hashed with predictions before it reads the builder's plants or flips; (4) runs 16 plants of its own, including q8 `r==0` removed, which I reasoned is an EQUIVALENT mutant (the key rule reads `s` only at the first `\restrict` line), so the gate must prove it equivalent, not call it a hole; (5) checks each new row can fail and censuses the 4 removed lines; (6) judges the operator sentences `:256-:263` of the new line.

## Facts re-measured (instrument; clock `date` 03:52-03:59 AEDT 2026-11-03)
- Pins `git ls-remote`: branch `63fe0b9ef514dbc76fc74c78fb6b102eaee8c70b`, main `01bc16e4e9f27d5d23d4eb0cbc9ee0cbdfecbc17`; `refs/heads/b1173*` none (control: b1170 ref prints).
- `gh api -X GET compare/main...branch`: ahead 1, behind 0, `DEPLOY.md` +1 -1, test +191 -4 (builder says +192 -5 in all: that is the sum, 192 and 5, so consistent). Commit: parent `01bc16e4`, tree `27e4fc97`, 19 message lines (`wc -l`), one trailer, author e-mail a local-host domain; check-runs `total_count` 0 (no PR, no CI yet); code-scanning branch ref `state=open` 0, main `state=all` 20 (control rows return).
- `diff` of raw `DEPLOY.md` main vs head: exactly line 203 (198 -> 255 characters, `awk length`); `restrict` lines in the head: `:203 :256 :257 :259 :263`; block `:198-:209`.
- b778 file: 1445 -> 1632 lines; `^  it(` rows 37 -> 46 (program). The 4 removed lines (`/usr/bin/grep -n -E '^-[^-]'` over the file patch) are the four `accepts` names of `closingKeyReadAsPrefix`.
- Open PRs and overlap: `pulls/<n>/files --paginate` for 113, 91, 86, 85 count 0 lines naming either path; control #85 lists `document-pdf.ts` (1).
- Round count: loop over 290 `*_STATUS.md` first lines (GATE VERDICT, NO GO, `route b|completeness check|restrict|awk|pcomp-116|pcomp-102|restore-footer|b778`) prints B779 and B787 only. Those are NO GO on a different class (the prose/pins of the Route B block; B787's major was a sentence made false). Control `change-report` prints B1151 and B1161. So I count NO GO 0 on this class (Tuesday's figure), and wrote a **neighbour-class rule**: a false operator sentence is graded Major and flagged as B787's class, never as round 3.
- Earlier gate data: `c3-files-sha256.tsv`, `c3-kind.tsv`, `c3-predictions.tsv` each 899 lines; the three real scripts' `shasum -a 256` equal `c3-real-sha256.txt` (4e0fee30, b569d672, 87c8f36d); `cutter.py` and `runset.sh` headers read (`sed -n`). `runset.sh` defaults its stderr file to `/tmp/b1037-err.txt`: the kit sets `B1037_ERR` into the project scratch.
- Landing: `CLARIFICATIONS.md:2032` printed (it names `:1799` as the authority; `PR #88` control at `:1797/:1799/:1802`).
- Ports: Tuesday assigned none; I chose 9350-9359 (none published). Python scan of 98 non-`.pre-` SEAT kits of 11-02 and 11-03 (4-digit numbers and ranges, width 30 or less, word-bounded): 0 kits for 9350-9359; controls 9980-9989 hit 7, 9340-9349 hit 1; `lsof -nP -iTCP:9350-9359 -sTCP:LISTEN` rc 1. Panes: `%0 tuesday`, `%117 Datasec/MPS-R147`, `%1 fleet-monitor`.
- Local engines: `/usr/bin/awk` "awk version 20200816"; `/bin/bash` 3.2.57; local images `node:24-alpine`, `node:24-bookworm-slim` (gawk: none seen).
- Heavy-lock mechanics: `P/.tools/b985/scripts/heavy.sh` lines 22-56 printed (lock path line 9, two-word holder release line 51); the b879 eight scripts present.

## Contradictions with this commission
1. **Gate-seat independence vs my reading.** I read the builder STATUS whole (plants, flips, design findings). The kit forbids the gate those ranges (`:9-11`, `:22-37`, `:55-105`, and the builder's evidence `runs/`) until its own plants, families and predictions are hashed; disclosed in SELF-CHECK.
2. **Round count** reads NO GO 0 by Tuesday's brief, but B779/B787 are two NO GOs on the same DEPLOY.md section (different class). Handled by the neighbour-class rule (Q-1).
3. **Commission asks "the b616 and b778 files whole green"**; the builder's STATUS and the file header say b616 does not read the 0021 section. Kept as a run anyway; the kit says so.
4. **Whole `vitest run`** in CI copies a gitignored SOW text (HP-NDA hold) into the container. The gate cannot supply it, so the kit asks for the same failed set at the main twin instead of zero failures. The builder reports 3108 passed / 1 skipped / 0 failed; if the E8 rows are failing at the gate, that is a difference to explain (the builder's environment may have had the SOW).
5. Drafter fix: the main twin is judged in the gate's own clone, not `P/.tools`.

## D-decisions (mine, for Tuesday to accept or strike)
- D-1. By-reference incorporation of the B1161 kit only for plumbing, LOAD and HOLDS (everything else inline; kit 51.8 KB).
- D-2. Cut set proven equal to the earlier gate's by sha256 per cell before it is used; that is the independence control for "the gate's real cut files".
- D-3. Hand-up STOP on any refused-to-accepted cell (data-destruction class, tier 1).
- D-4. NO GO output is findings + fix shapes (round 1); `residue.md` is left to round 2.
- D-5. Four landing files (pr-title, pr-body, squash-subject, squash-body); no `card-input.txt` (no product-owner trade-off in this subject except `:259`'s wording, listed in FOR TUESDAY).
- D-6. CodeQL graded as NOT SCANNED Condition at the verdict (no PR exists), Tuesday reads it on the PR head.
- D-7. Plants 16 (not 5), with q8 predicted equivalent; the gate proves or refutes it.

## Q-questions for Tuesday (each with a default)
- Q-1. Round count: accept "round 1 of 2, NO GO 0 on this class" with the neighbour-class rule for a false sentence? Default: yes.
- Q-2. Port block 9350-9359, none published. Default: accept.
- Q-3. Hard stop and target: 150 / 240 minutes after Step 0 written absolute (S6). Default: as suggested, never past the window you stamp.
- Q-4. Moved-main rule if PR #113 lands first (re-measure, not stop, unless a gated path moves; gated list in REFUSE 3: `DEPLOY.md`, `packages/db/`, `docker/`, `scripts/`, `package.json`, lockfile, tsconfig/vitest/eslint/prettier configs, `.github/`). Default: accept the list.
- Q-5. Whole-run failures that need the HP-NDA SOW text: compare failed sets at head and main twin rather than demand zero. Default: yes.
- Q-6. Keep `pr-title.txt` as a landing file (the earlier PRs carried one). Default: yes.

## UNMEASURED (drafter)
No test, build, container, awk, render or plant ran. That the new line accepts and refuses what the builder says; that q8 is an equivalent mutant (reasoning only); that mawk 1.3.4 is what the CI image holds (the earlier gate's record); that `node:24-alpine`'s `awk` is busybox 1.37 (builder STATUS); gawk; CodeQL on a PR head (none exists); `:259`'s wording being acceptable. Everything after 03:59 AEDT: pins, panes, lock, load, PR #113 state.

## Outside the fences (disclosure)
- Read-only reads outside my two files: DRAFTER_RULES, the B1161 kit and report, both B1170 kits, the B1170 STATUS (whole), `B1037_STATUS.md:206`, `c3-*` evidence names and hashes, the first lines of all `*_STATUS.md` in the Composer Briefs (round-count loops, also B779/B787/B1066), `CLARIFICATIONS.md` line 2032 and `PR #88` hits, `model-routing.md` lines 98-111, `models_latest.json:17`, `brief_seat.sh` and `launch_when_cool.sh` headers, `heavy.sh` lines, `.tools` listings (`b1037/scripts`, `b1037/scratch/real`, `b879/scripts`, `b985/scripts`, `b1170`), `shasum` of the three real scripts, `/usr/bin/awk --version`, `/bin/bash --version`, `docker image ls` (list only).
- `gh api -X GET` under the Composer `GH_CONFIG_DIR`: compare, pulls, pulls files, commits, check-runs, code-scanning, raw `contents` of DEPLOY.md, the b778 file, `scripts/ci.sh`, `package.json`. No git write verb; `git ls-remote` only.
- Scratch under the session scratchpad only (raw copies of the files, a patch, a python port scan). Written outside the scratchpad: only the kit and this report.
- Missteps: one Bash call was refused by the `====` zsh hook and re-run; one `wc` over the whole scratchpad glob printed other sessions' scratch file names (no content read).
- No decision-queue call, no `fleet/briefs_staged/`, no scoreboard or ledger, no other client's tree, no mail, no Jira, no write verb to GitHub, no deploy, no HTTP to a hosted host.
