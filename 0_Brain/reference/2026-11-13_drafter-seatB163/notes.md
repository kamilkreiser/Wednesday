# Drafter notes: Seat B 163rd brief (drafted 2026-11-13 about 01:40 to 02:2x AEDT)

Output: `brief_B163.md` (about 46.9 KB; the commission said ~45 KB; STAMP block blank, no SELF-CHECK line). Nothing written outside this folder, except the session scratchpad (`rc163` scratch clone, `moved_*`, `own_*`, `body_*`, `census163.json`, `cr_*`).

## B 162nd's measured meter readings (kit meter, 1M window; from its HANDOVER FINAL block and wrap mail)
| point | reading | delta |
|---|---|---|
| first read | 14.9 | |
| PLAN | 24.4 | +9.5 |
| SET-UP CLOSED | 31.4 | +7.0 |
| READY 2219 built (same-file product row, PR 2052 overlap proof, 17.7 KB READY) | 42.9 | +11.5 |
| MERGED 2219 sent (r) | 48.7 | +5.8 |
| READY 2217 built (test-only, no suite, no overlap, 9.8 KB lean READY) | 54.8 | r + 6.1 |
| MERGED 2217 sent | 57.5 | READY2 + 2.7 (r + 8.8) |
| wrap start | 59.8 | +2.3 |

**Pricing a second row by SHAPE.** The seat's STATUS 1 forecast for a second row was 59.6 to 67.9 after its send, priced from earlier second rows that were PRODUCT rows with a suite (+6 to +12 to the READY). The measured cheap second row (2217: one commit, no suite, no install, no same-file overlap, a tsc leg reproduced with no new install, a lean READY, kit warm) cost +6.1 to its READY and +8.8 to its MERGED send, below the low end of the forecast. Wednesday's ANSWER already made this argument (its item 1: the +11.5 of the first READY came from what 2217 did not have). For 2178 (one file, one test title, no fragment pair, no suite, no tsc leg) the brief prices about r + 6 to its READY and r + 9 in all, and says so as the drafter's estimate, not a rule change. Arithmetic for the stamp: at r = 48 to 51.9 a cheap second row's READY would land at 54 to 58 (under the 58 tripwire) and its send at about 57 to 61; the second-row bands themselves are unchanged in the brief (carried from B 162nd's stamp item 1).

Twelve first-MERGED readings now: the earlier eleven sum 606.5; adding 48.7 gives 655.2, mean 54.6; two of twelve are at or under 50 (B 160th's 49.2 and B 162nd's 48.7).

## Gate coverage found
Method: for every `verdict.md` under `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/` (601 scanned), read line 1 and matched 'PR 2208', 'PR 2207', 'PR 2178', 'PR 2184', 'PR 2218'.
- **2208: gate 330** `2026-11-12_gate330-tier2-pr2208/verdict.md`, `PR 2208: GO WITH NOTES (at head 44457d12eaa1; tier 2)`.
- **2207: gate 328** `2026-11-12_gate328-tier2-pr2207/verdict.md`, `PR 2207: GO WITH NOTES (at head 0d82e65bc5be; tier 2)`.
- 2218: gate 342 (read whole).
- 2178: none (hygiene by ruling). **2184: none either** (the commission lists it as product, needing a splice table and a stamp ruling; the scan confirms no gate exists).
Both heads equal their gate pins today. Gate 328 ran across a develop move (G328-2207-1) and measured on the old tree; its own merge-tree on the moved develop (`d390c397`) reproduces exactly as `d390c397ee1d` in the scratch clone. Gate 330's merge-tree `e7ed9cd4b587` against its develop `581296f039b4` reproduces too. Extra finding on 2208: its head has 20 check-runs, 12 failing (the extra one is `Standalone locks pass clean-room npm ci`), where the other four heads read 19 and 11; this is in BLUF 11 and the row text.

## Things I could not measure, or that disagree
- **FOUR vs TWO differing kit tools.** B 162nd's wrap and HANDOVER say four tools differ from v3 by program; its HANDOVER names only `merged_build` and `run_merge`. My hash run of all 31 manifest lines against `tools/` finds exactly those two. The brief says so and asks the seat to state its own count. v3 prefix `14e94642f20131c9` matches.
- The `docs-fragments` tool was not run: the brief gives plain `git ls-tree` file counts (develop 360 / 355; pair-adding merge trees 361 / 356) and a DERIVED tool count (241 on develop, 242 with a pair), labelled derived.
- No suite, install, build, tsc or audit was run (scratch clone has no checkout and the drafter wrote no worktree): governance 21 / 371, sdk build, audit:locks, ts equality are all the gates' figures, not mine.
- Only develop-side planted conflicts were run for 2178, 2208, 2207, 2184; PR-side plants were run only for 2218 against PR 2099 (line 606 rc 1/1, line 20 rc 0/0).
- Launcher preflight, inbox, mail after 01:4x (any GO or gate round for 2099, 2052, 2200, 2201), pane owners, `git worktree list`: not measured. tmux at 01:39: only %0 and %1 (the commission's %160 and %161 no longer listed).
- Re-key token counts for 162 -> 163 not measured (own-source set definition is the seat's).
- KS-961: a Linear lookup by number returned a different team's ticket (PS-961), so it was NOT read; the brief carries it with its source (B 162nd's brief line 14) and says so in PROVENANCE. All other keys named in the brief were read at Linear and read In Progress (KS-1964, Backlog, was read but dropped from the brief to save bytes).
- KS-1959's Linear title (revoke() swallowing a failed DB UPDATE) and PR 2184's title (the vc-issuer database probe reading a thrown value's message) describe different functions; flagged in the brief for the stamp ruling.
- Usage gauge (B 162nd's stamp item 12, 81%) not re-read; omitted.

## Notable measurements (all in the brief with instruments)
- develop `cf6a56fb69ff` has ONE parent `405ae16bd573`, tree `86d66c29cf1e` = B 162nd's expected; its tree for 2218, `dabf902295b5`, and the chain value after 2218 for 2178, `9e402b145674`, equal B 162nd's synthetic chain controls (the real chain happened exactly as synthesised).
- No queued row shares a path with another or with develop's move, so no `UNION=` field is needed (B 162nd's slip does not apply).
- 99 open PRs; only PR 2099 shares a path with a queued row (2218, `governanceService.ts`); 2218 vs 2099 reproduces gate 342's `825f70fefb78` in both orders; no open PR has been updated after 13:00Z 12 Nov.
- Slips of mine: a first `rm`-style call and two zsh word-split calls were refused by hooks (re-run under bash heredocs); the scratchpad already held a prior drafter's `rc` clone, so I used a fresh `rc163` and touched nothing of the old files.
