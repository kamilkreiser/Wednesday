---
date: 2026-08-07
type: principle
source: "Formulated by the Datasec/Vision_Sales_Portal agent — 'A check that cannot fail is not a check' — after catching two of its own. Four independent occurrences across three agents and me in a single day."
status: live
supersedes: ""
---

# A check that cannot fail is not a check

**The shape.** A verification runs, reports success, and could never have
reported anything else — because it measured the wrong thing, errored and
swallowed it, or asked a question whose answer was fixed in advance. It is worse
than no check, because it converts an open question into a settled one.

**Four occurrences on 2026-08-07 alone, across three agents and me:**

1. **Mine — the close-bell 403.** I verified the API key's value, length and
   byte-equality with a working one, and concluded it was valid. It was. The key
   was never reaching the process that used it (`source` without `set -a`).
   **Every check I ran was on the key at rest, and non-delivery is invisible to
   all of them.** Two nights of failure, and a wrong root cause reported to Kam.
2. **Vision — a private-key scan that errored and still printed "clean".** The
   shell scan of a mail for key material hit the `-----BEGIN` lines, read the
   leading dash as a flag, errored on exactly the two lines that mattered, and
   reported clean anyway.
3. **Vision — a print-layout check measuring a hidden element.** It measured
   `#quoteDoc` heights and got `0`, because the element is `display:none` on
   screen. Zero looked like a pass. Replaced with a real PDF render — which then
   found a customer-facing defect on page 2 that reading the source had missed.
4. **NexusAI — a `find` that timed out and read as a negative result.** A search
   for `pane_prompt_check.sh` silently timed out traversing an external drive and
   returned nothing; the agent came one step from reporting my evidence as
   fabricated on the strength of it. Their phrase: *"checking a premise badly is
   not checking it, and it fails in the direction that feels like diligence."*

**Why this is a distinct lesson and not just "verify properly".** All four
verifications were *performed*. The people running them were being careful —
that is the trap. `always-verify-and-check` fires on "did I check?", and every
one of these answers yes. The question it does not ask is **"could this check
have come out differently?"**

**How to apply — one question, asked of the check rather than the result:**

1. **"What would make this check fail?"** If there is no concrete answer, the
   check is decorative. For a credential: *what would show a valid key that
   never arrived?* — printing `len(key)` inside the failing process. For a
   layout: *what would show a broken page?* — the rendered artefact, not a
   hidden element's geometry.
2. **A zero, an empty result and a silent success are suspects, not evidence.**
   Zero rows, zero height, no matches, "clean" — each is equally consistent with
   "nothing is wrong" and "the check never ran". Distinguish them before
   reporting.
3. **Never let a non-zero exit be swallowed.** Occurrence 2 is
   [[2026-08-06_never-discard-stderr]] wearing a different hat: the error was
   printed *and ignored*, which is the same as discarding it.
4. **Prefer checking the artefact over checking the intent** — the rendered PDF,
   the served page, the value inside the failing process. Generating the real
   output beat reading the source twice in one day on the same project.
5. **When a check surprises you by passing, be as suspicious as when it fails.**
   Three of these four looked like good news.

**Meta-note:** the formulation is the Vision agent's, arrived at independently
while I was diagnosing my own instance of it. That is the second protocol
improvement the fleet handed me today. My job is to notice and propagate them.

## The concrete remedy, added 2026-08-13 (Secuura/Blockchain s28)

The rule above asks *"what would make this check fail?"* — good, but it is a
question you have to remember to ask. The Secuura agent found the **structural**
version, and it is cheap enough to be non-negotiable:

> **A negative-only test suite cannot distinguish "correctly rejecting" from
> "refusing everything". Every rejection suite needs a case that MUST succeed.**

**The case that taught it.** Its first HTTP matrix for the KYC callback guard
returned **401 for every probe — including the positive control.** Six rejections,
all "correct". Without the must-succeed case that reads as *"every rejection works,
confirmed"*, and it would have been reported that way. The logs showed why: the
route is JWT-gated, so **none of the six probes ever reached the guard being
tested.** Two real defects fell out of asking why the positive control failed
(the route Microsoft is told to call does not exist — registered URL 404, real
route 200; and the provider authenticates with an api-key and cannot hold a
Secuura JWT).

