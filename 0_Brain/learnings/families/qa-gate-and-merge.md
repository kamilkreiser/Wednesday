---
date: 2026-11-18
type: family
source: synthesised from the member lessons listed at the bottom; the lessons remain the source of truth and hold the cases
status: live
---
# The QA gate and the merge: who proves what before work is scored, merged or shipped

**The one idea.** Three different questions need three different instruments: the builder proves it built the thing, an independent testing agent proves it works for a user, and the coordinator proves it is what was asked for. A wrap mail, a green local run or well-argued reasoning answers none of the last two. The gate is weighted by what the change touches, capped so it cannot loop for ever, batched so it is not paid for twice, and once it has passed at the current head, only a current, specific reason keeps work from merging.

## The rules

1. **When a builder's wrap or READY mail lands:** it triggers QA, not a score and not a deploy. The order is: builder hands over (branch and commit, the set of surfaces changed, how it authenticates, what it did NOT do); I brief the testing agent; the testing agent checks every change visually AND through code, in a real browser for anything rendered, findings only, never fixing; then I do my completion check; then score; then any deploy GO. Briefs say so ("this round ends at READY FOR QA"; "no deploy until the QA pass and the coordinator's GO"). If the real surface cannot be driven, test the same commit locally and say exactly that; never claim the target was tested when localhost was. `2026-09-01_qa-gate-before-my-verification.md`

2. **When I do my completion check:** it is delivered against commissioned, item by item against the brief and against Kam's own asks in the agent's pane (his turns are part of the spec), plus the source facts only I hold (the ruling, the ticket, the remote head, the deploy target). It is not a re-run of the tester's tests, but it includes at least one independent probe of the headline claim. Where delivered differs from commissioned, I commission the refine round myself; Kam hears the delta and the fix, not a request to adjudicate. Escalation stays for his signature classes. `2026-08-10_own-the-spec-not-just-the-escalation.md`, `2026-09-01_qa-gate-before-my-verification.md`

3. **When I am about to write "ratified" on a builder's mail:** ask whether the sentence describes the PROOF or the CODE. A proof's design, a disclosure, a stated limit, an admission of what was not measured are in the mail and may be ratified. Whether the fix is correct, and any model of how the product behaves, however well argued, is the gate's question: the accurate reply is "received, and it goes to the gate". Excellent evidence and persuasive reasoning raise the risk. Name inline what the ratification does not cover. When the gate falsifies something I endorsed, that goes at the head of the findings mail, and the retraction calls itself premature. Deductions go to the session whose work it was, not the successor fixing it. `2026-09-01_qa-gate-before-my-verification.md`

