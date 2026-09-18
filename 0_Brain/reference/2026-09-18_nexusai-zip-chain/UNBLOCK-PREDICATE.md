---
date: 2026-09-18
type: reference
source: derived from S65's measured chain (this folder's README.md); Kam's instruction "let me know when the push is unblocked"
status: live
---

# "Kam's push is unblocked" — the predicate, so it is a CHECKLIST and not a judgement

**Kam's instruction, verbatim (2026-09-18):** *"keep going and let me know when the push is unblocked"*.

**This file exists because "unblocked" is the kind of word a tired seat decides by feel.** It is
evaluated against the list below, item by item, at every MERGED mail and every checkpoint. A seat that
cannot tick every line does not tell him.

## The wake, so this does not rest on remembering

- **`2_Project_Files/fleet/watch_nexusai_main.sh`** — reads `origin/main` directly and **exits** when it
  moves. The harness re-invokes the seat on a background job's exit, so the exit IS the wake. It is
  independent of every agent's liveness: a seat that dies quietly produces no merge and no mail, and
  this still reports. Both branches exercised before arming (fire: rc 0 with the SHAs; quiet: rc 3
  after a full minute of real polling, no false fire).
- The agents' own MERGED mails remain the primary signal. This is the backstop, not a replacement.

## ⚠ THE OPEN QUESTION THAT COULD UNBLOCK HIM EARLIER — ask before using the strict reading

S65's table is LINEAR: step 12 (his push) "cannot start until 10–11". **But step 11 is the
release-gate preconditions — main merged into the package branch, the dev scripts, the listing folds,
RD-526..529 — and none of those change the IMAGE he pushes.** The image is built from main.

**So there are two readings, and they differ by a whole round trip of his time:**
- **STRICT (S65's table as written):** push waits for 10 AND 11.
- **LOOSE (and possibly correct):** the push needs only **10** — the minimum-set merges on main. Step 11
  is package/template work that gates the **ZIP**, not the image, and can run in parallel with his push.

**Asked of S65 2026-09-18 ~10:3x. Until it answers, use the STRICT reading when TELLING him**
(never tell him he is unblocked when he is not), **but do not plan as though strict is settled** — if
loose is right, he pushes a full step earlier and step 11 overlaps his round trip.

## THE CHECKLIST — every line ticked, or he is not told

### Step 10 — the minimum set MERGED to main (each verified on `origin/main`, not on a branch)
- [ ] RD-436 + 452 + 501 + 499 **+ RD-535** — restore reopens a configured deployment to anonymous takeover
- [ ] RD-486 + RD-523 — stored Azure OpenAI key sendable to a caller-named host and to a redirect target
- [ ] RD-516 — anonymous SSRF via ai-test (same class as RD-486; one without the other half-closes it)
- [ ] RD-518 — `KEYVAULT_NAME` vs `KEY_VAULT_NAME`: Key Vault silently does nothing in every deployment
- [ ] RD-503 + 442 — SUPPORT.md's only AI-settings fix does nothing on a real deployment
- [ ] RD-464 round 3 — kept in (Kam approved it, it is built; first drop candidate if he shortens)
- [ ] The listing folds — RD-465 O-4, RD-454 O-4

### Step 11 — release-gate preconditions (gates the ZIP; **may or may not gate the push** — see above)
- [ ] main merged into the package branch
- [ ] RD-505 removal merged on the package branch
- [ ] `scripts/deploy-dev.sh` and `scripts/provision-customer.sh` stop passing the removed registry parameters
- [ ] RD-526..RD-529 fixed

### The telling
- [ ] Every applicable box above ticked and **re-read on `origin/main` in the same action as writing to him**
- [ ] His push steps from 2026-09-17 23:23:47Z re-confirmed as still correct (S65 said they are; re-ask if main moved a lot)
- [ ] Told on the panel, **action first**, with the steps on their own lines and no date attached to what follows

## What is NOT in the predicate

RD-524, 525, 531, 537, RD-495, RD-497, RD-510, 492, 519, 471/472/475/487/457/438, lock v3, HISTORY
entries. All real, all ticketed, none deploy-blocking. **Do not let them creep into the gate** — they
are the difference between telling him today and telling him next week.
