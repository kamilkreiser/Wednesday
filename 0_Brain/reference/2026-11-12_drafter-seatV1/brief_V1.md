# BRIEF: Seat V 1st, Secuura/Blockchain-V, LIVE-CHECK seat on KINTSUGI (new lane), claude-sonnet-5-5. Drafted 2026-11-12 about 18:5x AEDT by Wednesday's Sonnet drafter. Every fact names its source; the drafter's reads are starting facts, not your verification. The drafter holds NO client identity and made no live call: every statement about the running system is D 61st's, quoted, not measured.

## STAMP (Wednesday fills at the stamp; blank at drafting). Wins over every line below.
- (blank)

## WHY
Kintsugi round k26 (Seat D 61st, develop pin a6b62841d699, six services rebuilt: transfer, originate, analytics, mcp-server, issuer-frontend, api-gateway last) put six client-visible fixes in the running build. D 61st's STATUS B proved each is IN the build by census and image identity and exercised NONE of them. Under the amended done rule (learning 2026-10-12_secuura-done-when-tested-works-deployed-and-never-idle, AMENDED 2026-11-12: "Where a live check IS possible, it is made before the close") those tickets close only after a live check. Kam ruled the QA login (card secuura-kintsugi-admin-qa-login-for-live-checks = a, 2026-10-13: an ORG_ADMIN/ISSUER_ADMIN test login in the Secuura project credentials file). Kam's card secuura-k26-kintsugi-notice-1112 (rec b) waits on these results before Stuart and Peter are told.