**Why this generalises past HTTP:** a blanket refusal, an empty result set, a
universally-failing parse and a permanently-down dependency all *look identical*
to a working negative test. The positive control is the only thing that
distinguishes "the guard is discriminating" from "nothing is getting through".

**How to apply:**
- Any suite that asserts things are rejected/blocked/filtered/denied carries at
  least one case that must be **accepted**, and it is a failure of the suite if
  that case does not pass.
- Same for absence checks: prove the search *can* find something before reporting
  that it found nothing. (My own `cycle` subcommand shipped its first draft with
  an unbound variable, so it searched for nothing and reported "no child" — the
  same defect, in the code written to fix a repeated failure.)
- A check that cannot fail and **a check that cannot see** are the same defect —
  their phrase, after a CI poll ran blind for ten minutes because a control
  character broke a strict JSON parse, and a status query used a short SHA and
  returned "0 runs, 0 failures".

### A failure-only log going quiet is not recovery (2026-08-22, Secuura s61)

**The case.** Demo's Blockfrost quota errors ran 450–460/hr for days, stopped
dead at 12:15:54Z, and stayed at zero for eight hours — a textbook recovery
curve. The key still 402'd at that moment (403 wrong-key control
discriminating). **A successful verify-by-hash logs nothing** (verified in the
shipped image: only failure-side messages exist), so *"no errors"* and *"no
calls at all"* are the same picture in that log — and the second is what
happened: the CALLER had stopped, not the error.

**The rule, the agent's formulation adopted verbatim:** an error counter
falling to zero means the error stopped **or** the thing that could produce it
stopped. **Wherever only failures are logged, those two are indistinguishable
— and the cheap discriminator is a direct probe, not more log-reading.** One
request settled what eight hours of clean logs could not.

**The sibling caught in the same hour:** the traffic collapse timestamped at
minute resolution (12:17Z) PRECEDED the deploy credited with it (12:51Z) by
34 minutes — so the silence proved nothing about the fix; the fix's real
signature was elsewhere (71 anchors × exactly 1 poll at the 6-hour revisit
mark, against a proven-zero gap). **Attribute an effect to a cause only when
the evidence carries the cause's own fingerprint, not merely its timing.**

### The third member: a check that MISREPORTS what it saw (2026-08-14, same agent)

One GitHub secondary rate limit on a GHCR pull, wearing three disguises at once:
1. **Docker renders a 403 rate limit as** *"repository does not exist or may
   require 'docker login'"* — printed after `Login Succeeded!`, with a correct tag.
2. **The enforce step renders a SKIPPED suite as** *"k6 smoke failed"*.
3. **Re-running relocates the failure to a different suite**, so the second red
   reads as a different problem.

An operator reading only the top line audits PAT scopes and package visibility and
finds nothing. That is not hypothetical: it happened on **2026-08-05** with PR
#646, and I mis-attributed those reds to real Schemathesis/Akto findings when no
test had run — a Secuura session caught it. **Same mechanism, eight days apart.**

**And the nastiest variant, worth its own name: a remedy that hides its own
ineffectiveness by MOVING the symptom.** Re-running felt like new information and
was the same information; only comparing the two runs' *victim suites* showed the
retry had changed nothing. When a fix relocates a failure rather than removing it,
suspect a shared resource, not a flaky test.

**How to apply:** when a failure message names a cause, check that the message
*could* have named a different one. Error strings are written by whoever expected
a different failure than the one you have — a 403 rendered as "does not exist", a
skip rendered as a fail, a rate limit rendered as a permissions problem. **Find
the first failure and read the raw step output, not the summary that interprets
it** (see [[2026-08-06_artifact-presence-is-not-execution]], which this is the
message-layer twin of).


### A test that cannot CLEAN UP starts asserting against live data (2026-08-15, Secuura s35)

**The formulation is the agent's and it is the newest member of the family.** A cleanup
`fs.rmSync(link, { force: true })` **throws `ERR_FS_EISDIR` when the path is a symlink pointing
at a directory** — so a test's tmp-dir teardown silently failed, `ensureRunDir` resolved against
the **real** `output/reports` tree instead, and the assertion diff showed a live repo path where
a `/var/folders/...` path was expected.

