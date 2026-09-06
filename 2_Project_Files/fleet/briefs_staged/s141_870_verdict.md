## BLUF
**#867 is merged and verified here — develop `a8aa723a0`, base held, `094c88795` contained, control
fires. And #870 is PASS WITH FINDINGS but it does NOT merge yet: F-1 is a FALSE CLEAN in the guard
itself, and a guard whose whole purpose is to make a convention structural cannot ship able to
report "1 of 1 clean" over a corpus of 2. Fix F-1, F-2, F-4 and F-5 in this PR; F-3, F-6 and F-7
become one ticket. This is a fix round after a PASS — the cap is untouched.**

## #867 verified here
```
develop a8aa723a0   parents a821bd0aa + 094c88795   (base held)
094c88795 contained: rc 0      control b0526599f: rc 1
```
Read from objects at my seat. KS-913 → TND as you have it.

## #870 — what held, first, because it is most of the report
All eleven brief claims VERIFIED under independent re-derivation: both red-proofs re-derived outside
your suite with the cross-check that neither fixture trips both clauses; the suite shown to notice
an over-firing guard in **both** clauses (12 failed and 2 failed under the two over-fire tampers);
**leg 13 driven end-to-end against the tester's own bare remote — a good corpus pushes, a corpus
with one deleted re-link is REFUSED and the remote holds no refs**; the fixture fix confirmed not to
have weakened the guard (36/0 at BOTH SHAs, and the complete set of deletions in the whole PR is the
twelve `N/12` label strings); the class confirmed as 25 including `connectors/whatsapp-bot`; the
derived 4/21 count confirmed; report-only confirmed in both directions.

**And your timing cell is the highest-value assertion in the suite.** A three-way tamper showed
which of the two empty-corpus mechanisms is load-bearing — the `[ -z "$ALL_DOCKERFILES" ]` guard —
and that removing both reproduces your second-draft bug and fires the TIMING assertion verbatim.
`</dev/null` is redundant belt whose removal is undetectable. That is a cell that earns its place.

## F-1 — MAJOR, FALSE CLEAN, and it is why this does not merge tonight
`check-shared-relink.sh:91` selects the class with a **case-sensitive** grep, and Dockerfile
instruction keywords are case-insensitive by specification. So a file writing
`Copy --from=shared-builder` — an ordinary authoring slip, reproduced twice by the tester, including
first-letter-capitalised — **silently leaves the corpus**, and the guard prints `OK — 1 Dockerfile(s)
… 1 of 1 clean` over a corpus of two where the second is broken in both clauses. **It survives
`SHARED_RELINK_STRICT=1`, the strongest mode you offer.**

The part that makes it worse than an ordinary miss: **the vacuous-green protection at line 94 only
fires when the class is ENTIRELY empty**, so a partial miss is invisible — and the derived count
shrinks in step with it, so no figure looks wrong. **This is KS-921's own failure recurring with the
guard installed and green**, which is precisely the thing the ticket exists to prevent.
Fix: `-i` on the class grep, **plus** the cross-check the tester named — compare the derived class
size against `grep -ril 'shared-builder'` over the same file set and fail loudly if they disagree.
Regression cell: a two-file corpus, one lowercase and broken, asserting rc=1 and that the broken
file is NAMED.

## F-2 — MAJOR, FALSE BLOCK, and the message is factually wrong about the file
`:176` records only the FIRST `USER` per stage, so the legitimate root → link → drop-privileges
shape is rejected with "the re-link runs AFTER `USER` — it is attempted without the privileges to
create it". **The link in that file is created WITH privileges.** Your oracle is right and its
implementation inverts it: the test is the **effective** USER at the re-link's ordinal, not the
first one seen. Fix: track the last `USER` before the re-link and fail only if that one is non-root.

## F-4 — MAJOR, FALSE BLOCK, and the likeliest to be written by a real author
`:172` requires the literal `ln -s /shared node_modules/@secuura/shared`. Both
`ln -sf /shared node_modules/@secuura/shared` (the idiomatic idempotent form) and
`ln -s /shared /app/node_modules/@secuura/shared` (natural under `WORKDIR /app`) create the
identical symlink and are rejected as "final stage has NO …". **Clause A blocks today**, so this is
live friction on every author who writes `-sf`. Fix: allow `-s` combined with other short flags, and
allow an absolute destination matching `(^|/)node_modules/@secuura/shared$`.

## F-5 — take it now, it is the same defect as F-1 one field over
Docker resolves stage names case-insensitively; `pruned_by_name` keys on the literal. `AS Builder` +
`--from=builder` yields a false B warning today and a **false BLOCK the moment STRICT becomes the
default, which this PR states is the plan.** Cheap, and it belongs with F-1.

## F-3, F-6, F-7 → ONE ticket, not this PR
F-3's five legitimate shapes (BuildKit heredoc, an nginx final stage with no `node_modules`, the
non-final-stage write, `npm i` shorthand, the JSON `COPY` form) and the two parser edges. **Live
exposure today is none** — all seven frontend Dockerfiles use nginx/alpine final stages, none
consumes shared-builder, and no frontend source imports `@secuura/shared` (0 files, measured). Two
things go in the ticket verbatim:
1. **For the nginx case the guard offers no route forward** — a static-serving final stage cannot be
   made green except by adding a pointless `node_modules` write. A guard with no green path for a
   legitimate shape is a design question, not a bug, and it is the ticket's first item.
2. **That `A_FAIL` branch is pinned by NO test** — neutering it leaves the suite at 18/18, while the
   guard's other three `A_FAIL` messages are pinned. **A branch no cell can red is a check that
   cannot fail**, and it is the third instance of that family on your board tonight (KS-926, KS-927,
   KS-928 — this makes four mechanisms).

## Two instrument corrections in the tester's report, both worth reading
Its first tamper attempt used a double-quoted perl program, so the shell expanded the variable to
empty, **neither tamper landed, and both runs still reported "18 passed"** — caught only because a
verification grep printed nothing. Every tamper in the final report now carries an explicit sha256
landing assertion. And it first reported the base suite at 23/10, which was `git archive` producing
a tree with no `.git` where the fixture needs a real repo; re-measured at 36/0. **Both are the same
family as your own three corrections tonight.** Adopt the landing assertion: a tamper does not count
until its subject's hash has been shown to have changed.

## Sequencing
1. **The #870 fix round now** — F-1, F-2, F-4, F-5, each red-proofed with the tester's own repro
   shapes, and the F-1 regression cell named above. Then the ticket for F-3/F-6/F-7.
2. **#868's fix round is with a tier-1 tester as we speak** — its verdict comes to me.
3. Then **KS-920**. **KS-926 stays behind it**, and its campaign now opens with the four-mechanism
   family, this A_FAIL branch included.

## Standing
`develop` `a8aa723a0` as of my read just now — you moved it, so re-read it in the same action as any
use. Seat B is live on KS-720 and has #869's fix round queued for its re-gate. Kam's card is open at
default HOLD. Nothing deploys; the demo box stays pinned at `db1848abf`.

-- Wednesday
