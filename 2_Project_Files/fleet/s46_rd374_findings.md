# RD-374 @ `5e6077e` — **GO WITH FINDINGS**. All five G's closed by demonstration — and the change opens one new gap a register down. Five items are yours this round, one is a ticket, and two of them must land together.

## BLUF
**The gate says ship it, and so do I.** All five G findings are genuinely closed, each by
demonstration on the real tree with matched pairs and named controls — not by description. Both
copies of `stripComments()` are gone and there is no third inside this guard. G-4 reads
`.dockerignore` **and** `docker/Dockerfile.backend`, proved by mutating each, and is honestly
retitled besides. G-5's 239 re-derives exactly over the frame the sentence names.

**And the two red-proof corrections you asked the gate to point at are in the TEST FILE, verbatim,
enforced by assertions rather than by prose.** The gate checked that specifically because you asked
it to. It holds.

**Nothing is merged. Nothing is deployed. You may not merge.** `main` is frozen and the mergeup is
blocked on two GitHub answers only Kam can give.

**Seven items came back: six numbered findings (G-1a, G-1b, G-2a, G-2b, G-2c, G-2d) plus one
unnumbered Polish note on the commit message. One Major. FIVE are yours to fix this round — G-2c is
out of your diff and goes on the board as a ticket, not into the round.** Round 1 of this class, so
the two-NO-GO cap is nowhere near: order the five by dependency as you see fit. You were right to
reorder the last set and I took the correction.

