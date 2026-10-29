STARTABLE: YES (after Tuesday stamps the 7 slots and the last line; nothing in the facts blocks a launch now)

# B912 drafter report (kit: 2026-10-30_B912_SEAT-G209_nexusai-143-round2-roster-gate-tier1.md, 106 lines)

Drafted 2026-10-30 00:45 to 00:58 AEDT. Template: B906 kit + ADDENDUM-1 + B906 STATUS. Claims source: B911 STATUS and kit.

## BLUF
- Round 2 of 2 = the cap. The kit makes a second NO GO a STOP to the product owner with the CLOSED list + residue as ticket text and says so in G-4 and FOR TUESDAY. It tells the gate to FINISH every check even after a Blocker (round-1 ADDENDUM lesson), so the residue is complete.
- Head `802c0cfc` is live and unmoved at 00:45; the hosted merge ref WAS recomputed this time (`7d804e15`, over main `436a1bfb`, tree `2f87d7d2`), so the gate's own merge tree should equal the hosted tree (round 1 could not).
- The kit's heart is C4 (the round-1 differential re-run by the gate's own instruments on the new head, with the old pick as a control that must fire) and C6, a dedicated attack on D3b (the fallback's own roster read), as asked.
- Hosted: Analyze x3, CodeQL, scan, audit, Gitleaks green on `802c0cfc` with 3 analyses at 0 results; `build` still in progress (started after the merge ref, so it judges `7d804e15`).

## Facts re-measured (instrument; control)
| fact | value | instrument | control |
|---|---|---|---|
| head / branch / PR head | `802c0cfc` all three | `git ls-remote` read verb under project repo, 00:45:42 | `b895*` prints the branch; `b912*` / `b906*` print nothing |
| main | `436a1bfb` | ls-remote | compare `be13993a...436a1bfb` = the two rd407 tests |
| merge ref | `7d804e15`, parents (`436a1bfb`, `802c0cfc`), tree `2f87d7d2`, committer 13:41:56Z = 00:41:56 AEDT | `gh api -X GET git/commits/<sha>` | n/a (parents order read) |
| PR state | open, draft false, mergeable true, `unstable`, commits 2, changed_files 3, +707 -131, only open PR | `gh api -X GET pulls/143`, `pulls` | the body carries a Round 2 section (read) |
| delta | `compare 747f437b...802c0cfc`: ahead 1 behind 0; test +219/0, server.js +67/23, counts +2/2 | compare `--jq` | equals the builder's claim |
| blobs | server.js head `95ca9125`, main `312c352e`; test head `72865772` | `contents?ref=` `.sha` | main's server.js equals round-1 base blob |
| counts | main 5224/310; head and merge ref 5262/311 (= +38 cells, +1 suite) | raw contents parsed by `python3 -I` | main differs from head (not a degenerate read) |
| hosted checks on head | Analyze x3 / CodeQL / scan / audit x2 success; `build` in_progress since 13:42:03Z | `check-runs --paginate` | the build start follows the merge ref's committer date |
| analyses | 3 rows at `802c0cfc`, results 0, error empty; 3 rows at `747f437b` | `code-scanning/analyses?ref=refs/pull/143/head` | the older head's rows exist (non-empty read) |
| deploy switch | variables 0; environments [dev] | GET | n/a |
| round count | 96 STATUS files, 33 gate verdicts, 4 NO GO (B592 B647 B667 B906); only B906 is this class | first-line loop (`case "$l" in "GATE VERDICT"*`) | B909 (a gate on another PR) read GO WITH FOLLOW-UPS, not counted |
| model | `claude-opus-5-5`, `models_latest.json` line 17; routing G1 line 108, G-cap line 111 | `sed -n`, `grep -n` | the sonnet row is line 23, distinct |
| ports | 9970-9979 free, lsof rc 1 | `/usr/sbin/lsof -nP -iTCP:9970-9979 -sTCP:LISTEN` | unrestricted listing shows `*:7000` |
| port scan | 8 hits among 29 non-`.pre-` SEAT kits of 10-28/29/30, each naming 9970-9979 as the closed G205's block or a scanned range, none a live claim | word-boundary regex via `xargs grep` | `995x` hits 3 kits |
| panes | `tuesday`, `fleet-monitor`; no NexusAI pane | `tmux list-panes -a -F '#{@cockpit_name}'` | G209 hits 0 kits (name is new) |
| lock tool / fence | `cf01bafb...971f` / `55eaafcb...b55f` | `shasum -a 256` | equal to B906's values |
| instruments | the 10 b906 files hashed (prefixes in the kit); `extract.py` has 0 mentions of `pickUserCapture` | `shasum`, `grep -c` | the zero is expected (old code), so the kit says to rewrite the head side |
| landing rule | C-190 item 2 at `CLARIFICATIONS.md:2067`, C-68 `:665`, C-224 `:2412`, Analyze wait `:2073` | `/usr/bin/grep -n` | lines match the B906 kit |

## What I read in the D3b hunk (patch, whole) and what the kit attacks
- `generateUserActivityAnalysis` now does `candidates = userNameCandidates(query).map(dropLeadingMe)`; reads `getAllPrinterLogs({limit:1000})` only if `candidates.length>0 && !candidates.some(isBaseValidCapture)`; on throw it logs the warn line and `rosterNames` stays `uniqueUsers`; the lookup below reuses `rosterLogs ||`.
- Things the kit makes the gate test, not trust: (1) read counts summed and split across the main lookup and fallback, base vs `747f437b` vs head; (2) a read when a base-valid candidate exists (should not happen); (3) first/second/all-call failure arms incl. a non-array and null-row stub (if `rosterLogs` is set to a non-array the reuse in the lookup would call `.map` on it; I did not execute this, it is a source suspicion the kit lists); (4) `contextData.allLogs` caller census (builder says never set); (5) whether the shared read closes round 1's pick/resolve window split; (6) the warn text and what the Azure path could throw; (7) mutants MZ (read on every candidate-bearing message), MT (reuse removed), MD (typeof guard removed), MU (two-hit rule replaced).
- Ruling check: the product owner's 2026-10-29 comments on RD-870 (as relayed by B906 STATUS line 64) say the sibling takes the same capture and guards; so a strict-hit answer in the fallback is graded Note (ruled), a different user than base for a base-valid capture or a group question answered as one account is not.

## D-decisions (mine, for Tuesday to veto)
- D-1: Round 2 mutant set = round 1's nine + MX MY MQ MV (as asked) + four of my own on D3b (MZ MT MU MD); read-count-only or class-only survivors are Minor, a survivor that changes who is reached is Major (G-3 table kept).
- D-2: The fresh trees: clone, base, gate and a fourth tree `b912-r1` at `747f437b` (needed for the "old pick" control and the round-1 closed-items-still-closed differential). Budget rises to four `npm ci`. Target verdict 240, hard stop 330 minutes (round 1 used 210/300 and overran in practice).
- D-3: Instruments: the user said write fresh or copy from `session-tools/b906/instrument/` with cmp + sha256. The kit permits ten named files from there (not the whole directory), says they target the OLD function names, and requires a rewritten head-side extractor. It forbids `worktrees/b911-*` and `session-tools/b911/`.
- D-4: Grading additions: two-distinct-hits rule showing a user = Blocker, differing from base on a pair = Major; a fallback roster read when a base-valid candidate exists or the fallback is not reached = Major; failure path leaking rows or connection text reachable by a request = Major.
- D-5: The M4 rule was kept but sharpened: PR #144 (the M4 fix) has landed, so a hosted red there is NEWS to name, not base-rate noise.
- D-6: ADDENDUM-style instruction is built in (finish every check after a Blocker), so no mid-run ADDENDUM should be needed under the cap.
- D-7: Landing command written for `802c0cfc` with the same preconditions as B906's section; the recomputed merge ref lets the gate hold the "judged by build" fact exactly (verify via the job's checkout line).

