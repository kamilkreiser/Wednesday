# BUILD REPORT — QA gate set for Secuura/Blockchain PR #916 (KS-993 + KS-1026), TIER 2, ROUND 1

Drafter: Wednesday-assistant DRAFTING subagent (Sonnet), 2026-09-14 ~17:14–17:26 AEST. One of three gate sets
built in this commission (sibling sets: `2026-09-14_gate919/` for PR #919, `2026-09-14_gate939/` for PR #939 —
the third added mid-commission). Nothing launched, nothing committed, nothing mailed. The Secuura checkout was
touched with READ verbs only (`ls-remote`, `log`, `diff --name-only`, `diff --numstat`, `ls-tree`,
`merge-base --is-ancestor`) against the existing read-only checkout at
`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`; no `fetch`/`checkout`/`worktree`/`merge-tree`.

## THE HEAD-PIN COMPLICATION (read this first)

The s227 READY-FOR-QA mail on disk (`ready_916.txt`, sent 2026-09-14T06:57:57Z) names head
`3b368abaaf7c5f8538b1026f1eac3263ce672cbd` with a 2-file diff. Wednesday warned mid-drafting (17:0x AEST) that
a doc commit naming `npm run typecheck` in `systemTest/README.md` was landing as a fast-forward on top of that
head, and instructed the launcher's head pin be a single, one-line-editable `HEAD_SHA=` assignment for exactly
this reason.

**I confirmed the doc commit HAD ALREADY LANDED** before I finished drafting: `git ls-remote origin
refs/pull/916/head` read `12507d200375a5ebcab1579920cb75e74a6391f1`, and `git merge-base --is-ancestor
3b368abaaf7c5f8538b1026f1eac3263ce672cbd 12507d200375a5ebcab1579920cb75e74a6391f1` returned rc 0 (fast-forward,
confirmed). **This entire set is built against the NEW head, `12507d200...`, with a 3-file diff** (the
mail's 2 files plus `systemTest/README.md`). The brief documents this correction explicitly in its own
"head-pin correction" section and in PROVENANCE, naming both heads, the fast-forward proof, and the
read time.

**The launcher's `HEAD_SHA` is one line** (`launch_qa_secuura_916_ks993_ks1026.sh`, the `HEAD_SHA=` assignment
near the top) — a further re-pin, if the head moves again before real launch, is a one-line edit. `FILES_WANT`
(also one line) must be bumped alongside it if the file count changes again. Redproof cell 25 exercises this
substitution point directly (see below) and confirms tampering `HEAD_SHA` alone, with nothing else touched,
correctly trips the head-moved guard (exit 6) — proving the one-line mechanism actually works, not just that
it looks like it should.

## FOUND

- PR #916 (KS-993 + KS-1026), branch `kamilkreiser/ks-993-systemtest-typecheck-entrypoint`, base `develop`.
- Current head `12507d200375a5ebcab1579920cb75e74a6391f1`, chain `584b12ba1` (09-09 original) →
  `474799863` (`--no-ff` merge of develop M38, `actor_manifest.ts` conflict resolved ENTIRELY to develop's
  text) → `3b368abaa` (trim to cell 6) → `12507d200` (the README doc line).
- Diff vs develop M38 (`0e78c7270188ac45c1c29f927bdf90728f10215d`) = exactly 3 files: `systemTest/package.json`
  (new, +31), `systemTest/performance/tests/unit/runner/actor_manifest.test.ts` (new/trimmed, +65 net),
  `systemTest/README.md` (+3 −1).