**Why it belongs here rather than in a list of bugs:** the test still ran, still asserted, still
reported. It had simply changed *what it was testing* — from a controlled fixture to live data —
**and nothing in its output said so.** That is the family's defining property: the check failed
in a way that looked like the answer.

**The runtime half of the same defect is worse and is the reason to care.** At the two runtime
sites the block sits inside a **bare `catch {}`** documented "best-effort", so the throw is
swallowed and a `latest` symlink keeps pointing at the **first** run. The summary resolver reads
that link first, and its scan fallback only fires for a *different* scenario — so **re-running
the same scenario, the commonest workflow there is, makes a CI gate report on a stale run's
data.** A swallowed exception that changes which data a gate reads is not a convenience; it is a
gate that cannot fail, built out of an error nobody sees.

**How to apply:**
1. **Teardown is part of the check.** A test whose cleanup can fail silently can begin asserting
   against whatever the failed cleanup left behind. Assert that cleanup succeeded, or make it
   incapable of failing quietly.
2. **A bare `catch {}` around cleanup is [[2026-08-06_never-discard-stderr]] in costume** —
   narrow it to the expected conditions and LOG anything else. Deleting the catch is the wrong
   fix: cleanup that legitimately cannot proceed must not break the run.
3. **Verify at the destination:** "`rmSync` no longer throws" is the leg; "after a same-scenario
   re-run the link points at the NEWEST run and the resolver reads it" is the claim.

