STARTABLE: YES (after you stamp the eight slots; Q-1 and Q-2 below are stamp decisions with defaults, not blockers; a CodeQL wait is built into C4)

# B828 drafter report: gate kit for PR #98 (Composer, date-rule closing rows), seat G175, tier 2

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-27_B828_SEAT-G175_composer-98-date-rows-gate-tier2.md` (89 lines; `.pre-stamp` copy beside it, `cmp` equal; four-underscore line count 9, non-ASCII 0). Drafted 14:18 to 14:22 AEDT (clock `date`).

## BLUF
- The kit gates PR #98 head `c6246c671985426d323f5acf74500f0e9835435b` on main `8df52332e52bf520633317120c563a16387d1a13`, Sonnet, tier 2 (row G2 `model-routing.md:109`; G-cap `:111`), round 1 of 2, ports 9520-9529, pane `Datasec/Security-Composer-G175`, `BRIEF_SEAT_LEVEL=sonnet`.
- Heart of the gate is C2: the gate writes its own 15 mutants of `app.ts:105` (plus its own further shapes, FLg/FLy/IX2full regression, controls c0-c4) and quotes the failing assertion per red row, so "each row reaches the check it is named for" is shown by a `500` pass-through, not assumed. The builder's 47-mutant driver is read-forbidden.
- Re-read at 14:18: both pins match what you gave (head `c6246c67`, main `8df52332`, ahead 1 behind 0, one path +26 -0). CodeQL is NOT done: two runs listed, both `in_progress`, and no `CodeQL` run in the list yet. C4 waits (60 s polls, 40 min cap).

## Q-n questions (stamp decisions; defaults given)
- **Q-1 ports.** You wrote "0 kits" for 9520-9529. My whole-word scan of the non-`.pre-` `2026-10-2[67]_*SEAT*.md` kits found **8 kits** that name the block (B736, B737, B738, B739, B741, B742, B747, B761; all 2026-10-26, finished seats; one says the then-live Composer builder J21 held 9520-9529, others list it as another repository's range). `lsof` rc 1: no listener. Default in the kit: old kit mentions are not a refuse; only a listener or a live non-J26 pane claiming the block is. Accept, or give another block (this seat publishes no port).
- **Q-2 round count.** B674 and B682 (PR #92) and B626 (PR #88) already judged "a surviving mutant on the date rule"; the kit counts this as round 1 of 2 only by the coordinator's 13:0x ruling recorded in the B822 commission. Default: accept, with the cap sentence in ROUND COUNT. Confirm at the stamp.
- **Q-3 PR title.** The title is `PCOMP-103: date rule test rows ...`; the squash subject will carry the Jira key while the commit message does not. The kit grades it a Note (your edit before landing, suggested words match the commit title). Say so at the stamp if you want it a Minor.
- **Q-4 scope of the `m` flag.** The builder reports flag `m` green under both files. The kit lets the gate measure ONE line-break value and file it as a Note under FOR TUESDAY, never of the class. Default: yes. Strike C7's last sentence if you do not want the probe.

## UNMEASURED (by me)
No vitest, container, image build or mutant ran. Not measured: whether the four rows are green at main's product; the 13 red/green table; the group counts 81/1522 and 81/1526; unit chain; the load (`uptime` not read); whether a contract-layer refusal could pre-empt `DATE` for any of the four values (the kit has the gate answer it from the `500` assertions); the head's test blob and the three package/app blobs (REFUSE 5 relays the builder's, I did not re-read them with `rev-parse`); the `CodeQL` check run's existence (not yet listed); the open-PR file lists (#95, #91, #86, #85: relayed by the builder, I did not list them); the 26 branch compare (builder's claim); a listener control for 9520-9529.

## Facts relied on but not read at source
- The four blobs in REFUSE 5 (test `9bc0a71e...`, `app.ts` `2c5d5ad1...`, `package.json` `32fea116...`, `package-lock.json` `53305eb4...`) come from the B822 commission and STATUS. I read `app.ts` lines 100-128 at main and the test helper lines at the head by `git show`, but did not hash them.
- The builder's table, counts and the `m`-flag / QDst / `contract.ts` notes are its STATUS claims; the kit marks them RELAYED.
- Round-count frame (240 STATUS files, 30 gate first lines, hits B626, B674, B682) is my shell loop at 14:19; the class text of B674/B682 was read only from their first lines and B682's last line (`NO GO round 2 of 2; ROUND CAP reached`), not the bodies.
- The coordinator's 13:0x ruling is quoted from the B822 commission (line 11) and its Stamp, not from the wave-1 common file.
- Pane list from `tmux list-panes` at 14:18: `%71 NexusAI-G174, %70 NexusAI-M22, %69 Security-Composer-J26, %68 MPS-M47, %67 MPS-M44, %66 MPS-M40, %62 NexusAI-M21`. J26 is the only Composer pane.
- Model row G2 text read by `sed -n 109p` (proposal wording: "Whether a Sonnet G2 MISSED anything: unmeasured"); `levels.sonnet.model_id` = `claude-sonnet-5-5` taken from the B822 kit's quote of `models_latest.json` lines 23 and 38, not re-read.
- B827 (tier-1 NexusAI) was read by its section headings only; the shape came from B815.

## Read
B822 builder kit (112 lines) and STATUS (147 lines) whole; B815 gate kit whole and its drafter report in part; B827 headings; `model-routing.md` G2, G-cap and tier lines; the PR #98 object, compare, commit message and check-runs (GET); `git diff` of the head vs main (read verbs); Composer `CLAUDE.md` (first 70 lines; it carries no test command, the commands live in the builder kit and `scripts/ci.sh`/`test-db.sh`, which I did not open); CLARIFICATIONS line 1799 (printed truncated, the sentence matches what B815 quotes); `.tools/b822/scripts/heavy.sh` (read to copy the load-gate shape; the gate may not use `.tools/b822`).
