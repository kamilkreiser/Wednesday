# QA Agent Invocation Brief — Secuura / Blockchain — s102's set, THROUGH-CODE pass (2026-09-02, ~06:1x AEST)

**R0 (client isolation):** this brief carries exactly one client's content (Secuura / Blockchain, Platform K). Never name or reference any other client. Read only the paths named here. Your report goes under YOUR project tree at `projects/secuura/reports/2026-09-02-s102-rows-through-code/` (create it).

**Read FIRST, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`, then your own project's `CLAUDE.md`. **This is a CODE-REVIEW pass, not a browser pass** — no running surface, no browser, no Playwright, no suite runs, no repository writes. Your s101 pass is at `projects/secuura/reports/2026-09-02-s101-rows-through-code/` — read its SUMMARY: s102 was briefed to answer its asks 1 and 3 (plus F-15/F-17); you check whether each was answered AT SOURCE. Asks 2 and 4 were NOT started (handed to s103) — that is on the record, not a finding.

**Why this pass exists (Kam, 2026-09-01 17:55, standing):** every change is reviewed through code before Wednesday's completion check and any score. Session 102 was a SHORT seat (cut by the shift change): ONE push to #781, nothing merged, no demo contact. You check that one push through code before the session is scored.

**Merge fidelity: NOT APPLICABLE** — #781 is an OPEN PR. The row is the s102 DELTA `d660cc956..7bd66ef0f` (Wednesday's own diff --stat 06:1x: 4 files, +237/−20). Diff the delta, and where a claim spans the whole PR, diff `a079e1f6b...7bd66ef0f`. Any zero or empty result you obtain needs a positive control before it is reported.

---

## 1. Target
- **Client / Project:** Secuura / Blockchain (Platform K — TypeScript monorepo; the row's files are preflight bash, `Blockchain/Dev/package.json`, and a python unit suite under `systemTest/schemathesis/tests/unit/runner/`).
- **Where the code is:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` — **READ-ONLY**. Work by SHA only (`git log` / `git show` / `git diff <A>...<B>` and plain file reads). **NEVER** fetch/checkout/switch/worktree/stash/pull, no `npm`/`npx`/`python`, no writes. Wednesday fetched `refs/pull/781/head` (`7bd66ef0f`) at 06:1x AEST — the object is present; a missing object = NOT VERIFIABLE, say so. The checkout's HEAD is wherever the last tester left it — do NOT move it.
- **Environment identity:** none running. Static review against develop `a079e1f6b` and main `e44600ecc` (Wednesday's own ls-remote 06:1x AEST; both unmoved since s101).
- **Production?:** NO. No deploy, no demo contact, no chain writes this session.

## 2. The row (the builder's claims — inputs to falsify, not evidence)
| Row | head | claim | what you do |
|---|---|---|---|
| **#781 OPEN (s102 delta)** | `d660cc956 → 7bd66ef0f` (4 files +237/−20: `Blockchain/Dev/package.json` +1/−1 · `Blockchain/Dev/scripts/preflight/bare-path-scripts-executable.sh` +54/−17 · `Blockchain/Dev/scripts/preflight/preflight.sh` +2/−2 · `systemTest/schemathesis/tests/unit/runner/test_slot_targeting.py` +180/−0) | **Ask 1 / F-11:** the `--base-url http://localhost:6882` literal DELETED from `test:contract`; a CALLER-side guard added as property tests reading from the index (every tracked package.json, `*.sh`, workflow file; runner's own tree + docs excluded; corpus and exclusions in the docstring with counts "as one object"); red-before-green (three property tests named `Blockchain/Dev/package.json: ['http://localhost:6882']`); a SYNTHETIC positive control that passed while the tree was still dirty; the F-11 consequence now OBSERVED through the real parser (3-case table: slotted → :7082; unslotted → :6882 historic default; explicit flag beats slot = the defect, reproduced); 22 passed after, 325 across tests/unit/runner. **Ask 3 / F-12+F-13:** leg 9's corpus now `git ls-files` (37→46 package.json reached; 2→4 bare-path invocations; 5→17 interpreter-invoked; two live bare-path invocations found in `Blockchain/Dev/tests/e2e` the old globs never opened); both controls PROVED able to fail (a newly-reached package.json pointed at a tracked 100644 → exit 1 naming tests/e2e, file restored byte-identical md5 `37d11176fb5cfd0b48e9db3357992bc0`; pathspec narrowed to one file → "Corpus disagreement — pathspec 1, recount 46" exit 2, run on a throwaway copy, deleted). **F-15:** the vacuity comment now matches the code's condition (fires when BOTH counters are zero). **F-17:** `(see step 3/8)` labels → `(see step 3)`. **Header:** states the corpus AND what it does not cover with no count claimed for the not-covered set (first-token-only parsing with the two `docker compose exec` cases named; bare paths outside package.json; whether targets work). **No runtime change:** preflight + npm script + python unit suite only; no four-suite SET run and none claimed. 9/9 preflight PASSED with leg 9 running under its own new corpus. | FULL review, (a)–(e) below. Specifically: (1) is the docstring's corpus statement and the code's actual corpus THE SAME OBJECT (your own standing line) — reproduce the counts from `git ls-files` at `7bd66ef0f`; (2) could the caller guard stay green if the `--base-url` literal were re-added in a file its corpus misses (enumerate what the corpus excludes and check the exclusions are stated); (3) read the synthetic positive control — does it discriminate independently of tree state, or could it pass vacuously; (4) is the 3-case observed table CODE (tests that run the real parser) or prose; (5) does leg 9 read the INDEX (`git ls-files -s`), and does the pathspec-vs-recount control fire on the shape claimed; (6) is `test_slot_targeting.py` addition-only (180/0) with the pre-existing ruff-format state untouched; (7) do the two docs' slot-1 literals (DEV-PROCESS.md + local_environment.md, 4 lines) remain, and is leaving them named in the commit body as claimed. |

**Builder's own instrument disclosure (do NOT re-flag as a finding; DO note if its footprint reached the code):** its wrap-time approval re-poll used `gh api --jq --arg` — `gh api --jq` takes ONE argument, every call errored with empty stdout, and the loop printed a clean-looking empty set for all seven PRs; caught only because #745's KNOWN stale approval also came back empty. Redone with the raw-TSV + awk form; the control returned (#745 stale, #765 at-head). This never touched the pushed code — check nothing in the delta depends on the same `--jq --arg` shape.

**Wednesday's own instrument notes:** my verification of this SET is ls-remote + diff --stat only (06:1x); I have NOT read the delta's content. If any number in the row above disagrees with the tree, the tree wins — say so.

## 3. Scope — the questions (FAIL condition first, every time)
(a) Does the delta do what the wrap claims, and ONLY that? Name any hunk the claim does not account for.
(b) Is each test written at the CLASS, not the finding? Could the guard stay green if the fix were reverted (re-add the flag in package.json — through code, not by writing)? **"The ask is a floor":** does the delta test what IT changed, not only what the ask named?
(c) Were asks 1 and 3 answered AT SOURCE — and does any claim's last clause outrun its measured body (your scope-inflation pattern; "the corpus statement and the corpus must be the same object")?
(d) n/a (no security/data surface in this delta) — unless you find one, in which case say so loudly.
(e) Runtime change? The claim is NO (preflight/tests/npm-script only) — verify from the file list.
**Out of scope / do NOT touch:** running anything; demo/VM; ticket state; Peter's PRs (#777, #765); #776/#775/#778/#780/#773/#774/#779 except where a delta claim references them (the baseline duplicate is unchanged — verify by md5 only if you cite it). No repository writes anywhere.

## 4. Credentials — none. A prompt for any credential = STOP and report.
## 5. State-mutation & cleanup — you mutate nothing; if you find you have, STOP and report exactly what.
## 6. Output boundary (fixed) — findings, report, recommendations ONLY; fix-shape + regression test in prose, per finding.
## 7. Known-fragile / known-changed
- Known-fragile (hunt the class): `core.fileMode=false` hides modes — the INDEX is the instrument; POSIX ERE has no `\b`; a zero from a grep needs a positive control; the checkout's HEAD is not develop.
- Recent, do NOT flag as new: everything reviewed in your s100/s101 passes; the four-advisory baseline entries (KS-749/751) and their duplicates across PRs; the two docs' slot-1 literals are a DISCLOSED residual, judge only whether disclosure is where the wrap says it is.
## 8. Logistics
- **Time-box:** ~30 minutes (one small delta). Stop when findings repeat.
- **Findings sink:** `projects/secuura/reports/2026-09-02-s102-rows-through-code/` — `report-781-delta.md` + `SUMMARY.md` ranked by severity with a verdict (CLAIM HOLDS / DOES NOT HOLD / PARTIAL / NOT VERIFIABLE per claim cluster: ask 1 · ask 3 · F-15/F-17 · header/no-runtime) and the verdict line "PASS for review / PASS with findings / FAIL". Include an asks-answered table (asks 1, 3 → answered at source / partially / not; asks 2, 4 → NOT STARTED, handed over — expected).
- **Signal when done:** end your turn with the SUMMARY path on its own last line.
- **Escalation:** `wednesday-agent@agentmail.to`, subject `[QA -> Wednesday] QUESTION: <topic>`, or the top of `SUMMARY.md` and continue on the safest reading.

---

PROVENANCE:
- #781 head `7bd66ef0f` on origin (refs/pull/781/head) + fetched locally (objects only, HEAD untouched); develop `a079e1f6b` / main `e44600ecc` unmoved; delta stat 4 files +237/−20 | Wednesday's own ls-remote + fetch + `git diff --stat d660cc956..7bd66ef0f` in the Secuura checkout (read-only), 06:1x AEST | read 2026-09-02
- every per-claim number in the row (red counts, 22/325, 37→46, 2→4, 5→17, md5s, the 3-case table, the gh --jq disclosure) | s102's wrap mail 19:35:10Z at wednesday-agent@ (read whole 06:1x) — the builder's claims, inputs to falsify | read 2026-09-02
- s101 asks 1–5 and findings F-11/F-12/F-13/F-15/F-17 | your own s101 pass SUMMARY, projects/secuura/reports/2026-09-02-s101-rows-through-code/ | read 2026-09-02
- Kam's standing QA-gate process | dashboard chat 2026-09-01T17:55:18 + 17:55:45 AEST | read 2026-09-01
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-02 06:1x