**And the reproduction trap found alongside it:** `npx vitest run <file>` in those packages, run
without the package's own `vitest.unit.config.ts`, returns `ReferenceError: beforeEach is not
defined` **instead of the real assertion** — the wrong-runner member above, failing in the
direction that looks like a worse bug than you have.


### A positive control proves the suite it RAN IN, and nothing about its neighbour (2026-08-15, Secuura s35)

**The condition that caught this was "run the positive control PER SITE", and I set it without
knowing it would earn its keep this specifically.**

**The case.** One defect, two packages. In the first, restoring the broken call reddened the
suite — a genuine control. In the second, **the suite passed 290/290 with the defect fully
restored.** Its existing test only ever created the pointer from scratch, so it passed whether
or not the removal step worked at all. The failure originally reported there had been **leaked
state from a real output tree, not a test reding on the bug.**

**Consequence had the control been run once instead of per site:** a correct fix ships with
**no evidence for half of it**, under a PR that says "verified" — because the first package's
honest red would have been silently inherited by the second.

**The rule:** a positive control certifies **the suite it ran in**. Two packages, two
codepaths, two environments, two runners → two controls. **"The control passed" is a claim
about a place, and the place is part of the claim.** Same family as
[[2026-08-05_verify-the-chain-not-the-legs]] (a green leg says nothing about the chain) and as
the corollary from 2026-08-14 that **the positive control must run in the SAME PLACE as the
real query** — this is that rule pointed at suites rather than at searches.


### The inverse: a REPRODUCTION that cannot reproduce (2026-08-15, Datasec/NexusAI)

**Every member above is a check that cannot report a failure. This one is a check that cannot
find one — and it fails in the most expensive direction available, because "cannot reproduce"
CLOSES tickets.**

**The case.** Chasing a flaky test, the agent ran the failing test alone — `jest -t '<name>'` —
and got **20 runs, 20 green**. It was about to report that the flake does not reproduce. Then
it ran the full suite before believing its own result: **red the entire time, 1 failed / 162
passed, exactly as the ticket said.**

**Why isolation lied.** Running the test alone left the first call **cold**, and that cold
start supplied the exact millisecond whose absence was the bug. **The isolation did not fail to
find the defect — it removed the defect's PRECONDITION and then reported its absence as
evidence.** The narrowing that makes a test easier to study is the same narrowing that can
delete what you are studying.

**How to apply:**
1. **Before believing "cannot reproduce", ask what the reproduction ENVIRONMENT changed** —
   ordering, warm/cold state, parallelism, fixtures, a shared cache, the clock. A minimal
   repro is a different system, not a smaller one.
2. **Run the failing case in the configuration that FAILS before running it in the one that is
   convenient.** The full suite first, the isolated test second.
3. **"20/20 green" is a zero, and zeros are suspects** — the same rule as everywhere else in
   this file, pointed at a negative result you WANT to be true because it would close the
   ticket.
4. **Same shape as the mirror above** (an absence claim whose search could not have found the
   thing) — here the search is a test run and the scope is the runtime environment.

**And the unifying formulation, from the same agent, which is better than the one I had:**

> *"You accepted a claim because it fitted a pattern; I accepted a measurement because it was
> convenient and came from a method I had not questioned. Both are the same failure — **a
> result that arrives pre-confirmed and never gets asked for evidence.**"*

**Related:** [[2026-08-07_valid-is-not-delivered]] (my instance),
[[2026-08-06_artifact-presence-is-not-execution]],
[[2026-08-06_never-discard-stderr]],
[[2026-08-06_exercise-mechanisms-before-arming]],
[[2026-08-07_enumerate-every-surface-before-done]], [[_ledger]]

### The refinement that makes the positive-control rule actually work (2026-08-16, Secuura s37)

**The rule everywhere above is "pair a zero-result check with a control that must be non-zero."
That rule can fail, and it failed twice in one session — caught both times.**

> **A control only discriminates if it can fail INDEPENDENTLY of the check. When a control
> agrees suspiciously with a null result, suspect the harness rather than the finding.**

**The case, and it is the cleanest possible one.** A role sweep ran `grep --include=*.ts`
**unquoted**, so zsh glob-expanded it and **grep never ran**, returning `0`. The paired positive
control — an occurrence count that must be non-zero — **returned `0` as well**, because it went
through the same broken invocation. Quoted, the real answer is **133**.

**The control did not catch the defect by failing. It caught it by agreeing.** Two independent
questions returning the identical impossible answer is the signal — and it only reads as a
signal if you expect a control to *disagree*. The same agent hit it again the same session on a
published-ports regex and **rewrote the instrument rather than believing its zero.**

**How to apply:**
1. **Run the control through a different path than the check wherever possible** — a different
   command, a different tool, a hardcoded known-present value. A control sharing the check's
   invocation shares its failure modes.
2. **Suspicious agreement is as informative as disagreement.** If check and control both return
   zero, both return empty, or both time out, **the harness is the suspect, not the subject.**
3. **A zero that means "the command could not run" is indistinguishable from a zero that means
   "no such code"** — and quoting/globbing/shell differences are the commonest cause on macOS.

### An indicator that can MISS its own event (2026-08-24, Datasec/NexusAI)

**The case.** Building upload limits, the size cap genuinely cut the stream
at the boundary — the CONTROL worked — but the truncation flag never set,
because the 'limit' listener attached after an `await` and the event fired
into that gap. Result: HTTP 201 and a corrupt 2KB fragment stored as the
user's screenshot. **Worse than accepting whole and worse than refusing: the
user is told it arrived.** Every green signal stayed green; only reading the
stored bytes exposed it.

**The family property, new costume:** not a check that cannot fail — a
check whose SUCCESS INDICATOR depends on catching an asynchronous event, and
the event can be missed while the enforcement still executes. Control firing
and indicator reporting are two separate things wherever an event loop sits
between them.

**The fix shape, adopted as the standard:** the failure was a dependency on
an event firing, so the fix must not depend on an event firing — attach
listeners synchronously AND detect by measured state (size counted vs cap),
plus an exact-boundary regression test. Belt from mechanism, braces from
measurement.

### The control needs its own control (2026-08-23, Datasec/NexusAI)

**The case.** Proving a gitleaks allowlist fix, the agent injected a sabotage
regex to break the config — and the suite still PASSED, because the injected
regex was double-escaped and matched nothing. The "fix works" verdict was
real; the thing it was tested against was not. Caught only because *a control
passing is itself suspicious* (the 08-16 suspicious-agreement rule applied
one level down).

**The rule, its formulation kept:** *"check the sabotage actually sabotages
before believing the verdict it produces."* A positive control that never
fired is indistinguishable from a fix that works — so the sabotage needs its
own proof of effect (see it FAIL before the fix, or see the injected pattern
actually match) before its pass means anything. This is the positive-control
rule made recursive, and one level is enough: the discipline is "prove the
instrument can move" at whichever layer you just added.

**Same session's sibling, kept with it:** content over exit status — three
shell footguns in one day (two pipe-destroyed exit codes; zsh's unquoted
`$VAR` passing one two-word argument) all caught because the TEXT disagreed
with the status line. When output and status disagree, the status is the
suspect.

One agent produced five more members in five sessions. Kept together because the
shared property is what matters: **the check failed in a way that looked like the
answer.** None of them involved the code under test.

- **cannot see** — a status query with a short SHA returned "0 runs, 0 failures".
- **cannot parse** — a strict JSON load died on a control byte and reported zero
  matches; a CI poll ran blind for ten minutes the same way.
- **cannot receive input** — a `docker exec` heredoc with no `-i`, so psql silently
  never ran and the empty result read as clean.
- **runs before its own setup** — a test setting `process.env` after ESM had
  hoisted its imports.
- **run by the WRONG RUNNER** — vitest against a jest suite: "38 files failed, no
  tests", which reads as the code being broken when nothing ran at all.

Their generalisation, adopted verbatim: **a check that cannot parse, cannot receive
input, or runs before its own setup is the same defect as a check that cannot fail.**

**The inverse, done right, belongs here too:** when two auth test files showed red,
the agent stashed its own changes and re-ran clean before attributing them — they
were pre-existing and unrelated. *Blaming your own change for someone else's red is
the same error as missing your own.*

**And the measurement that makes the positive-control rule concrete**, taken three
times on different code: with the guard set to refuse everything, **24 of 35 tests
still passed** (image validation), **9 of 16** (token encryption), **7 of 10**
(billing idempotency). Every survivor was a rejection case. A suite without a
must-succeed case cannot tell you which of those numbers you are looking at.

### The condition we had not stated: on a side-effecting system, the positive control IS an action (2026-08-14, Secuura s34)

The rule above says *always prove the search can find something before trusting that it
found nothing*. Three separate catches today came from it. **Secuura s34 found its limit.**

**The case.** Verifying KS-472's control-byte guard needs both directions. The negative half
— a document title containing U+0000 — returned **400** and created nothing, free of charge.
**The positive half, the identical payload without the NUL, returned 201 and originate
auto-anchored it on the real Cardano preview testnet within seconds** — a permanent
transaction, `simulated=false`.

**And it did NOT clean it up, correctly.** The chain write cannot be un-made and the local
row is the only thing linking it to a document; deleting the row would manufacture **an
on-chain proof with no local record — exactly the KS-587 defect the same deploy was shipping
the fix for.** It relabelled the artefact instead and wrote the behaviour into the runbook.

**The generalisation, now standing:** the negative half of a validation test is usually
free; **the positive half writes.** Before running a positive control, ask what the success
path DOES — a chain write, an email, a webhook, a payment, an audit row, a notification. If
it commits something, either run it where those effects do not land, or run it knowingly and
**label the artefact so the next reader knows it was a probe.**

**Never skip it** — an unproven negative is still worthless, and that is the whole lesson
above. **Just stop treating it as free.**

**And the agent's own note on why this is easy to miss, which is the sharpest part:** *the
asymmetry trains the habit.* **You can run the negative half of a validation test a hundred
times for nothing**, which teaches you that controls are cheap — **and then the one that
costs you is the half you added in order to be rigorous.** The discipline and the trap
arrive together.

### The mirror: an ABSENCE claim needs a positive control too (2026-08-14)

The family above is about checks that cannot report a failure. This is its mirror —
**a search that could not have found the thing, reported as evidence the thing is not
there.**

**The case.** A Secuura session flagged that a claim in its own previous wrap was
false: an entry it said had been written to `BACKLOG.md` was in neither backlog file
nor Linear. It had grepped, found nothing, and disclosed it. **I amended my scoreboard
on the strength of it.** Then it retracted: the entry existed all along, committed on
an unmerged branch, and its grep had run from a tree that forked before that commit.
Its own formulation:

> an artefact-claim needs the same check as any other, and that includes the claim
> that an artefact is **missing** — before reporting "nothing matches", prove the
> search can find something

**Why this is harder than the errors above, and worth its own entry:** diligence was
performed. The agent did search, the search ran cleanly, and the negative was real
*for the tree it ran in*. Nothing errored, nothing was swallowed. The defect was
entirely in the **scope** of the search, which is invisible from inside its result.

**This is the same class as my own w=4 slip the night before**, mirrored: I claimed
something was "absent from every document" without opening the one document that
disproved it. Mine was an absence asserted without looking; theirs was an absence
asserted after looking somewhere that could not have contained it.

**How to apply:**
1. **Every "X does not exist" carries the corpus it was measured against** — the file
   set, the command, the count, and for a repository, **which ref**. `git log --all
   -S` would have settled this in one command; a working-tree grep never could.
2. **Prove the search can find something before trusting that it found nothing** —
   run it against a case you know is present. This is the positive control, applied
   to absence.
3. **Distinguish "I could not find why this still matters" from "here is what
   replaced it."** In a list of closed tickets those look identical and are not the
   same claim.
4. A bulk triage is a pile of negative claims — dozens of "is this still real?"
   judgements, each able to fail exactly this way. That is where this rule earns most.

**The meta-note worth keeping:** the disclosure AND the retraction were both
unprompted, and the churn is left visible in the scoreboard rather than tidied away.
A record that quietly returns to its original wording hides that a correction cycle
happened — and the cycle is the evidence the loop works.

### Three "cannot see" members from one micro-session (2026-08-25, Datasec/NexusAI s5) — and a derivation lesson from its neighbour

1. **A paginator whose unknown parameter is silently ignored.** The AgentMail list API accepts `page_token`; passing `last_key` errors nowhere and re-serves page 1 on every call. The loop reports a plausible scan count (550 "messages"), terminates, and says NOT FOUND with full confidence. Caught only by running three candidate parameter names against each other and noticing two returned byte-identical first pages. **Rule: a "not found" from a paginator nobody has proven can paginate is worth exactly nothing — prove the second page differs from the first before believing the scan.**
2. **A query for a field that lives on a different object.** `az acr manifest show --query digest` returns EMPTY because the manifest CONTENT has no digest field (it lives on `list-metadata`). The blank reads exactly like an absent image. Same shape as the wrong-runner member: the instrument answered a different question than the one asked.
3. **An index that lags the write.** Jira's JQL search index trails transitions by tens of seconds; a `statusCategory != Done` query returned a ticket already displaying Done, and the board count read 59 when the truth was 57. **The issue endpoint is authoritative; a board count taken straight after a transition is a stale rendering** ([[2026-08-14_i-read-representations-they-read-sources]]).

**And from Secuura s65 the same morning, the derivation half:** s64's decision pack reached the RIGHT answer (six operations stay on KS-592) via a list that summed to 11 against a ticket naming ten. *"A correct conclusion is not evidence of a correct derivation"* — and a correct conclusion is precisely what lets a wrong derivation survive review. Re-derive from the source when the record will be cited; a matching bottom line is not a check of the arithmetic above it.


## A test's NAME is not its coverage (2026-09-03, Secuura s119 — the member that let an AUTH BYPASS survive a suite that appears to test it)

**Their formulation, adopted verbatim: *a test's NAME is not its coverage.***

**The case.** KS-737: platform-admin login skipped MFA entirely when `mfaCode` was omitted —
password alone returning a full SYSTEM_ADMIN session. The obvious question is how that survived a
test suite. It survived one that *looks exactly like* the suite that would catch it.
`ks622-mfa-failure-lockout.test.ts` contains a **passing** case named
*"CONTROL — a missing MFA code is MFA_REQUIRED"*. It stubs `getPlatformAdmin` to return **null**,
so every request in that file falls through to the **regular-user** branch. **The control that
reads as covering the platform-admin branch never enters it.** It passed, it was named as a
control, and it measured the wrong code path for its entire life.

**Why this is a distinct member rather than another instance.** Every earlier member of this file
is a check whose *instrument* was broken — it could not parse, could not see, could not receive
input, ran before its setup, ran under the wrong runner. **This one's instrument works perfectly.
What is wrong is the SUBJECT: the fixture routes the test away from the branch its name claims.**
And the name is what everyone reads. A grep for "is this covered?" returns this file and stops,
which is exactly how a bypass lives for months inside a green suite.

**The structural half, which generalises further than the test.** The platform-admin branch exists
because platform admins are not in `users`. **The MORE privileged path was the laxer one**, because
it drifted from its sibling **with nothing comparing them**. Two code paths that must agree, and no
assertion assigned to the agreement — the same shape as
[[2026-08-13_establish-authority-before-reconciling]] rule 5 (nobody is assigned to read the pair,
so nobody does), here with a security consequence.

**How to apply:**
1. **Never accept a test NAME as evidence of coverage — read what its fixture makes reachable.**
   The question is not "is there a test for X?" but "does this test's setup enter X's branch?"
   A stub that returns `null` for the discriminator routes every case in the file elsewhere.
2. **A case named CONTROL earns the most suspicion, not the least.** It is the one nobody re-reads,
   because its name asserts the property the reader came to check.
3. **Where two branches must stay in agreement (privileged vs ordinary, admin vs user, service vs
   shared), assert the AGREEMENT itself**, not each branch separately. A divergence no test is
   assigned to notice is a defect with a countdown on it.
4. **Corollary from the same session, on the proof rather than the subject:** s119's own red-proof
   harness **failed both POSITIVE controls with 401 on its first run** — it had mocked
   `../utils/password` when the module is `../services/password`, so the harness refused
   everything. **Without those controls, "leg 1 returns non-200" would have reported a bypass that
   was never demonstrated.** A security claim proved by a negative-only harness is the
   negative-only suite rule pointed at the most expensive possible subject.


## A census, a writer and a verifier that descend from ONE parse are one view rendered three times (2026-09-04, Datasec/NexusAI S29 — its own diagnosis, then its own correction to that diagnosis)

**Their formulation, adopted verbatim and better than the rule it sharpens:**

> *"The script that added the grounds took each selector as `sel.split('\n')[-1]` — the LAST line
> only — so a grouped selector was silently truncated to its final member. I then 'verified' with
> `sed -n '/^\.nx-sus-rank th:last-child/,+7p'`, which starts AT that line and hides the
> `td:last-child,` above it. **Two views of the file, truncated the same way, and I never read the
> raw rule. I built the instrument that hid it and then trusted it.**"*

**The case.** A CSS ground was written onto the *combined* selector
`.nx-sus-rank td:last-child, .nx-sus-rank th:last-child`. The `td` half outranked the rule that gave
it its real ground, so six table cells silently changed from `#ffffff` to `#f8f9fa` — a visible
regression on a page the principal had ratified by eye. **Contrast never moved, so no contrast
assertion could catch it.** The writer's script and the writer's verification both saw only the last
line of the selector, so both agreed, and the agreement was worth nothing.

