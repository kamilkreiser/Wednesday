# DRAFTER COMMISSION — brief for Seat S 125th (Secuura/Blockchain-S: one licensed close + one live anonymous-caller check)

Written by Wednesday 2026-11-26 (morning). You are a DRAFTER: write ONE brief file and nothing else. You do not launch, mail, post, or touch any project file outside the output path. Every project tree is READ-ONLY to you (git read verbs only: log, show, diff, ls-tree, ls-remote, cat-file; `git --no-optional-locks status`).

## Output
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-26_seatS125_close2111_check1699.md`

## Template
Copy the SHAPE (sections, STAMP block, PROVENANCE table, plan-QUESTION-first rule, the launcher first-action warning, never-cd / never-rm / MOVE rules, mail tooling, WRAP section) from
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-25_seatS124_board_census.md`. Read it WHOLE first. Keep everything about seat discipline; replace the work items. For the licensed Linear close + archive step, read how Seat S 124th did it (its LICENCE: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-25_S124_licence_A.md`; its STATUS: `.../2026-11-25_S124_status_closed.txt`) and point the seat at the same kit, by path, after confirming the path exists.

## Authority (quote verbatim in the brief)
- Kam, live board 2026-11-25 18:21:21 (view=wednesday): "Please close and merge and archive what you can. That looks like great progress." (EXPIRING-GRANTS row: Wednesday's reading, this batch through Sun 2026-11-29.)
- Kam, live board 2026-11-25 06:57:19 (usage grant): "keep working.  I will log in with a new account after usage runs out".
- Kam, live board 2026-11-25 11:53 (to the other seat, recorded in Wednesday's note as the reason KS-1699 was not closed yesterday): "You should have tested". A security ticket is not closed on an untested line.

## Item 1 — KS-2111: close + archive (licensed, no comment)
Facts Wednesday measured 2026-11-25/26 (re-validate each at source and cite the instrument):
- KS-2111 "Admin Settings page pollutes Object.prototype on save when a stored settings category is named `__proto__`", In Progress, P3.
- Fix = PR 2159, merged (find its merge sha on develop; Wednesday's 11-25 note says it is live on Kintsugi round k45 in the api-gateway and admin portal).
- Gate 419's two sibling findings are filed as KS-2362 and KS-2363 (Backlog, created 2026-11-24, each names G419 and KS-2111) — verified on Linear by Wednesday 2026-11-25 19:28.
- The live 400 on the settings PUT and the live page are UNMEASURED (a platform-admin login is needed). Kam accepted the same class of close before (KS-2314, KS-2331, jsdom-only). The brief must say this plainly: the close rests on merged + deployed + unit/jsdom proof, and the live admin check was NOT made.
The seat: re-read state at source; then in its STATUS, propose the close; Wednesday answers with LICENCE CLOSE naming KS-2111; only then Done + archive, read back.

## Item 2 — KS-1699: a live ANONYMOUS-CALLER check on Kintsugi, then (only if clean) close
Read the ticket WHOLE first (title, description and all 8 comments, `comments(first:50)` sorted client-side). The routes: `POST /api/certifications/:id/verify`, `/:id/share`, `/:id/recertify`. Kam's rulings that changed the expected answers (from the ticket's 2026-11-16 comments; re-read them there, do not take this list as truth): verify is open to ANYONE including anonymous (card secuura-cert-verify-anyone-or-signed-in-1116 = b), and an anonymous call records NO billing event (card secuura-cert-verify-anonymous-billing-1116 = a). PRs 2250, 2233, 2239 merged; PR 2228 closed unmerged on Kam's ruling. Gate 375 (on PR 2250) left "anonymous callers get an answer on the running stack" UNMEASURED.
Derive from the ticket + the merged code at develop (cite file:line) an EXPECTED-ANSWER TABLE: route x caller (anonymous; and, only if a test account the seat legitimately holds exists, a signed-in non-party) -> expected status and body shape, plus "billing event written: yes/no" for verify.
Then the LIVE check on KINTSUGI ONLY (the dev box; never demo, never demo-pk, never anything named prod/UAT). Find how earlier seats reached Kintsugi (Seat D 87th's HANDOVER / the k45 brief under `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-24_drafter-seatD87-kintsugi-k45/` and the brief it produced) and give the seat that exact path. Confirm first that Kintsugi runs a build that CONTAINS the three merges (ancestry of each merge sha against the running service's recorded base).
LICENCE for the live check (write it into the brief as such): anonymous HTTP calls to the three routes on Kintsugi, at most 3 calls per route per caller class; a verify call may write an audit/verification row on the dev box (that is expected and licensed); NO share or recertify call may target a real certification with a signed-in caller unless the seat holds that test identity legitimately — anonymous calls only otherwise. No database write by hand, no deploy, no restart.
If every row of the table matches: the seat proposes the close in its STATUS with the table; Wednesday answers LICENCE CLOSE; Done + archive + read back. If ANY row differs: STOP, no close, FINDINGS mail to Wednesday with the measured difference.

## Holds (in the brief)
No Linear COMMENT on either ticket (closes only), no ticket creation, no PR, no push, no mail to any human, no demo/demo-pk/prod contact, no card writes. External comms, production, money and anything irreversible beyond the licensed closes are Kam's.

## Routing
Model: Sonnet (newest; Wednesday fills the id from models_latest.json at launch). Lane -S. Seat name exactly `Seat S 125th`.

## Return
When the file is written, reply with its path, byte count, and every fact in this commission you could not validate against the source (also mark it UNVALIDATED in the brief), plus any fact you found to be WRONG (with the source that says so).