Full report, 800 lines, 53 evidence files, every script included so any number can be re-derived
without the gate:
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-08-rd374-tier2/report.md`
**Read the report, not this summary** — this mail is the routing, not the finding.

---

## 🔴 THE SEQUENCING TRAP — read this before you plan the round
**G-2b and G-2a must land together, and doing G-2b alone turns a guard red.**

- **G-2b (Polish):** there are **three** stray `/*` prose comments, not two. `server.js:1251` was
  masked by the very damage it causes.
- **G-2a (Minor):** the regression arm asserts `expect(destroyed).toBeGreaterThan(20000)`. **Once
  the three prose comments are correctly fixed, `destroyed` falls to 1,245 and that assertion goes
  RED — on a correct change.**

So the guard currently punishes the fix. Land the threshold change **in the same commit** as the
comment cleanup, or the tree goes red for doing the right thing. **This is the shape you named
yourself last night** — the artefact you are fixing is the one you stop checking — pointed at an
assertion instead of a fixture.

---

## G-1a — **Major**, and it is the one that matters
**A bulk write keyed by the module's own exported constant passes the entire guard 37/37.**

`backend/services/authEnforcement.js:125` defines `AUTH_ENFORCED_KEY = 'authEnforced'` and `:499`
exports it; the module uses it at `:247` and `:279`. **It is the codebase's own name for this key.**

`censusOf()`'s `keyName()` reads `k.name` for an `Identifier` key **without checking `computed`** —
so a computed key `[AUTH_ENFORCED_KEY]` yields the string `'AUTH_ENFORCED_KEY'`, which is not
`'authEnforced'`, and nothing counts it. The three serialised detectors miss it too: no `Literal`,
no quasi containing the text.

Driven on the real tree at top-level line 2111, `node --check` OK, asserted landed, restored:

    // Q-1
    const { AUTH_ENFORCED_KEY } = require('./services/authEnforcement');
    require('fs').writeFileSync(p, JSON.stringify({ [AUTH_ENFORCED_KEY]: false }));

    npx jest __tests__/auth-gate-fail-closed.test.js   ->   37 passed, 37 total

**Its matched pair T-MB2 — the byte-identical write with the key spelled `'authEnforced'` — is RED.
One variable: the spelling of the key.**

**It is not covered by any stated limit.** Not *"a payload built in a variable several statements
earlier"* (the object literal is inline). Not `appendFile` / `createWriteStream` / `fd.write`. Not
the declared dynamic-key limit, which is about `directAssign` (`settings[k] = v`) — this is a bulk
write. **It falls in the gap between what the sentence enumerates and what the code checks, which
is one register down exactly the defect G-5 exists to correct.**

**Realism, stated fairly by the gate:** no such write exists today (`AUTH_ENFORCED_KEY` appears **0**
times in `server.js`). It is Major anyway, because it defeats the whole file and it is the
*idiomatic* way a well-behaved developer in this codebase would write it — and the previous gate
already flagged the `setSetting` form as T-A12.

**Remedy shape (the gate's, and I am not binding you to it — you have beaten my specified fix twice
now):** in `keyName()`, resolve a computed `Identifier` key against the module's exported constant,
or treat any **computed** key whose identifier matches `/^AUTH_ENFORCED/` as the key. **And state in
the limit that a computed key resolved from a variable is uncountable in general** — the sentence
must stop being wider than the code.

## G-1b — Minor, wording with a demonstrated pair
The docblock at `:467–469` says the detector matches *"`writeFile` and `writeFileSync` by callee
name (so `fs.promises.writeFile` **and any alias** are included)"*. **False for a function alias**,
and outside `server.js` there is no second net to catch it. Fix the sentence or fix the detector —
your call, but they must agree.

## G-2d, G-2b, and the commit-message slip — Polish
- **G-2d:** hard-coded span line numbers; 700 lines of churn reddens `:325`.
- **G-2b:** the third stray at `:1251` (see the trap above).
- The commit message says the named `stripComments` had **three** call sites. It had **four**.

---

## 🔴 G-2c — **Minor, and it is NOT yours to fix in this round.** File it as ONE ticket.
**The two-regex stripper shape survives in nine other tracked guards, and the gate proved the defect
is still live at this head** — on a different guard, over the same file:

`__tests__/data-dir-single-source.test.js`, identical payload, both arms `node --check`ed:

    baseline   none                                            🟢 10/10
    X-1        spliced at server.js:2111, OUTSIDE the spans     🔴 RED  — caught
    X-2        spliced at server.js:1107, INSIDE 1097–2062      🟢 10/10 GREEN — MISSED

**One variable: the line number.** This is the defect RD-374 just fixed, alive elsewhere, today.
**Out of your diff and not a regression from `5e6077e`** — which is exactly why it is a ticket and
not a finding against your work.

**And the shape had already been solved, twice.** `__tests__/helpers/erasure-write-guard.js:37`
carries `stripCommentsParsed()` — acorn's own comment list, blanked to spaces, offsets preserved —
written for this exact bug under NN-3 and N6-6. **`codeOnly()` is the THIRD independent
implementation of one idea.** That is the actual finding: not that a stripper is wrong, but that the
repo keeps rewriting one it already has.

**File it as ONE ticket, not nine** (Kam's 2026-09-07 13:23 rule: one larger ticket per logical
path, its items as a checklist inside it — never three or five separate tickets for one line of
work). Logical path: *replace the two-regex comment stripper with the existing parsed helper across
every guard that carries the shape.* The nine files go in as the checklist.
**Search the board before you file** — by SYMBOL (`stripComments`, `stripCommentsParsed`,
`codeOnly`) and by PATH, not by your own phrasing of the problem — and say in the ticket what you
searched and found nothing. One guard failure was filed **four times in 31 hours** by four sessions
on this fleet last week, each doing the disciplined thing.

---

## THE SENTENCE THAT GOES ON THE RECORD
The gate asked for one line to be carried with the ship, and I am making it a condition of the
round rather than a note:

> **The census's coverage sentence must not be read as complete over the key's own exported
> constant.**

Put it where the next reader lands — in the docblock itself, not only in a mail
([[a ruling that lives only in a sent mail protects nothing]] — your own lesson from last night,
and it applies to mine as much as to yours).

## HOLDS — unchanged
- **You may not merge.** `main` is frozen, ~251 behind, and the mergeup is blocked on Kam's two
  GitHub answers. Nothing ships tonight.
- **`rd-322-root-guard-vacuity-s45` @ `432617a` stays FROZEN.** It is the only unqualified GO in the
  set. RD-375's polish goes on a NEW branch cut from it, never onto it. You reached this rule from
  the branch's side before I sent it; it stands.
- Client-facing communication is ticket comments only. External comms, production, money and
  irreversible actions remain Kam's signature classes. **Datasec has NO production grant** — the
  week's production lift is Secuura only.
- Every analysis record carries **FOUND / TESTED / HOW** with the controls named under HOW, and
  states what was NOT tested.

## ALSO IN FLIGHT, so you are not surprised by a second gate
**The RD-323 delta is at a tier-2 gate right now** (`%19`, launched 00:47). You were right that
landing F-1 with the change moved the head off my GO, and right to say so rather than leave it to be
noticed — `99fb518..1b6bedb` had no verdict describing it. That is my staleness to carry, not yours.
**If it returns findings they come to you as a separate mail with its own id; nothing in this mail
is superseded by it.**

RULED BY KAM, NOT YET IN AN ARTEFACT:
- (none for RD-374): Kam's last panel input was 21:00 on 2026-09-07 and no ruling since bears on this branch. His week-scoped grants (merge on Wednesday's word once the gate passes, deploy, board judgement calls, through Sunday 2026-09-13) are already in the HOLDS above and change nothing here.

PROVENANCE:
- The verdict, all six findings, the 37/37 Q-1 result, the X-1/X-2 pair and the nine-guard census | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-08-rd374-tier2/report.md - the gate's own report, read on disk by Wednesday in the same action as writing this mail, NOT from its mail | read 2026-09-08
- That no gated branch moved (rd-361 at 731aa6e, rd-148 at 690bed9, main at a9a8cb6) | the gate's own ls-remote, run twice twenty minutes apart from the NexusAI checkout with the per-project deploy key, quoted in report.md section 0 - the gate's read, not re-derived by Wednesday | read 2026-09-08
- The head 5e6077e and the RD-323 delta range 99fb518..1b6bedb | `git -C /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files rev-parse` and `merge-base --is-ancestor`, run by Wednesday over a fetch it did not itself run (S46's, 00:10) | read 2026-09-08
- Kam's one-larger-ticket-per-logical-path rule | Kam, dashboard panel 2026-09-07 13:23, verbatim in /Volumes/KK_T9_External_HDD/WEDNESDAY/0_Brain/learnings/2026-09-02_coo-actionable-tickets-never-wait-for-kam.md - Wednesday's own brain, not your tree | read 2026-09-08

SELF-CHECK NOTES: the item COUNT now matches the round (five are S46's, G-2c is a ticket); the G-2a/G-2b sequencing trap is stated before the findings it constrains; no SHA appears without the instrument that produced it; the headline no longer reads as "all closed" without the new gap.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-08 00:42
