# Wave 14:40, 2026-11-15: common commission for four in-session kit drafters (Tuesday s278)

Tracked file, so the commission survives this seat's rotation. Each drafter gets this file plus its own
paragraph below. A drafter whose output files are absent at the next boot is RE-COMMISSIONED from this file.

## For every drafter
1. Read `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/DRAFTER_RULES.md` whole, first. Its paths say
   `/Volumes/Laptop-DEV/`; on this machine every such path is `/Volumes/Datasec_DEV/` (same tree, renamed drive).
2. Copy the SHAPE of your template kit (named below) and read its drafter report for the method.
3. Write ONLY your kit and your report into `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/`, plus
   the `.measured` sidecar via `stamp_check.py --init` and your own scratch files under
   `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s278/d<B-number>/`.
4. `stamp_check.py <kit>` must exit 0 before you report STARTABLE. The report's LAST line is
   `DRAFTED B<n>: kit <lines> lines, sidecar rc <rc>, questions <n>`.
5. Kam's rulings today (live board, view=tuesday, all option a), verbatim:
   - 13:47 `mpscalc-170-fleet-line-id-name-1115`: "a — fleetLineId, screen unchanged"
   - 13:48 `nexusai-field-grant-holder-1115`: "a — Viewer keeps them"
   - 13:48 `mpscalc-rollforward-stop-words-1115`: "a — Approve the words as written"
   - 13:48 `datasec-morning-plan-1115`: "a — Noted, carry on"
   - 13:48 `hpsmpoc-168-industry-list-1115`: "a — Keep the ten-option customer list as built; make the snapshot
     placeholder field a four-choice list (Healthcare, Financial services, Public sector, Other)"
   Read a card's full text only by `decision_queue.sh show <exact id>` into a scratch file (DRAFTER_RULES fence 1).
   In kit text the seat copies into commits/comments, cite a ruling as "the product owner's 2026-11-15 ruling".
6. Kam's standing words today: "keep going with the tickets" (Tuesday terminal, three times).
7. Live seats at commission (14:40): `Datasec/MPS-M139` (B1573, branch b1564, LaneMA tests + pool),
   `Datasec/MPS-M138` (B1572, evidence only, no repo write; may still be waiting to launch),
   `Datasec/NexusAI-N130` (B1568), `Datasec/HPSM-POC-H165` (B1571, `web/e2e/a11y.spec.ts` only, ports 9890-9899).
   Re-read `tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'` yourself.

## B1574 SEAT-R233 — MPS records (template: `2026-11-15_B1562_SEAT-R232_mps-records-192.md` + its report)
Landed today, NOT deployed: **#193 -> main ee447909** (kit B1566: MPSCALC-396 comments, 334 dev-stub held-rental
update, 399 dev-stub rebate default + Duplicate; gate `tuesday/briefs/2026-11-15_B1566_verify/VERDICT.md`
GO WITH FINDINGS, Minors M1/M2 stub fidelity -> ticket them) and **#194 -> main 3a69065a** (kit B1570:
MPSCALC-400 order, 401 shallow-is-undecided, 403 `\Z` anchors; gate `.../2026-11-15_B1570_verify/VERDICT.md`
GO WITH FINDINGS, 1 Minor about the kit's own 'no node' fact: decide whether it is a ticket or a kit note, say
which). Also: Kam's two MPS rulings (170 and the roll-forward stop words, item 5) into C-entries and comments on
their tickets (MPSCALC-170, MPSCALC-402); OWED to the stop-word ticket: the 401 shallow case prints
'git answered 128' though git answered 1 (RELAYED from s277's note; measure it at main 3a69065a). A records
closing for MPSCALC-91 if it is ALREADY-ON-MAIN (prove it at main). Ticket moves per the MPS records rule in the
template. B1564/B1573 is IN FLIGHT: not recorded here.

## B1575 SEAT-R234 — HPSM-POC records (template: `2026-11-15_B1558_SEAT-R230_hpsmpoc-records-317.md` + its report)
Landed today, NOT deployed: **#318 -> main 8766b253** (kit B1565, HPSMPOC-193 forward proof; G1 gate
`.../2026-11-15_B1565_verify/VERDICT.md` GO WITH FINDINGS: Minor 1 at Program.cs:130 -> ticket it; the Key Vault
reference refusal is a REQUIREMENT on the later infra kit -> record it on the ticket, build nothing). Kam's
hpsmpoc-168 ruling (item 5) -> C-entry + comment on HPSMPOC-168 (the build is a separate kit, B1577). OWED since
2026-11-11 (PRIOR-WORK CHECK first: a later records seat may have done some): a C-entry for the UAT user guide
v0.4 (emailed to the product owner 2026-11-11); TWO tickets from its FOUND (walkthrough step 12 says
"Service offers" while the menu says "Delivery phases"; Consultant/Admin customer lists show a fifth customer
not marked "(sample)"); and the record of the hpsmpoc-b1466-pre backup-copy deletion done on the product owner's
2026-11-11 word (D60, kit B1490). Next-phase/HTML items stay held.

