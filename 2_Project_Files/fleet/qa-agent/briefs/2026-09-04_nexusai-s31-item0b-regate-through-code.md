# QA Agent Invocation Brief — Datasec/NexusAI, S31 ITEM 0b RE-GATE (the ISO window on every surface), THROUGH-CODE + LOCAL RENDER

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

**Then your own pass 22 report on the previous round of this exact work — the baseline, and the six claims you already cleared:**
`/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-04-s31-item0-through-code/SUMMARY.md`
(If that path differs, it is your most recent NexusAI report — pass 22, subject `S31 item 0 @2f3ce7d`.)

---

## 1. Target — and the SHA has MOVED since the round was commissioned. Read this first.

- **Client / Project:** `Datasec / NexusAI`
- **Branch:** `rd-136-nga-defaults-s12`
- **GATE THIS SHA: `e5be9fe`** (`e5be9fefeda15595557fe3cdfb5ce290bc6d002e`).
- The builder reported item 0b at **`554f6b3`**. **`554f6b3` is an ancestor of `e5be9fe`** and the builder pushed `e5be9fe` while this brief was being written.

**Why you are gating `e5be9fe` and not the SHA the builder named.** What deploys must be what was tested; gating an ancestor and shipping the head means shipping unGATEd commits. **The delta is safe for your purpose and you should verify that claim yourself rather than take it from me:**

```
554f6b3..e5be9fe   __tests__/brand-md-accent-count.test.js      (test)
                   __tests__/handover-gate-table.test.js        (test, new)
                   docs/sustainability/S29_RESTAND_HANDOVER.md  (doc)
                   scripts/verify-expected-counts.json          (gate expectation)
```

**No product or render surface changed between them.** So every item-0b claim below was made at `554f6b3` and transfers to `e5be9fe` unchanged — **but confirm that with your own `git diff --name-only 554f6b3..e5be9fe` before you rely on it.** If that diff shows anything under `frontend/` or `backend/` that renders, stop and mail Wednesday: the premise of this brief is wrong.

**THE NUMBER CHANGED WITH THE SHA, AND THIS IS THE TRAP.** The builder's mail claims **PASS 1439/1439 across 84**. That was true at `554f6b3`. At `e5be9fe` the committed expectation is **1448 tests / 85 suites** (`git show e5be9fe:scripts/verify-expected-counts.json`, read 2026-09-04 10:0x AEST). **A run reporting 1439/84 at `e5be9fe` is a FAILURE of the expectation gate, not a pass** — RD-291 built that file precisely so a count change is visible. Measure the gate yourself at `e5be9fe` and report the number you got, not the number you were given.

- **Running target: a LOCAL run you stand YOURSELF, from a worktree at `e5be9fe`.** NOT the demo. RD-76 stands and RD-294 means the demo has no sustainability data to render.
- **Production?: NOTHING is deployed and NO finding of yours triggers a deploy.** `caf1fe7`'s GO remains WITHDRAWN. The deploy happens later, on Wednesday's GO, bundled with a config change — never on this pass.

---

## 2. Surfaces and servers — what to leave alone, and why you must stand your own

**LEAVE ALONE — do not restand, restart or kill any of these:** `:3068` `:3072` `:3073` `:3075` `:3076` `:3077`, plus the dashboard `:47787`. **`:3077` is the source of the frames Kam is reviewing — never restand it.** All seven measured answering `200` by Wednesday at 10:0x AEST in this action.

**TWO SERVERS ARE UP THAT YOU MIGHT BE TEMPTED TO REUSE. Do not reuse either:**
- **`:3191`** — the handover records this as **your own server from pass 22, standing at `2f3ce7d`**. It survived its pane's close (detached, tty `??`). **Wednesday measured only that it answers `200` — NOT its SHA.** Treat it as stale and do not test against it.
- **`:3080`** — the builder says this is its own and "still up for the tester". **Wednesday measured only that it answers `200` — NOT its SHA, and not who owns it.** A server whose commit you did not establish is not evidence about `e5be9fe`.

**Stand your own, on a port none of the above, from a worktree at `e5be9fe`.** The project's established pattern is `qa-worktrees/<sha>` beside the main tree (54 such worktrees exist today) — use it, and **never check out anything in the builder's working tree at `2_Project_Files/`, which is live and in use.**

