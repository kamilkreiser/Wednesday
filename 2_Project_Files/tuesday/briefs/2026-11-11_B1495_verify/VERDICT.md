GATE B1495: GO WITH FINDINGS @ 6b6d5e9 on main c684e80

Independent QA gate (Opus) for Tuesday, 2026-11-11, 14:42 to 15:01 AEDT (`date` at start and end). Subject: `b1495/composer-lane-b-web-api-polish` at `6b6d5e9e9373e14f6fe2845318f261a076c00545`, two commits (`2b3d59f9` 77a, `6b6d5e9e` 77b) on main `c684e808225ef04402b9e83f784831b2574ba633`. Gate clone (my own, SSH deploy key): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s266/gate1495/repo`. Evidence: `.../gate1495/out/`, probes `.../gate1495/probe/`, scripts `.../gate1495/scripts/`.

## BLUF
- **77a holds, and my attempts to break it failed.** The API takes a custom decision with no rationale only when the field is a secret AND the value is an exact value reference. Every other custom decision still gets 422 `DECISION_INCOMPLETE`, and the message is unchanged byte for byte. The stored `''` never reaches a reader as `''`: the API bodies return null, the snapshot leaves out `justification`, and the input hash equals the NULL case. That also holds after release and after the copy into the next draft. A scan of every stored text/jsonb column found no `"justification": ""`, and the scan's control fired.
- **77b holds.** I ran the web's own selection and request-body functions against the REAL API (not a scripted one). Every field they select is accepted, nothing is left afterwards, a recorded decision is not selected and stays unchanged, and a stale If-Match is refused with 412. The new words are exactly W1 to W3. No other user-facing word was added.
- **No regression.** Full `vitest run` (all projects) shows head equal to main except 18 added rows: lost 0, changed 0. The same holds for the API db suite (13 added) and packages/db (0 added). lint, format:check, typecheck and build all rc 0 at main and at head. gitleaks finds no leaks in the range.
- **Merge:** main is still `c684e808`. It is the branch's merge-base, and `merge-tree --write-tree` gives rc 0 with a tree equal to head's tree (`8a902dd3`).
- Four findings, all Minor (below). None blocks landing. PR and squash texts are written beside this file.

## FOUND (numbered, with severity)
1. **Minor: the 77a commit message overstates one rule.** `2b3d59f9` says "Every other custom decision, and not_applicable, still need a justification." At the API, `not_applicable` has never needed a rationale. Probe P5 shows the same result at main and at head (the comparison is True): with null it returns 200 and stores NULL; with `""` it returns 200, stores `""` and answers `""`. Only the web form requires one. The squash message I wrote replaces this sentence, so there is no product effect.
2. **Minor, pre-existing, not introduced by this branch:** a `not_applicable` decision with `rationale: ""` is stored and returned as `""`. The new read-path `NULLIF` covers only custom rows (`inputs.ts:391`). The web sends null for an empty box, so only a direct API caller can reach this. It is unchanged from main (P5). It is a candidate backlog item, not this ticket.
3. **Minor (behaviour to know):** before the first Generate, the controls list has no resolved rows (Q0: 0 rows, 0 targets). So "Mark all secret fields local" first appears after a Generate. This matches the rest of the Controls screen, whose rows come from the same data, but the product owner's card did not state it. Two more points: the S6 hint "Required for a custom value or an exclusion." is now untrue for a secret local value (W5 was kept unchanged on the owner's word), and there is no committed DOM row for the S6 label. The builder disclosed both.
4. **Minor (coverage limit):** the fixture content has one secret field. So the real-API run chains one PUT (Q1, Q4). The multi-PUT ETag chain (`"v-7"` to `"v-8"` to `"v-9"`) and stop-at-first-refusal are shown only by the builder's DOM test against a scripted API. I read that test (`b1495-mark-all-local-dom.test.tsx:329-410`) and the builder's plants E and F for it.

## TESTED, and HOW (each with a control that can fail)
**Readers census (my own).** `git grep -i 'control_decision|justification'` over the whole tree at head, tests and .md excluded. It found these readers of `control_decision.rationale`:
- `inputs.ts` `controlBodies` (the one SELECT behind getControl, putControl and listControls)
- `snapshot.ts:91/:186`
- `engagements.ts:515` `copyVersionInputs` (clone and next draft)

Two other hits are not rationale readers: `authz.ts:226` (reads `decided_by` only) and `engine/resolve.ts` (reads the snapshot). The migrations hold no view, trigger or function that reads `rationale` (3 hits, all in table DDL). `apps/worker` has no hit. The renderers' `rationale` is content release C13 labels, a different thing. The census is closed by the runtime scan below rather than by grep alone.

**Probe file 1** (`probe/gate1495-77a-probe.db.test.ts`). It runs in the container copy only, on the project's db route (postgres:16 at the project's pinned digest, `--internal` network). Results at head: 12/12.
- P1: a non-secret field with a value-ref-shaped value and no rationale returns 422 `DECISION_INCOMPLETE` with the exact message.
- P2, P2b, P2c: these return 422 and store nothing. They are a raw secret with `""`, a value ref with an extra key, and a whole-item custom carrying a value ref.
- P3: whitespace-only rationales (NBSP, spaces, U+3000) on a secret local value return 200. The stored value is `''`, GET returns `[null]`, and the list body holds no `"rationale":""`.
- P4: a later edit sequence on the same field (rationale text, then null, then text, then blank). Stored, answered and snapshot values were `First reason./""/Second reason./""`, `text/null/text/null` and `text/absent/text/absent`.
- P5: `not_applicable` on the secret field. Recorded, and identical at main.
- P6: `inputHashOf(buildSnapshot)` with the stored `''` equals the hash with the row rewritten to NULL (`f54725f3...`). Control: rewritten to `"x"`, it differs.
- P7: the full clean path with no rationale: Generate, exceptions, technical and customer approval, release, then `POST /draft`. The new draft's copied row stores `''`. GET returns null and the list has no `""`. The new draft's snapshot has no `justification`. The scan of every pc base-table json/jsonb/text/varchar/bytea column found 0 rows holding `"justification":""`, `"justification": ""` or `"rationale":""`.
- P8 (control for the scan): the same flow with a real rationale finds the needle in `control_decision.rationale` and `policy_version.input_snapshot`, and finds `"justification": "<needle>"` in `input_snapshot`. So the scan reads the stored artifacts, and the P7 needle format does fire.

**Controls that failed as they should:**
- (a) The same probe at **main**: P3 x3, P4, P6 and P7 are red with 422 `DECISION_INCOMPLETE`. P1, P2*, P5 and P8 are green.
- (b) **Plant snap** (the `snapshot.ts` guard back to NULL-only, sed count 1 to 0): P4, P6 (the hashes differ) and P7 (`justification` present) are red.
- (c) **Plant read** (the `controlBodies` CASE back to `d.rationale`, count 1 to 0): P3 x3, P4 and P7 are red (`[''] != [null]`). P6 stays green, which is correct because the hash does not use the read path.

**Probe file 2** (`probe/gate1495-77b-probe.db.test.ts`). It imports `unmarkedSecretFields`, `withLocalValue` and `decisionBody` from `apps/web/src/screens/w2/model.ts` and drives the real API. Results: 5/5.
- Q1: after Generate there is 1 target (`UQ-008/admin_password`, ref `LV-UQ-008-I1-F2`). It returns 200 with the list's ETag. Afterwards 0 targets are left and every decision's rationale is null.
- Q2: a hand-recorded decision is not selected, and its rationale and value_ref are unchanged after a run.
- Q3: the list ETag after the draft has moved returns 412 `PRECONDITION_FAILED`. This proves If-Match is enforced, so the chaining matters.
- Q4: another discovery state; everything selected is accepted.

**Words.** I read the full product diff and listed every added non-comment line that holds a literal or JSX text. The only user-facing additions are `Mark all secret fields local`, `` `Marked ${n} secret fields as local.` `` and `` `Marked ${n} of ${m} secret fields; the rest were not changed.` ``. All three match ADDENDUM-1 byte for byte. The `ControlDetail.tsx` label is the existing string, now behind a changed predicate. Everything else added is SQL, tokens, the path template and the header name. Control: `grep -c -i 'Mark all secret fields local'` over the `Controls.tsx` diff counts 2, the button text and its comment line.

**77b reading.** `canMarkLocal = isConsultant && blocked === null && engagement.state === "ready"`. Here `blocked` is `draftEditBlockedReason`, the same edit gate S6 uses (`ControlDetail.tsx:146`). It is not a Generate-readiness gate. The button shows only while `toMark.length > 0`. The run is sequential `await` with `etag = answer.etag`, and the `catch` stops it and sets W3. Generate is disabled while a run is in progress.

**No regression** (`scripts/build.sh`, `node.sh`, `db.sh`; ci.sh steps `:116`, `:117` and `:118`, run step by step, `--network none` for node):
| Suite | main `c684e808` | head `6b6d5e9e` | lost | changed | added |
|---|---|---|---|---|---|
| `vitest run`, all projects (ci:node's `test`) | 3129: 3126 passed, 2 failed, 1 skipped | 3147: 3144 passed, 2 failed, 1 skipped | 0 | 0 | 18 |
| apps/api db config | 1550 passed | 1563 passed | 0 | 0 | 13 |
| packages/db config | 629 passed | 629 passed | 0 | 0 | 0 |

The 2 failures are `packages/content/src/citations.test.ts` at both main and head: the E8 SOW text is withheld and was never mounted. lint, format:check, typecheck and build gave rc 0 at main and rc 0 at head. Compare control: dropping one row from a copy of the head JSON gives `lost 1` and names that row.

**Secret scan.** gitleaks (the project's pinned image and config, stdin mode) over the range diff scanned 43 KB and found no leaks, rc 0. The project's own `secret-scan.sh --self-test` (the control: planted secrets must be flagged) passed every check, rc 0.

**Name and ticket scan** (underscore-aware, `(?<![A-Za-z])name(?![a-z])`, re.I). It covered the owner's names and the other names in the records, over the 912 added lines and both messages: 0 hits. The control `_by_Kam_` fires (1). Ticket keys and the words Tuesday/Wednesday/Friday in the messages: 0 (control 1). The added lines carry `B1495` only in test engagement names and file names, which is the repo's existing convention (`b61-*`, `s43-*`).

**Identity.** Both commits are `88359143+kamilDatasec@users.noreply.github.com | same`, matching the stamped IDENTITY. Each has one trailer.

**Lock and hygiene.** The heavy lock was proven before use: a planted scratch lock made the script wait ("lock HELD by: PLANTED"), and a free scratch lock was taken with a holder line. Every heavy job then took the project lock `.tools/composer-heavy.lock` with holder `GATE B1495 (Tuesday s266 QA gate, Opus)`, waited on load above 24 several times, and released by `mv` into my own quarantine. No other holder was ever seen. Containers, networks and images were all named `pc-g1495-*`. The images were removed by exact name, and the final `docker ps -a`, `network ls` and `images` counts of `pc-g1495` are 0, 0 and 0 (control: postgres 1). The lock is absent at the end. `ls-remote` at 15:00:49 shows main `c684e808` and the branch `6b6d5e9e`.

## NOT TESTED
- How the button and banners look (no render or screenshot). The DOM test proves only their existence and their words.
- A multi-field real-API chain (the fixture has one secret field, so see finding 4). Real content release, a hosted database, and the demo were not used (never touched).
- The S6 label at DOM level was not re-run by me. I took it from the diff and the shared predicate rows.
- PCOMP-15's numbers were not re-measured (measure-only, no product byte). PCOMP-75 was not built.
- CodeQL is hosted only. Tuesday reads it on the PR.
- Open-PR partition overlap was not re-read by me. I relied on the builder's pre-push read; main is unmoved.

## Files
`pr-title.txt`, `pr-body.txt`, `squash-subject.txt`, `squash-body.txt` beside this file.

Note on pr-body.txt: the brief asked for ASCII, so the attribution line is written without its usual emoji ("Generated with [Claude Code](...)"). A program check counts 0 non-ASCII bytes in all four text files; its control, an e-acute, counts 2.
