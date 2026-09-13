BLUF. **RULED: option (a).** Your STATUS + QUESTION 14:32:21Z is received and read whole. **This SUPERSEDES the target of Tuesday's 14:13:38Z CONDITIONAL GO:** the live target is no longer `d0466da`, and **Tuesday will send NO GO mail for `d0466da`.** If one ever appears, hold it, exactly as you said you would.
- **Sequence:**
  1. G45 finishes its attachment file-name probes (all 11 shapes, RED first if any is stored).
  2. Merge `s45/cred-shapes-guard` onto main in the merge worktree.
  3. Chain `m12-s45` (chain, switch-ON e2e ZERO, clean-clone CI), and fast-forward main only on GREEN.
  4. Re-run both pre-checks on the new head.
  5. Mail Tuesday a short HEAD delta **and** a READY FOR QA delta for `d0466da..<new head>`.
- **The live GO now needs three things:**
  - (1) the current feedback gate's verdict on `d0466da`, with no Blocker or Major on feedback other than this finding;
  - (2) a **delta tier-1 gate on `d0466da..<new head>`**, with no Blocker or Major;
  - (3) Tuesday's GO mail naming the new head by full SHA and citing this ANSWER.

## Why (a), and what Tuesday is and is not ratifying
- **(b) is refused.** It knowingly puts credential storage onto Kam's live demo. Ruling (a) says credential-shaped free text fails closed with 422, and nothing in Kam's "upgrade as soon as it's ready" makes a known Major ready.
- **The PRODUCT CHANGE flag is accepted as a SHAPE:** scan the decoded path as `page_url` as well as the stored one, and leave the stored value unchanged. It is two source files, which is exactly the flag the brief asked for before merge.
- **Whether `decodedPagePath()` catches every encoded form, on every feedback field and every path (JSON, multipart, file name), is the delta gate's question, not Tuesday's.** Tuesday has not read the diff. The counts, mutants and controls are your measurements, relayed.
- **Credit where it is earned:** the guard gap the READY FOR QA declared (BACKLOG:45) is what found this. Declaring the gap and then closing it is the right order.

## Conditions carried
- **The 14:13:38Z conditions 1-8 all stand for the new head.** Lane-a first; exit semantics; the smoke writes nothing; Caddy `61f519cd` before and after with TUNNELLED labels; the untouched tenants; the Azure write path accepted as unexercised; DM2 and G45 pause at GO; the REPORT with rollback target = the new head.
- **`PC_ALLOW_MIGRATIONS=0016_feedback.sql` still applies,** because the base is still `9b8ea76` live.
- **Your pin answer is to be re-stated from the re-run pre-checks,** not carried forward.
- **The delta gate is Tuesday's to commission.** Ports 21480-21599 after the current gate closes. The docker lock gives the gate first claim, as before.
- **Do not contact the running feedback gate about this finding.** Its independent result is part of how it is scored.

## Unchanged
- No push. C11 STOPs for Kam. D-M1 and D-M2 STOP before live, and DM2's 7 spec questions are for Kam's Monday review. CR (`da64f28`) and DM2 (`22e4d61`) keep their merge slots after C11. The ONE delta tier-1 gate for the rest of the fix round stays owed.
