# C2 findings — audit C (rule accuracy + status), listC.txt lines 20-38

| file | audit | what was wrong | evidence |
|---|---|---|---|
| 2026-09-14_local-model-pilot-grant-qwen3-30b-simple-checked-tasks-only.md | C (status) | Marked `superseded`, so it is on no card. The file's own frontmatter says `status: live` and its body names no successor. The newer lesson supersedes it only "in model and in hours", and 09-16 says the mechanisms stand. Its still-binding limits (single file-in/file-out tasks, mechanism-checked, never a ruling/brief/gate/coordination, no board identity) are not carried by the Ornith row it points at. Spec: partly superseded = `live`, rule states the half that holds. | pilot file L5 `status: live`; L18-22 "it never coordinates and takes single tasks with a file in and a file out ... only work a MECHANISM checks afterwards ... never a ruling, a brief, a QA gate"; ornith-runs-at-night L53-54 "the pilot this supersedes in model and in hours"; 2026-09-16_local-model-is-long-term L27-30 "the *mechanisms* in both stand; what lapses is the language of a pilot" |
| 2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md | C (missing load-bearing clause) | The cap is stated without its authority clause: a third round on the same class needs Kam's word on a card. Without it the row does not say the coordinator may not open round 3 on her own. | L11 "no third round without Kam's word"; L21 "A third round on the same class needs Kam's word on a card." |

CHECKED: 19  WRONG: 2

Status checks inside this slice: 3 rows marked `dead` (all three verified: frontmatter `expires: 2026-09-13`), 1 row marked `superseded` (wrong, above).

Found correct (17):
- 2026-09-05_a-relayed-ruling-is-delivered-only-when-it-is-in-the-artefact.md (rule text current through the 09-23 RELEASE extension; enforced_by not audited here, see note)
- 2026-09-06_a-scoped-override-carries-its-own-expiry.md
- 2026-09-07_a-mechanism-is-recorded-by-its-path-not-its-runtime-id.md
- 2026-09-07_deploy-grant-and-fix-the-visible-data.md (dead: L7 `expires: 2026-09-13`)
- 2026-09-07_production-ban-lifted-for-the-week.md (dead: L7 `expires: 2026-09-13`)
- 2026-09-08_a-false-absence-is-usually-my-own-instrument.md (carries the 2026-11-10 "a returned line is PRESENT" form)
- 2026-09-08_a-ruling-can-be-voided-by-removing-its-precondition.md
- 2026-09-08_the-check-ran-and-was-not-checking-the-thing.md
- 2026-09-09_acknowledge-panel-instructions-on-receipt.md
- 2026-09-09_quarantine-by-rename-is-not-removal-on-an-additive-sync.md
- 2026-09-10_a-reviewers-protocol-is-our-acceptance-criteria.md
- 2026-09-10_claim-a-task-with-tuesday-before-starting-it.md (the "suspended while stopped" clause is not in this file; it is in 2026-09-14_the-coordinator-adds-value-or-it-is-waste L70, and is correct)
- 2026-09-10_deploy-both-boxes-grant-expires-sunday.md (dead: L6 `expires: 2026-09-13`)
- 2026-09-10_surprising-measurements-are-selector-errors.md (carries the later "before a step consumes a derived set" trigger)
- 2026-09-11_secuura-we-approve-and-merge-our-own-tested-work.md (carries the 17:50 extension's exclusions)
- 2026-09-14_coordinator-adds-value-or-stops.md
- 2026-09-14_the-coordinator-adds-value-or-it-is-waste-three-duties-not-watching.md

Outside this audit, noted for audit B: the relayed-ruling row names `send_brief.sh` as enforcer. The lesson says the tool refuses only a brief lacking the `RULED BY KAM` section (L47-49). The Wednesday-rulings section, the mark-is-not-the-world rule, the UNKNOWN rule and the RELEASE-in-handover rule are each an "enforcement candidate" or unenforced (L66, L105, L139-149), and the enforced listing truncates the rule at 120 characters.

Not checked: seats and enforced_by fields; whether the three dead grants' `doctor.sh` warnings still exist; whether any grant was renewed outside the learnings folder.