**Why this is a distinct member.** The existing rule in this file says *suspicious agreement is as
informative as disagreement — if a check and its control both return zero, the harness is the
suspect, not the subject.* That is stated for a check and a control. **This is stronger and less
obvious: a WRITER and a VERIFIER, built by the same person from the same assumption, are not two
observations.** They feel independent because they are different tools run at different times, and
they are not. Nothing in the second view could ever contradict the first, because the flaw is
upstream of both.

**How to apply:**
1. **When a verification confirms a change you just made, ask what the verification and the change
   SHARE** — a parser, a regex, a selector-splitting helper, an assumption about the input's shape.
   Shared upstream = one observation reported twice.
2. **Read the raw artefact at least once, unmediated.** Both views here were greps. Neither was the
   file. **A tool that extracts is a tool that can omit**, and the omission is invisible in its
   output by construction.
3. **Prefer a verifier with a different SHAPE, not just a different invocation** — render vs source,
   a second party, the consumer itself. The strongest check in this whole round was the tester's
   two-surface diff (declared ground now vs painted ground before), because its mechanism shared
   nothing with the writer's.
4. **A clean result from a method you cannot show is falsifiable is not evidence.** The same agent
   noted its other sheet came out 16/16 **by luck of the regex it happened to use there, not by
   judgement** — and said so, rather than banking it as proof of method. That sentence is what made
   the rest of its report believable.
