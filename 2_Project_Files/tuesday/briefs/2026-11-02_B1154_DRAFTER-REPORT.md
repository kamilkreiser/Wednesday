STARTABLE: YES. The kit reads as a whole gate; the one thing to settle at the stamp is the order against G293 (Q-2), and the kit is about 30 KB, over the 25 KB target (Q-5). All pins held at 19:23 to 19:32 AEDT; the heavy lock is free, no Composer pane is live, load1 was 7.44, so the first launch waits for load below 7.

# B1154 drafter report (kit `2026-11-02_B1154_SEAT-G296_composer-pcomp119-rows-gate-tier2.md`, 30,150 bytes, drafted 19:23 to 19:35 AEDT by claude-sonnet-5-5)

## BLUF
- Tier 2 stays (no reason to raise it measured). Round named in the kit: **round 1 of 2, new lane, own counter**, on the class "a new row of the command-guard test is not killed by the fault it names, or carries a sentence no run backs". Exact-class NO GO count 0.
- Template used: **B1108** (G281, `...B1108_SEAT-G281_composer-pcomp98-gate-tier2-r2.md`, 43,669 bytes): the newest Composer tier-2 gate, on the same test file, and the only one whose D-sections (carried states, mutants, oracle, words) transfer. B1085's (G272) kit is the first-round version of the same lane (75,660 bytes, too large to copy); B1101's was a timing-row gate (other file).
- Order against G293: **G296 first** (Q-2).
- Ports 9330-9339 (none published), pane `Datasec/Security-Composer-G296`, suffix `G296`.

## Contradictions with this commission (first)
1. **None on the pins**: ref, main, compare (ahead 1, behind 0, one file +79 -1), open PRs 91, 86, 85 all matched your text at 19:23.
2. The commission says "G2 row, model-routing.md:109 (tests only)" and "routing row C8, :93": `:93` is row C3 (auth/security design surface) in the file; C8 was not looked for. Not used in the kit. Only G2 `:109` and G-cap `:111` are cited, and both printed.
3. The commission lists the launch as the `cockpit.sh add` form (DRAFTER_RULES.md:61). The two newest stamped kits (B1108, B1144) use `launch_when_cool.sh ... "WED_USAGE_STOP=100 BRIEF_SEAT_LEVEL=sonnet bash '.../brief_seat.sh' ..."`. I followed the stamped kits; `BRIEF_SEAT_LEVEL=sonnet` is inside the quotes either way. Say if you want the `cockpit.sh add` form.
4. The commission says the kit stays under about 25 KB. It is 30,150 bytes (down from 34,983 in the first draft). I cut the plants P6/P8, the sibling lists and the duplicate landing text; what remains is the check list.

