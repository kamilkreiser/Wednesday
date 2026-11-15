PR 2234: GO WITH NOTES (at head 624dc4bf1678651bf1a8e97d2b03ec6a7cd4d9df; tier 2)

Gate 357 (tier 2, Sonnet, re-commission), 2026-11-15 17:32 to ~17:45 AEDT. Findings only: nothing was fixed, pushed, posted, mailed, merged, or written to Linear or GitHub. Every figure below was re-measured by me in this run; the first gate agent's logs in scratch/ were treated as hints only (my files are the `g357-*` ones).

**Pins (by gh api, and git ls-remote at 17:43:29).**
- PR 2234 head 624dc4bf1678651bf1a8e97d2b03ec6a7cd4d9df, open, not draft, 1 commit, 4 files +264 -7, parent (and merge-base) 4e4347818772. Read at 17:32:39 and 17:43:29: unchanged, equal to the commission.
- develop is now ce35818d50ae (PR 2140's squash; it moved from 4e4347818772). It differs from the PR base in ONE path (a `packages/shared` Identus test file), which the PR does not touch.
- `merge-tree --write-tree` of develop and head: rc 0, tree fcaa1605daf0, identical in both orders; overlap of paths changed by both: none (`g357-pin2.sh`, `g357-mt1.txt`, `g357-mt2.txt`).
- Reused clone: its worktrees were confirmed by `rev-parse` at ce35818d50ae (wt-dev, wt-red) and 624dc4bf1678 (wt-head); blob hashes of both product files at wt-head equal the PR's blobs (4a74061fddc2, ba3e9ded7895), before and after my mutants.

**Python.** Every run used `scratch/venv`, Python 3.14.10 (Homebrew 3.14.10; pytest 9.1.1, ruff 0.17.1, httpx 0.28.1, schemathesis 4.32.1, pytest-cov 7.1.0; all equal to `constraints.txt`). Host `python3` also read 3.14.10 at this time; nothing ran on the 3.9.6 window.

## FOUND

**G357-2234-1 (Low; test thinness, message text only).** Three of my 27 mutants survive the 33 cells, and all three change message text only:
- the unknown-status failure drops the slug (`isolation tenant {slug!r}: {unknown}` becomes `isolation tenant: {unknown}`);
- the refusal message drops `on the way to 'active'`;
- the ValueError message drops `(known: [...])`.

No behaviour is unpinned: the move sequence, the 409 path, the unknown-status failure and the value named in it are all killed. Optional: pin the slug in the unknown-status cell.

**G357-2234-2 (Info; pre-existing, not this PR's).** `ruff format --check .` and `ruff check .` over the whole systemTest/schemathesis tree FAIL at BOTH develop and head, identically: `tests/unit/support/test_platform_admin.py:135` (format + E501) and `tests/support/platform_admin.py:34` (E501). The PR's 4 files are clean (see Q3). Worth a ticket for the owner of platform_admin; not a block.

**G357-2234-3 (Info).** The new cell file's docstring and the comments cite the order table "at develop 48883ba5976b". I re-read it at develop ce35818: `STATUS_REACHABLE_FROM` is still at `tenant-provisioning/src/index.ts:467-471` with exactly `active: [provisioning, suspended]`, `suspended: [active, archived]`, `archived: [suspended]`. The citation is only a stale SHA.

**G357-2234-4 (Info; red-proof detail).** At develop, 12 of the 33 cells fail: the 4 fixture cells by AssertionError (below) and the 8 helper cells (`TestStatusMovesToActive`) by AttributeError, because `status_moves_to_active` does not exist at develop. The commission's question (2) is about the MockTransport cells, which are AssertionError only. The helper cells are red by absence, not by assertion.

**G357-2234-5 (Info; whole-suite).** One cell fails at BOTH trees: `runner_extra/test_config_and_environment.py::TestSetupWithoutHttpx::test_with_a_venv_the_remedy_is_to_activate_it` ("this harness runs from its venv ... `<worktree>/systemTest/schemathesis/venv/bin/activate` must exist"). Cause: my scratch venv lives outside the worktree; an artefact of my set-up, not the PR. The builder's "4653 passed, 0 failed, 99.32%" is therefore NOT reproduced bit-for-bit (mine: 4648 passed, 1 failed, 4 skipped, 99.13%); the delta head minus develop is exactly the PR's +18 cells.

## TESTED (instrument in brackets)

**Q1. Fixture behaviour (read of the diff and the 10 fixture cells, run at head).**
- Archived goes suspended then active: cells R1 and R2 (`patches == ["suspended","active"]`), over a MockTransport that answers 409 for any move the table forbids.
- A found active row sends NO PATCH: O1 (`patches == []`). Suspended and provisioning send one PATCH to active. Missing creates (O4).
- An unknown status fails loudly, naming the value, with zero PATCHes (R4; C1 and the no-status-key cell). A platform that refuses archived-to-suspended fails naming slug, start and move, and does NOT fall back to archived-to-active (R3).
- Ruling quoted is Kam's KS-1861 "b".

**Q2. Red-proof (`g357-red-fixtures.xml`, pytest on wt-red = develop ce35818 product files with the PR's cell files).**
- Fixture file: 4 failed, 6 passed, all 4 reds AssertionError (R1, R2, R3, R4); the 6 controls pass. Equal to the READY.
- Both cell files: 12 failed (4 AssertionError + 8 AttributeError, see G357-2234-4), 21 passed.
- At head: 33 passed, 33 of 33.

**Q3. Format, lint, suite, Python.**
- `ruff format --check` and `ruff check` on the 4 PR paths at head: both rc 0 (`g357-ruff.sh`). Planted control (a misformatted line and an unused import appended to a copy): format rc 1, check E402 + F401.
- Whole systemTest/schemathesis suite (`tests/unit tests/functional`, repo addopts, coverage gate `fail_under` 90), Python 3.14.10, sparse worktrees widened to include `Blockchain/Dev` (an earlier narrower sparse tree caused 16 false failures, identical on both trees; discarded):
  - head: 1 failed (G357-2234-5), 4648 passed, 4 skipped, coverage 99.13%, gate reached.
  - develop ce35818: 1 failed (same cell), 4630 passed, 4 skipped, 99.13%.
  - 4648 minus 4630 = 18 = the PR's new cells; the failed set is identical.
- mypy: my one invocation errored on package-base resolution (not run properly): UNMEASURED.

**Q4. No live request.**
- The PR's own cells build `httpx.Client(base_url="http://platform.test/api", transport=MockTransport)`; the only URL added by the diff is that one.
- Instrument: a `sitecustomize` that makes any socket connect and any DNS lookup raise; control (`create_connection('127.0.0.1', 9)`) raised NETBLOCK; with it active the 33 PR cells still pass at head. So the cells made no network call.
- `_ensure_tenant` is invoked only by the live-tier fixtures, which the PR leaves unchanged beyond the function body; no live platform was contacted by me.

**Q5. Own mutants (`g357-mut.py`, 27 plants on every changed product line: the table, the helper's guard/message/return, the loop, the status check, both failure messages, `start`, `needs_reactivation`).**
- 24 killed, 3 survive (G357-2234-1). Unmutated control after restore: 33 passed. Sha/blob restore verified equal after the run.
- Slip declared and fixed: my first run's control read 4 failures because of stale `.pyc` (same-size same-second rewrite); I re-ran everything with bytecode caching off and an empty pycache prefix, and quote only that run.
- tsc/eslint: not applicable, the PR is Python-only (4 .py files); no TS touched.

## NOT TESTED (UNMEASURED)
- Any live platform, slot or sweep; the integration suites; `run.py quality` as one command; pip-audit; mypy (see above).
- The PR's CI state (Actions retired), the pre-push hook's own output, Linear (KS-1914 state and comment).
- A Python other than 3.14.10; the builder's exact environment (4653/99.32%).
- Whether a platform older than PR 1885 behaves as the R3 cell emulates (the emulation is of a refusal, not a recording).

## For Kam
Nothing blocking. Optional: a ticket for the pre-existing ruff failures in `platform_admin` (G357-2234-2).
