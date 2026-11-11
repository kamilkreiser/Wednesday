STARTABLE: YES (small; see D-1: a full seat for one code-only half-item may not be worth a seat)

# B1496 DRAFTER REPORT: SEAT-H156, HPSM-POC lane H-C (server residues: HPSMPOC-228 N-5, 436, 408 item 2)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1496_SEAT-H156_hpsmpoc-lane-hc-server-residues.md` (105 lines) and its identical `.pre-stamp` (`cmp` silent). Written 2026-11-11 13:45-13:5x AEDT.

## BLUF
- **The lane mostly does not exist any more.** Two of its three items are already built on code main `009421a2` (2026-11-10 18:10 AEDT); SWEEP-1326 read them from records comments older than the landings:
  - **228 N-5 (refresh fan-out): FIXED AT MAIN** by PR 298 (b1393, squash 192c0a94, merged 2026-11-10 05:02 AEDT): an in-flight renewal map, `entra.ts:312`, and `refresh-fanout.test.ts` (5 rows). The ticket's 2026-11-06 records comment (at eaf77b3c) calls it "NOT built"; that comment is three days stale.
  - **436 (finding explanation of no finding): FIXED AT MAIN** by PR 302 (b1394, squash 856d15d1): `ReportingEndpoints.cs:187` refuses with `narrative.no-findings` / "There is no visible finding to explain.", pinned by `Hpsmpoc436NoFindingExplanationTests.cs` (2 Facts).
  - **408 item 2: only half is buildable.** (a) cap the default owner at 100 is code with no word; (b) "give the three limits real sentences" is the product owner's words (the 2026-11-10 lane plan `lanes.md:67` already left item 2 out for this reason). The kit builds (a) only, red-first, and HOLDS (b).
- So the kit is: Step 0 closes 228 N-5 and 436 with evidence that can fail (mutation controls; 436 also run on SQL Server as CI does); then one small web build (`startingOwner` in `remediation-store.ts`, used at `RoadmapScreen.tsx:99`), three red-first rows. Sonnet, row C2, ports 9620-9629, branch `b1496/hpsmpoc-register-default-owner-cap`, no PR, nothing deploys.
- None of the three is a 10 Nov HTML phase item or an HP-tool integration (checked against DECISION-DOCUMENT.md, below).

