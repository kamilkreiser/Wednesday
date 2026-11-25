# DRAFTER COMMISSION — brief for Seat S 127th (Secuura/Blockchain-S: READ-ONLY, two measurements)

Written by Wednesday 2026-11-26 (morning). You are a DRAFTER: write ONE brief file and nothing else. No launch, mail, post or box contact. Every project tree is READ-ONLY to you (git read verbs only; `git --no-optional-locks status`).

## Output
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-26_seatS127_ks1971_ks2366.md`

## Template
Copy the SHAPE of `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-26_seatS126_kintsugi_services_o1.md` (read it WHOLE; it passed the send gate). Gate needs, as BARE lines: `PROVENANCE:` with every row `- <fact> | <ABSOLUTE source path, URL or command> | read YYYY-MM-DD HH:MM` (relative paths are refused); `RULED BY KAM, NOT YET IN AN ARTEFACT`; a placeholder line starting `SELF-CHECK-PLACEHOLDER` for Wednesday. Keep the seat-discipline sections; replace the work. The box kit is Seat S 126th's REC tools (`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-26_seatS-126th/`), re-keyed by counted edit as S 126th did; host-key pin SHA256:gl2JBs7KpV7/wrYd/7bzqTNQ+wyFQJomCtQkfUs8nuU, mismatch = STOP.

## Authority (quote verbatim from the live board, re-read with kam_msgs.sh)
- Kam 2026-11-26 09:14:54: "Decision wed-morning-plan-1126: a — Carry on with the plan" (option a detail, from the card store: "one board seat; more closes as the board census allows").
- Kam 2026-11-25 18:21:21: "Please close and merge and archive what you can. That looks like great progress."
- Kam 2026-11-25 06:57:19: "keep working.  I will log in with a new account after usage runs out".

## Measurement 1 — KS-1971: is the ssrf guard in the RUNNING m365-integration?
Source: S 126th's STATUS `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-26_S126_status.txt` item F2 and its REC evidence. KS-1971 was reopened with the condition (quote it from the ticket, read WHOLE): "Closing again needs: m365-integration rebuilt on a revision that contains 4e529633d0a1, with a census line." S 126th measured m365-integration running image ed71e5446c87 (started 2026-11-19) and named it D 67th's k31 build at db2b80073264; verify both from records (D 67th's REC) and that 4e529633d0a1 is an ancestor of db2b80073264 (gh api compare).
The box read the brief licenses: ONE `docker exec <m365-integration container> ` running a read-only `grep -c` (or `grep -n`) for a distinctive string of the guard (derive the string from the guard's source at 4e529633d0a1; name the file) over the container's built output directory, plus a positive control (a string certainly in that build) and a negative control (a made-up string = 0). No other exec, no shell, no file write, no env/log read.
Outcome: a census line (image id, revision, guard string count, controls) and a CLOSE PROPOSAL for KS-1971 if the guard is present and the ticket names no other remaining work (read it whole). The close itself is a LATER licence (LICENCE CLOSE KS-1971), Done + archive, no comment, by S 125th's close kit (`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-26_seatS-125th/tools/close_s125.py`, counted re-key).

## Measurement 2 — KS-2366: can a certification's anchor ever leave 'pending'?
Read KS-2366 WHOLE (filed today; its "What a fix must decide" names the question). Measure:
(a) SOURCE at ref 9c1ecde5abd6 (originate base on Kintsugi) and at develop 59e89c87719e: EVERY writer of a certification row's `blockchain` blob (search the repo for the blob's writers and for anchor-state sync paths; list file:line; say for each whether it can match a certification row, citing the WHERE clause). Positive control: the documentRepo `writeAnchorBlobIf` external_id match KS-2366 names.
(b) BOX, read-only SELECTs only (session forced read-only as S 125th did): counts, by the certification blob's `anchoringStatus` and `status` fields, of default-tenant and all-tenant certification rows (certifications sit in `documents` with certification_metadata), and the oldest/newest created_at per bucket; plus the same for non-certification documents as the control (documents DO confirm, if the writer works). Print counts and dates only; no ids beyond what a count needs, no personal data.
Outcome: one paragraph answer "can leave pending: yes / no / unmeasured", with file:line and the counts, mailed in a STATUS. NO ticket write: Wednesday decides whether to post it on KS-2366.

## Holds
No Linear write except a licensed KS-1971 close (later licence); no comment; no GitHub write; no HTTP to any stack; box: the pin, boxrun reads, the one licensed exec grep, read-only SELECTs; no docker command that writes; no demo/demo-pk/prod contact; no human mail; no cards. Vault daily-note commit + one plain push at wrap allowed.

## Routing
Sonnet (Wednesday fills the id). Lane -S. Seat name exactly `Seat S 127th` (ordinal: 0, control S 126th: 1).

## Return
Path, byte count, every UNVALIDATED fact, and every commission fact you found WRONG with its source.