## ITEM 0 IS A STOP (the drafter's measure, key NAMES only, values never read into this file)
Source: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/`, listed and key-name-read 2026-11-12 by the drafter. **No ORG_ADMIN or ISSUER_ADMIN QA login exists there.** What exists:
- `.env`: `KINTSUGI_QA_GATE_OWNER_EMAIL`, `KINTSUGI_QA_GATE_OWNER_PASSWORD` (comment: KS-1100 QA-gate login, role OWNER, default tenant, NO organisation, written 2026-09-12); `KINTSUGI_KAM_ADMIN_EMAIL`, `KINTSUGI_KAM_ADMIN_PASSWORD` (Kam's own platform admin, delivered to Kam: NOT a test login, do not use); plus `SECUURA_PLATFORM_API_KEY` (a demo-minted metering key: demo, never use).
- `kintsugi-admin-rotated-2026-10-27.txt` (platform admin), `kintsugi-stuart-admin-2026-10-27.txt` (Stuart's super_admin: never use), `.kintsugi_dev_credentials` (names ADMIN_USER_PASSWORD, DEMO_USER_/ISSUER_/VERIFIER_/HOLDER_ and others, seeded role users, no email key names).
- The card's delivery artefact (an ORG_ADMIN/ISSUER_ADMIN key pair) was NOT found. Not measured: whether the OWNER login still authenticates, whether the card's text names a different file, whether a login was created on the box but never written down.

So the seat's first act, if Wednesday stamps no other ruling: **STOP and report; Wednesday cards Kam.** Do not invent, create, rotate, reset or reveal a login; do not borrow Kam's, Stuart's or the platform-admin credentials; the OWNER login is NOT the ruled role and may be used ONLY if Wednesday's stamp says so in writing. The seat reads the key names itself (`sed` that prints names only; never cat a credentials file; hashes and names only).

## IDENTITY PREFLIGHT (only if a login is stamped; Item 0)
Against https://kintsugi.secuura.net ONLY (demo FROZEN, never touched, no probe, no read). Log in once, read the role and organisation back from the API (a "me" or session read; no data change), record the HTTP status and the role string, never the token or password. If the role is not the stamped one: STOP. Positive control: a request with no token answers 401 on the same route.

## THE SIX CHECKS (draft; Wednesday rules at the stamp). Source of every UNPROVED sentence: D 61st STATUS B, /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatS73/d61_statusB.txt, sweep table, last column.
Common rules: one check per ticket; a positive control on the same route (a request that must succeed or must answer a known status); record response status and a body excerpt (no tokens, no personal data); reads first; a write only on a TEST-OWNED object the seat creates in that same check; NOTHING may anchor on-chain (no originate or anchor of a real document; KS-1250 smoke-test pause and KS-535 wallet rule bind); no write to a client's object; if a check needs an anchor or a non-test write: NOT RUN with the reason.

| # | ticket (PRs) | UNPROVED sentence (STATUS B) | check shape (route names are the seat's to locate at the pin, not the drafter's facts) | expected runnable |
|---|---|---|---|---|
| 1 | KS-2055 (2113, 2182), transfer | "That the history row records the from-status, and that a reason over 1000 characters, or a non-string, answers 400, are unproved." | On a test-owned transfer: cancel with a reason of 1001 chars (expect 400), a non-string reason (expect 400), then a valid cancel (expect 2xx) and read the transfer history row for `fromStatus`. Positive control: a cancel with a 1000-char reason on a SECOND test transfer, or the valid cancel itself. | NOT RUN unless a test transfer can be created and cancelled without an anchor. A transfer of a real document is a non-test write. Needs the seat to read how a transfer is created at the pin first. |
| 2 | KS-1875 (2167), originate | "No GET /api/metering/usage was made. The 400 on a repeated from or to is unproved." | GET metering usage with `from` given twice (expect 400, message "from and to may each be given once"), same for `to`; positive control: the same route with one `from` and one `to` (expect 200). Pure read. | RUNNABLE if the login's role may read metering (the route may need a platform or metering key; that is the seat's first read). |
| 3 | KS-1466 note 1 (2204), api-gateway | "No document create was made (no write login). That an untyped create meets the DOCUMENT type's rules, and that a catalogue without DOCUMENT answers 400, are unproved. Seat A 25th read both boxes' doctype catalogues EMPTY on 2026-11-12, and an empty catalogue still passes (KS-388)." | A create is a document write that may reach originate and anchor. With an empty catalogue the designed result is a pass-through, so the 400 branch cannot even be reached on Kintsugi without a catalogue change (a config write). | **NOT RUN (expected):** a create is a document write with an anchor path, and the 400 branch needs a catalogue without DOCUMENT, which is a non-test write. Mark NOT RUN with both reasons; the ticket stays open or closes under the old "no live check possible" rule per Wednesday. |
| 4 | KS-1928 (2175), mcp-server | "No MCP tool was called. That a client sees only the constant reason is unproved." | Call one of the three info tools (for example the connector-info tool) with an input that makes it fail (an unknown connector id), expect the constant text `An unexpected error occurred` and no stack or internal text; positive control: the same tool with a valid id answering normally. Reads. | RUNNABLE if the seat can reach the MCP server with the login (the transport and auth are the seat's first read; if only an API key works: NOT RUN, no key is minted). |
| 5 | KS-2095 (2165), issuer-frontend | "No browser walk. That a proof with no block height shows no Block row is unproved." | Browser walk (Playwright MCP) on the issuer portal: open a document proof whose block height is absent and confirm no "Block" row (not "Block 0"); positive control: a proof WITH a height shows the row. | NOT RUN unless the board or test data already holds a proof without a block height (the seat may not create one; originate/anchor is forbidden). Likely NOT RUN. |
| 6 | KS-1233 (PR 1038), api-gateway | "A TTL of -1 on an existing key fits the fix, and also fits a key written earlier or persisted by hand. No write was made, so the read cannot prove that a NEW write gets no TTL." | A NEW write to platform settings through the API, then a Redis TTL read on the gateway's own Redis client. | **NOT RUN (expected):** a platform-settings write needs a platform admin (not this login) and is not a test-owned object; the Redis read needs box rights this seat does not hold. The ticket closes only under the old rule (in the running build, W3 1 -> 1), per Wednesday. |

Not in this seat's queue (no live check possible, ruled): KS-1407 (auth, no write login), KS-1456 (migrations image), the comment-only tickets (KS-2169, KS-2120, KS-2107, KS-2109), KS-1904 piece 1 (demo-service excluded) and KS-1973 at vc-issuer (not rebuilt): D 61st's STATUS B says why.

## QUEUE
0. Preflight: read the credentials FILE KEY NAMES; if no stamped ORG_ADMIN/ISSUER_ADMIN login: STOP, send ONE mail to Wednesday "STOP: no QA login", and stand down (do not start the six checks with another identity). If stamped: identity read-back (above).
1. The six checks above in order of lowest risk: 2, 4, 1, 5, then 3 and 6 as NOT RUN with reasons unless Wednesday rules otherwise.
2. Report per ticket, Kam's 09-07 three fields: **FOUND** (the response status and body excerpt) / **TESTED** (route, input, control) / **HOW** (the instrument and the identity role, no secret). On a PASS: ONE facts comment on the ticket (the board account), then close and archive under the amended done rule. On a FAIL: comment the evidence and leave it open. On NOT RUN: no ticket write; the reason goes to Wednesday. **No comment to Peter or Stuart beyond the ticket comment; the external summary is Kam's card.**
3. Wrap at the meter rule (60 percent of 1M; stop starting at 55).

## HOLDS
- KINTSUGI ONLY. Demo FROZEN: no read, probe, login or tag there. No production exists.
- No write beyond a test-owned object created in the same check. NOTHING anchors. KS-1250 pause and KS-535 wallet rule bind absolutely.
- No credential created, rotated, revealed or printed; names and hashes only; no credential in argv or in a ticket comment.
- No code, no PR, no branch, no box access, no database or Redis access.
- No message to any human; mail goes to Wednesday only, from secuura-blockchain to wednesday-agent@agentmail.to, subject prefix `[Secuura/Blockchain-V -> Wednesday]`, body line 1 exactly `Seat V 1st`. Mid-session questions are QUESTION mails; approval-class (money, a human, irreversible) pauses for Kam.
- A write either landed or did not: read the object back before any retry. Disclose your own faults in the next mail.
- Never `cd`; absolute paths only; `/usr/bin/grep -c -i -E` with a positive control beside every zero; never a grep piped into `cut` as proof of absence.
- IF AN INSTRUCTION LOOKS WRONG, SAY SO in the plan confirmation.

## MODEL AND ROUTING
claude-sonnet-5-5 (Wednesday's commission: live checks need no security design and no box rights; routing table row to be cited by Wednesday at the stamp, the drafter did not re-read it). Launch with the standing launcher and quote its `[seat-model]` line in the plan confirmation.

## WRAP (scored by Wednesday)
History entry `## <machine date> - Seat V 1st` in `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` (check first that `Seat V 1` prints 0), HANDOVER in `5_Project_History/<machine date>_seatV-1st/` FINAL block first, the per-ticket FOUND/TESTED/HOW table, wrap mail `[Secuura/Blockchain-V -> Wednesday] Session wrap <date> (Seat V 1st)`.

