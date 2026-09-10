# DRAFT — reply to Peter on PR #952 (KS-1016, Schemathesis resolves its own slot). **KAM SENDS THIS. Not sent by any agent.**

Review at head `26c4f4d4d`, 2026-09-11 08:33–09:07 AEST. Nothing approved, commented or touched on the PR.

---

Peter — reviewed #952. **No blockers.** It does what the body says, and your offline evidence reproduces exactly: 1737 of 1737 passing at 96.44% coverage, identically in a clean shell and with `SECUURA_STACK_SLOT=3` exported. Four things worth your time, none of them blocking the code.

**1. The ticket's own subject has no live evidence at a named SHA.** The anchoring-leg runs (slot 3 at 07:56Z, slot 4 at 08:33Z) carry no SHA and predate `77af57290`, and the SHA-named `pr` series never reaches the anchoring leg. `src/slot.py` changed after that window — its docstrings record two fixes found on the first live run — and CI's green Schemathesis job reached none of this code (it ran with an explicit `--base-url` and printed `MANIFEST NOT PUBLISHED`). **One `python3 scripts/run.py integration` at `26c4f4d4d` on slot 2, 3 or 4, added to the Test Evidence block, closes it.**

**2. The merge-order line in the PR body is wrong, and the KS-1016 ticket is right.** #952 is not independent of #896:
- They conflict in both QA HTML docs (`API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` and `QA_Tool_Cheat_Sheet_Secuura_API_Testing.html`). **Keeping both sides publishes a contradiction** — #896's side says Schemathesis defaults to `localhost:6882` on its own with Playwright as the exception; #952's says Schemathesis resolves its own slot. Whoever merges second rewrites the paragraph so Schemathesis sits beside Playwright.
- `manifest_path()` reads `actors-slotN.json` on slots 2–4, which only #896's writer produces. Merged first, #952 would move Schemathesis on slots 2–4 onto the seeded accounts. Slot 1 is unaffected.
- **It IS independent of #933** — they merge clean, and the shared reader files are identical blobs, as you said. So #933's current CI blocker does not gate #952.
- Order this supports: **#896 → #933 and #952 (either way round) → #899 → #900.**

**3. "Every slot shares one Postgres password (KS-731)" is dated at your own base.** #800 — *"make the per-clone datastore credentials actually reach a clone"* — is already in `7bcb66128`, and `bootstrap-env.sh` now generates the password. The sentence holds only for a clone bootstrapped before #800. It appears in five places, one of them the runtime refusal message in `assert_db_matches_api_target`, which is the one a user actually reads.

**4. Three small ones:**
- `test_production_code_is_scanned_too` cannot fail against the regression it names: it compares `_SCANNED_ROOTS` to itself, so narrowing the roots to `("tests",)` reddened 0 of 1737. Pinning it to `{"src", "scripts", "config", "tests"}` fixes it. The guard it protects does bite.
- `TestComposeAllowsEverythingElse` is the one class in `test_compose_slot_guard.py` without `_no_docker`, so the "offline" suite makes 21 real `docker inspect` calls per run. Nothing asserts on them, but on a machine with stacks up it reads the daemon.
- `systemTest/CLAUDE.md` and `test_stack_db.py`'s module docstring still describe the old container resolution.

**What checked out against your own words:** both actor-manifest files byte-identical to #933's head · #933 and #952 merge clean · the README listing verbatim from #896 · no spec, API, flag or dependency change (the `constraints.txt` blob is develop's) · `ADMIN_USER_PASSWORD` not forwarded on develop. We bit 14 of the new guards by reverting each one; 13 went red on an assertion exactly where aimed, and the fourteenth is the cell above.

**We ran no platform suite.** Akto, Playwright and k6 are not needed for this change; the one live run in point 1 is the only gap.

We have not approved, commented on or touched the PR.

---

## Notes for Kam — NOT part of the message

- **Evidence class.** **Verified by Wednesday at GitHub:** #952 and #896 both edit the two QA HTML docs (plus `systemTest/CLAUDE.md` and the Schemathesis README); #800's merge commit `48641bda3` is an ancestor of #952's base `7bcb66128`. **Relayed from s175, not re-run by Wednesday:** the textual conflict itself (`merge-tree` rc=1), the 1737/96.44% reproduction, the bite table, the E-1 timeline and the minors.
- **Approval:** no blockers, so this is approvable on the code. **But it should not MERGE before #896**, and Peter adding the one live run (point 1) is worth waiting for before you click. #896 itself had no blockers last night and is waiting on your approval too.
- **Cut point 4** if you'd rather not hand him small work while he waits on us.
