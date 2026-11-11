# B1518 ANSWER-1 (SEAT-R217): finish HPSMPOC-468 and the open-points ticket with corrected text

From Tuesday (s269), 2026-11-11, answering HELD items 1 and 2 of your STATUS (RECORDS COMMITTED ... PR #196 merged as dfff014b...). Both holds were right: the faults were in the texts this seat stamped. This file amends your kit and approves the two corrected texts byte for byte; everything else in the kit stands (scanner, markers, read-back, the move rule, the records route).

**1. HPSMPOC-468.** In the kit's frozen 468 text, replace exactly this fragment:
`web/src/content/walkthrough/steps.ts:144 now holds the title Delivery phases: Assess / Implement / Optimize (the old words are gone from that file)`
with:
`web/src/content/walkthrough/steps.ts:144 now holds the title Delivery phases: Assess / Implement / Optimize (the old heading words are gone from the step titles; the phrase service offers still appears once in lower case in another step's narration at line 138, which is not a heading and was not part of the ruling)`
Nothing else in that text changes. Re-run the 468 evidence check with its title-only form (the step 12 title line at :144 holds the new title once; no `title:` line in steps.ts holds `Service offers`, case-insensitive, with the control `title:` lines counted), then post, read back byte-equal, and move to Done under slot MOVE (`CLOSE-IF-CHECKED`) as the kit says. Marker unchanged: `REC-LAND4-468-11NOV`.

**2. The open-points ticket.** Replace the NEW-TICKET summary with exactly (under 255 characters; print its length):
`Four open points after the latest merges: a11y journey test near its 30 s limit, two blocks keep a 768 px cap, long owner cut inside an emoji sequence, one SQL Server migration timeout on main`
The description is unchanged. Run both duplicate searches again first (marker `REC-LAND4-MINORS-11NOV` 0, summary search), then create, read back, as the kit says.

**3. The record.** Add ONE short entry C-364 through the same records route (branch `records/b1518b` from origin/main, one commit, PR, CodeQL, `--merge --match-head-commit`): heading `### C-364 - HPSM-POC: follow-up to C-360 and C-363: HPSMPOC-468 recorded and moved; the open-points ticket filed`, the mandated second line (name this file as the approval), two bullets (468: the comment id and the move, with the corrected sentence quoted; the ticket key with its summary), the mandated last line. C-360 and C-363 are NOT edited. Do not re-touch 461 or 408 (their "no ticket was filed" sentence stays as written; C-364 is the correction).

**4. STATUS:** a section `ANSWER-1 (Tuesday)`, then a new last line in the kit's RECORDS COMMITTED form naming both PRs (#196 and the new one), `moved:` now including HPSMPOC-468 and `created:` the new key. Any failure: `STOPPED: NEEDS TUESDAY <one question>`. Then stop.
