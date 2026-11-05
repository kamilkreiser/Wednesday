# DRAFTER REPORT: Seat F 34th, KS-692 bind-creator (drafted 2026-11-05 ~17:0x AEDT)

## BLUF
- **Brief:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-05_seatF_ks692_bind_creator.md`. Seat **F 34th** (max F ordinal in history.md is 33rd at line 275, 33 F headings, F 34th 0 hits, control F 33rd 1 hit). `claude-opus-5-5`, routing row C3 (line 93) for the build, gate row G1 (line 108) tier 1.
- **One ticket, KS-692, one PR.** Develop measured `5fc5569ed96ac61f64823cc9e1fa841899aa1f62` (ls-remote, local object present).
- **Scope sentence quoted (ticket description):** "`POST /api/status/:id/revoke` and `/unrevoke` enforce an **admin-class role** but **no tenant ownership check**. An `ISSUER_ADMIN` in one tenant can revoke or un-revoke a credential in **another tenant's** status list." Newest ticket text: "Left open: the "bind-creator later" step of Kam's 2026-09-16 interim ruling is not built."
- **File family, measured:** vc-issuer only. Handlers in `Blockchain/Dev/services/vc-issuer/src/routes/status.ts` (revoke line 247, unrevoke 304, router-level role gate 46-57). The gateway only proxies (`proxy.ts:1010`). **No live seat holds any needed file, so no stop-and-ask on the family at send.** Existing tests that pin the interim and must flip (declared, not deleted): `ks692-status-write-platform-only.test.ts` (A1, A2) and `ks586-status-write-authorization.test.ts` (OWNER 403 on every write route).
- **Four design questions are left to the seat as QUESTION mails (not pre-answered).** The first one needs Wednesday's eye before sending (below).

## Things that look wrong or need Wednesday before send
1. **Q-A (the big one): "creator" of what?** The ticket description, the 09-16 card ("credential_status_lists has no owner column, so bind-creator needs a migration") and the PR 1320 comment all assume a status LIST must carry an owner. Today's card and your commission say "same pattern as KS-1851", which keys on the stored owner of the CREDENTIAL named by the request body's `credentialId` (`credentialRepo.getRecordById` + `mayReadCredential`). That design needs no migration and no list owner. The brief commissions the KS-1851 reading and makes a migration or a list owner an explicit STOP. Confirm that is what Kam meant.
2. **Q-B: "keeping platform-role access as KS-1851 does".** KS-1851 as merged (with KS-1906) gives platform administrators NO blanket bypass: only owner-less credentials of their own tenant; a platform admin of another tenant gets 404 on an owned row. Today the status routes let any platform role revoke any entry in any tenant. Copying KS-1851 exactly NARROWS platform access on these two routes. The brief tells the seat to measure both sides and ask, not decide.
3. **Q-C: the router-level role gate** (`status.ts:46-57`) 403s every non-platform role before the handler, so "the creator allowed" is impossible until it is restructured; `create` and `allocate` are not commissioned and must keep refusing. The seat proposes the shape.
4. **Q-D:** which of the route's two existing 404s is "the unknown-id answer".
5. **Red-first trap, stated in the brief:** "another tenant's ISSUER_ADMIN refused" already PASSES at develop (403 from the role gate). The cell that is red for the right reason is "the creator allowed". The brief requires the seat to say which cells pass at develop.
6. The issue route does not allocate into status lists (own counter at `credentials.ts:122,160`), although `vc-issuer.openapi.ts:1039` says it does. Entries exist only via a platform `POST /allocate` with an arbitrary string, so some entries may name a credential that is not stored; the brief puts that under the availability cost.
7. The lane plan never mentions `status.ts` in any lane (lane I rows are KS-1295 and KS-1898); I found no other lane holding it.

## NOT commissioned (listed in the brief)
Per-list owner column or migration; `create` / `allocate` gating; the stale "tracked on KS-586" wording in the ks586 test header (comment `7074e6f1` candidate, only if the seat edits those lines, declared); KS-1429 (systemTest, Backlog, blocked by this ticket, to be named in the READY mail only); Peter's two questions on the ticket (comment `4e3680dc`); KS-1899, KS-1900, KS-1898's third ask, KS-1295, KS-1371 (Peter-assigned, touches `status.ts` unrevoke `index` validation lines 327-331; do not touch); KS-570; any deploy, live check, state change or new ticket. KS-692 stays In Progress (Done rule: deploy owed).

## Tickets excluded
None beyond the above; the commission named KS-692 only.

## UNMEASURED (all written as UNMEASURED in the brief)
Open PRs touching `status.ts`, the ks586/ks692 tests or the inventory doc (no GitHub PR list read; only one remote branch names KS-692, `feature/ks-692-status-write-platform-only-b36-5` at `b9111f2bfad2`, the merged PR 1320's branch, flagged "do not push onto"); the vc-issuer whole-suite count at develop (no suite run); whether `vc-issuer.openapi.ts` / `secuura-api.yaml` (revoke at line 40771, unrevoke 40852) must change for the new 404; whether `systemTest/tests/test_status_list_authz.py` pins the interim 403; the sha kintsugi runs after D 54th; the pane id; tool contents (names only); staged ANSWER mails since the previous F brief.

## Instruments and boundaries
Read-only throughout: `git show` / `ls-remote` / `merge-base` reads only (no fetch); Linear GraphQL read-only (`first:50`, sorted client-side, `includeArchived` for KS-1851 and KS-588); cards via `decision_queue.sh show` and `list ruled --undelivered` (0 for Secuura, Secuura/Blockchain, Secuura/Blockchain-F). Scratch copies in the session scratchpad only. `self_check_view.sh` run on the brief; scope-word regex from `send_brief.sh:434` returned 0 hits; all 19 PROVENANCE lines have two or more pipes and a `read YYYY-MM-DD`. SELF-CHECK stamp left as the literal `@STAMP@`. The common part's floor paragraph was replaced by the T/V/S/J/E/U floor you gave.

Paths:
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-05_seatF_ks692_bind_creator.md
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-05_seatF_ks692_bind_creator_DRAFTER-REPORT.md
