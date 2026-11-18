---
date: 2026-11-18
type: family
source: synthesised from the member lessons listed at the bottom; the lessons remain the source of truth and hold the cases
status: live
---
# Time-scoped grants

**The one idea.** When Kam gives an instruction or permission with a window in it ("for the week", "until X", "while Y"), the window is part of the instruction. A scoped permission applied without its ending becomes a permanent change nobody decided to make, so the end is written down, checked by something that fires on its own, and never renewed by inference. The dates themselves are measurements and get derived, not guessed.

## The rules

1. **When Kam gives a windowed instruction and I am about to apply it: decide what ends it before the edit lands.** Write the end into the artefact itself in his words, with the derived date stated as my assumption; build a check that warns unprompted the day after, in a place read at every boot (a comment, a diary line or a successor brief expires nothing); exercise both branches before arming, the passing state and the warning state, by moving the clock and not by waiting; keep the revert one line away (the superseded line commented in place plus a dated backup beside the file) and say where it is; tell Kam my date reading in the same breath as the receipt. `2026-09-06_a-scoped-override-carries-its-own-expiry.md`
2. **When writing any weekday beside any date** (an expiry, a due date, a ticket, a mail, a note, a commit message): derive one from the other with `date -j -f "%Y-%m-%d" "<date>" "+%A"`, every time. A phrase holding both looks self-checking and is not. Never infer from a nearby date I handled recently. If they disagree, the weekday is usually what Kam meant, since it is what he said aloud. `2026-09-10_a-weekday-and-a-date-are-two-claims.md`
3. **When an expiry turns out wrong: check which direction.** An error that extends a signature-class permission (deploy, production, money, external communication) is corrected immediately and reported; a restrictive error can wait for Kam. A wrong fact in a headline is already in every digest: fix the source file, regenerate both digests, and grep every artefact for the old value, reading the hits (the correction note will still match). `2026-09-10_a-weekday-and-a-date-are-two-claims.md`
4. **When a grant's end is an event and not a date: name the event, and re-ask when it arrives.** A grant that says "until the board is clear", "while he has accounts to rotate" or "until the project starts" ends on that event or on Kam's word, with an outer date stated where one was read; it is not renewed by inference. A grant with no stated expiry is recorded as "none stated, stands until he changes it", said out loud and not assumed. `2026-11-06_clear-the-secuura-board-over-one-to-two-weeks.md`, `2026-10-20_tuesday-no-90pct-line-two-accounts.md`, `2026-08-12_hpsm-continuous-readiness-grant.md`
5. **Permission is not a quota.** A grant to run around the clock still carries the duty to say honestly at each wrap whether self-closable work remains, and to stop and say so when the queue runs dry instead of manufacturing work. `2026-08-12_hpsm-continuous-readiness-grant.md`

## What a tool already enforces

No member's index row names an enforcing tool. The first lesson describes its own check living in `2_Project_Files/doctor.sh` for the case it was written about, and a register of open grants at `0_Brain/tasks/EXPIRING-GRANTS.md`; neither is recorded as enforcing these rules in general, so each new windowed instruction still needs its own check built.

## Grants and their limits

All of these leave production, money (unless named below), external communication to humans, irreversible actions and the QA gate before every merge with Kam or unchanged.

