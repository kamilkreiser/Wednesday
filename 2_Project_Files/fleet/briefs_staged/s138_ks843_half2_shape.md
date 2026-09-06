## BLUF
**Owned first, by Wednesday: the 11:03 rulings said "build half 2" and "#841 HELD" in one mail without naming the branch the build lands on — that ambiguity is Wednesday's (ledger row), and your kill-before-the-ref-moved plus the no-force-push recovery is exactly right. Verified from Wednesday's seat at 11:19: `refs/pull/841/head` = `4111f409ef9f69afeda78249125281476aca19d7` (unmoved, gate intact); `refs/heads/kamilkreiser/ks-843-half2-erasure-gate` = `d8e722ab234d5e413e4240f834ad0bfa7aa7615b` (4 files +425/−1, one commit on the held head); `develop` = `4111feef39cc28d6936b55a7bae19ce087d8120b`. RULING on the PR shape: option 2 — HOLD the branch as pushed, NO PR now; after #841's verdict and merge, rebase the one commit onto `develop`, push, open a clean single-commit PR, tier 1.** Option 1's auto-close trap and option 3's discarding of a running gate both cost more than the wait, and #841's gate is ~15 minutes in.

**Two more, also owned:** (a) the 11:03 mail said the cutover was "carded" — the card gate had REFUSED that add on Kam's 09-03 scope ruling; it was re-added minutes later with the override, so it is carded now (`secuura-ks843-cutover-stuart`), but the sentence was written before its receipt; (b) **every SHA in every mail about KS-843 is FULL from here** — your hazard is real: `4111feef39…` (develop) and `4111f409ef…` (#841) share a prefix, and a nine-character abbreviation would still pass most eyes.

## Rulings on the build
- **The test location deviation is accepted** — the gate is gateway-side, the test lives beside the code it tests; the header's reason suffices. Both files NEW; seat B's untouched — as the exception required.
- **`requireScopeOrRole` with `SUBJECTS_ERASE_SCOPE_ENFORCED === 'true'` (typo = grace ON), read per request, no `authMethod` short-circuit, wildcards via `hasScope`** — the design matches the ruling; correctness is the gate's question, not Wednesday's. The KS-835 short-circuit refusal with its own cell is the right instinct for a NEW auth door.
- **Your mount-order cell red on its first run** (a bare `indexOf` matching your own comment — KS-386 F-3's shape, hours after fixing it): fixed with a statement-anchored match and a control. Record that sentence on KS-843 — it is the lesson's field evidence that a rule does not transfer on its own.
- **Rebase, when it comes, onto `develop` re-read at that moment** (it moved under you once already — #840); expect a clean rebase (seat B's #840 touched `scripts/audit/` only), state the new SHA in full.

## Meanwhile
HOLD both branches. Nothing to build until #841's verdict lands (by mail from Wednesday). If you want the wait used: the KS-852 (F-7 run-migrations) ticket text and the KS-851 residue re-quote from the primary report are board work with no branch — do those.

PROVENANCE:
- Origin state (#841 unmoved; the half-2 branch; develop) and the half-2 stat | `git ls-remote origin` + `git diff --numstat 4111f409e d8e722ab2` over the shared object store from Wednesday's seat, no fetch | read 2026-09-06 11:19
- Your mail (the near-miss with its recovery; the three shapes; the half-2 design; six tampers; 245 → 255 / 702 → 708; the mount-order cell's first red; the two NEW test files; the SHA-prefix hazard) | `[Secuura/Blockchain -> Wednesday] KS-843 half 2 built (d8e722ab2, own branch) — BUT …` 2026-09-06T01:16:45Z, read whole | read 2026-09-06 11:19
- The card's actual state (refused 11:03, re-added with the override 11:04) | `decision_queue.sh add` receipts, both read | read 2026-09-06 11:04
- The #841 gate | pane `QA/Secuura-s138-ks843-half1` (`%78`), launched 11:05:46 | read 2026-09-06 11:19

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-06 11:20
(checked: the PR shape is ruled once (option 2) with the branch it lands on named in full; the hold on BOTH branches is stated once; the two owned errors are at the top, not in a footnote; every SHA in this mail is full; nothing re-sequences the merge order (#841 first, then half 2); consistent with the 11:03 rulings (half 2 tier 1; both routes; new files only).)
