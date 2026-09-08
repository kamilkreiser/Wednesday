# GO — merge #906. And Kam has ruled THREE cards, two of which change your holds.

## BLUF
**#906 is GO. Merge it.** The gate returned GO-WITH-FINDINGS and my completion check passes on
all six requirements. **Then file ONE ticket for the four residual findings** (Kam's aggregation
rule — one logical path), and act on **three Kam rulings** below, two of which move holds you
have been respecting all session.

## Recommendation, in order
1. **Merge #906** (`9f9a2a788` → `develop`). It closes a LIVE red on the trunk.
2. **File one ticket** for F1–F4 before this class is called closed.
3. **Kam's rulings** — the Platform S hold is LIFTED, and there is unarchiving to do.

---

## MY COMPLETION CHECK — delivered against what I commissioned, not a re-run of the gate

| I asked for | Delivered |
|---|---|
| The trunk-was-red claim reproduced **with its control** | ✅ and stronger than asked — the control SHA is the merge's own first parent, and it **planted a violation there** rather than trusting the green |
| The red-proof **re-run**, byte-identical restore confirmed by hash | ✅ 28/0 → 18/10 → 28/0, md5 both sides, plus `cmp` and a clean `git status` |
| The new suite shown to **FAIL** when the guarded thing breaks | ✅ far past the ask — **7 independent tampers, 2 controls**, and it proved the suite BLOCKS the runner rather than merely appearing in the glob |
| The 16 pre-existing base cells unaffected | ✅ in all three configurations |
| Tier precondition (no service/FE/spec/migration/auth) | ✅ with the grep shown |
| Anything unreproducible named as such | ✅ nine items under NOT TESTED |

**And the two gaps you stated: my brief said a stated gap is not automatically an acceptable
one. The gate treated them exactly right** — the platform suites were judged acceptable *with
evidence* (repo policy plus a byte-identical TypeScript emit at base and head, with a control),
and the deps-missing path it **measured itself**, which is how it became F1.

**Delivered == commissioned.** Your evidence held under independent re-derivation, including the
claim the whole shape of the change rests on.

## THE MERGE — mine to give under Kam's week-scoped grant, and I am giving it
F1 and F2 are MAJOR and neither is a regression: F1 is your own stated gap #2 now measured, and
F2 is the repo's standing working-tree convention, not something you introduced. **Neither
justifies withholding a change that fixes a red that is on the trunk right now.** Merge.

**Round 1 of 2 is now spent on this class and it closed. The cap is not near.**

## THE ONE TICKET — F1–F4, one logical path
All four are the same question — *what the new gate does and does not catch* — so they are ONE
ticket with four items, not four tickets (Kam, 2026-09-06: one larger ticket per logical path).

- **F1 (MAJOR)** — fails OPEN when a gated package's deps are absent: SKIP, exit 0, the red is
  pushed. Measured against the real akto tree on the real instance-6 red, with controls both
  sides. **This is the path by which instance 6 itself could still have slipped through.**
- **F2 (MAJOR)** — the gate reads the WORKING TREE, not the commits being pushed. Proven on a
  bare-remote fixture: red at HEAD, fix uncommitted, red lands at origin. Note in the ticket that
  the gate's own printed remedy is what creates the divergence.
- **F3 (MINOR)** — the "gate script missing → REFUSED" branch is correct but has no cell, and it
  is the one branch whose entire purpose is to fail closed.
- **F4 (POLISH)** — `grep -qx "$full"` treats a path as a regex; `-qxF` fixes it. Label only.
- **Robustness note, no finding:** `< /dev/null` on line 150 would close the stdin-inheritance
  hazard the fixtures cannot detect.

---

# RULED BY KAM, NOT YET IN AN ARTEFACT

Three rulings, 14:00 today. **Each must land in the artefact named, and your receipt says where.**

- **`secuura-ks963-getuserbyid-swallows` → `rethrow`.** *"Apply the KS-253 pattern to
  getUserById — rethrow instead of swallowing. The design question is already settled by the
  sibling; this is the missed function."*
  → **KS-963 is now ACTIONABLE.** It is no longer bounced and the "do not fix yet" line on it is
  superseded by this ruling. Put the ruling on the ticket, then build it. **Your read-not-run
  point stands: write the measuring cell in `ks949-platform-admin-seed-identity.test.ts` as part
  of the round**, so loud-vs-silent becomes a measurement rather than staying a code read.
- **`secuura-platform-s-count-was-wrong-when-you-ruled` → `all18`.** He is archiving all 18
  PS-Done, not the fifteen he was originally shown. → **THE PLATFORM S HOLD IS LIFTED.** Archive
  the remaining three as well. Record on the board that the correction was ours, not his.
- **`secuura-61-archived-while-still-open` → `three`.** *"Unarchive only the THREE In Progress."*
  → **Unarchive KS-174, KS-796 and KS-802** — nothing else of the 61. Two are children of
  KS-781 (Deployed to UAT) and may be finished in fact; say so on them rather than reopening a
  question nobody asked.

## STILL HELD
Tested-Not-Deployed — unchanged, and your measurement says it currently costs nothing.
Production, money, external comms to Peter or Stuart, irreversible actions: all still Kam's.
Nothing on the demo box; you hold no production grant this seat.

## ORDER
Merge #906 → the one ticket → the three rulings → then back to the P2 In Review queue.
