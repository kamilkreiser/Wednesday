# QA GATE — Secuura #892 ROUND 4 @ `1e31c80b9`, TIER 2 (through-code). **THERE IS NO ROUND 5.**

**Kam authorised this round himself** (`secuura-892-round3-nogo-blocker-still-open` => `round4`,
2026-09-07 20:55) after the two-NO-GO cap was already spent once. **A NO GO here goes back to Kam —
it does not ship, and it does not become a round 5.** Say that verdict plainly on the first line.

**Tier 2 is rounds 2 and 3's call, carried, not re-decided.** The severity ceiling is round 2's, and
it stands: *"coverage that asserts the wrong thing while looking healthy"* is worse than coverage
that does not run, in a repo with no CI where these suites are the only instrument.

## 1. Target
- **Head `1e31c80b9`.** Change set from the **PR files API**; resolve the merge base yourself.
- **Scope is F1-A and F1-B ONLY.** F2-A is filed as **KS-977** and is OUT. F1-C is a comment on
  **KS-973** and is OUT. The `ruff` auto-fix observation is OUT.
- `origin/develop` is at **`6a7a7824e`** (unmoved since #889 and #893 merged). **#892 is not merged.**

## 2. 🔴 THE BINDING CONDITION — this is why Kam granted a fourth round
Round 3's tester established that **every cell pinned the quarantine FUNCTION and nothing pinned the
CALL**: it neutered the call site and got **42 of 42 green with round 2's defect fully restored.**
It stated it would not accept a round 4 without a cell that fails when the call disappears.

**The builder claims that cell exists and reds.** Verbatim: *"with the drift-arm call to
`quarantineManifest` removed, the new call-site cell goes RED — 10 cells ran, exactly 1 failed, and
it is `DRIFT call site: provisionActors quarantined the stale manifest`."*

**VERIFY THAT SPECIFICALLY, and verify the IDENTITY of the failing cell, not just the count.** A
1-of-10 that reds the wrong cell is not this condition being met.

## 3. THE THREE RED-PROOFS — and the distinction that decides whether they count
Claimed, each restored byte-identical:

| tamper | claimed |
|---|---|
| drift-arm call removed | 1 failed / 9 passed — **the binding one** |
| catch-arm call removed | 3 failed / 7 passed — the round-3 state |
| quarantine on REFUSAL too | 1 failed / 9 passed — **over-reach, a DIFFERENT cell** |

**The builder's own qualifying claim, and it is the one to check hardest: *"All 10 ran under every
tamper, so each reddened by EXECUTING rather than by failing to build."*** That distinction is real
and it is the builder's own — it discarded a fourth red-proof on #889 tonight for failing it.
**A cell that reds because the file no longer compiles proves nothing about the guard.** Confirm the
executed-cell count under each tamper, not just the failure count.

**The third tamper is the interesting one.** The builder deliberately does NOT quarantine on the
REFUSED arm — its reason: a refused target is fatal, the suite never runs, provisioning never
started, so nothing was superseded, and quarantining there would **destroy a VALID manifest for an
unrelated reason.** **That exclusion has its own cell.** Judge whether the reasoning holds and
whether the cell actually pins it.

## 4. F1-A — the banner, and what changed about its claim
Round 3's banner **PREDICTED** what the suite would run as, and was false on the throw arm. The
builder's fix: the catch now quarantines **before** composing the banner, and **the banner reports
what was DONE to the manifest rather than predicting what the suite will use.**

Its stated principle: *"A prediction can be wrong while staying green; a report of an action can be
pinned to that action."* **Test it.** Drive the throw arm with a stale
`generated/actors.json` planted and confirm (a) the file is gone, (b) the banner's text is true of
what happened, and (c) **a clean-tree control at the same closed port**, so "absent" cannot pass by
the file never having existed.

## 5. What the builder says it did NOT use, and you should not either
The drift cell drives the real entry point against a **LOCAL STUB** that accepts registrations and
returns OWNER for everyone. **No real stack, no real accounts** — because the sibling suite already
creates five per run against `:6882` (**KS-973 item 3**) and this must not add to that. Throw cells
use a closed port.

**`:6882` holds UNTRUSTED DATA and the shared dev stack is STALE BY DESIGN.** Do not provision
against either. If you build a database, **confirm each migration BY NAME** — `run-migrations.sh`
reports `applied=N failed=0` for migrations it SKIPPED.

**`ks597-qa-pg` (127.0.0.1:6499) belongs to #889's integration suite and is the builder's to tear
down.** Leave it alone.

## 6. Bounds and report
Findings-only, **never fix**. **NO CI** — you are the only independent instrument, so type-checking
the changed files is yours or nobody's. **Say what each cell MOCKS.** **Never write into the
builder's checkout** — work in your own clone. **Never delete — quarantine.**
**Search the board before filing, BOTH ways:** exact (symbol / path / error string) to decide and
the fuzzy one to discover — the fuzzy search is what found KS-808 tonight. State what you searched
and what each returned, with a control that returns non-zero.

**GO / GO-with-findings / NO GO on the first line**, and **say plainly whether the BLOCKER is
closed.** The binding condition gets its **own heading**. **NOT-TESTED at equal prominence**, and
**record what was FOUND, what was TESTED, and HOW — including the controls** (Kam, 2026-09-07 18:56).
Mail `wednesday-agent@agentmail.to`, subject
`[QA -> Wednesday] Secuura KS-969 / #892 round 4 (tier 2)`.

## 7. PROVENANCE
- Head `1e31c80b9`, the three red-proof counts, the failing cell's name, the executed-cell claim, the REFUSED-arm exclusion and its reasoning | the Secuura seat's mail to `wednesday-agent@`, 2026-09-07T11:10:47Z, read whole in this action — **the builder's claims, not re-derived by Wednesday** | read 2026-09-07
- The binding condition and the 42/42 finding | round 3's verdict, `wednesday-agent@` 2026-09-07T10:49:17Z, read whole | read 2026-09-07
- Kam's authorisation for this round and the no-round-5 limit | `decision_queue.sh show secuura-892-round3-nogo-blocker-still-open`, ruled `round4` @ 2026-09-07T20:56:40 | read 2026-09-07
- Tier 2 and the severity ceiling | rounds 2 and 3's own verdicts — **the gates' call, carried, not re-decided here** | read 2026-09-07
- `origin/develop` at `6a7a7824e` | the builder's merge receipt; **Wednesday holds no Secuura identity and has not re-derived it** | not read by Wednesday
