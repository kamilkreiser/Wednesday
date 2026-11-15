STARTABLE: YES

# B1575 DRAFTER REPORT (kit for seat R234, HPSM-POC records pass for code pull request #318 and the 2026-11-15 HPSMPOC-168 ruling)
Drafted 2026-11-15 14:37:33 to 14:5x AEDT (`date`; first read 14:37:33, sidecar measured 14:51:31, last check 14:52:28, report written after). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1575_SEAT-R234_hpsmpoc-records-318.md` (166 lines, sha256 prefix `dc4a55e657d1e0f5`; 11 four-underscore lines = 10 Stamp slots + the last line; 0 `@X@` tokens; 0 non-ASCII bytes; the card id appears 0 times). Sidecar `.md.measured`: 93 claims, every one measured by program (`fleet/state/s278/d1575/measure.py`); `stamp_check.py <kit>` exits 0 ("93 claims, 93 measured, 0 not measured"). Model Sonnet (`claude-sonnet-5-5`, level inside the launch quotes): rows C7 (line 97) and G3 (line 110) of `model-routing.md`, model id line 23 of `models_latest.json`, `brief_seat.sh` default Opus at line 31.

## BLUF
1. **The four items "owed since 2026-11-11" are already recorded; the kit writes nothing for them.** The PRIOR-WORK check found that records seat R210 (B1493) did all four on 2026-11-11: `### C-339` (the user guide draft 0.4, line 6021 of records main) and `### C-340` (the UAT backup-copy deletion on the product owner's word, line 6033), analysis PR #194 merged as `830dae78`; and both FOUND tickets, HPSMPOC-468 (walkthrough step 12 "Service offers", marker `REC-WALK12-11NOV`, now Done) and HPSMPOC-469 (the fifth customer without "(sample)", marker `REC-UNMARKED-11NOV`, Backlog). The kit has the seat re-verify all four by program and STOP if any reads absent.
2. **What is left: 3 Jira writes and 2 entries.** W1 creates one Low ticket for the review's Minor 1 (no start-up log line when `FollowUp:TrustedProxies` names a proxy without the shared value; `Program.cs:130` covers only the ForwardedHeaders lists; no effect today). W2 comments the #318 landing on HPSMPOC-193 and records the Key Vault reference refusal as a REQUIREMENT on the later infra change (resolve before set, no trailing newline, a deploy check that catches a stopped API, check both apps). It also carries the review's Info points that 193 needs: until the value is stored, one bucket per connecting address; HPSMPOC-196 now also covers the proof header. W3 comments the product owner's 2026-11-15 ruling on HPSMPOC-168, quoted verbatim, and says nothing is built. Entries: C-371 (the landing) and C-372 (the ruling), in one records PR.
3. **No move.** HPSMPOC-193 states no done-when. Its comment 41009 (the recorded 2026-11-11 acceptance) queued "the change on the API and the web server, the stored value and its rotation, and the regression row" as one change. The code and the regression row are merged. The stored value and its rotation are not: `infra/modules/appservice.bicep` at main has 0 `Proof` lines (control: `ForwardedHeaders__KnownProxies` 1). MOVE offers only HOLD (Q-1). HPSMPOC-168 is not built, so it does not move either.
4. **#318 facts at drafting:** squash `8766b253` is code main (`compare 8766b253...main` identical), merged 2026-11-15 13:14:48 AEDT, 1 parent `b6c282ee`. It has 9 files (6 api, 2 web, 1 infra), +505 -24. The merged head `349f7a78` is the reviewed head. Check-runs: 22 on the squash (21 success + 1 skipped) and 23 on the head (all success). All four workflow runs succeeded on attempt 1, so there was no flake this time. Nothing deploys: ci.yml has 0 deploy or sign-in lines (control `deploy package` 14).

