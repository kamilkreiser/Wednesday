STARTABLE: YES (after the RULING-TIME slot is filled; without it the seat skips only Job B and says so)

# B681 drafter report - SEAT-R44, NexusAI records for PR #112 (drafted 17:41-18:0x AEDT, 2026-10-25)

## BLUF
The kit is written and shaped on the newest NexusAI records kit (B656). Four of your five premises needed correcting by a live read, and the kit carries the corrections:
1. **RD-777 and RD-776 are already Testing** (since 2026-10-08 08:45, changelog). There is nothing to transition; "transition 31" is moot. The kit makes TWO comments and ZERO transitions, and refuses to POST any transition id.
2. **PR #67 is already closed** (17:34:05 AEDT, two seconds after #112 merged, by the project account) with **0 comments**. The project's records kit rule is `gh` GET only, so the pointer comment is not the records seat's: it is FOR TUESDAY 1.
3. **No length-cap ticket exists**, and no earlier record names a key: B656 skipped the create (its pre-search rule), Tuesday's B650 addendum says "Tuesday owns filing it", Jira reads `text ~ "B647"` 0 and `text ~ "B650-1"` 0. The kit does not invent one: B650-1 stays out (Q1).
4. PR #112 merged 17:34:03 AEDT by the read (06:34:03Z), not 17:33.
The one ticket the kit does create is the three test cells (B667-1..-3).