## Facts re-measured (instrument; control)
- Jira (Python REST GET, credentials read in-process from the project `.env`, never printed; JQL `project = HPSMPOC AND ( key in (HPSMPOC-228, HPSMPOC-436, HPSMPOC-408) )`): 3 rows, all Backlog; 228 updated 2026-11-06 (3 comments), 436 2026-11-03 (1), 408 2026-11-01 (3). Control: the same JQL on a key that does not exist returned 0 rows. Full text of each read via `/rest/api/3/issue/<key>`.
- Code main `009421a28616c8b31dde86b59d4c4ca674c288fa` (`gh api -X GET .../branches/main`, 13:45:22 AEDT); open PRs 0 (control `pulls/99999` 404). Main's check-runs: success 21, skipped 1 (`commits/009421a2/check-runs`).
- 228 N-5: `gh api commits?path=` for `entra.ts` and `refresh-fanout.test.ts` both name 192c0a94 as newest; `commits/192c0a94/pulls` = PR 298 merged; `compare 192c0a94...009421a2` = ahead 10, behind 0 (ancestor). `grep -n` at main: `entra.ts:306` comment "HPSMPOC-228 N-5 (gate B176)", `:312` `const renewing = new Map<string, Promise<Renewal>>();`, `:380` `renewalsInFlight`. Control: the 11-06 records comment's own search terms ("in-flight", "pending") do hit this code now (`grep -n -i` printed lines 306-312, 379-380).
- 436: `commits?path=ReportingEndpoints.cs` newest = 856d15d1 ("Narratives: refuse a finding explanation of no visible finding ..."), `commits/856d15d1/pulls` = PR 302 (head b1394/hpsmpoc-api). `grep -n -F 'narrative.no-findings'` = line 187; the guard is lines 182-187. Test file present in the tree (`git/trees/009421a2?recursive=1`, 1803 entries, truncated false).
- 408 item 2 open at main: `remediation-store.ts:41/45/46` still return bare labels `"State"` / `"Owner"` / `"Evidence reference"`; `RoadmapScreen.tsx:99` starts the owner as `action.owner ?? ""` with no cap; `OWNER_MAX = 100` at store `:18` and screen `:72`; Owner input `maxLength={OWNER_MAX}` at `:130`. Test helper `owned(name)` at `RoadmapScreen.register.test.tsx:33`, the default-owner row at `:96`. All `grep -n` over raw files fetched by `gh api -X GET contents/<path>?ref=009421a2`.
- HTML-phase check: `/usr/bin/grep -n -i` over DECISION-DOCUMENT.md (1872 lines) for remediation, register, roadmap, narrative, explanation, refresh, entra, token, offline, template, owner, and the three keys. Nearest items: D-066 (register rule sentence, THIS PHASE, already built by PR 304 for HPSMPOC-438), D-077 (roadmap owner/status lines, NEXT PHASE, wording), D-044 (progress counts with customer owner, NEXT PHASE), D-016/D-017 (narrative re-approval). None is the owner cap, the empty-finding refusal or the renewal map; the build adds no word and no layout. SWEEP-1326's exclusion list (21 HTML-phase keys) does not name 228, 436 or 408 (positive control: it names 463 and 464).
- HP-tool check: none of the three touches the Security Manager API, Fleet Threat Assessment, firmware tools or SIEM (file paths above).
- Landing rule: "The landing form is a head-pinned squash" at CLARIFICATIONS.md line 3617, analysis repo origin main d4cc73ef (`gh api -X GET contents ... -H Accept: raw` then `/usr/bin/grep -n -i -F`, 13:48:59 AEDT; the local `1_Project_Definition` checkout is at 76bb8ba4 of 2026-09-29 and has only 192 lines, so it was not used).
- CI predicates: read from ci.yml at 009421a2 (682 lines): api-sqlserver-shard parts `api-assessment` / `api-other-and-feedback`, the `case "$PART"` filters, `MSSQL_IMAGE` pinned `2025-CU9-ubuntu-24.04@sha256:2b5b5816...`, `HPSM_TEST_SQLSERVER=Server=127.0.0.1,1433;...` via GITHUB_ENV; web-build/web-unit/web-e2e run lines as in the kit.
- Ports 9620-9629: `lsof -nP -iTCP:9620-9629 -sTCP:LISTEN` 0 rows at 13:47:45 (control: 9 distinct listening addresses machine-wide). Python range-overlap scan of the 63 non-`.pre-` SEAT kits of 10-11 Nov: only B1455's list of blocks held by other (finished) kits, 9590-9699; no bare number in 9620-9629. Control: 9950-9959 found in B1441 and 7 others. Panes (`tmux list-panes -a`): `%0 wednesday`, `%1 fleet-monitor`, `%19 Datasec/NexusAI-N123`, `%20`/`%21` unnamed.
- Branch `b1496/*` absent: `git/matching-refs/heads/b1496` length 0 (control `heads/b1463` length 1).
- `status_watch.sh` line 56 case arm, copied into `bash -c` and fed sample lines: `READY B1496: <40>`, `HANDOVER B1496: next ... | done ...`, `STOPPED: NEEDS TUESDAY ...` fire; `WORKING:` and `PROGRESS B1496:` do not.
- Kit self-checks (python): four-underscore count 6 (five Stamp slots + last line), `@TOKEN@` 0, non-ASCII 0, decision-card ids 0; name scan (underscore-aware) 0 for the coordinator, product owner and deputy names, control `_by_<name>_` fired. One test fixture name I first wrote was replaced by "Ops team".
- Model: model-routing.md line 92 row C2 (Sonnet 1st); id `claude-sonnet-5-5` from models_latest.json (checked 2026-11-11 07:13).
- Disk: `df -g` 1337 GiB free.

