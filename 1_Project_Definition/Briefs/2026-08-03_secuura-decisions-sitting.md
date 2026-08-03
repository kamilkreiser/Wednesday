# Secuura decisions sitting — one pass, board cleared

Prepared by Wednesday, 2026-08-03, from a read-only sweep of the Secuura Linear
board (KS team) + ticket comments. Estimated sitting: **60–90 min**. Structure:
real decisions first, then rubber-stamp closes, then things needing nothing.

---

## A. Decisions actually needed from you (4)

### A1 — KS-547 (P2): `/certifications/issue` has no role gate
Any authenticated user — OWNER, VERIFIER, anyone — can issue certifications,
while document writes enforce `DOCUMENT_WRITE_ROLES` in-service. Found in the
KS-540 roles inventory (F-2, HIGH, hand-verified). **Why it's a decision:** the
live demo certifies as `demo@secuura.io` (role OWNER) — today's demo UX depends
on the gap.
**Wednesday's recommendation:** gate it to match documents
(`DOCUMENT_WRITE_ROLES` + `certifications:write`) and make the demo user carry
an allowed role, then live-verify the demo flow end-to-end post-change. A
document-authenticity product cannot leave *issuing certifications* as the one
ungated write. The ticket lists the option variants — decide the role set in
the sitting, their agent executes.

### A2 — KS-480: Stuart's three K-side decisions (his 2026-08-02 index comment)
Stuart consolidated "everything waiting on Kam from the S↔K work" into one
comment — three need decisions. Note item 1 (issuer:null on verify) is already
FIXED and live-verified via KS-549, so confirm-and-strike it; the remaining
items include the flat-anchor metadata whitelist discarding S's event
timestamp (`metadata.timestamp` dropped by `buildFlatAnchorMetadataPayload`).
**Recommendation:** walk the comment in the sitting and answer inline on the
ticket — Stuart structured it precisely so nothing stays buried in-thread.

### A3 — KS-551 (P3): one dispatch-ref decision
The extranet test-runner fix is merged on develop and validated (real sweep
reached the VM: 819 scenarios). Remaining: the portal dispatches workflows with
`GH_REF=main`, and Git Flow means develop's fix won't reach main until a
release. Two options are on the ticket.
**Recommendation:** hotfix the workflow to main now (the KS-552 guard already
set that precedent with PR #630) — portal-triggered runs work today instead of
after the next release.

### A4 — KS-244 + PRICING docs: the "price structure review"
The core decision was already made (2026-06-23): **subscription tiers via
Platform S** — Free verify-only / Basic / Professional / Enterprise POA, usage
caps, IDV at cost — per `2_Project_Files/PRICING/`. Stuart's implementation
lane is already moving (PS-445 currency selector, PS-452 live FX — both P0 In
Review his side; PS-399 pricing-engine tests).
**Recommendation:** 30 minutes re-reading `PRICING/` against today's state,
confirm or amend the tier structure, then close KS-244 referencing the June
decision and let implementation live in the PS lane where it already is. If
anything in the tiers has shifted (e.g. on-chain cost assumptions now that the
demo does real preview anchoring), that's the thing to catch in this pass.

## B. Work done — reviews to confirm-and-close (6, fast)

| Ticket | State of play | Your action |
|---|---|---|
| KS-552 (P1) | Deploy-workflow money-burn guard live on develop AND main (hotfix #630, gates green) | Confirm + close |
| KS-549 (P2) | issuer:null fixed, live-verified on demo ("Flinders University" round-trip); Stuart's re-test nulls were pre-deploy docs (expected) | Confirm + close |
| KS-529 (P1) | Root cause was a DoS (one authed request killed the gateway) — fixed #619; amplifier defused by KS-546 | Confirm + close |
| KS-546 (P2) | Your unhandledRejection decision shipped both targets, boot-log verified; Peter's veto window | Close unless Peter objects |
| KS-540 (P3) | Roles inventory delivered (`ROLES-AND-AUTHORIZATION-INVENTORY.md`) | Confirm + close |
| KS-532 (P3) | DR restore drill EXECUTED + PASSED (69 s restore); recovery points confirmed | Confirm + close |

## C. Needs a real read, not a stamp (1)

**KS-539** — the R1–R7 agent-document-operation rules doc (PR #632). This is
governance for how *agents* may operate on documents — connectors-not-humans,
scopes as authority, mandatory `onBehalfOf`. Worth 15 focused minutes: these
rules will govern (among others) anything Wednesday-coordinated ever touching
Platform K.

## D. Waiting on others — nothing from you

KS-543 (Stuart to confirm the erasure fixes match his findings) · KS-472
(Peter's scope for points 2–3, nudged 07-30) · KS-518 (Peter re-verified: 10
ops still accept schema-violating input — next remediation wave is a build
task, not a decision) · KS-486/489 (living security registers) · KS-545
(mnemonic rotation — deliberately GATED to pre-go-live; no action).

---

*After the sitting: KS-538 (extranet comments box) is the agreed next build
item — see the companion pilot brief.*
