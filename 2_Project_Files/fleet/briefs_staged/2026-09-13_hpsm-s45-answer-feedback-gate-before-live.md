BLUF. **READY FOR QA received** (13:40:24Z, `qa-s45/feedback-ready/README.md`). **Tuesday is commissioning a tier-1 QA gate on the FEEDBACK delta now**, local only, on `d0466da` (`9b8ea76..d0466da`). Keep going with the pre-check and TK. CR also continues.
- **Why a gate now, not only inside the ONE delta gate.** The feedback batch is a NEW security surface: migration 0016, new routes, uploads with attachments, platform_admin triage and RLS on new tables. It is also headed for Kam's live demo tonight. The 2026-09-05 tier rule puts security surfaces and deploys at full weight BEFORE ship. The ONE delta gate sits after C11, D-M1, D-M2 and the credential round, hours away, so waiting for it would ship the feedback feature untested.
- **The LIVE feedback upgrade now needs all three:**
  - (1) TK's three-branch proof;
  - (2) this gate's verdict: GO, or GO WITH FINDINGS with no Blocker or Major on the feedback surface;
  - (3) Tuesday's ruling on the head mail.
  Send the head mail as soon as TK's proof is in; Tuesday may rule it conditionally on the verdict.
- **The ONE delta tier-1 gate on `09c1591..<fix head>` stays owed** for the rest of the fix round. It re-covers feedback only where later work touches it.

## What the gate needs from you: nothing new, and three things NOT to do
- **Ports 21480-21599 are the GATE's.** Your lanes stay on 20480/20580/20880 (seat), 25380-25399 (CR) and 25480 (TK); never 24080-24780 or 18580.
- **The docker lock** (`lockf -k …/dc13ed6b-f206-4b51-b117-ff3f2723cf9b/scratchpad/docker.lock`): the gate gets FIRST claim, per the 08:07:30Z amendment 2 ("gates get the lock first"). If a chain of yours is mid-step, finish that step, then yield.
- **Never touch the gate's stack, worktree or tenants.** It creates its own compose project and tenants on its own stack. It reads the repo and your README; it writes nothing into the repo.
- **If the gate mails an INTERIM Blocker on feedback, Tuesday relays it to you as a fix-round item.** Do not wait on the gate for anything else.

## Unchanged
- Pre-check PC_BASE_SHA 9b8ea76 → target d0466da; the TK proof (branches i, ii, ii-b, iii); R2 is Kam's word only.
- Head mail: the pre-check STOP lines, the pin answer, the three transcripts, lane-a first, the live feedback row count (expected none), and "the rollback target is now the new head".
- No push. C11 STOPs for Kam. Mail `tuesday-agent@` only.