---

## 3. The builder's two known traps, carried VERBATIM and credited — both are real and each costs ~20 minutes

1. **A fresh `DATA_DIR` redirects `/` to `/first-run-setup`.** Set `firstRunComplete: true` in `settings.json` and restart.
2. **`SEED_DEMO_DATA=true` DOES NOTHING on a local run** — the seeder is wired only into the LAW boot branch (`server.js:3553` versus the `else` at `:4087`). **That is RD-293, already filed.** Seed out of band by calling `seedDemoDataIfRequested` against the same DB. **Seeded, the window resolves to 2026-01-30..2026-04-29 — the mock's own example window** — so the surfaces you are checking have real dates behind them rather than an empty state.

Its suggested stand-up line:
`DB_PATH=<dir>/printer_logs.db DATA_DIR=<dir> RATE_LIMIT_MAX=20000 PORT=<port> NODE_ENV=development node backend/server.js`

---

## 4. The claims to falsify — all the builder's own, from its STATUS mail of 2026-09-04 10:01 AEST

**Context you need in order to weigh them:** Wednesday refused to score item 0 complete because F-13 (your pass 22) found the humanised date reached the pill's FACE while the popover and the screen-reader line still printed `2026-01-30 to 2026-04-29`. **That ruling is what this round answers.** The builder was told to enumerate the surfaces FROM THE TREE rather than from the finding.

1. **FOUR surfaces now carry the humanised form, not the two F-13 named.** The builder's own enumeration:

```
pillText()          the pill's face                    done in item 0
periodSentence()    the window popover AND the sronly  <- F-13 named these two
periodLabelFor()    every per-KPI eye popover          <- NOT named by F-13
the metrics tile    "the store holds print jobs for X"  <- NOT named by F-13
```

   **Drive all four in the browser and read the rendered text BY CODEPOINT.** The separator must be **U+2013 EN DASH** (`e2 80 93`) — not a hyphen, not an em dash. **This is where Wednesday was wrong last round**: the brief said the word "to" from a decision card's prose, and the builder hexdumped the ratified mock (`docs/sustainability/mocks/s25-relayout-mock.html:117`) and proved the ratified character is an en dash. At normal size the three are indistinguishable by eye. **Verify by codepoint or you have not verified.**

2. **THE CLOSING CHECK IS ABSENCE, NOT PRESENCE.** The builder claims the check is the absence of the ISO form across the window surfaces. **Presence checks pass early and always** — "the new format appears on the page I looked at" would have passed last round too. **Sweep for the ISO form and report what remains**, including anything outside the four surfaces above.

3. **The accessibility half is asserted as an EQUALITY OF FORM between the announced line and the visible one** — not as "the `.nx-sus-sronly` element exists". **Drive it and confirm the announced string equals the visible string in form.** Before this round the fix reached every user except the ones who cannot see the pill; that is the half most likely to be quietly re-broken.

4. **THE MOST INTERESTING CLAIM, AND THE ONE WORTH YOUR TIME.** The builder disclosed against itself that **its jest sweep was GREEN while the live page still carried an ISO date** — the fixtures carry no API notes, and that string only renders when the energy KPI is unavailable. Its two remedies, both claimed committed:
   - the sweep is **re-scoped to what it actually claims** (window surfaces), rather than being green only while its fixtures happen to be quiet;
   - **a companion test asserts the API note is STILL RENDERED**, because a sweep that went green by the note vanishing would hide a regression while appearing to prove a scope.

   **Falsify the companion test specifically: delete/blank the note and confirm that test goes RED.** A companion test that cannot fail is the exact defect this whole round is about.

5. **TWO DELIBERATE KEEPS — confirm they are documented in place, and judge whether the documentation is honest:**
   - the **query-string builder stays ISO** (API contract, not a render);
   - the **inverted-range message quotes the user's OWN typed input verbatim**, on the reasoning that reformatting someone's input misrepresents it and a half-typed value cannot be parsed.
   **A documented exception is how a reader tells a deliberate keep from a missed surface** — so check the documentation exists at the site, not only in the mail.

