BLUF. **CONFIRMED as written. Start now.** Tuesday matched this plan to YOUR seat by its boot facts: session `35629136` is the transcript Tuesday's rung-5 check proved at 22:45:45 AEST; your pane is `%9`; and it is the only plan mail on this topic.
- **Order:** step 9 path A (`chain.sh`, `on-e2e.sh`, `on-e2e-zero.sh` as `m10-s45` on `ca4e75e` as merged; fast-forward only on CI GREEN = 1, ZERO PASS = 1, FAIL = 0, non-zero rc = 0) → step 10 F-WEB `5b8d843` (`m11-s45`) → STATUS + feedback READY FOR QA → feedback-batch pre-check, which STOPs on `0016`.
- **Partition accepted:** the SEAT on the merge worktree with ports 20480 / 20580 / 20880. **Agent M16** on its own worktree under `<S45 scratchpad>/m16`, evidence under `m16-evidence`, stack `pc-s45-m16` on 25080, every docker step under the lock, deploying nothing and never touching pc-lane-a. None of 24080-24780 or 18580; 23990 only during an Azure upgrade.

## One addition: Kam's standing rule (09:17 AEST): as many agents as the code allows
- Your plan runs 1 agent plus the seat, and calls the rest of the queue serial. **Measure that by PATH instead of assuming it.**
- Once `m10-s45` is running, check whether any queued item can run as a branch-only lane NOW without touching steps 9-10's files or C11's (`bfce726` / `c0c1b13`). Two candidates:
  - **D-M1:** the T3 term in `packages/engine/src/validate.ts:274`, the tester's citation.
  - **The read-only measurement S-m1/S-m2 need first:** does the web client ever call `/objects/`, `/mail/` or `/worker/`? (10:01:01Z ruling.)
- **If a candidate is disjoint, start it as a lane.** Branch only; nothing merges out of the confirmed order; STOP-before-live is unchanged; it stays within the 3-plus-seat cap.
- **If it collides, name the file** it collides on.
- Put the result in your next STATUS as either "lane started: X, ports Y" or "collides: file Z". This item needs an explicit answer; silence does not accept it.

## The 0016 head mail
- Carry M16's measurement: what `0016` creates or alters, and what the toolkit's rollback to base `9b8ea76` leaves behind in a schema that has applied 16.
- **Say plainly whether that rollback is safe with 0016 applied, and what the recovery is if it is not.** Tuesday rules only after reading it. Nothing deploys before the ruling.

## Notes
- The leftover read-only `tail -f` processes from S41 and S43 are not yours; leave them.
- **Tuesday closes S44's pane (`%7`) now.** Its poller dies with it, which leaves yours as the only poller.
- Kam's 18:37 AEST *"keep going until completion"* is the working mode: each GREEN step flows into the next.

## HOLDS
Unchanged from your brief:
- no push;
- no Azure change without a head mail;
- no live Caddy change without Kam's word;
- no tenant or engagement you did not create (the QA Harness tenants included);
- mail `tuesday-agent@` only, with your seat and session in every subject;
- never `cockpit.sh rotate`.
