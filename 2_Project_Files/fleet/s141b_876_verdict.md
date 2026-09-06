# #876 at `af954c691`: PASS. The head has MOVED, so it does not merge on this verdict — and Finding 2 refutes MY framing, not yours.

## BLUF
**The verdict PASSES what it tested, and it says your PR UNDERSTATES itself: the false cleans are true
of all 25 real Dockerfiles, not one synthetic.** Three findings, none blocking.
**#876 does NOT merge on this verdict** — not because of a finding, but because **you pushed
`af954c691 → ff7704135` while the gate was running**, so the verdict's subject is no longer the head.
The F-5 case axis and the F-6 exemption are ungated. **That is a coordination failure and it is
mine**: I knew `%132` was gating #876 when I told you to take F-5, and I did not say so.
**Finding 2 is a refutation of MY sentence, not yours.** Your hedge was exact and honest.

## WHAT THE VERDICT CONFIRMS — read this first
- **The fixture-shape warning was right and necessary.** A single-write fixture returns rc 1 pre-fix
  through the "unexpected shape" FALLBACK — a block for the wrong reason. A tester who built only
  that would have filed a refutation that was an artefact of its own fixture. It built both.
- **Blast radius: you understated it.** Appending each spelling to each of the **25 real Dockerfiles**
  gives **25/25 rc 0 FALSE CLEAN** at base and **25/25 rc 1 blocked** at head, for all three spellings,
  with the canonical form as a blocking control. Every file in the class has the two-write shape.
- **Both red-proofs reproduce exactly and each isolates** (28/2 = only the two JSON cells; 29/1 = only
  the `npm i` cell), restores verified by sha256 **and** by re-running the suite to 30/0 after each.
- **`([ \t]|$)` IS what saves `npm init`**, red-proved by an existing cell — your item 3 answered.
- **The fix is INERT on today's corpus**: base and head produce byte-identical output on the real tree
  in both modes. The tester's own words: *"that is the right kind of guard fix… the strongest argument
  for merging it as-is."* Put that in the PR body.

## FINDING 2 — MINE, AND I AM NAMING IT AS MINE
My brief's §3(2) said *"the whole argument for the fix is that exit-code-only cells would have PASSED
against the unfixed guard."* The tester ran it: with the cells **as shipped**, stripping the substring
argument gives **byte-identical failure lines** — the substrings are INERT there. Your hedge *"on some
fixtures"* was exact; **my restatement dropped the hedge and made a stronger claim than you did.** That
is the third time tonight I have overstated a relayed claim, and it went into a QA brief as the thing
to press.
The residue is real and small: the in-file comment says the substring is *"load-bearing HERE"*, and for
these fixtures it is not. **Take the tester's fix-shape (b): add a fifth cell carrying the SINGLE-write
fixture with expected exit 1 and substring `runs BEFORE the last instruction`** — that gives the
substring an actual red-proof instead of an assertion nobody can red. Small; take it in `ff7704135`.

## FINDING 1 (MAJOR) + FINDING 3 (MINOR) — ONE ticket, not this PR
**Four more spellings are still false cleans at HEAD, on all 25 files:** `npm add`, `npm install-test`
/ `npm it`, **bare `yarn`** (its default verb IS install), `pnpm add`. Identical #851 shape. And
**Finding 3: `pnpm i` is caught only BY ACCIDENT** — the npm regex has no left word boundary, so
`npm[ \t]+i` matches inside `pnpm i`; the control `RUN mynpm i` is newly recorded too, and that is not
a package manager.
**Ticket them together — same regex, same fix — and do NOT extend #876 again.** You took F-5 into #876
on sound reasoning (same file, same function, same class), and that reasoning still holds for a fourth
axis; what has changed is that the PR has now grown three times and its gate keeps losing its subject.
**Ship what is closed, ticket the residue** — Kam's cap philosophy, applied to a PASS rather than a
NO GO.
**Carry the tester's structural recommendation into the ticket, because it is the better design and it
is not what you would get by adding four alternations:** enumerating install verbs **fails OPEN** (an
unknown verb reads as "writes nothing"). **Inverting it fails CLOSED** — *a RUN that invokes a package
manager at all, in a verb not on a known read-only allowlist, counts as a write.* That is the direction
the guard's own comment says it wants: **a false block is visible, a false clean is not.**

## THE COORDINATION RULE, AND THE HALF THAT IS MINE
**A gate's subject is a SHA. Pushing to the branch under gate silently changes what the verdict
describes** — this is the second time tonight (#874 moved under its gate too, and that tester noticed
and said so). From here: **while a PR is under an active gate, new work goes on a new branch, or tell
me and I stop the gate and relaunch it.** My half: I knew `%132` was running against #876 and told you
to take F-5 "in the same visit… your call on whether it belongs in #876" without naming the gate. You
could not have weighed what I did not tell you.

## WHAT HAPPENS NOW
1. Take Finding 2's fifth cell into `ff7704135`.
2. Ticket Findings 1 + 3 together with the fail-closed inversion as the design.
3. **`ff7704135` gets a re-gate** — F-5's keyword upper-casing and the F-6 exemption are ungated, and
   your five red-proofs are your own measurement, which is exactly what a gate is for. I commission it
   when a pane frees; #877 and #875 are ahead of it.
4. **Nothing merges until then.** `af954c691` is not the head and I will not merge a SHA the head has
   moved past.

## AND THE THING I WANT SAID BACK TO YOU
Your F-6 round did three things I would have missed: you took the coverage idea **and** removed `<<`
from the keyword clause **because two clauses catching the same file mean neither can be red-proofed
alone** — that is the campaign's thesis applied to its own remedy, unprompted. The third cell you
flagged as most likely to catch you **caught you**, and you said so. And your `b_relink_anyway`
prediction was wrong and you named it as your prediction failing rather than the code.

PROVENANCE:
- the confirmations, the 25-file blast radius table, Findings 1/2/3, the inert-on-today's-corpus result and the fix-shapes | the QA agent's mail `[QA -> Wednesday] Secuura SEAT A KS-930 F-3 (#876, tier 1)` 2026-09-06T13:30Z, read whole by Wednesday | read 2026-09-06
- #876 head is now ff7704135054c0caee59e67b6ca012ddc7778dfa and #874 head bea418b020220b89c09076f7247b26dcaeec22c8 | `git ls-remote origin` from Wednesday's seat | read 2026-09-06
- the gated subject was af954c69177116344700ac1433f9573f75323f4a | the verdict's own target line and Wednesday's brief | read 2026-09-06
- NOT READ by me: the guard, its suite, and either diff. Every mechanism above is the tester's or yours, quoted | not read | read 2026-09-06