- **Readiness sessions for the not-yet-started project (Tuesday seat). ENDED.** The project agent could run session after session, day and night, on understanding and readiness only: study, registers, drafts for discussion; no build, no cloud resources, no billing, nothing facing the client's vendor. It ran "until the project starts or Kam lifts it"; the project's architecture round began on 2026-09-10, so the stated end has passed. Do not act on it. `2026-08-12_hpsm-continuous-readiness-grant.md`
- **Cloud resources for the security-manager proof of concept (Friday seat, Datasec).** Friday may create what the install needs in the one named research subscription, install the product, then study integration and contents, reporting every resource and its monthly cost as it is created. The access route for colleagues is Friday's choice against stated criteria (named identities, no admin port open to the whole internet, cheapest browser route). Not covered: any ask or message to the vendor or any human (Kam relays and sends invitations), anonymous internet access to the console, other subscriptions or tenants, production, restricted vendor documents, licence terms. The inbound credentials stay in the credentials folder only. No expiry stated: it is tied to this setup; re-read if scope moves past that product. `2026-10-03_hp-security-manager-azure-deploy-grant.md`
- **No usage line for Datasec launches (Tuesday seat).** With the weekly gauge at or over 90%, launch with `WED_USAGE_STOP=100`, naming the grant. It lifts the spend line only; the machine-load wave rule (launch when the one-minute load is under 7), CodeQL and the routing table still apply. Ends on an event: it stands while Kam has accounts to rotate to; if the gauge nears 99% with no switch, say so on the board. `2026-10-20_tuesday-no-90pct-line-two-accounts.md`
- **Clear the Secuura board (Wednesday seat).** Until the board is clear, with an outer date of Friday 2026-11-20, then re-ask: work In Review and In Progress first, then Todo and Backlog easy to hard; every morning card carries the count by state against the baseline, from a paginated read. A ticket leaves by being completed, merged and archived, or sorted with evidence (duplicate, already done, stale, or carded to Kam); "clear" never means closing tickets to reach zero. Classify at source, archive leaves before parents. Demo stays frozen until Kam says otherwise; tickets on the client's own people stay theirs. The lesson's line "a ticket with no live check possible stays open" is older than the amended Done rule in the autonomy family (close with a "no live check possible" comment once unit tests pass and the fix is in the running dev-box build): the amended rule is the later one. The lesson's "the Spark is on" line is dead; the machine was returned on 2026-11-15. `2026-11-06_clear-the-secuura-board-over-one-to-two-weeks.md`

## The mistakes this family keeps catching

- A temporary pin or override that outlives its reason because nothing was built to end it.
- A weekday and a date written together, one of them wrong, and the wrong one in the headline.
- A grant quietly extended a day, or renewed, by my own reading.
- Treating "none stated" as "forever" without saying so, or an event-ended grant as still running after its event.
- Reading permission to run continuously as an obligation to produce.

## Members

2026-08-12_hpsm-continuous-readiness-grant.md — ENDED grant: the HPSM agent ran 24h readiness sessions until the project started (study, drafts only; no build, no Azure, nothing HP-facing). The project's architecture round began 2026-09-10, so the stated end has passed.
2026-09-06_a-scoped-override-carries-its-own-expiry.md — When Kam gives a windowed instruction (for the week, until X): put his words and the assumed end date in the artefact, build a check that warns after it, exercise both branches with the clock moved, keep the revert one line away, state the date reading to him.
2026-09-10_a-weekday-and-a-date-are-two-claims.md — When writing any weekday beside a date (expiry, due date, ticket, mail): derive one from the other with date -j -f %Y-%m-%d <date> +%A. Never infer from a nearby date. A wrong date in a headline is in every digest: fix and regenerate both.
2026-10-03_hp-security-manager-azure-deploy-grant.md — HPSM-POC: Friday may create Azure resources in the kamil@datasec-rd.com subscription for HP Security Manager 3.16, install it, then study integration, reporting each resource and cost. Not covered: asks to HP, anonymous console access, other tenants.
2026-10-20_tuesday-no-90pct-line-two-accounts.md — When launching a Datasec seat with the weekly gauge at or over 90%: launch with WED_USAGE_STOP=100 naming this grant; say on the board if the gauge nears 99% with no account switch. Production, money, comms, QA gate, CodeQL, load1<7 wave rule unchanged.
2026-11-06_clear-the-secuura-board-over-one-to-two-weeks.md — Until the Secuura board is clear (outer date Fri 2026-11-20, then re-ask): work In Review, In Progress, then Todo/Backlog; count by state on the morning card. Tickets leave by completed-merged-archived or sorted; done still means tested, working, deployed.
