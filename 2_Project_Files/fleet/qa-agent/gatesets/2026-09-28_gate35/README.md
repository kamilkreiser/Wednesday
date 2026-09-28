# Gateset 2026-09-28_gate35 — README for Wednesday

Written 2026-09-28T05:07:11Z by the drafter (make_readme_gate35.py; every figure below is read from the kit's own output files at that moment, each named beside it).
The drafter launched nothing, sent no mail, tapped no pane, merged nothing, committed nothing, pushed nothing, posted nothing, changed no ticket or PR and deleted nothing. It wrote this kit directory `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-28_gate35/` and scratch under `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4901153c-5db0-4cfc-bf83-c25726202b34/scratchpad/g35` (the scratch clone `g35_sp/clone.git` — `git clone --bare --shared --no-checkout` of the checkout, objects borrowed READ-ONLY via alternates, then fetches FROM ORIGIN into it with the checkout's repo-local key; the logprobe workdirs `g35_logprobe_*`; the control workdirs `g35_controls_*`; three `pred*.py` assembly parts). Superseded outputs were RENAMED / copied `superseded_*`, never deleted. It did NOT write the routing line (§4). **One stray write outside both:** a mistyped redirect wrote a copy of security `index.ts` at #1322's head to `/tmp/x` (source code, no secret) — left in place, not deleted, per the no-delete rule; remove it at will.
The Secuura checkout was touched only by read verbs (ls-remote, `config --get`, `clone --shared` as a source, and node `require()` of its typescript and winston). GitHub: REST GET only (GH_TOKEN read by name, never printed). Linear: queries only. decisions.json and inbox_routing.conf: read only.

**gate35 = TWO PRs, both T1, one kit, no sibling, NO stack, ONE base.** Every head re-read by TWO instruments (ls-remote AND the PULLS API) and fetched: all agree (predict_1.out (a)).

| PR | ticket | tier | head (READ: API == ls-remote pull/head == branch == fetched) | commits on merge-base | why this tier |
|---|---|---|---|---|---|
| #1321 | KS-1348 | T1 | `52c96db4cf495c4438ad989473ffb0bfe5ab5be3` | 1 on `54f37d6399bd` | T1 logging (production log FILE format, secret-leak class), ruled "Third attempt: allow-list the file format" |
| #1322 | KS-888 | T1 | `4e8e11bdefd257e2cf1de48df2b68b8075f84b89` | 1 on `54f37d6399bd` | T1 security (the API-key mint's failed-save answer; credential surface), ruled "Fix all three routes" — this PR is the mint only |

### Squash subjects and bodies

| PR | declared subject (WITHOUT `(#n)`, the PR title as the PULLS API returned it) | declared | lands at (+8, ` (#n)`) | <= 92 | ends in `(#n)`? | squash-body keys: own | FOREIGN hyphenated keys seen (title / body / commit msg) |
|---|---|---|---|---|---|---|---|
| #1321 | KS-1348: allow-list the originate production file log format to named safe fields | 81 | 89 | yes | no | KS-1348 | none (keyscan_1.out) |
| #1322 | KS-888: a mint whose key save fails issues no key and answers 503 or 500 | 72 | 80 | yes | no | KS-888 | none (keyscan_1.out) |

Measured by fill_1.out: `subject scan: every declared subject WITHOUT a (#n) suffix, landed length <= 92: #1321 81->89, #1322 72->80`; `key scan: 2 mandated squash text block(s), each carries only its own key: #1321 ['KS-1348'], #1322 ['KS-888']`. keyscan_1.out: no foreign hyphenated key and no closing word before a key in either title, body or commit message.
**Commit messages that must not be pasted:** on MG-3 grounds, NONE — neither commit message carries a foreign hyphenated key (MEASURED). The standing rule still holds (compose, never paste): both messages end in a `Co-Authored-By` trailer, and #1321's names `#1310`, a cross-reference GitHub would attach to the squash.

Routing `QA/Secuura-batch1321` (**NOT added by the drafter** — §4). GO string `GO: merge #1321, #1322 batch` (or the subset); **the GO mail's SUBJECT must name Seat B 37th**, e.g. `GO (Seat B 37th): merge 1321 1322 on gate35` (the prompt carries this as kit rule exit 51). MERGE ORDER #1321 -> #1322 (END_TREE is order-independent, measured in both orders). The GO goes to **Seat B 37th**, which raised both and merges its own.

**Kam's rulings (READ from `0_Brain/dashboard/data/decisions.json`):** card `secuura-ks1348-r2-files-still-leak-allowlist` ruled **a** "Third attempt: allow-list the file format (recommended)", ruled_ts 2026-09-28T06:58:50+10:00. Card `secuura-ks888-failed-key-save-design` ruled **b** "Fix all three routes", ruled_ts 2026-09-28T06:58:57+10:00 (the card RECOMMENDED a, mint-only; Kam chose b). Card `secuura-ks888-revoke-validate-on-failed-save` is **OPEN** (what a failed revoke / validate answers).

## 1. BLUF
- **Kit: READY to launch once the routing line is added** — launcher `--check` rc 0 (`all guards pass:`, launcher_check_1.out); repin `--dry-run` rc 0 (repin_dryrun_1.out: DRY RUN COMPLETE 2026-09-28T04:31:50Z — every read agrees with the pins; the real run continues with the usage gate, --check and cockpit.sh add). The real launch refuses rc 1 at step 0 until `QA/Secuura-batch1321|coagent@agentmail.to|yes` is in inbox_routing.conf (§4).
- **Pinned over develop `54f37d6399bd5eeb62a4c75220f42c106fad4b4a`** (tree `14b9382edbd7d605552402aaba7cd614e8bf8f3f`, == gate34's END_TREE) — ls-remote AND fetched AND the API compare agree; gate34's #1316-#1320 squashes in; #1310 CLOSED unmerged. ONE merge-base `54f37d6399bd` for both; develop has not moved since, so the move ∩ every own path is EMPTY.
  - **END_TREE `a87715ebff3ec63e7513fe9a7d5314150fdd08f1`** (4 files changed, 408 insertions(+), 4 deletions(-)), identical in both orders (4 merge-tree calls); diff(develop, END) == the union of the four own paths and every END blob == its PR's head blob (MG-1).
  - Final re-read by `ls-remote` as this README was written (final_lsremote_1.out): 2026-09-28T05:07:11Z | 54f37d6399bd5eeb62a4c75220f42c106fad4b4a	refs/heads/develop | 52c96db4cf495c4438ad989473ffb0bfe5ab5be3	refs/pull/1321/head | 4e8e11bdefd257e2cf1de48df2b68b8075f84b89	refs/pull/1322/head — every pin still current: **True**.
- **Controls, both ways (controls_gate35.sh):**
  - normal (controls_1.out, rc 0): `SUMMARY gate35: 156 controls, OK 156, MISMATCH 0`
  - `--invert` (controls_2.out, rc 1): `SUMMARY gate35: 156 controls, OK 0, MISMATCH 156 (inverted: every control must MISMATCH-then-flip to OK; a MISMATCH here is a control that could not fail)` — every one of the 156 controls reported MISMATCH (rc 1 by design): each control can fail
- **OVERLAPS:** NONE. The pair is not stacked and shares no file; every kit path is disjoint from ALL 20 other open PRs. `merged_blob_paths` NONE and `noop_paths` NONE (predict (c)).
- **Every head == its READY and its golden (MEASURED, predict_1.out (e)):** each READY block is byte-identical to its brief's golden and to the Spark checker's patch.diff; both goldens apply strict with `git apply --cached --check` at 54f37d6399bd and every blob == the head's. #1322's golden writes three blank lines as -/+ pairs, so its raw +/- count (27) differs from the head's `git diff -U0` (21); netted of identical pairs (6 lines) it is IDENTICAL — a representation difference, not a code one (the blob equality above is the discriminating instrument).

### 1a. The #1321 LOG-FILE WIDEN, repeated through the REAL logger (MEASURED by the drafter, logprobe_gate35.py -> logprobe_1.out)
The REAL originate logger.ts at each revision (transpiled by the checkout's typescript 5.9.3, the checkout's winston 3.19.0), NODE_ENV=production, a fresh cwd per revision. Revisions: develop, #1321 head, END_TREE, #1310 head (the file-leak CONTROL) and a planted arm (#1321 + `ip` in FILE_LOG_FIELDS). Controls: stdout at develop carries every P1 sentinel (the instrument reads stdout): True; #1310 head: BOTH files carry every P2 and P3 sentinel (the instrument sees a file leak, as gate33 measured): True; #1321 head: the POSITIVE line is in combined.log (the capture reads the written file): True; the planted ip arm: the P3 ip sentinel reaches BOTH files, and at the unplanted head it does not (a one-key widen is visible): True; every probe ran (rc 0) at every revision: True.
- **VALUE sentinels in a FILE** (nested Error under `error` and `upstream` with config.headers.Authorization + response.data.token; a nested Error's toJSON and a top-level toJSON; secretKey, privateKey, passwordHash, mnemonic, phone, email_address, userEmails[], ip, jwt, sessionId, recipientPhone; the six ruled keys; a top-level Error's password): **#1321 head {'logs/error.log': 'NONE', 'logs/combined.log': 'NONE'}; END_TREE {'logs/error.log': 'NONE', 'logs/combined.log': 'NONE'}.** Under #1310's logger every nested-Error and unnamed-key sentinel reached both files (the control), so the instrument can see the leak it reports absent.
- **Every key any file line carries at the head:** ['error', 'level', 'message', 'method', 'path', 'requestId', 'service', 'statusCode', 'timestamp'] — the allow-list, nothing else.
- **Message and error text still reach both files:** {'logs/error.log': {'P4': True, 'P6': True}, 'logs/combined.log': {'P4': True, 'P6': True}}.
- **Disclosed loss (a consequence of the ruling, not a defect):** userId / documentId / ip / stack in the files at the head: {'logs/error.log': 'ABSENT (as disclosed)', 'logs/combined.log': 'ABSENT (as disclosed)'}. predict_1.out READ 27 single-line logger calls carrying documentId and 5 carrying userId in originate; errorHandler.ts loses userId and ip.
- **Residue by design (allow-listed strings):** {'logs/error.log': {'P7': ['String(Array) element', 'String(toString obj)'], 'P9': ['metadata message key', 'path query token', 'requestId']}, 'logs/combined.log': {'P7': ['String(Array) element', 'String(toString obj)'], 'P9': ['metadata message key', 'path query token', 'requestId']}} — gate33's W-3 (`error: String(<Array>)`, 75 originate call sites of that shape, READ) still reaches the files as a string; a secret put in `path` / `requestId` / a metadata `message` would too (no caller found logging req.originalUrl / req.url, READ).
- **STDOUT — the commission's "no value reaches ... stdout" does NOT hold, and never did:** at the head stdout still carries {'P2': ['error.config.headers.Authorization', 'error.response.data.token', 'upstream.config.headers.Authorization', 'upstream.response.data.token'], 'P2T': ['top-level meta toJSON()', 'upstream Error toJSON()'], 'P3': ['email_address', 'ip', 'jwt', 'mnemonic', 'passwordHash', 'phone', 'privateKey', 'recipientPhone', 'secretKey', 'sessionId', 'userEmails[]']}; at develop it carried every one of those plus the ruled keys. NEW at the head vs develop: **NONE**. So stdout is not a widen of #1321 (it improves nothing there beyond r2's six keys), and the PR body discloses it ("The Console is unchanged from #1310."). Kam's ruling says redaction stays on the Console. The prompt makes the gate measure and RULE it (§6 Q2).

### 1b. #1322 — READ predictions (the gate measures at runtime; the drafter ran no security code)
- Only the mint opts in to `rethrow` (index.ts :1140); revoke (:1286) and validate (:1354) keep the log-only swallow — their handlers take no `next` (READ).
- The KS-577 order holds as READ: save + rethrow :1140, in-memory drop :1142, `return` 503/500 :1145 — all before the rotate revoke at :1158, so a failed save never revokes the prior key.
- No-database mint: dbSaveApiKey sets memory first (:293) and returns before the INSERT (:294) — no throw, 201 from memory (C4).
- **Seat prediction slip (READ):** the #1322 body says "the newly reachable 503 is not declared in the spec"; security.openapi.ts already declares `503: commonErrorResponses[503]` on POST /api/security/keys (:797). The gate runs `check:openapi`.
- **Scope vs ruling:** Kam ruled b (all three routes); this PR delivers the mint third and says so (`Refs KS-888`). The prompt grades it as disclosed partial delivery (ONE-OF-THREE-ROUTES). TRANSIENT-REFUSES (08 / 57 now answer 503 instead of the ticket's log-only) is Wednesday's reading of the KS-1194 contract — carried as a Kam question, not a defect.
- Not pinned by the cells (the prompt owes them at runtime): the unsaved key's plaintext through validate; the rotate path under a failing save; a numeric / absent `code`; the refusal's own log line; stdout / process exit under the candidate arm with the DEFAULT reporter (the seat: `--reporter=json` hides the 2 unhandled errors).

### 1c. Other
- **Fleet STOP (READ, bounded region, NOT-FOUND control):** #1321 28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60) (PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.); #1322 28/0 · 6/0 · 49/0 · 60 passed, 0 failed, 0 skipped (of 60) (PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.). After this merge: 28/0 · 6/0 · 49/0 · 60 of 60.
- **Linear: both PRs link `contributes`; NONE `closes`** (linear_reads_1.out). KS-1348 and KS-888 In Progress (KS-888 was Backlog at the seat's boot; the board bot walked it).
- **Re-key / namespace (rekey_1.out):** rekey_check_gate35 | dir /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-28_gate35 | 18 file(s), 2283 line(s) | 61 forbidden spelling(s), 5 lineage-only | 85 lineage hit(s) ALLOWED by marker | RESULT CLEAN: 0 hit(s)
- **A drafting lesson recorded in predict:** this git's `grep -E` does NOT support `\s` (it gave 0 for documentId where `[[:space:]]` gave 27) — every predict grep now uses POSIX classes and carries a >0 control.
- **Sizes / sha256:** `2026-09-28_secuura-batch1321.prompt.txt` 42835 bytes sha256 `c1062a1650d2d1b6c578fb7930ffbe7bf4af9a2c6f6f2de2dc69c7beb5891b69`; `launch_qa_secuura_batch1321.sh` 18649 bytes sha256 `ddfc61a59caec64db414c9cb63101ba1964468284c76782a08fb7ed2ae1034f1`; `mail_gate35_ready.md` 16505 bytes sha256 `1a3a3a93da1fbf93e6c84c9a90658adec9f6e138696dd7cab9732b6ff6b891c3`.

## 2. Pins — predict_1.out (rc 0)
- #1321: 1 commit `52c96db4cf49` over merge-base `54f37d6399bd5eeb62a4c75220f42c106fad4b4a`; 0 behind develop; merged tree `9132b8264fade92d1c853f48c74f8e8e1fe192b5`; every merged blob == its head blob; numstat ['203\t0\tBlockchain/Dev/services/originate/src/__tests__/ks1348-production-file-logs-allow-list.test.ts', '41\t2\tBlockchain/Dev/services/originate/src/utils/logger.ts']; no mode change; move ∩ own paths EMPTY.
- #1322: 1 commit `4e8e11bdefd2` over merge-base `54f37d6399bd5eeb62a4c75220f42c106fad4b4a`; 0 behind develop; merged tree `dba4eae0a090d10eccf5cd909e19df82d8bd01a0`; every merged blob == its head blob; numstat ['145\t0\tBlockchain/Dev/services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts', '19\t2\tBlockchain/Dev/services/security/src/index.ts']; no mode change; move ∩ own paths EMPTY.
- Simulations: foreign1321 -> REFUSED: FAIL=10; foreign1322 -> REFUSED: FAIL=10; moved -> PASS: FAIL=0. `moved` = develop + one unrelated synthetic commit (must PASS); `foreign<n>` = develop + a foreign edit of that PR's first own file (must REFUSE). `predev` (`aee347c5f60a`, develop^) is the moved-develop pin in controls D / RC / RD / RE / RN / RO.
- Superseded, kept: `superseded_prelogprobe_*` — the first pinned run (predict before logprobe existed, so its WIDEN line read UNMEASURED) and a controls run stopped at control 5 once that was noticed; predict, fill and --check were re-run after logprobe, then the controls ran clean both ways.

## 3. What the gate owes
- Prompt `2026-09-28_secuura-batch1321.prompt.txt` — the #1321 LOG-FILE WIDEN through the real logger (files, stdout, text kept, the disclosed loss, #1310 as the file-leak control), the allow-list arms; the #1322 route table (no `sk_` in any refused body, unsaved not listed / not valid, each infra class, revoke / validate under a failing INSERT with exit codes and unhandled-rejection counts, the memory-only 201, the rotate order), the candidate arm under both reporters, `check:openapi`; every seat red proof re-run; suites at develop / head / END_TREE; tsc with `exclude: []`; lint (security has none); the MANDATED SQUASH TEXT blocks; `## MERGE ADDENDUM` last.
- Report dir `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-28-batch1321-g35/`; mail subject as in the prompt, FROM coagent@ TO wednesday-agent@.

## 4. Routing line — NOT added
Add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` (beside the other QA/Secuura batch lines — the previous kit pane line sits at line 135, READ) — backup first:
```
QA/Secuura-batch1321|coagent@agentmail.to|yes
```
Until it is present the launch action's step 0 refuses rc 1 (repin_dryrun_1.out: "line present: 0").

## 5. The ONE launch command
```
/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-28_gate35/repin_and_launch_gate35.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-28_gate35/launch_qa_secuura_batch1321.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4901153c-5db0-4cfc-bf83-c25726202b34/scratchpad/g35
```
- Dry run (`--dry-run` appended): repin_dryrun_1.out -> DRY RUN COMPLETE 2026-09-28T04:31:50Z — every read agrees with the pins; the real run continues with the usage gate, --check and cockpit.sh add (rc 0).
- Argument 2 may be ANY Claude session scratchpad dir (`/private/tmp/claude-501/*/scratchpad*`); if `g35_sp/clone.git` is absent there, predict rebuilds it on a re-pin (logprobe is NOT re-run by a re-pin). A develop move re-pins in the same action (step 3b); an own-path move, a stack, an overlap or an END-tree disagreement refuses rc 10. A new PR on KS-1348 / KS-888 or on a `-b37-<n>` branch outside the kit refuses rc 15. A moved head or a base not develop refuses rc 11.

## 6. Questions for Wednesday (each with the drafter's recommendation)
1. **The routing line** (§4). *Recommend:* add it, then launch.
2. **Stdout.** The commission says "confirm no value reaches either file or stdout". Measured: the files are clean, but stdout still carries the nested-Error, toJSON and unnamed-key values — exactly as at develop (nothing new), disclosed in the body, and inside Kam's "redaction stays on the Console". The prompt asks the gate to measure it and grade it as a pre-existing exposure carried forward, not a widen of #1321. *Recommend:* launch as drafted; if stdout is collected into log storage in production, that is a new Kam card (allow-list or value-walk the Console too), not a NO GO here.
3. **KS-888 scope.** Kam chose b (all three routes) over the recommended a; the PR is the mint only and the revoke / validate card is still open. *Recommend:* launch; GO on the mint as disclosed partial delivery; KS-888 stays In Progress.
4. **Transient faults now refuse the mint (503)** — Wednesday's reading of the KS-1194 contract. *Recommend:* confirm with Kam in the same card round as revoke / validate; a one-line narrowing if he meant structural-only.
5. **§5f:** both are runtime changes — neither moves to Done on offline evidence. *Recommend:* the merge seat posts the canonical `live sweep owed` comment.
6. **The disclosed loss** (userId / documentId / ip / stack out of the files). *Recommend:* accept as ruled; if operators need userId / documentId in the files, add them to FILE_LOG_FIELDS as a follow-up (the planted ip arm shows the allow-list is the single control point).

## 7. Controls: `controls_gate35.sh <scratchpad> [--invert]`
- **controls_1.out:** `SUMMARY gate35: 156 controls, OK 156, MISMATCH 0` (rc 0).
- **controls_2.out (`--invert`):** `SUMMARY gate35: 156 controls, OK 0, MISMATCH 156 (inverted: every control must MISMATCH-then-flip to OK; a MISMATCH here is a control that could not fail)` (rc 1, by design).
- Same arms as gate34's kit, re-keyed: wrong heads (one hex digit), a moved develop (predev), per-PR path renames, capture / prompt doctoring, every kit rule 35 / 40-44 / 46-51 SPLIT, the GO string and merge authority, the addendum, the verdict subject, a wrong END_TREE, a moved launcher, the non-TTY launch path, repin argv / routing / WIDEN by title and by branch / a false STACK / the REAL re-pin across a move in a copy / RE-RN-RO declaration plants, predict `--simulate foreign1322` and `moved`, fill from SIM / failed pins, SJ1-SJ3 subject plants, and NS[<spelling>] over gate34's and gate33's namespaces.
- Not controlled: exit 16 (needs a TTY), repin steps 4-6 (usage gate, cockpit add), a `mergeable=False` refusal, logprobe's verdicts beyond its five built-in controls.

## 8. Could not measure (the drafter's NOT-MEASURED list)
- No suite, tsc, lint or red-proof run by the drafter; the seat's figures are claims in its PR bodies (its raise/ holds no per-item red / green / suite files; its quarantine/ no tsconfig).
- #1322 at runtime: nothing — no `sk_` scan, no list / validate of the unsaved key, no revoke / validate under a failing INSERT, no rotate run. All READ only.
- #1321 through a real fail500 route or errorHandler (logprobe drives `logger.error` directly with shaped metadata), the error.log level filter, a non-string `message` — not measured.
- `check:openapi`, the served spec, Schemathesis, legs 3 / 4 / 8 — need a stack or were left to the gate.
- Whether stdout is shipped to persistent log storage in production (deployment config) — not read.

## 9. Files
- Kit: kit.json · COMMISSION.md (make_commission_gate35.py) · README.md (make_readme_gate35.py) · rekey_check_gate35.py -> rekey_1.out
- Pins: predict_gate35.py -> predict_1.out, predict_sim_*.out, pins_gate35.json (+ .SIM-*.json) · keyscan_gate35.py -> keyscan_1.out · final_lsremote_1.out
- Measurements: logprobe_gate35.py -> logprobe_1.out, logprobe_gate35.json (#1321 WIDEN)
- Reads: gh_read_gate35.py -> gh_read_1.out, gh_body_*.md, gh_comments_*.md · linear_reads_gate35.py -> linear_reads_1.out, linear_KS-*.md · capture_mail_gate35.py -> capture_1.out, mail_gate35_ready.md, stopcounts_gate35.json · _api_peek_gate35.py -> _api_peek_1.out
- Prompt/launcher: prompt_gate35.TEMPLATE.txt, launcher_gate35.TEMPLATE.sh.txt, fill_gate35.py -> 2026-09-28_secuura-batch1321.prompt.txt + launch_qa_secuura_batch1321.sh (fill_1.out), launcher_check_1.out · repin_and_launch_gate35.sh -> repin_dryrun_1.out · controls_gate35.sh -> controls_1.out / controls_2.out