## Facts re-measured (instrument; control)
- Pins 19:23:32 and 19:26:01: `gh api git/ref/heads/b1144/...` = `bf5b9454e8b853428b1ae8a32b51059499418b14`; main `69b01339237dd4175a1afed249f9537756845188`; `git ls-remote` agrees and shows `refs/heads/b1140/*` @ `57ecad38...`; `refs/heads/b1154*` absent (control: `b1144*` printed one). `compare` = ahead 1, behind 0, one file `+79 -1`. Open PRs by `pulls?state=open`: #91, #86 (dependabot), #85 (draft). `gh auth status`: Datasec 1, Secuura 0.
- Commit `bf5b9454`: tree `0faee59874887c3d9229c7a0e141bf655c3f62cc`, one parent = main; author and committer `...@users.noreply.github.com`; message read whole (one trailer, Claude Sonnet 5.5); `verification.verified` false (unsigned; not a gate item). `check-runs` total 0 on the head (control: 2 on main).
- `F` raw at both shas, `git hash-object`: main `59e7caea...` 2639 lines, 87 `^\s*it\(`; head `50d91dd2f715e6c83cc87e7038851ca9f532b6e6` 2717 lines, 92 (equals the builder's blob). Hunks from `compare` `patch`: `@@ -912`, `@@ -1849,6 +1849,54`, `@@ -2093,6 +2141,36`; the only removed line is the old `F:915` comment (printed).
- Line pointers printed by `awk NR==n`/`grep -n` over the head raw file: `unclosed:` at 677, 693, 704, 716, 733, 772 (same on main); 813, 840, 869, 876-889 (residue comment unedited), 1304, 1846, 2276; rows A1 1855, A2 1870, A3 1885, B1 2144, C1 2158; comments with `(measured)` at 915, 1856, 1871, 1886, 2145, 2159.
- CI predicate read raw at main: `ci.sh:117`, `package.json:21`, `ci.sh:118`, `test-db.sh:58`, `packages/db/vitest.config.ts:9/:11/:12/:13`, `packages/db/tsconfig.json:8` (`"include": ["src"]`, so no CI step typechecks `F`). Blobs at main: `DEPLOY.md` 2e48c823, vitest config d9c74dfd, `package.json` 32fea116 (match B1144/B1108).
- Landing and not-deployed: `CLARIFICATIONS.md:1799` (C-101) printed; `:2247` (C-120 authority), `:2257` (permits a later lane, round count not ruled), `:2262` (round count not settled) printed.
- Round count: loop over all `*_STATUS.md` whose first 3 lines hold `GATE VERDICT` (47 such files) and `pcomp-119|pcomp119|b1144|b1154|deploy-commands-rows|no row kills` = 0 (control `pcomp-118|...` = 1, B1066). Class strings across the 10 verdicts that print one: no earlier NO GO on a class about rows not killing a plant. Nearest: B1085, B1108 (scan class, same file); B674, B682 ("a surviving mutant on the date rule", another file, two NO GO rounds).
- Ports: python (`-I -B`) over 154 non-`.pre-` SEAT kits of 11-01/11-02: 9330-9339 0 hits (control 9320-9329 hits B1151; 9980-9989 hits 5 kits); wide ranges only (`4503-9834` B1031/B1048/B1108, `9000-9999` B1108, `9300-9399` B1151). `lsof` 9330-9339 rc 1 (control 9520-9542 prints listeners). Panes at 19:25: 9 (none Composer); `G296` count 0, control `tuesday` 1. `G296` in the briefs folder: 0 files (control `G293` in 2). Heavy lock `ls -d` rc 1 (control `.tools/b879/scripts` lists); `.tools/b1154` and `wt-b1154-head` absent; load1 7.44/7.10/7.64 at 19:25.
- Builder leftovers `du -sk` 19:26: `.tools/b1144` 5260, `wt-b1144-fix` 13836, `wt-b1144-mut` 22588, evidence 956. Image `pc-b1144-node:head` is RELAYED only (the drafter fence forbids docker).

## D-decisions
- D-1 Template B1108 over B1085 (see BLUF).
- D-2 Tier 2 kept; Q-1 carries the thin spots.
- D-3 Round named as a new lane with its own counter; adjacent NO GO classes are listed in the kit so the stamp can see them.
- D-4 CodeQL **deferred to Tuesday's landing step** on `refs/pull/<n>/head`; the gate records NOT SCANNED (a Condition) and the check-runs/alerts reads on the head ref.
- D-5 The gate writes PR and squash text files only on a GO, as B1108 did, with the B1108 naming rules (no `PCOMP-`, no person, one Sonnet trailer). This differs from the builder kit, which left the squash text to Tuesday; say if you want the gate not to write them.
- D-6 Gate plants are written from source before the gate reads the builder's plant table (the builder admitted its P1-P3 predictions were informed by its instrument). I added two plants the builder did not run: P5 (the per-line half flags line 6: tests the A rows' second assertion) and P6 (a realistic scan fix: ends the open `$(` at a bare `esac`, closes the here-document skip in an open `${`), so B1 and C1 are shown to go red under a fix, not only under the blunt "any `!`" plant.
- D-7 The bash oracle is the gate's own pty; the builder's `pty.mjs` is design reading only. The kit adds a 30-block table of 3 openers x 9 closers for B1's class, because the builder reports that a lone `)` does not make bash fail in the 4-line shape while the ticket's list names it.
- D-8 Grading: the residue list `F:876-889` not naming B1/C1 is Minor (the builder was told not to edit it; whether block B counts against the ticket clause is NOT ruled, `CLARIFICATIONS.md:2262`); the builder's process deviations are Notes.
- D-9 Budget about 20 heavy starts (the B1108 kit allowed 55); READY target 120 and hard stop 180 minutes, suggested in the Stamp.