## Facts re-measured (instrument; control)
- PR #112: merged true, merge_commit_sha dbbf5881f1594916d4abb90df884ea4ad42ef80c, head 8993b233..., `git/commits` parents a0093d56b9e86252cf6b101add618b0cd0d37797 + 8993b2334f07e301da5254a7fb2ff97db5955b12 (gh api -X GET under NexusAI GH_CONFIG_DIR; control: the kit's REFUSE line uses pulls/110, a different merge). Files 334/0, 59/18, 3/3.
- Main = dbbf5881 at 17:45:07; compare dbbf5881...main identical 0/0. Open PRs: 0 (control: closed list shows #112, #113, #67).
- Push runs on dbbf5881: Deploy demo skipped, npm-audit success, Gitleaks success, Push on main (dynamic) success; **Build 40169545129 in_progress at 17:45:07** (the kit waits up to 45 min, records the conclusion, never re-runs). Check-runs: three Analyze success, scan success, audit-production-deps success.
- Alerts 83, 84, 43, 136 by number: fixed, fixed_at 06:36:52Z, updated_at 06:36:53Z (your "updated" figure matches), dismissed empty; control 9999999 = 404.
- Jira (in-process GET, project token never printed): RD-777 and RD-776 Testing, 5 comments each; transitions list 31 In Review -> Testing, 51 -> Declined (trap); changelog moves 2026-10-08 08:45:01/02. Searches `B667`, `B667-1`, `B647`, `B650-1`, `dbbf5881`, `labels = b656-2026-10-25`: 0 each, with the nonsense control 0 and `key in (RD-777, RD-776)` returning both (jira-query.sh prints "control passed"). RD-876: Task, Low, labels b362-2026-10-21 and gate-29.
- Gate: B667 STATUS read whole (269 lines): NO GO 2 of 2 on class B647-2, B667-1 (M35 TAB/LF/CR before a scheme colon), B667-2 (M36 two whitespace after `<`), B667-3 (M39 value that settles to empty); B647-1 quadratic closed. Survivor inputs read in `check3a-survivors-probe.txt`; M35/M36/M39 diffs exist.
- CLARIFICATIONS.md: 2390 lines, 443149 bytes, last entry C-221, last section `## 58.` (B656). HISTORY.md on main already holds the B656 entry (line 8491), so records/b656 landed. `records/b681` absent (matching-refs length 0; control records/b362 length 1).
- Model: row C2 (`model-routing.md:92`) + C7 (`:97`), Sonnet, id claude-sonnet-5-5 (`models_latest.json`, checked 15:53:22). Launch line carries BRIEF_SEAT_LEVEL=sonnet inside the quotes.
- Ports: no block was assigned. Reserved 9480-9489: `lsof -nP -iTCP:9480-9489` and 9600-9999 printed nothing; word-boundary scan of 128 non-.pre- SEAT kits of 10-24/10-25 hits `948x` only in B596 and B611 (HPSM-POC records kits that "propose" it for a seat with no server). Every candidate block I tried had some hit in an older kit; the highest block named today is 9740-9749 (B679). Tuesday may move it. Live panes: tuesday, Security-Composer-J15, MPS-G121, fleet-monitor (no NexusAI seat).
- Stamp slots: 9 lines match the four-underscore pattern (8 slots + last line); non-ASCII only in structural middle dots and the one HISTORY heading em dash; no at-sign placeholders; no person name or card id in the kit (scanned: 0).

## D-decisions (mine, veto at read-whole)
- D1: Order is A (create ticket first, the comments cite its key), B (C-entry), C (comments after the Build wait), D (HISTORY on records/b681), E (ruled-not-delivered).
- D2: New ticket priority **Medium** (RD-876 reads Low; this closes a gap the gate graded Major). Labels `b681-2026-10-25`, `b667-finding`. No Jira link write (none authorised in earlier kits); the key is cited in text.
- D3: `{BUILD}` has three closed forms (success / failure with attempt and "not re-run" / still running at the 45-minute end); comments are posted in every form, a failure is loud in STATUS and FOR TUESDAY.
- D4: One C-entry (C-222, section `## 59.`); the option label is quoted verbatim; the ruling time is a Stamp slot because the id-only filter shows the card's id line and nothing else.
- D5: Comments on RD-777/RD-776 are posted (final-evidence rule of the project CLAUDE.md work-tracking) even though no transition is made.

## Q-questions for Tuesday (each with a default)
- Q1: File the length-cap ticket (B650-1 figures plus the B647 linear shapes) in this seat? **Default: NO**, it is a product-owner question and "Tuesday owns filing it"; FOR TUESDAY 2 lists it. If YES, say "create" and give the NEW-* texts of B656 (still valid, unchanged) a slot.
- Q2: Fill RULING-TIME (HH:MM:SS AEDT of the round-cap ruling). **Default: you fill it at stamp**; if empty the seat skips Job B only.
- Q3: Pointer comment on #67 ("superseded by #112, merged as dbbf5881"). **Default: Tuesday posts it** (or rules it unnecessary); it is not in the seat's authority.
- Q4: Priority Medium for the cells ticket. **Default: Medium** (D2); Low if you want RD-876's shape.
- Q5: Port block 9480-9489. **Default: keep**, the seat starts no server.

## UNMEASURED
- Build 40169545129 conclusion; the ruling's clock time; the open-alert total on main after the landing; the three Jira hits of the A4 third search (`scheme` AND `whitespace` AND `test cell`, left for the seat to READ); the project's own written rule for aggregating residue into one ticket (searched NexusAI CLAUDE.md, JIRA.md, CLARIFICATIONS.md: no line; the kit cites your instruction and the routing row G-cap); "nested flag unset" wording of cell 3 (B667 STATUS line 196 says "asserting 200, nexted, stored ''"; I read "nexted" as the nested flag, and the probe shows head 200 with '' and the mutant 400, so the cell asserts accepted + flag unset + empty); the exact wording "KQL mode"/"general mode" (taken from the gate's `kqlQuery`/`condition` probe fields).

## Outside-the-fences disclosure
- Read-only throughout: gh `-X GET` only under the NexusAI GH_CONFIG_DIR; Jira GETs by an in-process python (`-I`) reading `.env` by name (no token printed), every JQL `project = RD AND ( ... )`; project helper `jira-query.sh` used for searches.
- Card: ran `decision_queue.sh show nexusai-112-validators-round-cap-1025` (exact id) into a scratch file and read it only through `grep -F` on the id; `list` never run. The option label in the kit is the one in your instruction, not read from the card.
- One printed account login: the `pulls/67` read showed the project account's login and the issue events showed it as actor into my context; it is NOT in the kit (kit says "the project account").
- One unexplained gh message ("needs the admin:repo_hook scope") printed once during the alert-number loop, after the 9999999 control returned its 404; every real read in that loop returned data and no write was attempted. Cause UNMEASURED.
- A zsh hook refused one command line (a bare `====` separator) and warned on case-sensitive greps; re-issued. No `cd`. No HTTP to hosted/demo/prod hosts. Not read: fleet/briefs_staged, scoreboard.md, `_ledger.md`, WEDNESDAY/FRIDAY trees, non-Datasec projects. Read the NexusAI Briefs/ STATUS files B656, B667, B650 addendum and the project's CLAUDE.md, JIRA.md, CLARIFICATIONS.md (all Datasec/NexusAI).
- Written: the kit and this report only. A scratch file in the session scratchpad holds the card output and the main HISTORY.md copy.
