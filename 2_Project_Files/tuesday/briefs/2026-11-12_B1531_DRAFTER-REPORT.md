STARTABLE: NO

# B1531 DRAFTER REPORT (HPSM-POC residues of 462 and 406; drafter, 2026-11-12 10:2x AEDT)

No kit was written: `2026-11-12_B1531_SEAT-H160_hpsmpoc-residues-462-406.md` does not exist (only this report). Marks: MEASURED = printed by a named instrument this pass; RELAYED = read in another file; UNMEASURED = nobody has.

## BLUF
- **The premise "462 fill-versus-outline REPRODUCED at main with a fix shape" is stale: that fix is already at main.** B1503's branch landed as pull request 311 (squash `448dc395`, 2026-11-11 18:39 AEDT). Main `globals.css` lines 114-116 hold the rule `[class^="rounded-"]:not(.sidebar-ring):focus-visible, [class*=" rounded-"]:not(.sidebar-ring):focus-visible { border-radius: revert-layer; }` (MEASURED: `grep -n revert-layer` on the raw file at `c717ba1a` printed 110, 116, 127, 135). The same squash holds 406 item 4 (`parts.tsx:49` carries `min-h-11`, MEASURED) and the 465 Training look. So nothing of B1503's is left to build.
- **406 item 5 is closed** (the product owner's 2026-11-11 ruling "Leave both as they are", card ruled `a`, entry C-359, comment 41121). **405 is Done** (comment 41116). The 405/406 card is RULED and has no delivered mark: marking it delivered is Tuesday's (`decision_queue.sh --delivered`), nothing for a seat.
- Every remaining item is (B) or (C). (A) is empty, so STARTABLE: NO.

## Facts re-measured at drafting (10:22 to 10:25 AEDT, `date`)
- Code main `c717ba1a945191ffa31f13320c19967a6cf7f15a` (`gh api -X GET branches/main`, committed 2026-11-11T10:24:41Z; the squash of pull request 313, SDK exact pin). Recent history by `commits?per_page=8`: `c717ba1a`, `c014503d`, `51b5a21e` (309), `448dc395` (311), `b34046d1` (310), `009421a2`.
- Open pull requests 0 (`pulls?state=open` length 0; control `pulls/99999` 404). `matching-refs/heads/b15` lists `b150`, `b1503`, `b1507`, `b1519` and the old `b152` to `b158` scratch refs (19 refs, instrument `--jq '.[].ref'`); `heads/b1531` length 0 (control `heads/b1519` length 1). No ref names 462 or 406 work other than `b1503/...` (already landed by squash, so its tip is not an ancestor of main).
- Panes (`tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'`): `%0 tuesday`, `%141 Datasec/MPS-M126`, `%138 Datasec/MPS-M127`, `%1 fleet-monitor`, six unnamed panes. No HPSM pane live.
- Ports: `lsof -nP -iTCP:9860-9869 -sTCP:LISTEN` 0 rows (control: `lsof -nP -iTCP -sTCP:LISTEN` 13 rows machine-wide). Scan of the 44 non-`.pre-` SEAT kits of 11 and 12 Nov (python, range-aware): 0 hits for 9860-9869 (control: 9670 found in B1503's kit). A bare grep over ALL dates finds `986x` in older finished-seat kits (B636, B638, B691 to B693, B719, B723, B725, B726, B729 and more; none has a pane). Block 9860-9869 is free for a later kit.
- Tickets read whole by Jira REST GET (my own GET-only reader, `.env` read in-process, no token printed; scratch `j462.txt`, `j406.txt`, `j405_357.txt`, `j457.txt`, `j470.txt`): 462 Backlog, 1 comment (41120); 406 Backlog, 2 comments (40746, 41121); 405 Done, 2 comments (40650, 41116); 357 Backlog, 4 comments (40287, 40311, 40555, 41122). Also read 457 (partner dashboard, v2.1) and 470 (five landing minors).
- Card `hpsmpoc-405-406-two-held-items-1111`, read by `decision_queue.sh show <exact id>`: options a "Leave both as they are", b "Change both", c "Decide each"; ruling `choice='a'` at 2026-11-11T17:18:34+11:00; no delivered line (MEASURED, 13-line output).

## Classification
**462 (pill fill versus outline)**
- Fill half: DONE at main (above); comment 41120 says "the first part is met".
- (B-1) Review half: "a UX/UI review with itemised screenshots", neither done nor scoped as its own ticket. Needs the product owner. Question: "Do you want a UX/UI review of the buttons scoped as its own ticket, or recorded as declined, given the fill defect is fixed?" Default: record it as declined with the fix as the answer (nothing is built and it costs no phase budget; the lesson says build only what this phase needs). Files touched: none.
- (B-2) Sidebar rows (and the skip link, which declares `focus:rounded-md`) still square to 4 px on keyboard focus; `web/e2e/shell-sidebar.spec.ts:290-296` pins the sidebar's 4 px as "the ring it always had" (RELAYED from B1503 STATUS lines 67 and 79). Changing it edits a spec and a product look: a decision. Question: "Should the sidebar's keyboard-focus corner stay at 4 px as the spec pins it?" Default: yes, leave. Neither element shows a fill that disagrees with its outline (one radius serves both), so I did not find a defect. Files it would touch: `web/src/app/globals.css`, `web/e2e/shell-sidebar.spec.ts` (an e2e file, outside every earlier kit's fence).

**406**
- Item 1 built (comment 40746). Item 4 built (311). Item 5 declined (C-359).
- (B-3) Item 2 (one-column order of Recommended next actions and Practice readiness; 1280 table density) and (B-4) item 3 (pipeline table stages versus the "Customers by stage" bars). Both are layout calls ("a later ticket may set the order", the gate wrote), and both sit on what the v2.1 partner-dashboard rebuild replaces: ticket 457 lists "Customers by stage" (P2-026) as removed, the "Customer assessment pipeline" panel (P2-030/031) as replaced, "Recommended next actions" (P2-032) as restructured and the grid composition (P2-036); 457's text says "whether they survive the rebuild is open". Main still has `Customers by stage` at `PartnerDashboard.tsx:174` and the pipeline panel at `:143` (MEASURED, grep). Under the product owner's 2026-11-10 13:42 ruling nothing derived from the v2.1 HTML is built before he and his colleague mark the phase decision document, and under the build-only-this-phase lesson a fix that the rebuild deletes is waste. Question: "Items 2 and 3 of the Home notes: hold until the phase decision document is marked, then record them as superseded by the dashboard rebuild or as declined?" Default: hold; nothing built; the records seat notes them as waiting. Files they would touch: `web/src/components/partner/PartnerDashboard.tsx`, `partner/parts.tsx`, `partner/home-next-actions.ts`, the dashboard's mock data source.

**405**: Done. Nothing remains.

**357 (360 px sideways scroll)**
- (C-1) UAT half: UAT is held, no measurement at 360 px on the UAT copy, none possible (no hosted HTTP). The mock half is met at main (comment 41122). Held until UAT is reopened; question for then: "Measure the UAT copy at 360 px after the next UAT deploy, or record the UAT half as declined?" Default: hold.

**Also found, outside the four tickets (not classified into this kit)**
- Ticket 470 (Backlog, five landing minors). Point 1 (the journey test `web/e2e/a11y.spec.ts:39` takes 26 to 28 s of a 30 s limit at main and times out under machine load) is engineering with no word and no ruling needed, so it WOULD be (A) if it were in scope; but it sits in an e2e file (`web/e2e/**`), the ticket itself says "which are built is a scope call that is not made here", and it was not among the tickets I was given. Point 3 (cut a long default owner at whole characters) is cosmetic engineering, also (A)-shaped. Points 2 (768 px cap of two blocks) and 5 (runtime float, a decision) are (B). Question for Tuesday (Q-1): "Add 470 point 1 (widen the a11y journey test's margin) as a small kit?" Default: no; hold until the HP Playbook feedback lane is partitioned, because it touches `web/e2e/a11y.spec.ts` which many lanes read.

## D-decisions
- D-1: not to widen the brief to 470 on my own (a kit I was not asked for, in a file class no earlier kit let a seat edit).
- D-2: not to write a "close with evidence" kit for 462/406/405 (a seat cannot write Jira, and those closures are the records seat's; the evidence is already in comments 41120, 41121, 41116).
- D-3: treat the stale premise as the finding rather than draft a kit that rebuilds merged work.

## Partition note for the later HP-feedback lane
The (A) set is empty, so the kit touches no file. If B-2, B-3 or B-4 are ever released, the files are those listed above; the HP-feedback lane should treat `web/src/components/partner/*`, `web/src/app/globals.css` and `web/e2e/shell-sidebar.spec.ts` as potentially contested until then, and `web/e2e/a11y.spec.ts` as contested if Q-1 is taken.

## Q-questions for Tuesday
- Q-1 above (470 point 1), default: no.
- Q-2: "Mark card `hpsmpoc-405-406-two-held-items-1111` delivered with artefact = Jira comments 41116 and 41121 and entry C-359?" Default: yes (Tuesday's own action; nothing for a seat).
- Q-3: "Put B-1 (462 review half), B-3 and B-4 on a card for the product owner now, or wait for HP's Playbook feedback?" Default: one combined card after the feedback arrives, since the feedback may supersede them.

## UNMEASURED
- Whether any button-like element OTHER than the sidebar rows and the skip link still snaps on focus at main: B1503's 80-route census (RELAYED, STATUS) says 0 of 2045 own-radius elements; I did not re-run it (no build, no browser, by the fence).
- The `focus:rounded-md` skip link's appearance (my claim that it shows no disagreement is DERIVED from one radius serving fill and outline, not measured).
- Whether HP's pending Playbook feedback touches any of the files above.

## Outside-the-fences disclosure
- One Bash call contained a `cd` (inside a compound command) and the hook refused it; nothing ran. I reran without `cd`.
- No project Jira read helper exists that is read-only (R217's and R219's helpers can write); I wrote a GET-only reader at `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s271/d1531/jget.py` that reads `4_Credentials/.env` in-process and prints no credential. GETs only, project HPSMPOC, issue and comment paths.
- I fetched the analysis repository's `CLARIFICATIONS.md` (2,060,302 bytes) by `gh api -X GET ... -H 'Accept: application/vnd.github.raw'` under the project's `GH_CONFIG_DIR` into the scratch folder, and main's four web files by the same route. One `gh api search/code` call returned an error and nothing.
- The card id came from my own reading of `2026-11-11_B1518_SEAT-R217_*.md` and its drafter report (slug text only), then `decision_queue.sh show <exact id>` once; no `list`. Not read: `briefs_staged/`, scoreboard, `_ledger.md`, WEDNESDAY/FRIDAY trees.
- All scratch is under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s271/d1531/`. No git write, no clone, no listener, no Jira write, no hosted HTTP.