4. **When I commission a QA pass:** name the tier and its reason in the brief header.
   - **Full gate** (through code, plus a real browser for any rendered surface), mandatory: security surfaces (authentication, tokens, sessions, key revocation), data destruction or erasure, anything deploying to a dev or demo environment, anything handed to a human as a test block.
   - **Through code only:** tests-only changes, docs, config and CI, follow-ups whose mechanism a prior gate already measured, style changes.
   - **No gate** (the builder's own proof stands): backlog and citation fixes, ticket hygiene, comment corrections, record-only changes.
   Unchanged by tiering: my completion check on every round, the signature classes, and that a deploy needs Kam's word. `2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md`

5. **When a class of change has had two NO GO rounds:** stop. Ship the closed instances as the tier allows, ticket the residue with the tester's cases attached, and reopen the class later as its own commission. A third round needs Kam's word on a card. Every fix-round mail states the round count. The known price: late rounds do sometimes find real defects; Kam took that trade. Track first-time pass rate per project weekly. `2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md`

6. **When I schedule gates:** batch by default. One session covers changes of the same tier that share no file (normalise path prefixes before checking for collisions); colliding changes are gated in sequence order. Read the base and head commits again in the same action as the launch, never after a refusal. Never re-gate an unchanged diff: if head and base are unmoved the earlier verdict stands, so record it. A harness fault resumes the same round and is logged; it does not spend a new one. Tier honestly. A second round after a real finding is the gate working and is not cut. Never cut the gate on anything in a signature class: a gate that misses things is worse than none, because it comes with a receipt. `2026-09-18_minimise-gate-duplication-batch-them.md`

7. **Before I accept a green local run:** ask what the local environment fakes on purpose (mocked services, seeded data, stub credentials, a different mode) and whether the change depends on data only the real one produces. Prefer fixtures captured from the real system; a hand-built fixture tests the design, not the data. Require the verification matrix on the target AFTER deploying. Reward the honest receipt ("unit-proven; this path cannot be exercised locally") over a green tick. `2026-08-06_local-proof-is-not-target-evidence.md`

8. **When a change adds an early return, a guard, or switches a call site to a function with an extra gate, inside shared code:** the population to check is the callers of the changed function, not the files in the diff. For each existing test on those paths that asserts a NEGATIVE (refused, ignored, absent, returns nothing), confirm it still reaches the check it is named for; a positive assertion fails loudly on its own. Prove a suspected disarmament with a paired mutation: remove the later check and expect the suspect test green and a known-good test red. Repair the fixture, not the guard. Report both halves: the product may be right while the guard is now unexercised. Exclusions must be sound by construction (no pre-existing callers; newly added routes). A sweep carries a self-test (positive control, negative control, non-empty population) that aborts instead of emitting an empty list. The same applies to a new cache, flag, fail-fast validation or earlier middleware. `2026-09-20_an-early-return-disarms-tests-outside-the-diff.md`

9. **When I or a seat is about to post a correction on a ticket a client reads:** it is a new set of claims, not a retraction. Draft it, hold it, and post it only after the gate covering its change has read it. Every sentence carries its instrument or the word "unmeasured", above all the reassuring ones ("unchanged", "only local"). Say less: what was wrong, what the change does, what is not known. Where the platform allows, edit the wrong comment and say it was edited; do not stack corrections. `2026-09-29_a-correction-to-a-client-is-a-new-claim-gate-it-like-code.md`

10. **Datasec GitHub organisation only (Tuesday and Friday seats):** a commit reaches `main` of any repository there, code or records or docs, only if CodeQL scanned THAT commit on a pull request: either a head-pinned squash merge, or a fast-forward of the same scanned commit. Seats push branches only; the coordinator opens the pull request and lands it once CodeQL and the checks are green, then compares the merged tree with the head. Every brief carries that standing line. An alert is fixed in code, even in a test file. Do not extend this to other clients' repositories without Kam's word. (The first headline, "never a direct push", was narrowed the same hour: the forbidden thing is an unscanned commit on main, not the push verb.) `2026-09-29_datasec-github-commits-go-through-codeql.md`

11. **Secuura only (Wednesday seat): when a gated pull request is held by an old hold carried from brief to brief** (a "not in queue" list, a "do not merge" sentence, a hold with no recorded reason): lift it and merge; do not keep it "to be safe". Only a CURRENT, specific reason holds it: the gate's verdict at this head says it must not merge as written; a card Kam ruled after the newer merge rules that names it; or a signature-class step (the merge stays allowed, the deploy waits). Say in the GO which hold was lifted, or name the current reason in one line for one kept. `2026-11-15_recent-merge-rules-override-historic-holds.md`

12. **Secuura only (Wednesday seat): pull request text carries no "do not merge until the pre-merge tests run" sentence,** and requests held for that sentence merge like the rest on their own gate verdict at their current head and a head-pinned GO. The Test Evidence block still names what was NOT run, and the GO says once that those suites were not run. Existing bodies are not edited. The standing line lives in `2_Project_Files/fleet/STANDING_LINES.md`. `2026-11-13_premerge-do-not-merge-sentence-dropped-nine-released.md`

13. **Secuura only (Wednesday seat): when a pull request is called "tested":** that means tested the way the client reviewer's own process tests it: all 16 pre-push preflight legs plus the Schemathesis pre-merge, Akto, Playwright and k6 suites, on a local stack slot of the request's tree, with a baseline run on the development branch so a red is attributable, and the suites' own pass lines quoted. Bring the slot up only when the machine has room (load and memory checked), never on shared hosts. Skipped legs are reported as skipped. Until a slot is live, merging continues on gate verdicts and says the suites were not run. This changes what is run, not what is written (rule 12), and the reviewer remains reviewer of his own process. `2026-11-15_mirror-peters-tests-so-we-catch-everything.md`

## What a tool already enforces

No member's index row names an enforcing tool. The Datasec ruleset itself refuses an unscanned commit on main; that is the client's enforcement, to be worked with and never around. The lessons record that "no score without a QA report" was still run by hand when written.

## Grants and their limits

- **Tiered gate and two-round cap** (Kam, 2026-09-05): standing. A third round on a class, and any deploy, stay Kam's.
- **Batch gates, do not repeat them** (Kam, 2026-09-18): standing rule, no expiry. Does not permit dropping a gate on a signature class.
- **Secuura: no self-hold sentence; held requests released** (Kam, 2026-11-13) and **recent merge rules override historic holds** (Kam, 2026-11-15): standing. The gate before every merge, the signature classes and the frozen demo are unchanged.
- **Datasec:** dismissing a code-scanning alert, any ruleset bypass and any change to the organisation's policy are Kam's (and the client's IT), never a seat's.

## The mistakes this family keeps catching

- A score or a "ratified" issued on the builder's own account of its work.
- Tests that pass honestly against a shape the author invented, not one the real system produces.
- A green suite in which a test still carries its name but no longer reaches its check.
- The same unchanged diff, or a stale pin, paid for with a second gate session.
- A hurried correction to a client that is wrong in a new way.
- A hold kept alive because nobody remembers why it was placed.

## Members

- `2026-08-06_local-proof-is-not-target-evidence.md` — Before accepting a green local run: ask what this environment fakes on purpose and whether the change needs data only the real one produces. Prefer fixtures captured from the real system; require the verify matrix on the target after deploy.
- `2026-08-10_own-the-spec-not-just-the-escalation.md` — When I accept delegated work: diff what was delivered against the brief and Kam's in-pane asks item by item, run at least one independent probe of the headline claim myself, and commission the refine round rather than asking Kam to adjudicate the gap.
- `2026-09-01_qa-gate-before-my-verification.md` — Every change goes agent wrap, testing agent (visual and code; real browser if browser-facing), my completion check against the brief, then score or deploy. A wrap triggers QA, not a score. Gate weight is tiered. I ratify proof shape, never code correctness.
- `2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md` — When a builder's READY lands: name the QA tier in the brief (full: security, data destruction, deploys, human handovers; through-code: tests, docs, config, gated follow-ups; none: hygiene). Two NO GO rounds on a class: ship closed items, ticket the rest.
- `2026-09-18_minimise-gate-duplication-batch-them.md` — Batch QA gates: one session covers file-disjoint changes of the same tier; re-pin just before launch; never re-gate an unchanged diff; resume after harness fault; tier honestly. A round 2 after a real finding is fine; never cut gates on signature classes.
- `2026-09-20_an-early-return-disarms-tests-outside-the-diff.md` — When a change adds an early return, gate or switched call site in a shared function: enumerate its callers' negative-asserting cells (not just the diff) and confirm each still reaches the check it is named for; prove with a paired mutation.
- `2026-09-29_a-correction-to-a-client-is-a-new-claim-gate-it-like-code.md` — When posting a correction on a ticket a client reads: it is a new claim set. Hold it until the PR's gate has read it, give every sentence its instrument or 'unmeasured', say less, and edit the wrong comment rather than stacking.
- `2026-09-29_datasec-github-commits-go-through-codeql.md` — Datasec GitHub repos: only a commit CodeQL scanned on a PR lands on main (head-pinned squash merge or fast-forward of that commit). Seats push branches only. Fix alerts in code, never dismiss; never seek a ruleset bypass.
- `2026-11-13_premerge-do-not-merge-sentence-dropped-nine-released.md` — Secuura PR bodies carry no "do not merge until pre-merge tests run" sentence, and PRs held for it merge like the rest on their gate verdict. The Test Evidence block still names what was NOT run; the standing line is in fleet/STANDING_LINES.md.
- `2026-11-15_mirror-peters-tests-so-we-catch-everything.md` — When a Secuura PR is called tested: run Peter's suites (16 preflight legs, Schemathesis, Akto, Playwright, k6) on a local slot when the floor has room, with a develop baseline. Until a slot is live, merge on gate verdicts and say they were not run.
- `2026-11-15_recent-merge-rules-override-historic-holds.md` — When a gated PR is held by an old carried-forward hold with no current readable reason: lift it and merge. Only a current specific reason holds it (NO GO at this head, a later Kam card naming it, a signature-class step); say which in the GO.