## B1576 SEAT-R235 — Security Composer records (template: `2026-11-14_B1552_SEAT-R228_composer-records-128.md` + its report)
Landed today, NOT deployed (Composer deploys only on a card): **#129 -> main 27adb709** (kit B1569, PCOMP-128
items 3 and 4, three Route B bullets in DEPLOY.md; G2 gate `.../2026-11-15_B1569_verify/VERDICT.md` GO WITH
FINDINGS, 1 Minor -> ticket or record, say which). The kit's 12/6 diff prediction was a drafting miscount (the
real diff is +9 -3): the record states the real numbers only.

## B1577 SEAT-H166 — HPSM-POC builder: HPSMPOC-168 (template: `2026-11-15_B1571_SEAT-H165_hpsmpoc-lane-h3-a11y-journey-margin.md` + its report)
Build Kam's ruling (item 5): the ten-option customer industry list stays as built; the snapshot's placeholder
industry field becomes a four-choice list: Healthcare, Financial services, Public sector, Other. Find the field
and every test/fixture/generated file that pins its OLD shape by program (a by-program census, ledger 2026-11-15
B1555 row) and list each as rewrite or unaffected. Those four labels are the product owner's words, verbatim; no
other new user-readable word. Ports: choose a free block (start 9920-9929; check per DRAFTER_RULES). Must share
no path with H165 (`web/e2e/a11y.spec.ts`). Model row by `model-routing.md`; G-tier by what it touches. One
branch `b1577/...`, one plain push, no PR (Tuesday opens and lands through CodeQL). Nothing deployed; no
HP-tool integration.

## B1578 SEAT-M140 — MPS builder: MPSCALC-170 fleetLineId (added 15:04 by s278; template: `2026-11-15_B1573_SEAT-M139_mps-ma-round2-pool-determinism.md` for the MPS build shape + `2026-11-15_B1566_SEAT-M136_*` if present)
Build Kam's 2026-11-15 ruling (item 5, mpscalc-170 option a, verbatim "fleetLineId, screen unchanged"; the option's words: "Approve fleetLineId. The audit screen keeps showing fleet[line number] and the id is stored alongside it, so staff see no new word."): a stable id on each fleet line in the API contract beside fleetLineNumber; old quotes get an id worked out on read and saved ones keep it; the price audit finds a fleet line by the id so removing one line and renumbering the rest no longer records override changes nobody made (MPSCALC-170 clause 1, the row on renumbering after a removal; read the ticket and comment 40395 whole). Customers and staff see no new word. By-program census of every test, fixture, generated file (openapi.json, schema copies, stub) that pins the old shape, each REWRITE or UNAFFECTED. Name the toolchains by PATH (DRAFTER_RULES, added today: `.tools/dotnet-10.0.404` as DOTNET_ROOT). Partition: must share no path with M139 (B1573: LaneMA test files and the source-wait pool on branch b1564) — check its kit and say so; M138 writes no repo file. Model row and gate tier by `model-routing.md` (a contract change: say which row and why). Ports: a free block (start 9930-9939). One branch `b1578/...`, one plain push, no PR. Nothing deployed (MPS hosted is a card per deploy). Records (C-entry, Jira) are NOT this seat's: the MPS records seat R233 is recording the ruling now.

## B1579 SEAT-N131 — NexusAI: rebuild PR #202's counts after #201 landed (added 15:30 by s278; template: `2026-11-15_B1567_SEAT-N129_nexusai-lane-b-test-pins.md` + its landing file `2026-11-15_B1567_verify/landing.txt`)
PR #201 LANDED 15:28 by head-pinned merge commit: NexusAI main = `0fdc77f0181bf7b0534ca562ebb142c8e5da435e` (parents 4ba2e03c + a6eae4f1; Deploy demo read skipped). PR #202 (branch `b1567/nexusai-lane-b-test-pins`, head `8586c094434b294749dc66ea02d6c35f3690a44f`, gate G2 GO 0 findings) now conflicts on `scripts/verify-expected-counts.json` (#201 set 5651/352; #202's head says 5638/349; base 5636/349). The seat: ONE merge commit of origin main into the b1567 branch (the only allowed conflict is the counts file; any other conflicted path = STOP), then regenerate the counts with `npm run verify -- --maxWorkers=2 --update-counts` on the merged tree (NEVER by hand; expected 5653/352 = 5636 + 15 + 2 suites +3: the drafter MEASURES or marks the expectation DERIVED, never a 'measured' guess), one counts commit, ONE plain fast-forward push to the existing branch (moves #202's head; no force). Prove by program that the new head differs from 8586c094 only by main's changes plus the counts file (`git diff 8586c094 <new head> --name-only` minus main's diff). It takes the NexusAI jest lock (the shared FIFO; N130 B1568 holds it now). Model row and gate by `model-routing.md` (a mechanical rebuild; say whether a gate round is owed or Tuesday's own diff check suffices, with the rule). Nothing deployed; the demo hold stands. The NexusAI records pass (#201, #202, the field-grant ruling, the B1563 F1 ticket) is a LATER kit, not this one.