- **The measured proof the merge-in resolved fully to develop's text**: `systemTest/performance/runner/
  actor_manifest.ts` is byte-identical between the head and develop (`git ls-tree`, both blob
  `22feeb3970e0f3813fe648f6df888d355bd9e873`) — confirmed by `cmp`, not by re-reading the commit message.
  `controls_check.sh` asserts this as a first-class check, not a grep.
- The builder's (s227) full Test Evidence, trim-cell table, 4/4 tamper table, and NOT-covered block — read
  from `ready_916.txt` and quoted verbatim in the brief, with the head/file-count discrepancy called out
  explicitly rather than silently corrected.
- The gate's own commissioned leg: `npm run typecheck` from `systemTest/` (the exact seven-config script read
  directly from `git show 12507d200:systemTest/package.json`, quoted verbatim in the brief) plus the whole
  `performance` unit suite — both to be RE-DERIVED by the QA seat, not re-quoted, with the evidence-class rule
  (MEASURED AT RUNTIME / PROBED / READ ONLY) applied explicitly, and the install-artefact trap (a red before
  all four packages are installed is not a defect) stated as a named known-fragile item.

## TESTED / HOW

- **`--check` against the LIVE current develop tip and the live PR head**, run twice: once during
  authoring (17:19 AEST, using `QA916_BRIEF`/`QA916_PROMPT` overrides pointed at the in-progress files) and
  once as the final close-out step below, both with the real head SHA and no env overrides on the
  launcher's own pins. Both **rc 0**, "all guards pass," 11 guard lines each, reading `compare: mb=0e78c7270…
  ahead=4 files=3` and `origin develop still 0e78c7270… (M38; git ls-remote)`.
- **`controls_check.sh`** (`controls_check.out`): fetches `systemTest/package.json`, the trimmed test file,
  `systemTest/README.md` (both head and develop), `actor_manifest.ts` (both sides), and develop's
  `actorManifest.test.ts` via the GitHub contents API at the pinned SHAs; asserts every blob against the
  table above, asserts `actor_manifest.ts` head==develop by `cmp`, re-derives the package.json anchors
  (the seven-tsconfig line, the `typecheck`/`pretypecheck` script keys, the "no dependencies" prose — two
  wordings, both present), the trimmed test file's single kept cell and its "corrupt" anchor, develop's
  Peter file's 8 `it(` + 2 `it.each` (24 cells) with 0 "corrupt" hits (confirming the trim's premise), the
  `catch` block anchor on both sides, and the README's before/after wording. One anchor wording mismatch was
  found and fixed during authoring (the "no dependencies" phrase differs between the package's `description`
  field and its `pretypecheck` error string; both are now asserted separately). **Result: FAILS=0, rc 0.**
- **`redproof.sh`** (`redproof.out`) — this bullet described the ORIGINAL drafter's run (work dir `redproof.XMoJC0/`,
  27 cells 0–26, FAILS=0); superseded twice since — see REDPROOF RECONCILIATION below for the actual final state.
  Every guard the launcher declares fires at its own distinct exit code — 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
  12, 13, 14, 15, 16, 17, 18, 20, 22, plus the natural `127` at the exec line with `claude` absent from
  PATH, plus `0` (green first and green again, pristine sha-identical). Two cells needed real debugging
  during authoring, not just scripting:
  - **Exit 13 (env file missing)**: originally mis-designed to expect exit 10 (a compare mismatch); live
    testing showed the compare API call raises an unhandled exception when the env file is missing (empty
    `GH_TOKEN` → the GitHub API 401s → `urlopen` raises `HTTPError`), so `CMP_READ` comes back empty and the
    launcher correctly refuses at exit 13 ("could not read the compare"), never reaching the exit-10
    comparison at all. Fixed the launcher's first compare call to catch the exception explicitly (so the
    failure mode is deterministic rather than an uncaught traceback) and fixed the redproof cell's expected
    exit code to 13, confirmed live.
  - **Exit 18 (develop content-judgement)**: originally designed as a single `DEVELOP_SHA` tamper, but that
    variable was ALSO used to build the compare guard's expected string (`CMP_WANT`), so tampering it broke
    the WRONG guard (exit 10, not 18) and collapsed two intended test cases into one. Fixed by splitting the
    launcher into two independent constants — `BASE_SHA` (used only by the compare guard) and `DEVELOP_SHA`
    (used only by the content-judgement guard) — even though both hold the same value today, so each guard
    can be exercised independently. The redproof cell now forces `CUR_DEV` (the live-read variable, not a
    pin) to a nonsense 40-hex value via a launcher tamper, which makes the develop-move comparison
    unreadable and correctly refuses at exit 18. Both fixes verified live before being folded into the kept
    `redproof.sh`.
  - **Cell 25** specifically tampers ONLY the `HEAD_SHA=` line (to a wrong-but-valid-looking 40-hex value)
    and confirms the head-moved guard fires at exit 6 — the direct proof that Wednesday's required one-line
    substitution point is real and load-bearing, not decorative.
- **Raw-control-byte census**: 0 across all five text/script files; the synthetic NUL positive control fires
  at its expected offset (`[16]`) in both `controls_check.sh` and `redproof.sh`'s own census.
- **`bash -n`**: clean on the launcher.

## POST-HANDOFF CORRECTION (by the closing drafter, 17:34–17:40 AEST)

The launcher's `BRIEF`/`PROMPT_FILE`/`REAL_BRIEF` defaults, and the prompt's own brief-path line, originally
pointed at the CENTRAL install target (`fleet/qa-agent/briefs/2026-09-14_secuura-916-ks993-ks1026-tier2.md`) —
matching gateL9's own convention, but that path does not exist yet (nothing in this commission is installed).
Run as-is with no overrides, `--check` refused at exit 3 ("brief missing") against a genuinely uninstalled set —
a real gap between the BUILD_REPORT's claimed "close-out, no env overrides, rc 0" and what the file on disk
actually does when run fresh. **Fixed**: both path constants and the prompt's brief-path line now point at THIS
gateset directory (matching gate919's and gate939's convention, decided during this session so all three sets
are internally runnable in place without an install step first). Re-verified: `bash
launch_qa_secuura_916_ks993_ks1026.sh --check` now genuinely returns **rc 0** with zero env overrides, against
the live current develop tip and live current PR head, run fresh at 17:34 AEST — see the regenerated
`check.out`.

This also required two `redproof.sh` fixes: (1) two tamper anchors (cell "prompt lacks the real brief path" and
the two cells exercising the "real launch, defaults point at scratch copies" scenario) referenced the OLD
central-path string, which no longer exists in the tampered files verbatim — fixed to the new local-path
string; (2) the "real launch, not installed yet" cell's premise was invalidated by the fix (the default paths
now DO exist, so it no longer naturally refuses at exit 3) — repurposed to assert the launcher reaches the
TTY-refusal guard (exit 22) directly on its own pristine defaults, which is the more meaningful assertion once
the set is genuinely runnable in place; the now-redundant scratch-copy variant of that same assertion was
removed rather than kept pointlessly parallel. Net cell count at this point: **25 named cells (0–23, 25 —
cell 24's number was retired along with the redundant cell, not reused) plus the standing final "green again"
cell, FAILS=0** — this paragraph undercounted by omitting the always-present final cell from its own tally;
see REDPROOF RECONCILIATION immediately below for the corrected count and the actual final work dir.

The original drafter's core guard logic, `controls_check.sh`, and the brief/prompt content itself were correct
and needed no changes — only the three path constants, the prompt's one path line, and the two dependent
redproof cells.

## REDPROOF RECONCILIATION (closing pass, 17:43 AEST — reconciles the two paragraphs above)

A run after the POST-HANDOFF CORRECTION above was written (but before close-out) is the one actually on disk.
**The file that IS `redproof.out` right now, verified by reading it directly:** 26 cells total —
`0`–`23`, `25`, `26` (cell `24`'s number stays retired, exactly as the correction paragraph describes; that
paragraph's own tally of "25 cells" simply forgot to add the standing final `26 green again (pristine
sha-identical)` cell to its count). **FAILS=0.** Work dir actually kept: `redproof.c7umZI/` (NOT `XMoJC0` —
the original bullet's dir — and not a dir named in the correction paragraph, which did not name one). The
other two work dirs in this directory, `redproof.XMoJC0/` and `redproof.gH004m/`, are earlier kept runs from
the original drafter and the mid-correction pass respectively — left in place for lineage, per the
never-`rm` rule; `redproof.c7umZI/` is the current/final one. Re-verified directly: `bash -n` clean, pristine
sha256 in the file's own last line matches the launcher/brief/prompt's current on-disk sha256 (no drift since
this run). **This section, not the two above, is authoritative for the final redproof state; the deliverables
table below points at the actual files.**

## CAVEATS

- The head may move a THIRD time before real launch (the `HEAD_SHA` one-line mechanism is the designed
  remedy; `FILES_WANT` must be checked alongside it if the file count changes).
- `controls_check.sh`'s `model/` copies are the fetched-bytes record from THIS authoring pass — if the head
  re-pins, they should be refreshed by re-running `controls_check.sh` (it writes into `model/` on every run).
- The typecheck/unit-suite legs named in the brief were NOT run by this drafter (drafting a gate set is not
  running the gate itself, per every prior exemplar's own convention) — they are commissioned for the QA
  seat to run at launch time.

## PINS (re-read live at 17:26 AEST, the close-out `--check` run)

- Head: `12507d200375a5ebcab1579920cb75e74a6391f1` (`git ls-remote origin refs/pull/916/head`).
- Base: develop M38 `0e78c7270188ac45c1c29f927bdf90728f10215d` (`git ls-remote origin refs/heads/develop`) —
  unmoved throughout this drafting session.
- Compare: `mb=0e78c7270188ac45c1c29f927bdf90728f10215d ahead=4 files=3` (GitHub compare API, live).

## `--check` RETURN CODE: **0** (both runs, authoring-time and close-out; live develop tip, live PR head, no env overrides).

## Deliverables (this dir → install targets)

| file | install target |
|---|---|
| `2026-09-14_secuura-916-ks993-ks1026-tier2.md` | `fleet/qa-agent/briefs/2026-09-14_secuura-916-ks993-ks1026-tier2.md` |
| `2026-09-14_secuura-916-ks993-ks1026-tier2.prompt.txt` | `fleet/qa-agent/briefs/2026-09-14_secuura-916-ks993-ks1026-tier2.prompt.txt` |
| `launch_qa_secuura_916_ks993_ks1026.sh` | `fleet/qa-agent/launchers/launch_qa_secuura_916_ks993_ks1026.sh` |
| `controls_check.sh` (+ `controls_check.out`: FAILS=0) | this set |
| `redproof.sh` (+ `redproof.out`: 26 cells [0–23, 25, 26; cell 24 retired], FAILS=0; final work dir `redproof.c7umZI/` kept — `XMoJC0/` and `gH004m/` are earlier kept runs, lineage only) | this set |
| `model/` — fetched-bytes copies from `controls_check.sh`'s own run | this set |
| `SHA256SUMS.txt` — sha256 of every other top-level file in this set | this set |

**Install:** copy the brief + prompt into `briefs/`, the launcher into `launchers/`, then

```
cockpit.sh add "QA/Secuura-916" "bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_916_ks993_ks1026.sh"
```
