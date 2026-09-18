Seat A 10th successor (Secuura/Blockchain), from Wednesday

## BLUF
**Two jobs, in order: (1) the #922 fix round, then (2) raise four local-model fixes as PRs.** You merge nothing in this session unless I send you a signed GO. #922 does NOT merge at all while Peter's review is open. **Your predecessor (the 9th) wrapped clean at ~02:32Z. Read its handover first; it names the traps.**

## ITEM 0 — boot, before any write
- Read your predecessor's handover WHOLE: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatA-9th-successor-2026-09-18.md` (FINAL STATE at the top).
- Re-read `origin/develop` and `refs/pull/922/head` yourself. The values below are MY reads; **if either has moved, say so before acting.**
- Send me your plan confirmation (QUESTION mail, topic `plan confirmation`) before the first write.

## QUEUE, in order — every write gated on the previous step's rc
**1. #922 fix round (KS-679).** The spec is my mail to your predecessor at 2026-09-18T01:16Z, subject beginning `#922 gate GO WITH FINDINGS - one fix round ordered`, plus the gate report `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks679-922-8664826e5-tier2-r1/report.md` (findings F1-F7). In short:
- **F1 (the reason for the round):** the E7 exemption `/^[a-z]+_<uuid>$/i` in `scripts/spec-examples/check/contract.mjs` lets `token_<uuid>` and `secret_<uuid>` through to NOTHING. Bound the prefix (for example `[a-z]{2,12}`) and deny secret-named prefixes (`token|secret|sk|pk|key`). **But `key_<uuid>` in services/security is a legitimate RECORD id, so allowlist that exact site and measure it; don't guess.** Decide on `/i` (the service mints lower-case). **Pin each boundary with a cell, then re-run the gate's five loosenings: each must now go red.**
- **F3:** body `Closes KS-679` → `Refs KS-679`, Linear link kind `closes` → `contributes`. KS-679 is In Review today and is NOT moved to Done on merge (external `anc_` consumers are unmeasured).
- **F2, F4, F5:** polish (a false red-proof claim in the record, stale Test Evidence, stale line citations in shipped comments: anchoring `index.ts:423/:727` are `:473/:806` at head).
- **F6** (eslint applies `rules: {}` to `scripts/**/*.mjs`): FILE a ticket; don't fix it in #922.
- **F7:** the gate wrote "no preflight record at 8664826e5". That's false (see `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-18_seatA-9th/ks679/push.out` :1009-1031, YOUR project). The new push makes a new preflight record; cite that.
- **The branch is held by a quarantined worktree** (`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/quarantine/2026-09-15-s233/worktree-ks679`, YOUR project). Your predecessor worked detached and pushed to the ref. Never enter the quarantined worktree.
- **Then push, and mail me the new head.** I gate the DELTA only.
**2. Raise four local-model fixes, one PR per ticket.** Each is HELD, source-read and PASS 7/7 in my project. **Apply each diff VERBATIM at current develop, run its own test red-first then green, and only then raise.** If a diff doesn't apply cleanly or the test doesn't red-then-green, **STOP on that one, report it, and don't hand-fix it.** The files are in MY project (read-only to you):
- KS-1233: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1233_ornith35b-q4_BRIEFED-REDIS-NOTTL-PASS-7of7_2026-09-18.diff.md`. **Put its deploy caveat in the PR body verbatim:** the fix covers the write path only, and an existing key keeps its TTL.
- KS-1125: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1125_ornith35b-q4_BRIEFED-TESTONLY-DIRECTCALL-PASS-7of7-ON-RETRY_2026-09-18.diff.md` (test-only).
- KS-1209: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1209_ornith35b-q4_BRIEFED-BASHPATCH-FAILCLOSED-PASS-7of7_2026-09-18.diff.md` (**it changes the pre-push gate everyone runs; say so in the body**).
- KS-1248: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1248_ornith35b-q4_BRIEFED-DEGRADEDADVICE-PASS-7of7-ON-RETRY_2026-09-18.diff.md`.
- Every PR: `Refs KS-<n>`, linkKind `contributes`, no closing phrase. **Mail me all four heads in ONE mail.** They are file-disjoint, so I gate them as ONE batch (Kam's 09:22 rule on minimising gate duplication).

## HOLDS — do not do these
- **#922 does not merge**: Peter's 09-09 review ("not approving yet") is open, and merging over it is Kam's decision, pending.
- **KS-1250: do NOT raise it.** After it, a full smoke run against a named gateway logs in with the demo credentials, POSTs and ANCHORS a real document there. That's Kam's call.
- **No kintsugi deploy this session.** #1037 lands at the next deploy; don't take Stuart's box for ~2 h to land one PR. It gets batched with the next merges.
- **Nothing to demo.** No direct messages to humans; the rule-7 ticket comment at wrap is the only channel.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- 2026-09-18 10:27, verbatim: *"deploy to kintsugi. this is the dev server so it should be the first to update. the other server should only have proven deploys."* So demo takes only kintsugi-proven work, and that comes BEFORE Peter's formal nod, not instead of it.

## What Wednesday owes you
- A delta gate on #922 when you mail its new head; a batched gate on the four PRs when you mail their heads; a signed GO naming each head before any merge.

PROVENANCE:
- origin develop = 207716440e2a6282b90ed2a118614d9cf98bee1e (#1037 merged) | git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin refs/heads/develop, run 12:31 AEST - YOUR checkout | read 2026-09-18
- refs/pull/922/head = 8664826e53cc47d4dd69c784926c9c14af444cec | git -C /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files ls-remote origin refs/pull/922/head, run 12:31 AEST - YOUR checkout | read 2026-09-18
- KS-679 In Review with PR 922 attached; KS-1233, KS-1125, KS-1209, KS-1248 and KS-1250 are Backlog, not archived, with NO PR attached | Secuura Linear GraphQL, read-only query run by Wednesday 12:3x AEST (7 of 7 returned) | read 2026-09-18
- #922 gate verdict GO WITH FINDINGS, findings F1-F8 | /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks679-922-8664826e5-tier2-r1/report.md - QA project, read-only | read 2026-09-18
- Peter's 09-09 "Review — not approving yet", answered 09-14, no reviewer reply since | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-18_gate922/pr922_snapshot.md (GitHub API capture 00:45:15Z) - my project, not yours | read 2026-09-18
- the four READY diffs, each PASS 7/7 and source-read by Wednesday | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-*_2026-09-18.diff.md - my project, not yours | read 2026-09-18
- your predecessor wrapped clean; rule-7 comments posted (KS-485 b12eaaa2, KS-772 bf13f13f); kintsugi runs a105cd32b | seat A 9th wrap mail to wednesday-agent@agentmail.to, 2026-09-18T02:30Z | read 2026-09-18
- weekly usage 25%, under the 90% cap (the 40% cap was lifted by Kam 2026-09-17 11:21) | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/usage_gate.sh and fleet/USAGE_STOP, run 12:31 AEST - my project, not yours | read 2026-09-18

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-18 12:32
- Merge authority is consistent: #922 needs Kam's ruling on Peter (not my GO alone); the four new PRs need my signed GO after a gate; nothing merges in this session without a mail from me.
- KS-1250 appears only under HOLDS, never in the raise list.
- FOUND AND FIXED by this check (self_check_view): (a) KS-679's state was hedged "In Review / In Progress"; it's In Review, and the real claim is that it is NOT moved to Done on merge. (b) two body paths (`ks679/push.out`, the quarantine worktree) were relative; both are now absolute and marked YOUR project. Every other path was already absolute.
- Ticket states were read fresh at 12:3x: none of the five fix tickets already has a PR, so no queue item is stale.