5. **Same family, one level up:** the tester in the same round built an RD-286 probe, got a clean
   green, and then proved its own probe *structurally could not fail* for that set — because the
   ground-walk terminated on the element itself. **It replaced the check rather than reporting the
   green.** A green from an instrument that cannot go red is the thing this file is about, and it is
   worth as much attention when it comes from your own new tool as from someone else's old one.

**Related:** [[2026-08-14_i-read-representations-they-read-sources]] (a grep's output is a
representation of a file) · [[2026-08-06_selector-discipline-in-ui-verification]] (suspect your own
selector first — here the selector was suspect in both tools at once).


### CORRECTED the same session, by the same agent, and the correction is the better lesson

**Wednesday filed the above as "two views sharing a truncation" — the builder chased the lead and
reported that it was THREE, and that the first one is the one that mattered.**

> *"I described two views sharing a truncation. It was three, and the first one is the one that
> mattered: **the original inventory** — the listing that decided *which* rules needed a ground —
> used the same `sel.strip().split('\n')[-1]`. So the blindness was not in the writer and the
> checker; **it was in the census.** The writer then applied grounds to a population that had
> already been mis-described, and the `sed` check confirmed it against the same mis-description."*

**Its formulation, adopted as the headline of this section:**

> **"When a census, a writer and a verifier all descend from one parse, they are not three views —
> they are one view rendered three times. Agreement across them carries no information at all, and
> the failure surfaces as a POPULATION THAT LOOKS COMPLETE because it was counted by the thing that
> was wrong."**

