# QA/Testing Agent — Industry Practices Research
**Date:** 2026-08-11 · **Researcher:** web-research agent for Wednesday · **Purpose:** inform the design of a cross-project QA agent that tests builds *from a demanding real user's perspective* ("here is the build + spec — break it").

---

## BLUF — the practices that matter most for this agent

1. **Run testing as chartered sessions, not open wandering** — every test run gets a written charter ("explore X with Y looking for Z"), a time box, and a session report (SBTM, Bach & Bach).
2. **Falsify, don't confirm** — the agent's mission on every feature is "try to prove this DOESN'T work"; research shows LLMs default to confirmatory tests, and lower confirmation bias directly correlates with task success. Prompt it to design disconfirming tests explicitly.
3. **A check that cannot fail is not a check** — for every test the agent runs, it must be able to state what outcome would have counted as failure; if nothing could have failed, the test was theatre (Bolton/Bach's testing-vs-checking distinction).
4. **Judge against oracles, not vibes** — encode FEW HICCUPPS: every "is this a bug?" decision cites which consistency was violated (claims, comparable products, history, user desires, world knowledge, standards…).
5. **Cover the product with SFDIPOT** — Structure, Function, Data, Interfaces, Platform, Operations, Time — as the coverage outline so nothing is tested only along the happy path.
6. **Attack data and state, not just UI** — boundaries, CRUD lifecycle, interruptions, replay/double-submit, multi-user collision, sequence reordering — the Hendrickson cheat-sheet attacks are the highest bug-per-minute heuristics in the literature.
7. **Cold acceptance from a fresh environment** — test as a brand-new user with zero developer context: fresh account, empty data, first-run flow, only the spec in hand. The first-run empty state is not an edge case; it's the product's handshake.
8. **Walk the user's actual journeys as personas** — including the impatient user, the error-prone user, the keyboard-only user, and the malicious user (Whittaker's tours give ready-made walk patterns).
9. **Every claim in the spec is a test** — enumerate the spec's explicit and implicit claims and challenge each one (HTSM Claims Testing: "challenge every claim").
10. **Report findings in one-defect-per-report shape**: numbered repro steps from a known state, expected vs actual, evidence, environment, severity (impact) separated from priority (urgency) — and follow RIMGEA before filing (replicate, isolate, maximize, generalize).

---

## The tester's mindset — distilled from the literature

