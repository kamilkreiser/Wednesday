STARTABLE: YES (after Tuesday stamps: 8 four-underscore lines, Q-1 to Q-6 to answer)

# B1009 drafter report (SEAT-G248, MPS tier-1 QA gate, V4 engine: groups, tier override, sell basis; round 1 of 2; NO PR)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1009_SEAT-G248_mps-v4-252-258-259-gate-tier1.md` (about 46 KB, 34 lines; unstamped copy reads 8 four-underscore lines, control a scratch line with four underscores reads 1; non-ASCII 0; no person name).

## BLUF
- Gate row G1 (`model-routing.md:108`, cap `:111`), Opus `claude-opus-5-5` (`models_latest.json:37`), `BRIEF_SEAT_LEVEL=opus` inside the launch quotes. Pane `Datasec/MPS-G248`. Ports none; fallback 9450-9459.
- Seven checks: (1) byte-equal when unset, rebuilt, two serializers, purchase AND rental unstripped, path-based member checks; (2) own hand cases for 252/258/259 incl. the 200-seed grouped-vs-ungrouped equivalence and a reconciler tamper test; (3) delta, row O one line, commit 4 text-only proof, new literals equal main; (4) own mutants G1-G10, T1-T6, S1-S8, B1-B8, V1; (5) commit sentences and four squash/PR data files checked by program; (6) CI judged locally (no PR); (7) merge/overlap and LANDING CHECKLIST.

## Facts re-measured (instrument; control)
- Branch `fa2124f1e3b001afd6e986dd69fe88767931e5b6`, main `5d96a3dc62871dd526f34a86215bacf5f7943ad6`: `git ls-remote origin` read-only, plus `gh api -X GET git/ref/heads/main` = same main. `rev-list --left-right --count` = `0 4`.
- `diff --numstat main head`: 9 paths, sum +571 -17, exactly Tuesday's list. Removed lines: `src`/`docs` 17 (the filter lists them, so the filter fires), `tests` 0. All four test files are NEW at main (`ls-tree` 0 each). Commit 4 (`8737ef5..fa2124f`): ENGINE.md 1/1, PurchaseResult.cs 1/1, Api file 67/0, SectionPricingMethodTests 4/1 (row O).
- `ci.yml` blob `212b0da1...` equal at main and head; job at line 31, `timeout-minutes: 20`, build line 42, test line 43. Register: X-35/X-36/X-37 1 each at head, 0 at main (control X-34 1 at main, 2 at head).
- Squash settings: COMMIT_OR_PR_TITLE / COMMIT_MESSAGES. Open PRs 121, 120. No PR for the branch (`pulls?state=all&head=` length 0).
- Round count: 289 `*_STATUS.md`, 66 first lines `GATE VERDICT`, 0 name b1000/252 (control B988 line with `b974` = 1). NO GO 0 before; the B980/B988 class is a different class.
- Ports: 945x: 0 kit files of 232 scanned (10-30..11-01, non-`.pre-`), `lsof` 0 rows; controls 948x = 7 kit files, unrestricted lsof 14 rows. Decades 954x-979x all had kit hits.
- Panes: tuesday, HPSM-POC-R101, HPSM-POC-H88, fleet-monitor: no MPS seat live. `G248`/`B1009` 0 files; `.tools/b1009`, `.tools/wt-b1009-*`, heavy slots, `.git-lock` absent (control `.tools/b1000` etc. list).
- Commit messages read whole. Source facts that shaped the kit: builder STATUS DESIGN says the reconciler mirror takes the RECORDED basis when a line's percent equals the section's, but commit 3 says "The reconciliation applies the same rule from the input" (made a graded sentence and a tamper test); the margin error text is re-emitted with a computed field path (made a byte-for-byte literal check); `checked(N x q)` throws on overflow (graded Note, unreachable from the Api); member-name greps would be wrong because the purchase line already has `PricingMethod` and rental `TierOverride` (path-based checks).

## D-decisions
- D1 Tier 1/G1 by B980/B988 precedent (the G1 row text does not literally name money figures; see Q-1).
- D2 No-PR form from B1003: the gate writes `pr-title.txt`, `pr-body.txt`, `squash-subject.txt`, `squash-body.txt` from its own counts, program-checked, plus a LANDING CHECKLIST and the exact merge line.
- D3 Row O is judged on the commit-3-to-4 delta, because versus main no test line is removed at all (all four test files are new at main).
- D4 The coordinator's design call (line's own margin wins; no opt-back) is stated in the properties as a design choice (Note if the register row says it, Major only if code contradicts the row).
- D5 No gate-side Api src byte: the Api-leak mutant V1 lives only in the mutant tree.
- D6 Target verdict 4 h, hard stop 6 h (about 40 mutant builds, two full CI lines, two-serializer harness at both ends); priority cut order stated.

## Q-questions for Tuesday (each with a default)
- Q-1 Tier 1 for a money-figure gate although the G1 row names security/deploy/client surfaces. Default: yes, tier 1 (B980/B988 and the ticket labels `tier-1`).
- Q-2 Ticket keys in the PR title and squash subject. Default: MPSCALC-252/-258/-259 MAY appear there (as #133's title did), never in the bodies, and the title must say "engine half".
- Q-3 Reconciler recorded-basis limit: default Major only if a tampered line passes where the input alone fixes the method (no catalogue percent), else Note.
- Q-4 Pool-less line stays at Core under the override. Default: Note if the register row says so and a quote without the override equals main; Blocker only if the no-override figure moves.
- Q-5 Hard stop 4 h target / 6 h stop. Default: as drafted.
- Q-6 Port block: none needed; fallback 9450-9459 (the only clean decade near the used range).

## UNMEASURED
Nothing built or run: no compile, test, mutant, harness. SDK version 10.0.401 is RELAYED from the builder STATUS. Builder numbers (471/193/3165, 22 harness files, MU results, 3 `D-0x` register citations) are claims. Whether the new Api test is timing-free, whether the Api maps or returns the engine result directly, and the real tier thresholds (R-03) were not read for numbers: the kit tells the gate to derive them. Two PRs' file lists (121/120) are RELAYED from the B1000 kit and re-read by the gate. Not read: `fleet/briefs_staged/`, the scoreboard, the ledger, `Source_Documents/`, `inbound/`, `.local/`, any card store.

## Outside-the-fences disclosure
None breached. Read-only git verbs with `--no-optional-locks` on the code repo (ls-remote, log, show, diff, cat-file, ls-tree, grep); `gh api -X GET` under the project `GH_CONFIG_DIR` (repo settings, open PRs, PR search, main ref); `tmux list-panes`, `lsof`, `ls`. I wrote two small helper scripts in the session scratchpad (`scan.sh`, `scan2.sh`, `scan3.sh`, `kits.txt`) for the port and round-count scans. Only the two output files are in the project.
