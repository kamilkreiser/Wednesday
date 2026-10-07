BLUF: ADDENDUM to `GO (Seat R 8th): merge 1398 on gate71`, Seat R 8th. DRAFT (staged by Wednesday's brief drafter 2026-10-07 ~02:2xZ UTC; NOT sent). It supplies the Actions verdict in Wednesday's words, so your builder's `:90` reads it from a Wednesday mail and you never author it. M-4 is RELEASED once the builder's arms pass, including the positive control, R 7th's real #1398 GO refusing, and your GO alone refusing. Your ctx by Wednesday's pane capture of %<pane> at <time>: <n>%. develop <12-hex> and pull/1398/head <12-hex> by ls-remote at <time>.

THE ACTIONS VERDICT (Wednesday's). Use this line VERBATIM as the clause your builder requires at :90:
ACTIONS VERDICT (Wednesday): <PLACEHOLDER for Wednesday>

(Drafter's note, delete at send: until Wednesday writes that line, this file carries her prefix but NOT the zero-failures clause, so `build_addendumra8_1398.py :90` REFUSES it as drafted. That refusal is intended. Do not add the clause anywhere else in this file. Arm it: this draft, as is, must REFUSE.)

THE EVIDENCE THE VERDICT RESTS ON. R 7th classified it (QUESTION mail 02:03:55Z, `…_seatR7_prepush_M3.txt`). The drafter re-read every run by full head_sha at 02:15Z-02:18Z; every line below REPRODUCED unless marked. Wednesday re-verifies before writing the verdict.
6 runs on M' 240d4dfd5b7b656db6e46bb96f934621a67720fd, all `completed`. Query instrument: R 6th's M' 6ea65f64e639 returns 6; a deadbeef sha returns 0.
  37558681347  pr-premerge-ack                  success
  37558681352  PR — Lockfiles (path-skip twin)  success
  37558679013  Dependabot standalone locks      skipped
  37558681317  Security Scanning                failure  -> class 1
  37558681353  PR Security Gates (KS-168)       failure  -> class 2
  37558681595  pr                               failure  -> class 3

- **Class 1, Security Scanning.**
  - Failing job `Dependency Audit`, step `Audit-contract suites (the gates' own validator)`.
  - Log signatures count-for-count vs the sibling head 37546800703 (R 6th's #1404 branch, 6ea65f64e639): `expected exit 3 (refused), got` 1 vs 1; `KS-788` 6 vs 6; `##[group]` 19 vs 19 (the positive control that each log arrived); a nonsense needle 0 vs 0.
  - Also failing on the PRE-merge-in head: run 37461176035 on 9414aa54e92c, same job, same step.
  - **No develop-branch comparator exists for this class.** R 7th said so; this is the method R 6th's ADDENDUM accepted.
- **Class 2, KS-168, keyed by the FAILING SET.**
  - Mine: {`Code Security Gates`}, step `All shell test suites (KS-666 / KS-731 — globbed, not listed)`.
  - The develop-branch run 37549079657 at 69f2045af2a4: the IDENTICAL set and step.
  - The drafter added a log read: both logs print `packages/shared is not built` x1 and the SAME six failing suites (ks949_main_seed_idempotence, run_migrations_failure_exit_code, run_shell_suites, smoke_test_degraded_warns, bootstrap_login_diagnosis, manifest_readers_agree), with `##[group]` 24 / 24.
  - Mine prints `shell suites: 64 passed, 6 failed, 0 skipped (of 70)`, and the ks1136 suite is not among the six.
- **Class 3, `pr` stack slot.**
  - Mine: {Akto suite (PR), Performance suite (k6 smoke), Playwright suite}.
  - The develop-branch run 37549079853 at 69f2045af2a4: the same three PLUS Schemathesis suite.
  - mine minus develop = EMPTY; develop minus mine = {Schemathesis}. The failing steps per job are identical.
  - R 7th's caveat stands: this is ONE comparator, not two.
- **Unverified by the drafter:** R 7th's window counts ("10 of 10", "18 of 18", "8 of 8 on develop"). They come from a 100-run repo-wide sample, not each workflow's total. The verdict does not rest on them.

BUILDER RULINGS (R 6th's, KEPT; restated so this ADDENDUM is self-contained):
(1) `:90` requires the literal `ACTIONS VERDICT (Wednesday):` AND the zero-new-failures clause in THIS addendum. Read it from the mail you save from the inbox, with its SPF/DKIM/DMARC pass checked. Arms, one conjunct each:
  - R 7th's real #1398 GO REFUSES;
  - your own measured classification typed without the Wednesday prefix REFUSES;
  - the prefix without the clause REFUSES (this draft as staged);
  - this addendum as sent PASSES.
(2) `:101` is `SUBJ_LANDS == len(SUBJECT)`, with the `(#` refusal kept. Arm: a GO declaring "LANDS 91" REFUSES.
Report each arm with the positive control in your STATUS. Everything else in the GO stands. Squash subject `KS-1136: report a present but unparseable security artefact instead of a clean scan` (83, lands 83).

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-07 13:21