## Q-questions for Tuesday (each with a default)
- **Q-1 Tier.** Default: tier 2 (G2 `:109`: tests-only, one test path, no product or `DEPLOY.md` byte, nothing a user sees, mechanism measured by two earlier gates). I measured no reason to raise it. Thin spots: the pty claims were measured only by the builder, and the gate re-measures them (D4); the guard concerns operator paste of a psql `SELECT`, not a security surface.
- **Q-2 Which runs first, G296 or G293?** Default: **G296 first.** Reasons: G296 is test-only and short (about 20 heavy starts, each seconds, one cached build; the builder's whole run took under 40 minutes), G293 is a tier-1 PDF render rig with a long matrix and a hog-prone footprint; the lock is project-wide, so a short job ahead costs G293 minutes while the reverse can hold G296 for the whole of the 5400 s wait cap. Both branches are on `69b01339` and touch disjoint paths (renderers vs `packages/db/test`), so landing order does not matter, and the second lander squashes onto a moved main without conflict. G296 is not yet launched and G293 is "drafted, not launched"; the lock is free now.
- **Q-3 Round name.** Default as written: "round 1 of 2, new lane, own counter" (same naming as B1037/B1038/B1066). If you count this lane as a continuation of the PCOMP-98 class instead, B1108 was round 2 of 2 and a NO GO here would go straight to the product owner by G-cap; `CLARIFICATIONS.md:2262` leaves it open.
- **Q-4 Ports and pane.** Default: 9330-9339, none published; pane `Datasec/Security-Composer-G296`.
- **Q-5 Size.** Default: accept 30 KB (every remaining line is a check from your list). If you want 25 KB, the first things to cut are the B1 class table in D4 and plants P5/P6.
- **Q-6 Squash text from the gate.** Default: the gate writes `pr-title`, `pr-body`, `squash-subject`, `squash-body` only on a GO or GO WITH FOLLOW-UPS (D-5).

## Things the gate will find first (for your reading, not decided)
- The builder's A rows assert `[6]` as the union and that the per-line reading lacks 6; if P5 leaves an A row green, the second assertion is vacuous.
- The builder's rows use unique tokens `zqc81a1`, `zqc81b1`, etc. in the file; harmless, but a person-name scan will not see them.
- B1 and C1 pin `[]` for bangs bash fails on; whether they should be numbered in the residue list is not ruled.
- The builder's commit message names PCOMP-119 (the squash text replaces it; the kit forbids `PCOMP-` in the squash text per the B1108 naming rule).

## UNMEASURED
Whether bash fails on the five bang lines (builder's pty only); whether the five new rows are green in the image (builder's runs only); the plant results (builder's table only); the live branches `b10*`/`b11*` vs `F` (the builder read 184 branches; REFUSE/D7 reads it at launch); CodeQL on any ref (no PR); the `fleet/briefs_staged/` port claims; the image `pc-b1144-node:head`; the PCOMP-119 ticket text (the kit quotes the builder kit's quote; D0 GETs it); whether `postgres:16@sha256:f1c3376c...` is local.

## Outside-the-fences disclosure
- Wrote only the kit and this report (plus scratch under the session scratchpad `.../scratchpad/{h,m,ci}/` raw copies of `F` and CI files, and `patch.txt`).
- Read: DRAFTER_RULES.md; the B1144 kit and STATUS; the B1108 kit (template) and the B1151 kit (grep for lock, ports, pane lines only); first lines of the project's `*_STATUS.md` files (47 gate verdicts) and `head -1` of B1085, B1108; B1140 STATUS last line; `CLARIFICATIONS.md` lines 1799, 2072, 2246-2265 and greps; `model-routing.md` lines 91-95, 108-111; `models_latest.json:23`; `brief_seat.sh` lines 21-25; `launch_when_cool.sh` header; the B878 addendum; the QA charter head.
- `gh api -X GET` only, under the Composer `GH_CONFIG_DIR`: refs, compare, commits, check-runs, pulls, contents (raw), about 20 calls. `git ls-remote` read-only. `git hash-object` (no `-w`) on scratch files. `lsof`, `tmux list-panes`, `uptime`, `du -sk`, `ls`. No docker, az, ssh, Jira, mail, hosted host, decision queue, scoreboard, `briefs_staged`, ledger, or non-Datasec tree.
- Two shell slips, both harmless: one `cd` was refused by the hook before it ran (nothing happened); one `==` word in an `echo` was refused by the zsh hook; and two loops expanded an unquoted `$f` containing the project path's space, so a few `head`/`basename` outputs printed "No such file" noise (the counts that matter used quoted `"$f"` and printed correctly; the round-count loop was clean).
- Wrote the project nothing; no git write; no deletion.
