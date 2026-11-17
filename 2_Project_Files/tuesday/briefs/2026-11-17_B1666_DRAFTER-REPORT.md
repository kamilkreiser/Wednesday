STARTABLE: NO, not yet: pane %249 Datasec/NexusAI-R256 is LIVE (B1663 STATUS last line `RECORDS B1663: PENDING | JIRA pending` at 15:14) and writes the same Jira tickets and `CLARIFICATIONS.md`; the kit refuses on that by its REFUSE 6 and is otherwise ready for Tuesday's stamp (stamp_check 56 claims, 56 measured, rc 0; 9 four-underscore lines = 8 slots + last line).

# B1666 drafter report (SEAT-R258, NexusAI: dismiss the seven intended alerts), drafted 2026-11-17 (`date` first read 15:13:02, last 15:18:46 AEDT)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-17_B1666_SEAT-R258_nexusai-dismiss-seven-intended-alerts.md` (120 lines, 41,836 bytes, 0 non-ASCII, sha256 prefix 56bcdd6ebf194185; line 14 is 2,231 chars, read the tail). Sidecar `.md.measured`. Work folder `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s286/d1666/` (`texts1666.py`, `scan1666.py`, `build1666.py`, `kit_body1666.md`, GET-only `jget1666.py`, fetched source copies). The authority's em dash is written ' - ' in ASCII and the kit says so.

## What the seat does
1. Start check; helpers with selftests; Step 3 re-reads alerts 142-150 by number on main (an already dismissed/fixed one of the seven is skipped and named; 145, 146, 151 never written, helper refuses them).
2. Seven one-per-command PATCHes (body exactly state dismissed, reason `won't fix`, comment), order 142, 143, 144, 147, 148, 149, 150, each read back byte-equal; first PATCH is the permission test, 403/404 = STOP. Counts before/after (expect 29 -> 22 open, 222 fixed, 0 -> 7 dismissed).
3. One comment each on RD-805 (marker DISMISS-805-17NOV) and RD-804 (DISMISS-804-17NOV), only when every alert named read back dismissed.
4. Optional move of RD-804 only; one new entry in `CLARIFICATIONS.md` (section/C-number by program at Step 3 and again at the append, expected 96 / C-298 after R256's 95 / C-295..297; C-190 and C-294 referenced, no card id).
Slot defaults: DISMISS NONE, JIRA HOLD, MOVE NONE, RECORDS HOLD (plus STAMP, LAUNCH WINDOW, BASE, Hard stop).

## The seven readings as frozen (each verified at main 58c5823e against the source line and the B1656 review)
- 142 azureLogAnalytics.js:798: request body to the Log Analytics query address; host from an allow-list (:439), workspace segment GUID-checked and percent-encoded (:757-758); no file data in host or path.
- 143 mondayClient.js:36: request body (query, variables) to the fixed Monday endpoint.
- 144 marketplace-api.js:511: request body (plan id, quantity); address is a fixed base plus one percent-encoded subscription id (:504).
- 147 emailService.js:387 (columns 43-46 = the `url` argument): stored mail configuration to its own fixed mail service; fixed host plus one percent-encoded, address-checked inbox segment (:385).
- 148 emailService.js:387-392: the message body (recipients, subject, content) at a fixed address.
- 149 emailService.js:393-396: the authorization header carrying the service's own stored key to that service only.
- 150 entraGroupGate.js:204: request body (group id list) of the membership check at the Graph base address.
Each is 193 to 269 characters (limit 280), ends "Read as intended; dismissed on the product owner's ruling.", and passes the text scan (no person, client, seat, B-number, card id). I split 147/148/149 by the alert's own sink columns instead of one shared sentence, since they are three different sinks. Correction found while freezing: `normaliseAddress` (mailAddress.js:29,36-44) checks an email-address shape only; it does NOT refuse a slash, so the one-segment guarantee is `encodeURIComponent` at emailService.js:385. The comment says "address-checked" and "percent-encoded" (both true) and never says a slash is refused. The R256 kit's wording "address-shaped path parameter" is consistent with this.

## Permission evidence
- Repo is private; project `gh` user has permissions admin true; token scopes `gist, read:org, repo, workflow` (NO `security_events`). GET of an alert is 200 with X-Accepted-Oauth-Scopes `repo ... security_events ...`.
- GitHub docs (fetched): the PATCH "update a code scanning alert" needs the `security_events` scope for private or public repos (public_repo for public-only). So the PATCH may well answer 403 with this token; whether `repo` also satisfies it for PATCH is UNMEASURED (no write made). The kit makes the first PATCH the test and STOPs on 403/404 without any scope refresh or workaround.
- No earlier NexusAI seat dismissed an alert: 0 dismissed on main; 26 'dismiss' lines in CLARIFICATIONS.md are prohibitions (C-190 item 3 "NEVER dismiss ... from any side", C-202, C-204) or "stay open" rulings. This is the first dismissal; the kit states it is the product owner's own exception for these seven numbers only.
- Possible extra boundary: an organisation "dismissal request / approval" setting could hold the dismissal; not measured.

## RD-804 move proposal
Rule text (NexusAI/CLAUDE.md "When completing work" step 2): code change -> Testing; decision/docs/non-code -> straight to Done. This kit changes no code and the closures are a decision, so the only rule-fitting move is RD-804 -> Done (transition id 41), and only after all five of its alerts are closed (138-141 fixed 2026-10-18, 142 dismissed) and its comment reads back. Proposed slot `MOVE 804`; RD-805 never moves (145 and 146 stay open). Caveat for Tuesday: 138-141 were fixed by code that never took RD-804 through Testing, so Done also closes that history; `MOVE NONE` is the safe alternative (R256's rule: move only where alerts read fixed, and dismissed is not fixed).

## Open questions for Tuesday
1. Launch only after R256's pane is gone and B1663's last line is final (READY/STOPPED/HANDOVER); the kit computes the C-number then (expected C-298; if R256 stops without section 95 it becomes 95/C-295 and the entry omits the C-295 reference).
2. Model-routing has no row for a GitHub alert write; the stamp is the approval (stated in the kit). Sonnet as in the commission.
3. MOVE 804 (Done) or NONE? RD-804 to Done skips Testing/Release Ready.
4. SEAT-R257 does not exist in the folder (highest earlier R256); kit uses R258 as named.
5. The two Jira comments are written after R256's comments on the same tickets (markers LAND-211-805/804, which say the seven "stay open"); ours supersedes by its own text and the C entry; R256's C-295 says the same, so the record carries both in order.