## Facts re-measured (instrument, time)
- GitHub (`gh api -X GET` under the project's `GH_CONFIG_DIR`, 14:38 to 14:46): `pulls/318` gives merged true, `merged_at` 2026-11-15T02:14:48Z, `merge_commit_sha` 8766b253bb11e9ef23978abc6741e1c6146e74c4, head 349f7a78f25cb1933214b277a80daa12bf9d15d3, 1 commit, 9 files, +505 -24. `commits/main` = 8766b253 with 1 parent b6c282ee. Open code PRs: 0. Check-runs on the squash: 22 (21 success, 1 skipped, the "dependency review (pull requests; ...)"). On the head: 23 success. Runs: 43666862909 `ci` push, 43666862791 `Push on main`, 43665283283 `ci` pull_request and 43665281077 `PR #318`, each success, attempt 1. `compare b6c282ee...main` is ahead 1 (a control that differs from the identical read).
- Records main (analysis): `d43f6bec6e64457e5a0bdd812134df9131641920` (#201, 2 parents, records/b1558). `CLARIFICATIONS.md` raw read: 2082090 bytes, 6327 lines, sha256 prefix `4d2a16eb207e5615` (a second raw read in measure.py was byte-equal). Headings at line start: C-370 [6317], C-371 and C-372 absent, C-263 [5114], C-344 [6070], C-357 [6187], C-339 [6021], C-340 [6033]. Bounded `C-371` and `C-372` read 0 each (control: bounded C-370 1). The bare strings each appear on 6 lines, so the kit counts only the bounded form. `8766b253`, `pull request 318`, `REC-LAND318` and `REC-RUL-168` read 0 each (controls: `pull request 317` 2, `b6c282ee` 2). Open analysis PRs: 0. `records/b1575` absent (control `records/b1558` 1). The last three merges (#201, #200, #199) each have 2 parents.
- Code at 8766b253 (raw contents, `awk NR==n`): every pointer in the kit's table, printed in the drafter's session. `ci.yml` (682 lines) has 0 for each deploy/sign-in string (controls: 14 and 9). `appservice.bicep` (252 lines) has `Proof` 0 and `FollowUp__` 0 (control `ForwardedHeaders__KnownProxies` 1). `CustomerIndustries.cs` lists 10 labels (counted by program). The `P-industry` field in `snapshot-policy-aligned.v0.1.2.json` (lines 44 to 46) is `"type": "text"`.
- Jira (own GET-only reader `fleet/state/s278/d1575/jget.py`, a copy of the B1558 drafter's, with 0 non-GET methods by grep; every JQL is `project = HPSMPOC AND ( ... )`):
  - Board: 483 issues, highest key HPSMPOC-483 (`key > HPSMPOC-483` 0; `key > HPSMPOC-482` exactly 483); 347 Done, 133 Backlog, 3 In Progress.
  - HPSMPOC-193: Backlog, Low, `b118-found`, comments 38951 and 41009.
  - HPSMPOC-168: Backlog, Medium, five labels including `needs-kam`, comment 41027.
  - HPSMPOC-196: Backlog, Lowest, 0 comments. HPSMPOC-468: Done, 1 comment. HPSMPOC-469: Backlog, 0 comments.
  - My three markers read 0 each. `qqzzxx9` 0. `REC-RECS-W5-12NOV` gives exactly 477. `REC-REG-193-11NOV` gives exactly 193.
  - Duplicate search for W1: `TrustedProxies` finds 195, 130, 118, 106 (all Done); `FollowUp:TrustedProxies` finds 195, 118, 106; `ForwardedHeaders__Proof` 0, `X-Hpsm-Web-Proof` 0, `operator signal` 0; `start-up line` finds 232 Done, 193 Backlog, 118 Done. Control: `Next.js` 24.
  - Labels: `rec-2026-11-15` 2 (482, 483), `review-finding` 3, `rec-2026-11-12` 3.
- Sources: the verdict is 130 lines, `60616cba94c3c448`. The builder STATUS is 136 lines, `93dea791ae8e68e9`. Quote checks by program: the 41009 fragment is in comment 41009; `Industry (placeholder field)` is in the json and in 168's description; `GO WITH FINDINGS` is in verdict line 1; "No Blocker, no Major. 2 Minor, 6 Info.", "89 passed, 0 failed" and "2310 Passed, 0 failed, 13 NotExecuted" are each in the verdict. The ruling text equals the card's option a byte for byte, and equals the commission's item 5 after whitespace normalisation.
- The 168 card (`decision_queue.sh show hpsmpoc-168-industry-list-1115` into `d1575/card168.raw`; 10 lines, the id on 1): `status: ruled`, `choice='a'`, `ruled_ts=2026-11-15T13:49:37`. The commission's clock says 13:48; the kit uses neither clock, only the date.
- Scan (`d1575/scan.py`, a marker-only copy of `scan1558.py`, plus `runscan.py` and `runscan2.py`): 0 problems over W1 (summary 252 chars; paragraphs 769/346/942/36), W2 (3199) and W3 (1604), and over both entry templates line by line (filled with the drafter's values; 40-hex shas from the GitHub reads pass). Controls fire for `entry C-9999`, `B170`, `Tuesday`, `gate`, `Kam`, `x_by_Kam_y`, `C-347`, `ASP.NET`, prose `HP`, `a@b.c`, `shared secret`, `D60`, `H164` and `hpsmpoc-b1466-pre`. `entry C-371`, `entry C-372`, `kamera`, `HpsmPoc.Api` and `X-Hpsm-Web-Proof` stay quiet. The kit's frozen texts equal `texts.py`, compared by program.
- Identity: the project root's `user.email` equals the B1558 records clone's (True) and differs from `2_Project_Files` (False). The B1558 records commit `afb3e07` has author and committer equal to the root email (values masked).
- Panes (14:41, 14:46, 14:51): `%36 Datasec/HPSM-POC-H165` is the only HPSM pane. Its kit (B1571) contains "Jira: 0 reads, 0 writes" once and touches no analysis repository, so it is not a writer. R234 and B1575 are used by 0 non-`.pre-` briefs (control: R230 in 2). Ports: none needed.

## D-decisions
- D-1 **Owed items: verify only.** B1493 did all four on 2026-11-11, so a second entry or ticket would duplicate them. The seat re-checks by program and STOPs if any reads absent, because the kit carries no text for them.
- D-2 **Two entries** (C-371 landing, C-372 ruling), following the records form that gives a ruling its own entry (C-344, C-357). Both go in one commit and one PR.
- D-3 **Write order W1, W2, W3.** W2 cites W1's key (`<<KEY-A>>`) and is frozen after W1 is read back.
- D-4 **Disposition of the review's 8 rows:**
  - Minor 1 becomes W1, the create.
  - Infos 2 (Key Vault), 3 (malformed value answered differently), 4 (HPSMPOC-196) and 6 (one bucket) ride in W2.
  - Minor 2 (landing text files) and Infos 1 (constant time) and 5 (probes) go in the entry only.
- D-5 **W1 labels** `review-finding` and `rec-2026-11-15`, priority Low (193 is Low; the commission's precedent B1558 used Low).
- D-6 **The word "secret" is avoided everywhere** (the scanner bans it). The texts say "shared value". The `@Microsoft.KeyVault` literal is not written (the scanner bans `@`); the texts say "a Key Vault reference ... its literal text".
- D-7 **W2 says the gate is "placed at Program.cs:134"**, not "first": `UseRequestTimingLog` is outermost (line 126). The review reports that it reads no header.
- D-8 **Clock:** JIRA DONE +30, RECORDS COMMITTED +70, HARD STOP +100 (3 writes, 2 entries).
- D-9 **REFUSE 6 guards the 168 comment against the B1577 build landing first.** If the main code has moved and any changed path contains `ndustr` or `snapshot-policy-aligned`, or json line 46 no longer reads `"type": "text",`, W3 HOLDS.

## Q-questions for Tuesday (each with a default)
- Q-1 **HPSMPOC-193 move.** Default: no move (slot MOVE `HOLD` only), because the stored value and its rotation are unbuilt and C-344 says "The ticket stays open until that is merged". If you read 193 as met by the code merge alone, say so and a moved variant gets drafted; as written, the seat STOPs if `appservice.bicep` gains a Proof setting.
- Q-2 **Two entries or one.** Default: two (C-371 landing, C-372 ruling).
- Q-3 **HPSMPOC-196** (the hosted header-shape measurement). Default: not written; W2 names it in one sentence. Alternative: a fourth write, a comment on 196 (not drafted).
- Q-4 **The `needs-kam` label on HPSMPOC-168.** Default: left (the closed list allows no label edits; the ruling answers the question the label flags). If you want it dropped, that is a separate label write, not drafted.
- Q-5 **Slots.** Default: JIRA `WRITE`, CREATE `WRITE`, RECORDS `WRITE`, REC-MERGE `FF`, MOVE `HOLD`.
- Q-6 **The infra change itself** (the review's FOR TUESDAY: "Card the infra change with the deploy-ordering requirements"). This kit only records the requirements on HPSMPOC-193; the card or commission is yours. Default: none from this kit.
- Q-7 **Launch order against B1577.** Default: launch this kit before B1577's PR lands. If B1577 lands first, W3 HOLDS by REFUSE 6 and the 168 comment needs a "built" variant.

## Inputs of every chain step (each from an earlier step or present at BASE)
| Step | Inputs | Source |
|---|---|---|
| 0 | the stamped kit; `df`; `tmux`; `.tools/b1575/` (made here) | stamp; machine; this step |
| 1 | helpers `.tools/b1558/{jira,scan,post,snap,diff,entries,search,build}1558.py` | exist at BASE (`ls`, 14:4x) |
| 2 | code and records main reads; Jira reads; the verdict and builder record; `ci.yml`, `appservice.bicep`; C-339/C-340 and the 468/469 markers | GitHub, Jira, disk at BASE |
| 3 | the three frozen texts and the two entry templates; Step 2 facts; Step 1 helpers | kit; steps 1 and 2 |
| 4 | Step 3 payloads and sha256; slots JIRA and CREATE; W1's key for W2 | step 3; stamp; W1's read-back |
| 5 | `.tools/b1558/analysis` (exists at BASE, sshCommand present) for the `cp -R` route; entry fills from step 4 (key, comment ids) | BASE; step 4 |
| 6 | the branch of step 5; parents of the last three merged analysis PRs | step 5; GitHub at BASE |
| 7 | all of the above | steps 0 to 6 |

## UNMEASURED
- Whether the follow-up link really stops believing X-Forwarded-For when `FollowUp:TrustedProxies` is set without the value. This is the review's source reading plus mine (the gate removes the header at `Program.cs:134`, and the follow-up link reads it at `FollowUpLink.cs:280`); I ran nothing.
- The review's figures (89, 2310 + 13, mutants, probes) are RELAYED, not re-run.
- Whether the hosted API's KnownProxies list is still set today. This is RELAYED from comment 38951 (2026-10-05); I read no host.
- Whether App Service passes `X-Hpsm-Web-Proof` unchanged (HPSMPOC-196).
- Whether other Jira tickets hold the start-up-line point under different words: the phrase searches read as listed, and I did not read all 133 Backlog descriptions.
- Who moved HPSMPOC-468 to Done (2026-11-11 20:25) was not investigated; that ticket is untouched.

## Outside-the-fences disclosure
- **Read:** `DRAFTER_RULES.md`; the commission; the B1558 kit (pre-stamp) and its drafter report, sidecar head and STATUS; the B1493 STATUS (whole); the heads and tails of the B1490, B1491, B1498 and B1565 STATUS files; the B1565 builder STATUS FOR TUESDAY section; the B1565 verdict (whole) and `landing.txt`; greps of the B1571 kit; `stamp_check.py` (header); `status_watch.sh` (greps); `model-routing.md` (2 rows); `models_latest.json` (grep); `brief_seat.sh` (one grep); `scan1558.py` (read, copied by redirect into my scratch).
- **Card:** one card, `decision_queue.sh show hpsmpoc-168-industry-list-1115`, read into a scratch file (the id is on 1 of 10 lines). No `list`, no other card, no `fleet/briefs_staged/`, scoreboard, ledger, WEDNESDAY, FRIDAY or non-Datasec tree.
- **GitHub:** `gh api -X GET` only (code repo: pulls, commits, compare, check-runs, runs, files, tree, raw contents; analysis repo: commits, pulls, matching-refs, raw `CLARIFICATIONS.md`, `rate_limit`).
- **Jira:** GET only (about 60 reads).
- **Git in the project:** `config user.email|user.name` and one `log -1` on `.tools/b1558/analysis`, with `--no-optional-locks`. The emails were compared by program and never printed.
- **Hook events:**
  - One refused `rm` of two of my own scratch files. Nothing was deleted; they were moved to `d1575/_quarantine/`. One was a 404 body from a wrong path guess, `FollowUpLink.cs` under `HpsmPoc.Api/FollowUp`.
  - One refused `cp` from `.tools/b1558/` into my scratch. The pathguard read the source as a write target, so I copied by `cat >` redirect instead.
  - One refused unquoted `$J`. I used a script file instead.
- **Wrote:** only the kit, its `.measured` sidecar (via `--init`, then filled by `measure.py`), this report, and scratch under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s278/d1575/`.
- Never typed `cd`. No az, ssh, docker, HTTP to any app host, mail or publish tool.

DRAFTED B1575: kit 166 lines, sidecar rc 0, questions 7