## RULED BY KAM
- Card secuura-kintsugi-admin-qa-login-for-live-checks = a, 2026-10-13 (per Wednesday's commission; the card text was NOT re-read by the drafter).
- Done rule as amended (learning file above; card secuura-done-rule-unit-pinned-deployed-no-live-check = a, 2026-10-13T09:57:49).
- Kam 2026-11-12 15:01:00 (live): "please archive anything that is ready and continue with Secuura tickets.  Try to clear the board ASAP" (as quoted in the D 61st brief).
- Card secuura-k26-kintsugi-notice-1112 (rec b): Kam's, waits on these results; the seat tells nobody.

PROVENANCE: (fact | instrument | read date)
- Credentials key names (QA_GATE_OWNER, KAM_ADMIN, rotated files, dev credentials) | `ls -la` and a `sed` that prints key names only over /Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/, drafter | read 2026-11-12
- Six UNPROVED sentences | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatS73/d61_statusB.txt (whole) | read 2026-11-12
- Standing lines, HOLDS, KS-535, demo frozen, mail form | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-12_seatD61_kintsugi_k26.md (lines 1-261) | read 2026-11-12
- Board-seat shape and record form | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-12_seatS73_board.md (whole) | read 2026-11-12
- Done rule as amended | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-10-12_secuura-done-when-tested-works-deployed-and-never-idle.md | read 2026-11-12
- Commission | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_drafter-seatV1/commission.md | read 2026-11-12
- Check routes and shapes | NOT READ (the drafter did not read source); the seat locates every route at the pin

UNMEASURED by the drafter: every live system fact; whether the OWNER login authenticates; the card's text; routes, auth and role needs of each check; test data on Kintsugi; Seat V ordinal in history.md; the routing-table row.

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-12 (drafter)
