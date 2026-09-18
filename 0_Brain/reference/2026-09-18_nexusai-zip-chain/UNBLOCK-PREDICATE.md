---
date: 2026-09-18
type: reference
source: S65's measured answers (this folder's README.md + its 00:34:50Z dependency measurement); Kam's instruction "let me know when the push is unblocked"
status: live
updated: 2026-09-18 — the open question is RESOLVED; the push waits on step 10 ONLY
---

# "Kam's push is unblocked" — the predicate, so it is a CHECKLIST and not a judgement

**Kam's instruction, verbatim (2026-09-18):** *"keep going and let me know when the push is unblocked"*.

**This file exists because "unblocked" is the kind of word a tired seat decides by feel.** It is
evaluated line by line at every MERGED mail and every checkpoint, **on `origin/main`, never on a
branch**. A seat that cannot tick every line does not tell him.

## THE PRECONDITION, in one sentence

> **Kam can push as soon as the minimum set is merged to main, the release version string is agreed
> (`2.2.0`), and RD-529 O-8 has landed on main. Step 11 gates the ZIP, not the image.**

**RESOLVED 2026-09-18 00:34:50Z, and it recovered a whole step of his time.** S65's chain was drawn
linear (push waits for 10 AND 11); Tuesday challenged it; S65 measured the Dockerfile and `.dockerignore`
and confirmed step 11's artefacts — `scripts/deploy-dev.sh`, `scripts/provision-customer.sh`,
`azure-marketplace/**`, `docs/MARKETPLACE_TEST_PROCEDURE.md`, `docs/REFERENCE_ARCHITECTURE.md` — are
**not shipped in the image**. So step 11 runs in parallel with his round trip.

## 🔴 SAFETY RULE — build from MAIN at the merged head, NEVER from the package branch

The package branch has not merged main since RD-470 landed. Relative to main it **re-adds the
`ADMIN_RESET_KEY` break-glass route** (`/api/setup/admin-reset`) that **Kam himself ruled removed** —
C-48, `CLARIFICATIONS.md:291-292`, his panel words 2026-09-17 08:05:14: *"Decision
nexusai-rd470-break-glass-remove: remove — Remove the route (Recommended)"*.

**An image built from the package branch would not be a regression — it would silently reverse the
principal's own decision, inside the artefact he was about to submit, with nobody positioned to notice.**
The image is opaque and "the package branch" is the obvious ref to pick when building a package. This is
a safety rule with his name on it, not a build preference.

## The wake, so this does not rest on remembering

- **`2_Project_Files/fleet/watch_nexusai_main.sh <baseline-sha> <poll-s> <max-min>`** — reads
  `origin/main` directly and **exits** when it moves. The harness re-invokes the seat on a background
  job's exit, so the exit IS the wake. **Armed 2026-09-18 ~10:3x, baseline `e0ea198a`, poll 60s, max
  180m.** Independent of every agent's liveness: a seat that dies quietly produces no merge and no mail,
  and this still reports. Both branches exercised before arming (fire rc 0 with the SHAs; quiet rc 3
  after a full minute of real polling, no false fire).
- The agents' own MERGED mails remain the primary signal. This is the backstop, not a replacement.
- **If it has expired, re-arm it from the current head.** Do not replace it with an intention to check.

## THE CHECKLIST — every line ticked, or he is not told

### The minimum set, MERGED to `origin/main`
- [ ] RD-436 + 452 + 501 + 499 **+ RD-535** — restore reopens a configured deployment to anonymous takeover
- [ ] RD-486 + RD-523 — stored Azure OpenAI key sendable to a caller-named host and to a redirect target
- [ ] RD-516 — anonymous SSRF via ai-test (same class as RD-486; one without the other half-closes it)
- [ ] RD-518 — `KEYVAULT_NAME` vs `KEY_VAULT_NAME`: Key Vault silently does nothing in every deployment
- [ ] RD-503 + 442 — SUPPORT.md's only AI-settings fix does nothing on a real deployment
- [ ] RD-464 round 3 — kept in (Kam approved it, it is built; first drop candidate if he shortens)
- [ ] The listing folds — RD-465 O-4, RD-454 O-4

### The two additions the dependency measurement turned up
- [ ] **RD-529 O-8** — the one-line placeholder wording fix in `DEPLOYMENT_GUIDE.md`, **which IS shipped
      in the image**. Ruled by Tuesday: it lands on main BEFORE the push rather than being baked in.
- [ ] **The release version string is agreed: `2.2.0`.** No prior ruling existed (C-24 and C-39 fix only
      that 2.1.1 is live/submitted), so this is Tuesday's call: a minor bump, not a patch, because the
      release carries new behaviour and new guards. **The build checker requires the image tag to EQUAL
      the package version**, so it must be settled before the push, not after. **It is baked in by the
      push, so it goes to Kam in the same message that tells him he is unblocked, labelled as Tuesday's
      call with the correction invited — that is the last moment it is free to change.**

### The telling
- [ ] Every box above ticked and **re-read on `origin/main` in the same action as writing to him**
- [ ] His push steps from 2026-09-17 23:23:47Z re-confirmed as still correct (S65 said they are)
- [ ] Told on the panel, **action first**, steps on their own lines, **the version named**, no date attached

## NOT in the predicate — gates the ZIP, runs in parallel with his push

main merged into the package branch · the RD-505 removal on that branch · the dev scripts ·
the listing folds in `azure-marketplace/**` · RD-526..RD-528 · RD-543.

## NOT in the predicate at all

RD-524, 525, 531, 537, RD-495, RD-497, RD-510, 492, 519, 471/472/475/487/457/438, lock v3, HISTORY
entries. All real, all ticketed, none deploy-blocking. **Do not let them creep into the gate** — they are
the difference between telling him today and telling him next week.
