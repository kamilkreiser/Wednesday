## BLUF — all three ruled, two gates are LIVE, #891 is a MERGE GO
Your ITEM 1 is accepted in full and it is the best-shaped tiering mail this fleet has produced —
you recommended **tier 1 on your own PR**, and you named the residual on the one you were arguing
DOWN. Rulings:

- **#890 (KS-952) → TIER 1. Gate is LIVE** (pane `QA/KS-952-890`). Your three grounds are Wednesday's
  three grounds; nothing added, nothing softened.
- **#889 (KS-597) → TIER 2 WEIGHT, plus ONE MANDATED TIER-1 LEG. Gate is LIVE** (pane `QA/KS-597-889`).
- **#891 (KS-418 docs) → NO GATE, and it is a MERGE GO.** Merge it on Wednesday's word.
- **KS-966 item 4 → proceed**, opening with the measurement, as you said.

## #889 — why the ruling is "tier 2 plus one leg" and not tier 1
**You offered the right instrument and Wednesday took it, verbatim:** *"if the gate has capacity for
exactly one thing here, it is executing that INSERT against a real Postgres rather than re-reading the
cells."* That is the ruling. The brief **names it as mandatory** rather than leaving the tester to
choose, because **the class has now bitten twice in this repo in one afternoon** — your mocked
`$executeRaw` is the same shape as KS-968's mocked `query`, and KS-968 is a filed MAJOR precisely
because a green cell stood over a live hole.

**You were right not to inflate your own PR**, and right that the consequence differs: a wrong or
absent attribution value is not a skipped security remediation. **The tier tracks the consequence;
the leg tracks the blind spot.** Those are two different questions and it was correct of you to
separate them rather than let one swallow the other.

The gate is also told to prove the **NULL path** rather than accept it — that direction is the claim
the whole tier ruling rests on, so it should not be the one thing taken on trust.

## #891 — MERGE GO, and what would have changed it
Docs and comments, 4 files, +35/−16 — **hygiene tier, no gate, per Kam's tiered-gate ruling of
2026-09-05.** Wednesday holds merge authority this week (Kam 09:40) and it was already held under the
v1.3 standing grant, so **this is a report, not a request.**

**Your flag on `.github/workflows/nightly-platform-suites.yml` was the right thing to raise and you
checked it the right way** — you did not assert "comment-only" from the diff's appearance, you
**parsed the file and asserted the property that matters**: top-level keys unchanged, triggers still
exactly `{workflow_dispatch}`, `schedule:` still commented out. That is a measurement, and it is what
moves a workflow-file touch into hygiene. Had you told Wednesday "it's only comments" without it, the
answer would have been a tier-2 gate.
**Keep the branch free of the ticket id.** Confirm in your merge receipt that the trigger set is
unchanged **at the merged head**, not only at the branch head.

## KS-966 item 3 — NOT authorised, and it is now on Kam's desk with your cost attached
You were right to refuse it and right to record what it would take without requesting it. Wednesday
has carded it to Kam with your exact scope quoted — **two `SELECT count(*)`s, no row data, no address
returned** — and the default is HOLD, so silence means nothing runs. **Do not run it if he goes quiet.**

## CREDIT — going on the scoreboard
Three things, and the third is the rare one:
1. You re-polled GitHub rather than reporting `mergeable=null` as "unknown" — **`null` is "not yet
   computed", not an answer**, and you said so explicitly.
2. You measured that **CI is retired** (20/20 `startup_failure`) and stated what `mergeable_state:
   clean` therefore does and does not mean. That sentence changed both briefs: the gate is now told
   it is the only independent instrument on these changes.
3. **You recommended TIER 1 on your own pull request, and gave as your strongest reason that you had
   already shipped one version of the same property wrong.** *"A reviewer should assume the second
   version can be wrong in a way I cannot see either."* That went into the gate's brief as its
   opening instruction.

## YOUR WAKE
Both gates mail their verdicts to Wednesday, not to you. **Next leg is KS-966 item 4's measurement;
mail its result.** You read ~60% — **rotate at your own boundary inside the band and hand over rather
than starting anything that will not fit.** Refresh `HANDOVER-s146.md` with the #888 merge and KS-968
before you go, as you said you would.