**Why the census is the worst place for this flaw — CORRECTED by the agent, and there are TWO modes
with DIFFERENT countermeasures.** Wednesday first wrote *"a wrong census removes items from
existence… the completeness is an artefact of the defect."* **The agent pushed back, as invited, and
was right: its census dropped nothing.** All 18 items were enumerated; the grouped rule was listed
**under the identity of its last member only** — present, counted, and described as selecting one
thing when it selected two. It verified rather than remembered: a grouped rule whose last member was
missing from the writer's lookup would have been *skipped entirely* and left with no ground, and the
audit found zero such rules. **So the mode was mis-description, not omission.**

| mode | what happens | is the tally wrong? | countermeasure |
|---|---|---|---|
| **Under-counting** | items vanish from the list | **yes, short** | **reconcile the count against an independently built enumeration** — a count check WORKS |
| **Mis-describing** | every item present, under a wrong identity | **NO — the tally is CORRECT** | **compare each entry's EXTENT** — how many things does this entry actually select — **never the total** |

**The agent's strongest form, adopted:**
> **"The census is the worst place for the flaw not because items disappear, but because a
> mis-describing census produces a tally that RECONCILES. Completeness is not an artefact of the
> defect — completeness is genuine, and irrelevant. That is a nastier property than a short count,
> because a short count at least has a tell."**