## Q-questions for Tuesday (each with a default)
- Q1: Does a NO GO at the cap also need the gate to name which residue items the product owner could take as follow-up tickets? Default: yes (the kit asks for it in G-4, one line each).
- Q2: The builder's F2 (two-word names answered under the full name in the fallback) was left unruled by the builder. Should the gate grade it Note? Default: Note, pre-existing since `747f437b`, wording only in the not-found quote.
- Q3: Is a third gate round past the cap allowed if the gate finds only Majors the product owner could accept? Default: no, per `model-routing.md:111` (the product owner's word on a card).
- Q4: The builder pushed a commit with the Sonnet 5.5 attribution trailer; the kit does not grade the trailer. Default: Note ("the author field").
- Q5: Port block 9970-9979 reused (the closed round-1 G205's). Default: use it; fallback is 9980-9989 only if a live kit claims it at launch.

## UNMEASURED (by me)
- The hosted `build` conclusion (in_progress at 00:46) and any alert on the merge ref; CodeQL results on the added lines beyond the 3 analyses at 0 results.
- Any runtime behaviour: I read the patch only; I executed no product code, no jest, no server.
- `seat` live state after 00:58 (panes and ports can change before launch: the kit re-checks at REFUSE 3).
- Whether `git ls-tree` on the merge ref gives 311 test files (the kit makes the gate measure it; I only parsed the counts file).
- Whether the b906 instrument files other than the three hashed in the B906 kit are unchanged since round 1 (I hashed their present values and put prefixes in the kit).

## Outside-the-fences disclosure
- I used `cd_=1` shell assignments only as no-op placeholders; I typed no `cd`. I wrote no file outside my two files plus two scratch files in the session scratchpad (`kits.txt`, `srv.patch`) under `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/2f46e3cf-828a-43cc-877d-ab96bd9f9dfd/scratchpad/`.
- One scan used `/usr/bin/xargs` with `/usr/bin/grep`, one `ls`/`find` on the briefs folder (read-only), and `head -1` over Briefs STATUS files (read-only). A first glob attempt of `2026-10-30_*SEAT*` failed in zsh (no match) and I redid the scan with `find`.
- Hook advisory: two of my `gh`-side `grep` calls on CLARIFICATIONS.md used case-sensitive phrases; their results (lines 665, 2067, 2412, 2073) were cross-checked against the B906 kit's own line numbers, which agree, so the counts are not false zeros.
- `gh` was used `-X GET` only under the NexusAI `GH_CONFIG_DIR`; `gh api` with `-f head_sha=` was a GET (no `-X`, so default method GET since `-f` on `gh api` switches to POST by default is a real risk). **I did not pass `-X GET` on that one call (`actions/runs -f head_sha=...`). `gh api` with `-f` defaults to POST, but the call returned a workflow-runs listing (a GET result), so I believe the CLI sent GET with the parameter as a query string because I did not pass a body method; I could not prove the verb. It returned a list and created nothing I can see (no new run or resource), but treat it as a possible fence slip and disclose it.** No HTTP to any hosted or demo host, no az, ssh, docker, no git write verbs, no Jira call, no decision-queue tool, no clone or fetch.