## D-decisions (drafter's, Tuesday may overturn)
- **D-1: wrote a builder kit, not a records-only kit.** The only build is 408 item 2 part (a). It is real (an owner over 100 units makes Save unusable) but reachable only with content that does not exist today (the gate's own grading). Recommendation: launch it if a seat slot is idle; otherwise fold the two closures into the HPSM records kit SWEEP-1326 Q6 already proposes and park the cap. The kit's Step 0 closures stand alone either way.
- **D-2: built (a) as "unchanged when it fits; otherwise trim, cut on a code-point boundary, end-trim".** The "unchanged when it fits" clause keeps every default that saves today exactly as shown today. It is the gate's "cap or truncate" written down. It is not a word.
- **D-3: Sonnet (C2), not Opus.** The lane as swept carried 228 N-5 on `entra.ts` (an auth surface, row C3 would argue Opus). That item is built, and the seat only runs its tests and a mutation in a throwaway clone. The build is not on an auth surface.
- **D-4: 436 closure runs on SQL Server** (port 9620, CI's pinned image). This takes the lane's "API tests on SQL Server as CI runs them" literally for the only API item. It is evidence for the records seat, not a gate.
- **D-5: mutation controls in a second clone `.tools/b1496/mut`.** These are what make each closure fail-able. Without them, "the test exists and main is green" cannot fail.

## Q-questions for Tuesday (each with a default)
- **Q-1:** launch H156 at all (D-1)? Default: yes, Sonnet, if a slot is idle. Otherwise records-only.
- **Q-2:** 228 carries a stale "N-5 is superseded" line in its own description BLUF (about Friday's allow-list rule), and the 11-06 records comment calls N-5 not built. After this seat, N-5 is CLOSED-WITH-EVIDENCE but the ticket stays open on N-7's second half (words). Default: the records seat posts one comment naming PR 298. The ticket stays open for N-7, which goes to the product owner's word list.
- **Q-3:** 408 item 2 (b), the limits' sentences, and 228 N-7 second half ("Retry saving" after "reload the page") are both words. Default: one card to the product owner with both, after this lands.
- **Q-4:** 436's refusal text "There is no visible finding to explain." landed in PR 302 as a new user-readable string. UNMEASURED by me whether that word was ruled or gated as a word. Default: the records seat checks PR 302's gate verdict for it before closing 436.

## UNMEASURED
- Whether any real roadmap action owner exceeds 100 units (content or API). The gate said no such content exists. The kit's tests use synthetic owners.
- Whether `refresh-fanout.test.ts` and the 436 class fail under the mutations named. That is the seat's Step 0. I ran nothing.
- Whether the 436 class passes on SQL Server locally (main CI's success is RELAYED by check-run conclusions, not by test name).
- Which e2e shards render the roadmap register. The seat greps `web/e2e`; the tree has 59 specs and none is named for roadmap or register.
- Whether `web/src/lib/customer-text.test.ts` (it reads string literals as screen text, per a comment in `entra.ts`) scans `remediation-store.ts`. The build adds no literal, so it should not matter.
- SWEEP-1326's other HPSM lanes (H-A, H-B, H-D, H-E): not re-read here beyond the file names used for the partition.
- The B963 gate STATUS on disk (lines 163/175): not opened. The kit tells the seat to read it.

## Outside the fences (disclosure)
- I wrote scratch files under `/tmp/b1496_drafter/`: ticket texts, source files fetched by `gh api -X GET`, the tree listing, the kit list and CLARIFICATIONS.md. Nothing went in any project folder. I removed the folder at the end of drafting.
- The brief asked for the identical `.pre-stamp` copy, so I wrote three files, not the rules file's two.
- No Jira write, no GitHub write, no git verb in any project repo. The only git call was one `--no-optional-locks log -1` and `remote -v` on the stale local analysis checkout. One `git ls-remote` over SSH was attempted without the deploy key. It failed with "Repository not found" (read-only; no state changed). After that, every read of origin went through `gh api -X GET`.
- No `decision_queue.sh`, no `briefs_staged/`, scoreboard or `_ledger.md`, and no WEDNESDAY/FRIDAY tree.

READ-WHOLE-BY-TUESDAY: ____