**Both branches must stay in this lesson, because "reconcile your counts" is the right answer for
the first and a FALSE COMFORT for the second.**

**The self-application that proves it, and the agent found it in its own mail.** It had sent
Wednesday *"corpus reconciles 18 against 18, no omissions in either direction"* as reassurance.
**That is precisely the check that could never have caught the defect.** Its words: *"I offered a
correct number as evidence of correctness in the same mail where I was explaining that a true number
can vouch for nothing."* **A true, reconciling, entirely honest number, offered as evidence, that was
vacuous with respect to the thing it was offered about.**

**The operative question, which replaces "did I verify it?":**
> **"Was this population counted by a reader built INDEPENDENTLY of the one that wrote it?"**

The builder's own answer for its two sheets: for one, yes — **by luck**, a stricter exact-match regex
it happened to use; for the other, **no**, not until after the regression shipped. And the first
independent reader was unremarkable: *"nothing clever about it; it was just the first reader built
independently of the writer."*

**The second near-miss, disclosed in the same mail, and it inverts the first.** One rule was skipped
by the background-detection because it declares `background: transparent` explicitly — and **it was
correct BECAUSE it was skipped**: it is a ghost button, and giving it an opaque ground would have
changed the render, *"the same harm reached from the opposite direction."* Its words: **"my landing
was saved from a second regression by an accident of detection, not by judgement."**

**The consequence for any "state your own ground" style rule, and it generalises past CSS.** The
population has three kinds, not two: (1) **restating something that was already true** — the
assertion applies; (2) **asserting something new on purpose** — false for those by design;
(3) **explicitly declaring that the value is INHERITED and that this is deliberate** — the assertion
is meaningless, and the correct treatment is to leave it alone. **A guard that does not distinguish
(3) from (1) will push the deliberate-inheritance cases into the restatement bucket and produce
exactly the defect it exists to prevent.** Any lint, migration or invariant of the form "every X must
declare its own Y" needs that third category before it ships.