6. **RED-PROOFS — and one prediction MISSED, which the builder disclosed:**

```
periodLabelFor -> ISO     claimed 1 failed / 31 passed
periodSentence -> ISO     claimed 5 failed / 27 passed   (it PREDICTED 4; the 5th was a
                                                          control it had itself updated an
                                                          hour earlier and forgotten)
```
   **Re-run at least the `periodSentence` one.** Per the ritual: **green baseline FIRST** (assert against unmodified `e5be9fe`), then tamper, **then read the COUNT — the number of cases EXECUTED must match the baseline's.** `1 failed / 0 tests` is a build failure wearing a red-proof's clothes. Then confirm the SPECIFIC cases that reddened are the ones the tamper should hit, restore, and confirm green.

7. **ALSO LANDED AT `554f6b3`, in scope for this pass — F-8 and F-7 from your pass 21:**
   - **F-8:** the 4.16 guard's proximity excuse is replaced by **a finite allow-list of three records, pinned by SHA-256 of their normalised sentence.** The builder's argument for not narrowing the window a fourth time: every narrowing left residue (26.0% → 11.0%), and a past-tense predicate fails because the `c-generator` wording opens with "took". It claims **residue is zero by construction**, and that its normaliser is pinned from both sides — **changing a record's WORDS goes red; RE-WRAPPING the same words stays green.** Test both directions.
   - **F-7:** the both-off clause now runs **FIRST, as a candidacy control** — answering whether each fixture is a real candidate or its 0 means "never examined" rather than "correctly excused". Claimed proved reachable.

8. **NOT IN SCOPE, do not test and do not report on: RD-297** (a fifth ISO date at `backend/services/sustainability/metrics.js:72`, in server-side prose about a dead ingest). The builder filed it rather than deciding it; **it is with Kam and it is deliberately unchanged.** Finding it again is not a finding.

---

## 5. Boundaries

- **You are findings-only.** Make no change of any kind to the NexusAI tree, author no fix, file no ticket, touch no running system of theirs. Your own worktree and your own server are yours.
- **Never round a green up to "fixed."** Report what you tested, what you did not, and how deeply.
- **A test's NAME is not its coverage** — read what each fixture makes reachable, and give the case named CONTROL the most suspicion, not the least.
- Report to **`wednesday-agent@agentmail.to`** when your SUMMARY is written.

---

## PROVENANCE (every load-bearing fact, its instrument, and when it was read)

```
e5be9fe is head of rd-136-nga-defaults-s12 | git ls-remote origin rd-136-nga-defaults-s12 | 2026-09-04 10:08 AEST
554f6b3 is an ancestor of e5be9fe          | git merge-base --is-ancestor 554f6b3 e5be9fe   | 2026-09-04 10:07 AEST
554f6b3..e5be9fe touches 2 tests, 1 doc,   | git diff --stat 554f6b3..e5be9fe               | 2026-09-04 10:07 AEST
  1 gate-expectation config; no render     |
gate expectation at e5be9fe = 1448/85      | git show e5be9fe:scripts/verify-expected-counts.json | 2026-09-04 10:08 AEST
gate expectation at 554f6b3 = 1439/84      | git show 554f6b3:scripts/verify-expected-counts.json | 2026-09-04 10:08 AEST
all builder claims in section 4            | S31 STATUS mail, wednesday-agent@ inbox, 2026-09-04 10:01 AEST | read in this action
:3068 :3072 :3073 :3075 :3076 :3077 :47787 | curl -o /dev/null -w %{http_code}              | 2026-09-04 10:06 AEST
  each answered 200                        |
:3191 and :3080 answer 200; their SHAs are | curl (status only) + lsof -iTCP:LISTEN         | 2026-09-04 10:06 AEST
  UNMEASURED — :3191 = 2f3ce7d is from the |
  handover, :3080 = the builder's claim    |
54 qa-worktrees/<sha> exist (the pattern)  | git worktree list                              | 2026-09-04 10:07 AEST
```

**Unmeasured, stated as such:** whether `:3080` or `:3191` serves any particular commit; whether the builder's browser verification covered the metrics tile as well as the popover.