**Falsification over confirmation.** The defining trait of an excellent tester is that they attempt to disprove, not demonstrate. Bolton/Bach's core distinction: *checking* is confirming what you already believe; *testing* is an open investigation designed to discover what you don't know — including things that would embarrass the belief. The design of a test is where the intelligence lives ([DevelopSense, Testing vs. Checking](https://developsense.com/blog/2009/08/testing-vs-checking); refined in [Testing and Checking Refined](https://www.satisfice.com/blog/archives/856)). Operationally for an agent: before running any test, write down the outcome that would count as a FAIL. If you cannot, redesign the test.

**You can never verify quality — you assess it and tell a story.** Bach's HTSM is explicit: "You can never know the 'actual' quality of a software product — you can't 'verify' quality, as such — but by performing tests, you can make an assessment, and that takes the form of a story you tell (including bugs, curios, etc.)" ([HTSM v6.0](https://www.satisfice.com/download/heuristic-test-strategy-model)). The agent's output is therefore a *testing story with evidence*, never a binary "passes."

**Oracles are fallible heuristics, applied not followed.** An oracle is a means of recognizing a problem. Bolton: oracles "are, like all heuristics, fallible and context-dependent; to be applied, not followed" — they can make you see problems that aren't there or miss ones that are. A strong tester cites *which* oracle a suspected bug violates, which is what makes the report credible ([FEW HICCUPPS](https://developsense.com/blog/2012/07/few-hiccupps)).

**Simultaneous learning, design, and execution.** Exploratory testing is not "unplanned testing" — it's a loop where each observation reshapes the next test. The tester follows surprises. Charters keep the loop accountable without killing it ([Session-based testing](https://en.wikipedia.org/wiki/Session-based_testing)).

**User empathy — but genuinely simulated.** HTSM's User Testing warning is directly relevant to an AI agent: "Otherwise, systematically simulate a user (be careful — it's easy to think you're like a user even when you're not)." Powerful user testing involves *a variety of users and user roles, not just one*. The agent should never test as "a user" — always as a *named persona with attributes* (novice on mobile, expert power-user, hostile actor, accessibility-dependent user).

**Curiosity patterns of legendary bug-finders:** vary one thing at a time past its limit (boundaries); do things in the wrong order (sequences); do things twice (replay/idempotency); do two things at once (races); interrupt everything mid-flight; leave things half-done and come back; follow the data's whole life, not just its birth (create → read → update → delete → restore); ask "what did the developer probably assume?" and violate exactly that assumption.

---

## Heuristic catalogs worth encoding

These are spelled out so the agent can execute them as instructions.

### 1. SFDIPOT — product coverage outline (Bach, HTSM v6.0)
Walk every category; for each, ask "what here have I not yet touched?" ([source PDF](https://www.satisfice.com/download/heuristic-test-strategy-model))

- **Structure** — everything that comprises the product: code modules/executables, hardware, independent services/processes, non-executable files (help, sample data), collateral (docs, web pages, license text).
- **Function** — everything the product does: multi-user/social features; calculations; time-related behavior (timeouts, periodic events, time zones, business holidays); security-related (rights per user class, encryption, front-end vs back-end protections); transformations (anything that modifies something); startup/shutdown (every method of invocation and exit); multimedia; **error handling — every function that detects and recovers from errors, including all error messages**; interactions between functions; testability features (logs, diagnostics).
- **Data** — everything it processes and produces: input/output; preset data (defaults, prebuilt DBs); persistent data (settings, states); interdependent data; sequences/permutations (sorted vs unsorted, order of operations); **cardinality (zero, one, many, max, uniqueness constraints)**; big/little size and aggregation extremes; invalid/noise (corrupted, uncontrolled data); **lifecycle (created, accessed, modified, deleted)**.
- **Interfaces** — every conduit: user interfaces; system interfaces (logs, other programs, disk, network); API/SDK; import/export.
- **Platform** — everything it depends on but outside the project: external hardware, external software (OS, concurrent apps, drivers, fonts), embedded third-party components, product footprint (memory, file handles).
- **Operations** — how it will be used: user attributes; physical environment; **common use patterns; disfavored use (ignorant, mistaken, careless, or malicious input); extreme use** (challenging but legitimate patterns).
- **Time** — every product/time relationship: when input arrives vs when output is created; fast/slow input, fastest and slowest combinations; changing rates (spikes, bursts, hangs); **concurrency (multi-user, threads, shared data)**.

### 2. FEW HICCUPPS — oracles for "is this a bug?" (Bolton & Bach)
Desirable behavior is *consistency with* each of these; a suspected bug should name which one is violated ([DevelopSense](https://developsense.com/blog/2012/07/few-hiccupps)):

- **F**amiliarity — inconsistent with patterns of problems seen before.
- **E**xplainability — we expect the system's behavior to be articulately explainable; "I can't explain why it did that" is itself a finding.
- **W**orld — consistent with what we know of the real world (dates, money, geography, physics).
- **H**istory — consistent with previous versions of itself (regressions).
- **I**mage — consistent with the reputation/brand the org wants to project (typos, jank, embarrassments).
- **C**omparable products — consistent with competitors and analogous features elsewhere.
- **U**ser desires — consistent with what reasonable users would want (not just literal expectations).
- **P**roduct — internally consistent with comparable elements of itself (two screens doing the same thing differently).
- **P**urpose — consistent with the explicit and implicit uses people put it to.
- **S**tatutes & standards — consistent with laws, regulations, and adopted standards (incl. WCAG, privacy).

### 3. HTSM Quality Criteria — the risk dimensions (per category, "how would I recognize if the product worked poorly in this regard?")
**Capability** (sufficiency, correctness) · **Reliability** (robustness over time; *error handling: resists bad data, fails gracefully, recovers readily*; data integrity; safety) · **Usability** (learnability, operability, accessibility) · **Charisma** (aesthetics, entrancement, image of quality) · **Security** (authentication, authorization at each privilege level, privacy, holes) · **Scalability** · **Compatibility** (with other apps, OSes, hardware, earlier versions of itself; footprint) · **Performance** · **Installability** (missing-component detection, clean uninstall, upgrades respecting existing config) · **Development** (supportability, testability, maintainability). ([HTSM v6.0](https://www.satisfice.com/download/heuristic-test-strategy-model))

### 4. HTSM's nine General Test Techniques (each is an executable recipe)
- **Function testing** — *test what it can do*: identify every function and sub-function; decide how you'd know it works; test each one at a time; confirm it does what it should AND doesn't do what it shouldn't.
- **Domain testing** — *partition the data*: find all data (outputs too); pick boundary values, typical values, invalid values, best representatives; combine data worth testing together; force the whole range of possible outputs to occur.
- **Stress testing** — *overwhelm the product*: find sub-systems vulnerable to overload; hit them with large/complex data, high loads, long runs, low memory.
- **Flow testing** — *do one thing after another*: chain activities end-to-end **without resetting the system between actions**; vary timing and sequencing; try parallel threads.
- **Scenario testing** — *test to a compelling story* of someone who matters doing something that matters, with everything going on around the product.
- **Claims testing** — *challenge every claim*: collect claims from spec, help text, ads, SLAs; analyze and clarify vague claims; test each; if spec and product disagree, expect one of them to change.
- **User testing** — *involve the users*: identify user categories/roles; determine each category's use cases and what they value; use real user data; otherwise systematically simulate a variety of users.
- **Risk testing** — *imagine a problem, then look for it*: list the worst problems this product could have; focus on the ones that matter most; design tests specifically to reveal each; consult past bug reports.
- **Tool-supported testing** — use tools to perform many actions and check many things; automatic change detectors; test-data generators.

### 5. Hendrickson/Lyndsay/Emery Test Heuristics Cheat Sheet — concrete attacks
The highest-density attack list in the field ([Ministry of Testing edition](https://www.ministryoftesting.com/articles/test-heuristics-cheat-sheet); [BBST](https://bbst.courses/elisabeth-hendrickson-james-lyndsay-and-dale-emery-test-heuristics-cheat-sheet/)):

**Data-type attacks**
- *Numbers:* 0, negatives, decimals, scientific notation, powers of two (32768, 65536, 2147483648), leading zeros, European formats (1.234.567,89), number-as-string.
- *Strings:* empty, single space, all spaces, 255 / 2048+ chars, accented chars, CJK chars, emoji, delimiters (quotes, commas, slashes), SQL fragments (`'; DROP TABLE`—as input-handling test), HTML/JS (`<script>` — injection test).
- *Dates/times:* time zones, DST transitions, Feb 29 (and Feb 29 in non-leap years), format variants (06/05/2001 vs 6/5/2001), timeouts, clock changes mid-operation.
- *Paths/files:* long names (>255), special characters, nonexistent paths, write-protected, corrupted files.

**Behavioral attacks**
- **Boundaries** — just below, at, just above every limit. **Goldilocks** — too big, too small, just right.
- **CRUD** — create, read, update, delete every data entity; then *delete-and-restore*, delete-while-referenced, update-after-delete.
- **Interruptions** — log off, kill the tab, reboot, timeout, cancel mid-operation; then check what state remains.
- **Sequences** — vary order of operations; undo/redo; do steps backwards; skip a step; repeat a step.
- **Flood / replay** — submit the same request many times, fast (double-click submit; refresh on a POST; retry a payment). Idempotency check: did the second submission create a second effect?
- **Multi-user collision** — two accounts (or two tabs) create/update/delete the same record simultaneously; who wins, and is the loser told?
- **Starvation** — max out CPU/memory/network/disk; slow network; offline mid-flow.
- **Dependencies & cardinality** — customer with 0, 1, many, max invoices; parent deleted while children exist.
- **State analysis** — map states, events, transitions; then force *illegal* transitions (paste a URL to skip a wizard step; use back button after checkout; act on a stale page after session expiry).
- **Web-specific** — back button (expired-page messages), refresh, bookmark deep pages, hack URL parameters, multiple browser instances of the same session.

**Permissions/role matrix (composite of Hendrickson Multi-User + HTSM Security):** build a matrix of every role × every sensitive action/URL/API endpoint; verify each denied cell is actually denied *server-side* (not just hidden in the UI); test privilege changes mid-session; test direct-object references (change the ID in the URL to someone else's record).

### 6. Whittaker's tours — ready-made exploration walks
From *Exploratory Software Testing* ([Whittaker](https://www.amazon.com/Exploratory-Software-Testing-Tricks-Techniques/dp/0321636414); [summary](https://www.getxray.app/blog/test-tours-exploratory-testing-strategy-qa-teams)). Each tour is a session charter template:
- **Guidebook/Money tour** — walk exactly the features the sales pitch / spec / demo promises; do they hold up under a paying customer's scrutiny?
- **Landmark tour** — pick key features, order them, visit each in sequence.
- **Intellectual tour** — ask the software hard questions: most complex input, biggest legal document, most nested data.
- **FedEx tour** — follow a piece of data through the entire system, everywhere it travels.
- **Garbage-collector tour** — methodically visit every screen/menu item, however minor, checking each briefly.
- **Back-alley tour** — exercise the *least*-used, least-polished features.
- **All-nighter tour** — never close the app; leave it running, sleep the machine, come back, keep using it.
- **Supermodel tour** — look only at the surface: layout, alignment, spelling, visual states in every screen.
- **Obsessive-compulsive tour** — repeat every action twice, three times; enter the same data again; revisit the same screen.
- **Saboteur tour** — actively undermine: deny resources, kill connectivity, feed it the wrong thing at the worst moment.
- **Supporting-actor tour** — test the features *next to* the ones changed (neighbors regress first).
- **Rained-out tour** — start operations and cancel every one of them midway.

### 7. Session-based test management — the accountability wrapper
([Wikipedia/SBTM](https://en.wikipedia.org/wiki/Session-based_testing); [Bach's SBTM](https://www.satisfice.com/blog/archives/downloads/reference))
- **Charter:** one sentence — mission, area, what problems we're hunting. Created up front; revisable.
- **Session:** uninterrupted, time-boxed (60–120 min human-scale; for an agent, a bounded work unit), one charter.
- **Session sheet:** charter · time breakdown (**T**est design/execution %, **B**ug investigation %, **S**etup %) · bugs found · issues/questions raised · notes of what was actually done · data files used.
- **Debrief (PROOF):** Past (what happened), Results, Obstacles, Outlook (what remains), Feelings (tester confidence). For the agent: report obstacles and *untested areas* with the same prominence as bugs — "what I could NOT test" is first-class output.

---

## User-perspective specifics

### Nielsen's 10 usability heuristics — walk as an evaluation checklist
([NN/g](https://www.nngroup.com/articles/ten-usability-heuristics/)) — for each screen/flow, check:
1. **Visibility of system status** — is the user always informed of what's going on, promptly?
2. **Match with the real world** — user's language, not internal jargon.
3. **User control and freedom** — a clearly marked emergency exit from every mistaken action (cancel, undo, back).
4. **Consistency and standards** — same words/actions mean the same thing everywhere; platform conventions followed.
5. **Error prevention** — does the design prevent the error before a message is needed?
6. **Recognition over recall** — options visible; user never has to remember info from another screen.
7. **Flexibility and efficiency** — shortcuts for experts without confusing novices.
8. **Aesthetic and minimalist design** — no irrelevant information competing with the relevant.
9. **Help users recognize, diagnose, recover from errors** — plain language, no bare error codes, precise problem, constructive suggestion.
10. **Help and documentation** — ideally unnecessary; if present, task-focused and findable.

### Error-message quality (a dedicated pass)
NN/g's standard ([Error-Message Guidelines](https://www.nngroup.com/articles/error-message-guidelines/); [scoring rubric](https://www.nngroup.com/articles/error-messages-scoring-rubric/); [hostile patterns](https://www.nngroup.com/articles/hostile-error-messages/)): every error message must be **visible near the point of error, explicit, human-readable (no raw codes/stack traces), polite (no blame), precise about what went wrong, and constructive about what to do next**. Anti-patterns to flag: premature errors (shown before the user finished), errors that clear the user's input, generic "something went wrong," and blaming language. Agent procedure: deliberately trigger every reachable error (bad input, network cut, permission denied, expired session) and score each message against this rubric.

### First-run / empty-state / cold-start testing
The first-run empty state is the product's handshake with a new user, not an edge case ([Smashing Magazine](https://www.smashingmagazine.com/2017/02/user-onboarding-empty-states-mobile-apps/); [Raw.Studio](https://raw.studio/blog/empty-states-error-states-onboarding-the-hidden-ux-moments-users-notice/)). Agent procedure: create a **fresh account in a fresh environment** with zero developer context; every list, dashboard, and tab visited before any data exists must show a designed empty state with a clear next action — never a blank screen, spinner, or error. Then test the *second* cold start: data added then all deleted (the "emptied" state often differs from the "never-used" state).

### Journeys and personas
- Derive 3–5 end-to-end journeys from the spec's purpose (per HTSM Scenario Testing: a compelling story of someone who matters doing something that matters) and run each *without resetting between steps* (Flow Testing).
- Run each journey as distinct personas: **novice** (reads nothing, clicks the obvious thing), **expert in a hurry** (keyboard, double-clicks, back button), **interrupted user** (abandons mid-flow, returns next day), **keyboard-only / screen-reader user**, **skeptic** (checks that displayed numbers add up), **hostile actor** (URL hacking, other users' IDs).

### Accessibility quick hits (WCAG-derived)
([WebAIM WCAG checklist](https://webaim.org/standards/wcag/checklist)) — the machine-plus-judgment short list:
- **Keyboard-only pass:** Tab reaches every interactive element in logical order; Shift+Tab reverses; nothing traps focus; visible focus indicator everywhere; all functionality achievable without a mouse.
- **Contrast:** body text ≥ 4.5:1, large text ≥ 3:1 (light-gray-on-white is the classic offender).
- **Images:** every meaningful image has meaningful alt text (automated tools catch *missing* alt; only judgment catches *useless* alt).
- **Zoom to 200%** without loss of content or function; **links descriptive** (no bare "click here"); form fields labeled.
- Note: automated tools detect only ~30–40% of WCAG issues; the rest require judgment — which is exactly what the agent pass adds.

---

## LLM-agent-as-tester: what works, what fails

### What works (2025–26 practice)
- Agents that **perceive app state, plan toward a testing goal, act, evaluate, adapt** — the exploratory loop — now credibly reach parity with scripted automation for broad coverage, and they self-heal across UI changes because they navigate semantically rather than by brittle selectors ([Autify](https://autify.com/blog/ai-agent-testing); [DevAssure](https://www.devassure.io/blog/autonomous-qa-agentic-ai/)).
- The mature 2026 deployment pattern is **hybrid**: agents take broad exploratory coverage and maintenance-heavy regression; deterministic scripts keep compliance-critical and performance-benchmark checks ([DevAssure](https://www.devassure.io/blog/autonomous-qa-agentic-ai/)).
- **Comprehensive logging from day one** — every action, observation, and verdict traceable — is called out as non-negotiable for trust in agent findings.

### What fails — the failure modes, named plainly
1. **Confirmation bias / failure to falsify.** LLMs preferentially propose tests that *confirm* their current hypothesis (the Wason 2-4-6 failure). Measured directly: models favor confirmatory tests, and a lower confirmation bias strongly correlates with higher task success ([Failing to Falsify, arXiv 2604.02485](https://arxiv.org/html/2604.02485v1)). **Mitigations that measurably work:** *Think-in-Opposites* prompting ("design tests that would both confirm AND contradict your current belief") improved success in 11/11 model scenarios; *Dual-Goal* prompting (simultaneously track the hypothesis and its complement) helped in 8/11.
2. **Checks that cannot fail.** An agent asked to "verify the feature works" will find a way for it to work — happy-path input, generous interpretation, retry until green. This is Bolton/Bach's checking-without-testing failure: confirmation of existing belief, no discovery ([Testing vs. Checking](https://developsense.com/blog/2009/08/testing-vs-checking)). **Rule to encode: before executing any test, the agent states the concrete observable outcome that would count as FAIL. No falsifiable outcome → the test is redesigned or discarded.**
3. **Verdict swayed by metadata instead of evidence.** In LLM-assisted security review, agents accepted broken changes because commit messages and PR descriptions *argued* they were fine; redacting the persuasive metadata recovered ~69% of missed detections and instructing the agent to ignore it raised detection to 94% ([arXiv 2603.18740](https://arxiv.org/html/2603.18740v1)). **Rule: the agent tests the build, not the build's marketing — spec claims are inputs to challenge (Claims Testing), never evidence of correctness.**
4. **Can't catch its own mistakes.** LLMs are poor at spotting errors in their own reasoning chains (GPT-4: ~53% at finding planted simple mistakes) ([Google research via Nova Spivack](https://www.novaspivack.com/technology/ai-technology/why-ai-systems-cant-catch-their-own-mistakes-and-what-to-do-about-it)). **Implication: the tester agent must be a different session/agent from the builder, with no shared context — cold acceptance is structurally, not just procedurally, important.**
5. **Confident false positives.** Agents report bugs that aren't bugs, especially in GUI tasks. Mitigation: the RIMGEA discipline — *replicate before reporting*; a finding the agent cannot reproduce twice is filed as a "curio/flaky observation," not a defect.
6. **Missing business context.** Agents spot pattern-level anomalies but miss domain nuance and regulatory edge cases ([Autify](https://autify.com/blog/ai-agent-testing)). Mitigation: the invoking project must pass spec + user description into the charter; the agent's FEW HICCUPPS "Statutes/Standards" and "Purpose" oracles are only as good as the context given.

### How to prompt a testing agent to genuinely BREAK things (synthesis)
- Frame the mission as adversarial and falsifying: "Your job is to find the ways this fails a demanding real user. A run that finds nothing must prove it *earned* that nothing — list the attacks attempted and the failure criteria each one had."
- Give it charters, not scripts (SBTM), tours as walk patterns (Whittaker), attack tables as ammunition (Hendrickson), oracles as the judging standard (FEW HICCUPPS), and SFDIPOT as the coverage ledger.
- Require Think-in-Opposites at the hypothesis level: for each feature, state the belief ("saving works") and design tests for both the belief and its complement ("under what conditions would saving silently lose data?").
- Require the "what I could not test" section — untested areas reported with the same prominence as bugs (PROOF's Obstacles/Outlook).

---

## Reporting standards — the shape a finding should take

**Before filing — RIMGEA** (Kaner, BBST Bug Advocacy; [RIMGEN at BBST](https://bbst.courses/rimgen/); [Atomic Object summary](https://spin.atomicobject.com/2015/03/20/rimgea-testing-mnemonic)):
- **R**eplicate — reproduce on demand; no "sometimes" in reports (if truly intermittent, report it AS intermittent with the observed frequency).
- **I**solate — minimize to the fewest steps that still trigger it; identify the triggering variable.
- **M**aximize — find the worst consequence this bug can cause (a cosmetic symptom may have a severe variant).
- **G**eneralize — find how broadly it occurs (other browsers, other data, other roles).
- **E**xternalize — write for the reader who must act on it.
- **A**nd say it clearly and dispassionately — no blame, no snark.

**The report itself** (Tatham; BrowserStack; Marker.io; Kualitee — see Sources):
- **One defect per report.** Similar symptoms may be different bugs; separate reports track, close, and regress independently.
- **Title:** symptom + location + condition, free of dynamic details (IDs, emails) so duplicates group.
- **Environment:** build/version, OS, browser/device, account/role used, data state.
- **Steps to reproduce:** numbered, starting from a *known state* ("1. Fresh login as role X on build Y…"), each step one action, specific enough for someone with zero context.
- **Expected result** (with the oracle: *which* consistency it violates — spec claim, comparable product, internal consistency, user desire) vs **actual result** (facts only — report symptoms, not diagnoses; separate observation from speculation, and label any speculation as such — Tatham).
- **Evidence:** screenshot/recording/log excerpt/response body for every defect. No evidence, no defect.
- **Severity ≠ priority** ([Kualitee](https://www.kualitee.com/blog/bug-management/severity-levels-vs-priority-levels-bug-tracking/)): severity = technical impact (how badly it breaks), priority = business urgency (how soon to fix). The agent assigns severity with justification; priority belongs to the product owner (Kam/Wednesday). Classic illustration: a crash in a retired feature = high severity, low priority; a typo on the checkout page = low severity, high priority.
- **Session-level report** wraps the defects: charter · coverage achieved (SFDIPOT areas touched) · attacks attempted with their failure criteria · bugs · curios/questions · obstacles · **explicitly untested areas** · overall testing story and confidence.

---

## Sources

**Exploratory discipline & heuristics (primary)**
- Heuristic Test Strategy Model v6.0 (Bach, Satisfice) — https://www.satisfice.com/download/heuristic-test-strategy-model (also https://www.developsense.com/resource/htsm.pdf)
- FEW HICCUPPS (Bolton, DevelopSense) — https://developsense.com/blog/2012/07/few-hiccupps
- All Oracles Are Heuristic (Bolton) — https://developsense.com/blog/2012/04/all-oracles-are-heuristic
- Testing vs. Checking (Bolton) — https://developsense.com/blog/2009/08/testing-vs-checking
- Testing and Checking Refined (Bach & Bolton) — https://www.satisfice.com/blog/archives/856
- Session-based testing — https://en.wikipedia.org/wiki/Session-based_testing
- Satisfice reference downloads (SBTM et al.) — https://www.satisfice.com/blog/archives/downloads/reference
- Test Heuristics Cheat Sheet (Hendrickson/Lyndsay/Emery, MoT edition) — https://www.ministryoftesting.com/articles/test-heuristics-cheat-sheet
- BBST on the cheat sheet — https://bbst.courses/elisabeth-hendrickson-james-lyndsay-and-dale-emery-test-heuristics-cheat-sheet/
- Whittaker, *Exploratory Software Testing* (tours) — https://www.amazon.com/Exploratory-Software-Testing-Tricks-Techniques/dp/0321636414 · tour summaries: https://www.getxray.app/blog/test-tours-exploratory-testing-strategy-qa-teams · https://www.softwaretestinghelp.com/exploratory-testing-tours/

**User perspective**
- 10 Usability Heuristics (NN/g) — https://www.nngroup.com/articles/ten-usability-heuristics/
- Error-Message Guidelines (NN/g) — https://www.nngroup.com/articles/error-message-guidelines/
- Error Messages Scoring Rubric (NN/g) — https://www.nngroup.com/articles/error-messages-scoring-rubric/
- Hostile Patterns in Error Messages (NN/g) — https://www.nngroup.com/articles/hostile-error-messages/
- WebAIM WCAG 2 Checklist — https://webaim.org/standards/wcag/checklist
- WCAG 2.1.1 keyboard accessibility (UXPin) — https://www.uxpin.com/studio/blog/wcag-211-keyboard-accessibility-explained/
- Empty states & onboarding — https://www.smashingmagazine.com/2017/02/user-onboarding-empty-states-mobile-apps/ · https://raw.studio/blog/empty-states-error-states-onboarding-the-hidden-ux-moments-users-notice/ · https://userpilot.com/blog/empty-state-saas/

**Acceptance & regression**
- Acceptance Testing (Agile Alliance) — https://agilealliance.org/glossary/acceptance-testing/
- UAT best practices for Agile teams (TechTarget) — https://www.techtarget.com/searchsoftwarequality/tip/User-acceptance-testing-best-practices-for-Agile-teams
- Regression testing in agile (BugBug) — https://bugbug.io/blog/software-testing/regression-testing-agile/

**LLM/agent-driven testing**
- Failing to Falsify: confirmation bias in LMs (arXiv) — https://arxiv.org/html/2604.02485v1
- Confirmation bias in LLM-assisted security code review (arXiv) — https://arxiv.org/html/2603.18740v1
- Why AI systems can't catch their own mistakes (Spivack, summarizing Google Research) — https://www.novaspivack.com/technology/ai-technology/why-ai-systems-cant-catch-their-own-mistakes-and-what-to-do-about-it
- How Agentic AI improves QA (Autify) — https://autify.com/blog/ai-agent-testing
- Autonomous QA in 2026 (DevAssure) — https://www.devassure.io/blog/autonomous-qa-agentic-ai/
- Rethinking agent-generated tests for SWE agents (arXiv) — https://arxiv.org/pdf/2602.07900

**Reporting**
- How to Report Bugs Effectively (Tatham) — https://www.chiark.greenend.org.uk/~sgtatham/bugs.html
- RIMGEN/RIMGEA (BBST Bug Advocacy) — https://bbst.courses/rimgen/ · https://spin.atomicobject.com/2015/03/20/rimgea-testing-mnemonic
- Severity vs priority (Kualitee) — https://www.kualitee.com/blog/bug-management/severity-levels-vs-priority-levels-bug-tracking/
- Effective bug reports (BrowserStack) — https://www.browserstack.com/guide/how-to-write-a-bug-report
- Steps to reproduce (Marker.io) — https://marker.io/blog/steps-to-reproduce-a-bug
