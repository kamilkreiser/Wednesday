STARTABLE: YES, after the stamp. The kit is complete and every slot is an unfilled `____` (8 lines, the unstamped control); nothing in it is blocked by the live state at 20:47 AEDT. It runs 37.7 KB, over the 35 KB target (see D6).

# B1156 drafter report (SEAT-G298, HPSM-POC tier-1 gate, round 1 of 2, class "remediation register read and refusal rules")

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-02_B1156_SEAT-G298_hpsmpoc-424-425-register-gate-tier1.md`

## Contradictions with the commission (first)
1. **Commission says "your OWN plants written before reading the builder's plant table", and the 424/425 builder's plant table is in the builder KIT as well as its STATUS.** The gate seat must read the builder kit for the stamped WORDS (kit lines 102-104). I made the order explicit: WORDS are read from the kit by program in step 2b; `plants-own.txt` (sha256 and clock) is written and printed before the builder STATUS "TESTED" section or the kit's plant table is read (step 4, then step 5). I read both before drafting (I had to, to draft); the gate seat is the one that must be blind.
2. **Commission: "ports (free block by lsof and a scan of the 11-01/11-02 kits)".** No block in 9610-9899 is free of kit mentions (every block has 1-13 hits, almost all finished seats' reservations or ranges). The gate needs no listener (jsdom, in-process), so the kit says **ports none**, with 9650-9659 as a reserved fallback (lsof 0; one kit hit, B1051's own fallback, a finished gate, no pane). If you want a hard block, 9650-9659 is the cleanest.
3. **Commission: "Tuesday's ruling on hold 1".** Recorded verbatim in step 5. Re-measured from the builder's STATUS: its PN count is 6 red and **includes R5, R6 and a screen row**, not only R13. Those fixtures hold Not started entries with empty evidence, and PN makes them fail; so PN reddens the drop rows for a second reason. The kit tells the gate to print it by name and to say whether "Not started/In progress unchanged" is pinned unambiguously.
4. **Commission: "the HPSM-POC heavy slots and hv.sh pattern".** The pattern is `.tools/b1131/hv.sh` (slot `heavy-slot-N`, 2-minute heartbeat read), not `.tools/b1113/hv.sh` (a different, `heavy.lock`-based script that the builder used). I pointed at b1131's. `heavy-slot-1` is held right now by another seat (`B1147 20:34:23 census-prev`).
5. **Commission: "the squash form: find it in the analysis repo's CLARIFICATIONS and print the line".** The local `1_Project_Definition/CLARIFICATIONS.md` is a stale 192-line copy that holds the phrase once and no line 3617. I read the real file by `gh api` raw (5371 lines): `head-pinned squash` count 97 (control 0), line 3617 begins "The landing form is a head-pinned squash...". The kit says to print yours from the API.

## BLUF
The gate has seven measured steps. The new ones that matter: (2a) 424 is drop-only by a **whole equals merge-of-singles** differential over 5000 fixed-seed registers plus main-vs-head regression guard and a **round trip** (does head ever drop what its own save wrote); (2b) 425 is the same predicate by a **full code-point sweep** (1,112,064 cells x 4 states, alone/tripled/with `a`/spaced) with the empty cell, byte-equal sentence by sha256, and field-priority combinations; (2c) the **data-loss behaviour measured**: six scenarios incl. main's own saved entries read by head's parser (the entries main could write that head now drops) and a 40-entry case (main loses 39, head 1); (2d) the **visible-text set** by TypeScript compiler API plus a rendered main-vs-head differential. Plants are the gate's own (cap 24, property first) and written before the builder's table is read. Landing is a head-pinned squash pinned to `8bc72bb1...`; the ruleset has NO required status checks and strict policy false, so Tuesday reads `refs/pull/N/head` checks; CodeQL threshold errors.

## Facts re-measured (instrument, time)
- Head ref `8bc72bb1a66c37ac30ea184bbe1cafc568c620ad` (`gh api git/ref`, 20:36:37 and again later). Main `491348ed0cb409ed98228118f3c9a7f43fde7b4b`. `compare 5f128fb8...head` = ahead 2, behind 0, 3 files, +/- exactly as the commission (+159 -25, +18 -9, +43 -0). `compare main...head` = diverged, ahead 2, behind 1, merge base `5f128fb8`.
- PR #276 paths (`compare 5f128fb8...main`, 4 files): `api/src/.../SqlServerWakeRetry.cs`, `NarrativeOutputValidator.cs`, two `api/tests` files. **None touches the branch's three paths.** The REFUSE regex over that list prints 0 (control 1).
- Blobs: `RoadmapScreen.tsx` `a115a3ef729c` and `partner/browser-store.ts` `ff2e5e3f2a59` are equal at main and head. `remediation-store.ts` blob `971f67fb453a` (main) to `db4187388203` (head).
- `SHOWS_NOTHING` regex is byte-identical in both trees (sha256 prefix `caa4f84805b3`); `node` sweep over all non-surrogate code points: 4199 matches alone (4174 non-white-space) and the empty string; equals B1005's 4199.
- Head code (`awk`/`grep -n` over blobs): `parseRegister` `:84 continue`, `:80` still returns null for a non-object customer; `checkEntry` table `:28-31`, lookup `:48-49`. Main `:75 return null`, sentence `:41`.
- Round count: frame 581 `Briefs/*_STATUS.md`, 15 mention `remediation-store`; last-line verdicts B963/B989/B1005 GO WITH FINDINGS, B1022 NO GO (class "customer security preview, part B", reads the store). Control: B1107 last line prints as a NO GO. NO GO on this class: 0. (My first loop used `head -1 | grep NO GO` and mis-counted "NO GO 0 before"; I redid it on the last `VERDICT:` line.)
- CI: `web-build` `:371` (audit-dev `:395`, lint `:396`, typecheck `:409`, build `:413`, check-shards `:426`), `web-unit` `:450` `npm test` `:478`, `web` aggregate `:526` passes iff results == {web-build, web-unit, web-e2e} all success (`:540`, `:543`). Ruleset: required_status_checks empty, strict false, code_scanning CodeQL errors, non_fast_forward, deletion.
- Ports: `lsof -nP -iTCP:9500-9999` shows listeners only at 9520-9522 and 9540-9542. Kit scan: 158 non-`.pre-` SEAT kits of 11-01/11-02. Hits by block: 9610 3, 9620 2, 9630 3, 9640 2, 9650 1, 9660 1, 9670 3, 9680 2, 9690 1 (all others 2-13). Controls `960[0-9]` 5, `959[0-9]` 3.
- Panes at 20:36: tuesday, MPS-M80, NexusAI-G295, NexusAI-G297, Security-Composer-G296, HPSM-POC-G291, HPSM-POC-G288, fleet-monitor. No H106, no G298.
- Disk 278358868 KiB available (265 GiB); load1 5.87, 7.18, 8.29 at 20:36. Builder trees exist (`.tools/wt-b1145-fix` at `8bc72bb1`, porcelain 0; node_modules 368 entries; lock blob `81393fd7` both sources).
- Builder commit messages read (`git log -n2 --format=%B`, read-only): the two bodies make the claims the gate must check (18 of 92 / 27 of 119 red).
- Builder STATUS sha256 prefix `c6ea4c2a86a70801`, 95 lines; last line begins `READY FOR QA: B1145 ... @ 8bc72bb1a66c37ac30ea184bbe1cafc568c620ad`.

## D-decisions
- D1 Landing tree = a commit OBJECT (`commit-tree` of `merge-tree --write-tree`), no ref written; the suite and the plants run on it, base on main. Two worktrees, one clone. Reason: judge the landing tree; the web files cannot be affected by PR #276's api paths, but the kit says to prove it.
- D2 No new node_modules install: `cp -Rc` from b1113's tree, else b1145's tree, with the lock-file blob as control; both gone is a STOP.
- D3 Round 1 of 2: a NO GO writes `fixlist.md` (plain-words paragraphs), not the cap.
- D4 Severity: a sentence off by a byte is a Blocker; Evidence submitted vs Verified complete disagreeing on any sweep cell, or Not started/In progress differing from main on any cell, is a Major; data loss beyond one entry per failing entry is a Major.
- D5 Equivalent mutant c7 (untrimmed test of the same predicate) is planted on purpose; 0 red is the expected answer and the gate must say why.
- D6 Size: 37.7 KB against the 35 KB target. I cut twice (about 2.5 KB). What remains is the sweep/differential specification and the plant list, the two parts that carry the verdict; I would not cut them. The template is 20 KB and covers one narrower mechanism.
- D7 The squash subject begins `HPSMPOC-424 HPSMPOC-425` (main's own recent subject has the key); the KIT text itself carries no card id and no person's name (the two `HPSMPOC-` hits are the ticket keys in Limits and the subject rule).
- D8 N2 (`RoadmapScreen.tsx:75` names only Verified complete) and N3 (the security view reads the same store and shows the same drop) are Notes to carry, not findings; N1 is the measured count of main-saved entries that head now drops.

## Q-questions for Tuesday (each with a default)
- Q1 Size over target: accept 37.7 KB? Default yes.
- Q2 Ports: stamp "none, fallback 9650-9659"? Default yes.
- Q3 Is the builder's use of the first name `Sam` (new, one fixture row) a finding? Default Note, as written in the kit.
- Q4 Should a NO GO round 1 here stop at `fixlist.md`, or may the gate also write the four landing files for the parts that pass? Default fixlist only.
- Q5 `RoadmapScreen.tsx:75` words: left as a Note for the product owner. Default yes (the commission says the file is untouched and no other word).
- Q6 The gate is told b1113 may be gone; if both node_modules sources are gone the gate STOPS rather than `npm ci`. Default STOP (no install was authorised for the builder either).

## UNMEASURED by the drafter
Every test outcome; hosted CI; CodeQL; whether `.tools/wt-b1113-fix` will still exist at launch; whether `heavy-slot-1` is free at launch; the harness scripts (the gate builds them; I did not run any vitest, build or plant); the 5000-register and 1,112,064-cell sweeps (specified, not run; only the regex-alone sweep of 4199 was run); `b1113` and other live branches' file lists (the gate recounts at Step 0); the Jira ticket texts (read through the builder kit's quotation only); the two SecurityRoadmap tests.

## Outside-the-fences disclosure
- Read-only reads of the project's tree: builder STATUS and kit; `.tools/b1131/{hv.sh,sampler.sh,gl.sh,plants.py (head 30 lines),names.py (head 15 lines),co.sh,landing.sh,lock.sh}`, `.tools/b1145/{heavy.sh,lock.sh}` listings, `.tools/b1113/hv.sh` header, `heavy-slot-1/holder`; the builder's worktree `.tools/wt-b1145-fix` by `git rev-parse`, `status --porcelain`, `log`, `hash-object` and `grep -rn` over `web/src` and `web/e2e` (read-only; a worktree, not the checkout); `node_modules` listing counts and `node24 --version`; `node` over two scratch regex files. These tools and trees are named in the B1145 and B1131 kits as the builder's/gate's own; reading them was needed to cite pointers.
- `grep` over local `1_Project_Definition/CLARIFICATIONS.md` (stale) and one `git remote -v` there, then the real file by `gh api` raw, all `-X GET`.
- Scratch files (not project files): in `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/0c50bece-7f27-4991-9384-67c716dfc1fe/scratchpad/`: fetched blobs of the five web files at both shas, `ci.yml`, `clar.md`, `kits.txt`, `kitpaths.txt`, `moved.txt`, `sweep.js`. No project file written, no ref written, no deletion, no network write, no mail, no Jira, no az/docker/ssh, no `cd`.
- I used `gh api -X GET` for `rules/branches/main` and `pulls?state=open` (read).
- No decision-queue, `fleet/briefs_staged/`, scoreboard, `_ledger.md` or WEDNESDAY/FRIDAY tree was read.
