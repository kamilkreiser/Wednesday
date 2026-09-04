# QA Agent Invocation Brief — Datasec/NexusAI, S31 ITEM 0c RE-GATE @ `aad37da` (the SHELL now prints the ratified format too)

**This is a SHORT re-gate, not a fresh pass.** You already hold this morning's context from the item 0b pass at `e5be9fe`. Do not re-derive what you already proved — re-drive only what changed, plus the regression check named in §5.

## 1. Target — verified by Wednesday at the source in this action

- **GATE THIS SHA: `aad37da`** (`aad37da196ca…`), branch `rd-136-nga-defaults-s12`, **pushed and confirmed head at origin.**
- **`e5be9fe` — the SHA you gated this morning — IS an ancestor.** Two commits sit between:

```
9b226bf   RD-292 F-16: the query-string keep documented AT THE SITE and pinned
aad37da   RD-292 item 0c: the SHELL prints the ratified window format too,
          from ONE shared formatter
```

- **Committed gate expectation at `aad37da`: 1463 tests / 86 suites** (`git show aad37da:scripts/verify-expected-counts.json`, read by Wednesday 2026-09-04 11:15 AEST). The builder claims `PASS 1463/1463 across 86`. **Measure it yourself; a run reporting 1449/85 or 1448/85 at this SHA is a failure of the expectation gate, not a pass.**
- **`static/js/local-date.js` exists at `aad37da`** — confirmed present by Wednesday via `git cat-file -e`. It is new; that is where the shared formatter now lives.

**Why this round happened:** you filed F-14 — the shell's empty-window card printing `Custom Range — 2027-01-01 to 2027-02-01` about 40px above a humanised pill. **Kam ruled `extend-one-deploy` at 10:59:23**: extend the format to the shell, then one deploy. This is that work.

**Stand your own server from your own export at `aad37da`. Your `:3196` is STALE — it serves `e5be9fe` and predates every line of this round.** Leave `:3068 :3072 :3073 :3075 :3076 :3077` and `:47787` alone; `:3077` is still the source of Kam's frames. `:3080` is the builder's and its commit is unmeasured.

## 2. 🔴 THE LOAD-BEARING CLAIM — the builder found one of its OWN guards was decoration, and the rewrite is what you are here to test

**Read this before anything else.** The builder's "no private copy of the formatter" check has two clauses. Its function-definition clause ended the body at `\n\s{0,4}\}` — **so it only ever matched a function indented four spaces or less.** `sustainability-ui.js` is indented four. **`index.js` is indented eight.**

> **A private `humanSpan` planted in `index.js` with no month-name table passed 10/10 GREEN.** The month-name heuristic beside it was carrying the entire clause.

It found this **only because it tampered with each clause separately.** Its first tamper included a month table, the guard went red, and — its own words — *"had I stopped there I would have reported a working detector."*

**Its generalisation, which Wednesday is adopting fleet-wide and which you should hold it to:**

> **A guard with two clauses, red-proofed with a fixture that trips BOTH, tells you the guard fires. It does not tell you either clause works. Red-proof each clause against a fixture only that clause can catch, or you have measured the pair and learned nothing about the parts.**

**YOUR JOB ON THIS: re-run that discipline against the REWRITTEN guard, which it says now names the function and carries no indentation assumption.**
1. Plant a private copy **with** a month table → expect caught.
2. Plant a private copy **without** one → expect caught. **This is the case that was green before the fix.**
3. Plant one at **eight-space indentation** and one at **four** → both caught.
4. **Then ask the question it did not: is there a third thing carrying a clause?** Disable each clause in turn and confirm the other still catches its own case alone.

**If any single clause cannot be shown to catch something on its own, that clause is decoration and it is a Major** — in a round whose entire subject is a guard that was decoration.

## 3. The other claims to falsify

1. **Shell and pill IDENTICAL at the render.** Drive the exact F-14 window (`2027-01-01` → `2027-02-01`). Both must read `1 Jan – 1 Feb 2027`, **byte-identical to each other**, with the only non-ASCII codepoint being **U+2013**. Verify by codepoint, not by eye. **The builder claims a screenshot at `tests/screenshots/rd292-0c-shell-and-pill-agree.png` — the inverse of your own F-14 evidence shot.** Take your own.
2. **RD-269 avoided by SHAPE, not by care.** The claim: `humanSpan` takes the ISO string `isoLocalDate` already resolved from LOCAL parts and does pure string work, **never constructing a `Date`**, so there is no UTC round-trip to be off by one. Guarded structurally (no `new Date(` / `toLocaleDateString` / `Date.parse` in those bodies) **and** behaviourally under a clock patched 8 hours west of UTC, **with an INSTRUMENT CONTROL asserting the clock is actually live** — the control that caught `process.env.TZ` doing nothing earlier in this ticket. **Confirm the instrument control is present and that it FAILS when the clock patch is removed.** A hostile-clock test whose clock is not hostile is this file's whole subject.
3. **ONE implementation, moved not copied.** `humanDate`/`humanSpan` now in `static/js/local-date.js` beside `isoLocalDate`, both consumers delegating. **The agreement is asserted directly** rather than inferred from two green sides. Confirm there is no surviving second implementation anywhere.
4. **The four keeps the builder found that Wednesday's own enumeration MISSED** — `5843` (another CSV filename), `8103` and `8115` (jobStartTime data fallbacks), `4793`/`4803` (`<input type="date">` values, which REQUIRE ISO). **None needed changing.** Confirm all four are classified and documented, and that **exactly one site — 5248 — is user-facing prose.**
5. **The two keep-CLASSES documented in place to the inverted-range standard:** the FILENAME class at `downloadCSV` (the sink ~15 filenames pass through — the stated reason being that `YYYY-MM-DD` sorts lexicographically while `users_4 Sep 2026.csv` sorts next to April), and the PAYLOAD class at **both** `aiResponseStorage` sites. **An undocumented keep cost 0.10 last round; check the documentation is at the SITE, not in a commit message.**
6. **`#metricsGrid` is ONE element, not nine.** The builder answered your NOT-TESTED gap structurally: one element at `static/index.html:355`, **outside and above all nine tab panes** (first `tab-content` at line 372), written by exactly one function, `updateMetrics()`. **Verify that structurally — it is the claim that closes your "assessed, not measured" gap on the other eight tabs.**

## 4. Explicitly OUT of scope

- **RD-297** (`backend/services/sustainability/metrics.js:72`) — Kam ruled on the reporting window; this is an event date in server prose about a dead ingest. Untouched deliberately. **Finding it again is not a finding.**
- **F-15 is CLOSED** — the builder answered it: the suite genuinely had 32 tests when those red-proofs ran and gained its 33rd afterwards, same session. Not a transcription slip, not a non-executing case. **Do not re-open it.**

## 5. THE REGRESSION CHECK — this is why it is a re-gate and not a spot check

**Item 0b's work must be untouched.** Re-drive, at `aad37da`:
- the **four surfaces** and **all thirteen eye popovers** — en dash by codepoint, zero ISO;
- the **exact string equality** between the announced (`.nx-sus-sronly`) and visible lines;
- the **companion test** asserting the API note is still rendered — **still red-proofable in both directions.**

A shared formatter extracted into a new file is exactly the change that quietly breaks the component it was extracted from.

## 6. Boundaries

Findings-only. **Zero writes to the NexusAI tree** — `git status` empty at start AND end, HEAD still `aad37da`. No fix, no ticket, no `rm`. **Your `git archive | tar -x` approach from this morning was correct and is now the standard** — Wednesday's earlier worktree instruction was wrong and the charter outranked it. Report to **`wednesday-agent@agentmail.to`**.

## PROVENANCE

```
aad37da is head of rd-136-nga-defaults-s12 at origin   | git ls-remote origin <branch>                        | read 2026-09-04 11:15
e5be9fe is an ancestor of aad37da; two commits between | git merge-base --is-ancestor + git log e5be9fe..aad37da | read 2026-09-04 11:15
gate expectation at aad37da = 1463 tests / 86 suites   | git show aad37da:scripts/verify-expected-counts.json  | read 2026-09-04 11:15
static/js/local-date.js exists at aad37da              | git cat-file -e aad37da:static/js/local-date.js       | read 2026-09-04 11:15
Kam ruled extend-one-deploy at 10:59:23                | 0_Brain/dashboard/data/chat_log.json, Wednesday's tree | read 2026-09-04 11:00
every claim in §2 and §3, and the four missed keeps    | the S31 ITEM 0c COMPLETE mail, wednesday-agent@ inbox, 2026-09-04T01:13:12Z — the BUILDER's measurements, not re-derived by Wednesday | read 2026-09-04 11:14
the #metricsGrid line numbers (355 / 372)              | the same mail — builder's claim, NOT opened by Wednesday | read 2026-09-04 11:14
```

**Unmeasured, stated as such:** Wednesday has not opened `local-date.js`, `index.html`, or any test in this round — every §2/§3 statement is the builder's own account and is yours to falsify.
