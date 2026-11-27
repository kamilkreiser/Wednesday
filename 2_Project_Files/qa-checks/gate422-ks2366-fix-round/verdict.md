PR 2296: NO GO (at head af5e35fb2d4b837acd428860dd0a877d384551ea; delta, tier 1)

# QA GATE 422, delta, tier 1: PR 2296 fix round (KS-2366 legacy certification anchor repair)

Gate: claude-opus-5-5, findings only. Started 2026-11-27T08:05:11Z, finished 2026-11-27T09:18:29Z (both from `date -u`).

**PR state:**
- Read at the start (gh as kksecura, 08:05:44Z): OPEN, head af5e35fb2d4b837acd428860dd0a877d384551ea, base develop 4764b2cfbc28768ef9c7b684e2af2e0f2f1438e5, 6 files, +1517 -0. Commits: 329fae8c, then af5e35fb.
- Re-read at the end: 09:18:10Z, as kksecura: OPEN, head af5e35fb2d4b837acd428860dd0a877d384551ea, base develop 4764b2cfbc28768ef9c7b684e2af2e0f2f1438e5, 6 files, +1517 -0 (unmoved).
- PR body: read as raw JSON through urllib (`_work/out/pr2296.json`, body sha16 b1600b92d5e016bf). It is byte-equal to the builder's `evidence/pr2296_body_after.md`.
- The delta 329fae8c..af5e35fb touches 5 files (+669 -116). `git diff --name-only 4764b2cf af5e35fb` over `services`, `packages` and `migrations` returns 0 files, so no product code is in the PR.

**My setup:**
- Clone: a fresh `gh repo clone` (`_work/repo`). Worktrees: `_work/head` (af5e35fb) and `_work/p329` (329fae8c).
- node_modules: copied with `cp -c` from the builder's `s-w79-fix` (same commit, porcelain 0). I built packages/shared and ran originate's `generate` myself.
- Postgres 15.19 (my own throwaway): data in `/private/tmp/g422/pg`, socket in `/private/tmp/g422/sock`, `listen_addresses=''`, TimeZone UTC. Schema built the suite's way: docker/init (11 files) plus 59 main-DB migrations, giving 115 tables.
- Fixtures: gate 421's own 63 synthetic rows (`_work/g422/fx.sql`, copied, unedited: 20 WRITE). Plus my 31 rows (`_work/g422/tsq.sql`: timestamp shapes and sentinel-forging text).
- Every tool and script: `_work/g422/`. Raw outputs: `_work/out/` (attacks under `_work/out/att/`).

## BLUF

- **NO GO, on one finding.** G422-1, a Blocker under this commission's severity rule: reverse still COMMITS a wrong restore from a forged manifest.
  - The new integrity guard checks BEFORE against AFTER everywhere EXCEPT the `blockchain` key, and never checks what that key holds.
  - So a manifest whose AFTER equals the live columns of ANY certification-class row can set BEFORE's blockchain blob to anything, and reverse writes it.
  - I wrote a forged "confirmed" blob, with a fake 64-f transaction, onto an unrepaired certification whose own anchor is simulated (R_SIM_TRUE). Reverse said COMMITTED, rc 0. The REAL `isAnchoredHonestly(presentBlockchainHonestly())` then answers **anchored=true** for it (false before).
  - The same forged row hidden among the 20 genuine rows passes too: the whole manifest is accepted and 21 rows are written.
  - The forger needs the row's live columns to the microsecond, which only a box superuser can read. That is the same precondition as G421-2, which gate 421 rated Medium and Wednesday ruled must be fixed before merge. This residual is that class, inside the certification class, and it is the meaning-changing write ("confirmed on chain") itself.
  - If Wednesday reads the superuser precondition as gate 421 did, this is a Major and the verdict would be GO WITH NOTES. The guard that would close it is cheap and inside the 6 files (see G422-1).
- **Everything else the fix round set out to do holds under attack:**
  - **The reverse mechanism.** The three documented commands, taken by program from the PR body (equal to the header) and run LITERALLY under zsh, bash 3.2 and /bin/sh with only the gate-421 docker substitution:
    - all work byte for byte: the whole-database hash returns to its pre-apply value;
    - output files are 0600 under a parent umask of 022;
    - `set -C` refuses a second apply (and a second reverse).
  - **Stream attacks.** Every truncation, interleaving and wrong-input stream fails closed with the whole database unchanged:
    - 35 hand-built streams (`stream_attacks.sh`, `stream_attacks2.sh`);
    - a sweep that cut pass 2 after every one of its 597 lines and mid-line on 158 more: 755 cuts, 0 changed, 0 rc 0, with a positive control.
    - Gaps (Lows): a `\.` line after pass 2 lets reverse commit and then runs whatever follows (G422-2). A stream without the script exits rc 0 (G422-3).
  - **Injection is data in every position.** That covers JSON values, keys and nested keys, box fields and hostile lines around the manifest, including psql meta-commands, `\.`, backticks and `$(...)`, and also a database AND a superuser whose NAMES are hostile (full dry/apply/reverse cycle, hash back to start).
    - Canaries: none created, no row changed.
    - The RAW control DID run the injected `\!` and an UPDATE.
  - **No manifest content or base64 on any argv or environment** during a lock wait, with a positive control.
  - **Every integrity term refuses whole**, rc 3, a quoted sentinel naming the check, whole database unchanged: 22 forgeries, plus the builder's F1 to F17 in the suite.
  - **G421-6:** about 2 million generated timestamps went through the guard with no raise. 19 shapes the builder did not list each refuse one row, and dry and apply complete.
  - **Gate 421's guarantees** re-run at the new head on gate 421's own fixtures: all hold.
  - **The predicate's meaning is unchanged** apart from the stated timestamp guard: a term-by-term diff shows only the guard plus four aid columns that decide nothing.
  - **W-1 is TRUE** at develop 4764b2cf and at develop as of 2026-09-17: nothing in anchoring confirms a DEMO_MODE mock row.
- **Re-runs (mine):**
  - new suite: 133/133, then 20 more runs under /bin/bash 3.2.57, 20 of 20 rc 0 and 133/133 each, so no flake in R10, R10b, R10c or L3 (21-26 s each, load 7-20);
  - run-shell-suites WHOLE 134 passed, 0 failed, 0 skipped (of 134), rc 0. Gate 421's skip did not recur with these installs;
  - docs-fragments OK;
  - portability on a copy: OK, planted rc 1;
  - 0 docker calls through a recording stub (21 suite runs at the head, plus two arms whose header the substitution cannot match).
- **Mutants:**
  - 31 of the builder's 85, re-made from its own edit list: all killed, each by its named cell. That includes all 9 of gate 421's former survivors and both apply terms.
  - The declared pair: each half alone IS sufficient (tested both ways).
  - 19 of my own: 7 killed by the builder's suite, 12 survived it. My judges see 10 of those 12 (suite gaps, Low, G422-5). Of the other 2, one is stricter (the safe direction) and one is equivalent on any realistic date.

## Gate 421's findings at the new head

| # | status at af5e35fb | evidence |
|---|---|---|
| G421-1 (Major) | **MET** | PRECONDITION in the header (`.sql` 42-48) and the PR body (lines 39-43). It claims no detection ("this script does NOT detect the mock"). Each dry ROW line prints `tx`, `block`, `slot` and `network` (seen on every row of my dry runs). W-1 re-derived: TRUE (below). The header's "why" sentence overstates the mock's mechanism (G422-6, Note); the precondition stays. |
| G421-2 (Medium) | **PARTLY** | Every listed term refuses the WHOLE manifest, 0 rows changed, rc 3, with a quoted sentinel. Tested by 22 forgeries of mine (table below) plus the gate-421 forged manifest (`forge_outside_class`: `live_row_outside_class`, db unchanged). Drift and repeat behave as ruled. BUT a forged blob INSIDE the class is written (G422-1, Blocker). |
| G421-3 (Medium) | **MET** (with Lows G422-2 and G422-3) | The literal dry, apply and reverse work under zsh, bash and sh. The manifest is on no argv. Files are 0600. `set -C` refuses an overwrite. The header says plainly the commands cannot be pasted into a `bash -s` body. The ssh form is honestly named NOT RUN. |
| G421-4 (Low) | **MET** | The KNOWN LIMIT sentence is in the header (`.sql` 38-40) and the body (45-47). The withdrawn E2 sentence is gone (cell HDR-LIMIT). DESIGN_ADDENDUM §1 corrects E2. |
| G421-5 (Low) | **MET** | `G5:apply_tenant_term` was killed by R10c and `G5:apply_external_id_term` by R10b (1 red cell each, my run). |
| G421-6 (Low) | **MET** | No raise over 1,995,840 generated strings (`ts_brute.sql`): every accepted one casts to exactly its own fields. 19 shapes beyond the builder's each refuse ONE row as `payload_timestamp_malformed`, and dry (rc 0) and apply (expected=32, COMMITTED) both complete. |
| G421-7 (Note) | **PARTLY** | Newline, CR, tab, space, VT, FF and the C0 controls are escaped: line-based readers see one SUMMARY. U+2028, U+2029 and U+0085 are printed raw, and so are NBSP and U+3000. A Python `splitlines()` reader sees 5 SUMMARY lines in my dry output and 15 in the apply output, and `str.split()` field counts vary (G422-4, Low). NUL cannot be stored (jsonb and text both reject it). |
| G421-8 (Note) | **MET** | DESIGN_ADDENDUM.md (builder's REC) corrects census rows 5a, 5b, 8, 9 and 10 and E2. Its row 8 repeats the mock "confirms the row" mechanism that W-1 refutes (G422-6). |

## Findings

### G422-1 (Blocker, by the commission's rule; Major if the superuser precondition is weighed as gate 421 did): a forged manifest makes reverse write a forged blockchain blob onto any certification, including a "confirmed" one
- **FOUND** at `ks2366-legacy-certification-anchor-repair.sql`:
  - 512-517: the two diff checks compare BEFORE and AFTER only after removing `blockchain` (`- 'blockchain'`).
  - 518-520: the class check asks only `certificationType IS NOT NULL AND external_id IS NULL` of the live row.
  - 528-538: the UPDATE then writes `metadata = m.before_metadata, certification_metadata = m.before_cm`.

  Nothing checks the CONTENT of BEFORE's or AFTER's blockchain key:
  - that BEFORE is a stuck-class blob (anchoringStatus `submitted`, no status, no txHash, no createAttempts);
  - that AFTER is the confirmed shape apply writes (same anchorId, a 64-hex txHash);
  - that the two copies agree;
  - that the anchor row named exists for this certification.
- **TESTED** (`_work/g422/forge_attacks.sh`, `forge.py`, outputs in `_work/out/att/`). Each forged row is built from the row's live columns as AFTER, with BEFORE = the same columns with the blockchain key replaced. The diff check is satisfied by construction.

| case | db | result |
|---|---|---|
| one forged row: R_SIM_TRUE (in class, REFUSED by the repair because its blob is simulated), BEFORE blob = `{status: confirmed, txHash: 64×f, network: preview, anchorId: g422-forged-anchor, …}` | gf4 | **rc 0, COMMITTED, reversed=1**; the row now holds the forged confirmed blob |
| the same forged row appended to the GENUINE 20-row manifest (target R_TS_PLUS1100) | gf5 | **rc 0, COMMITTED, manifest_rows=21, reversed=21** |
| BEFORE with the blockchain key removed, on U_STATUS_CONFIRMED | gf6 | rc 0, COMMITTED; the key is gone |
| control: the gate-421 out-of-class forgery | gf1 | refused, `live_row_outside_class`, db unchanged |

  What the REAL verify rule then answers (tsx over `routes/verification.ts`, `_work/g422/honest.ts`):
  - R_SIM_TRUE: anchored false before, **true** after;
  - R_TS_PLUS1100: anchored false before, **true** after.
- **Why it meets the rule:** "any stream or manifest that makes reverse commit a wrong or partial restore … is a Blocker even on unusual input." This restore is wrong, and it produces exactly the tier-1 harm: a public verify answering "anchored" for a certification whose anchor was simulated.
- **Why Wednesday may weigh it lower:**
  - Forging needs the row's exact live columns (updated_at to the microsecond), read by the box superuser who runs reverse. That person could also UPDATE the row directly.
  - No accidental, stale, truncated, other-box or double-pasted manifest can do this: I proved each fails closed.
- **Ask:** in the same `chk`, require for every row:
  - (a) BEFORE's effective blob (the class's COALESCE of the two copies) is in the stuck class, with no `createAttempts`;
  - (b) AFTER's `metadata.blockchain` equals AFTER's `certification_metadata.blockchain`, with `status = 'confirmed'`, a 64-hex `txHash` and the same `anchorId` as BEFORE;
  - optionally (c) the anchor row with that anchorId names this certification and carries that txHash.

  The worst a forged manifest could then do is turn an apply-shaped confirmed row back into a stuck one, which answers false: the conservative direction.

### G422-2 (Low): a `\.` line after pass 2 ends the tail's COPY early; reverse commits rc 0 and psql then runs whatever follows
- **FOUND:** the tail (`.sql` 588) is `COPY ks2366_reverse_rest FROM STDIN; SELECT pg_temp.ks2366_stream_ends_here(); COMMIT; …`. psql ends COPY at the first `\.` line, so the check sees only the lines before it.
  - The header (83: "commits only if NOTHING follows it"; 86: "input followed pass 2. Nothing was changed") and the PR body (67) say more than holds.
- **TESTED** (`stream_attacks2.sh`), on the documented stream plus a tail:

| tail after pass 2 | result |
|---|---|
| `\.` | rc 0, COMMITTED (harmless) |
| `\.` + an UPDATE | rc 0, COMMITTED; the UPDATE ran after the commit (title changed) |
| `\.` + `\! touch …` | rc 0; the canary file was created |
| `\.` + a third pass of the script | COMMITTED, then rc 3 "function … already exists". This rc 3 comes AFTER a commit, and the header's rc-3 list does not name it. |

  Without the `\.`, every tail is refused, rc 3, db unchanged: a comment, `\q`, `COMMIT;`, `ROLLBACK;`, `END;`, COMMIT without a newline, `\endif`, a third pass, the whole stream twice. Spaces and blank lines (and a lone CR) are allowed, as designed. A tail line holding a TAB fails closed: COPY reports "extra data".
- **Impact:** no wrong or partial restore. Whoever composes the stream already controls the SQL that follows. The claim is narrower than stated, and an rc 3 can follow a completed reverse.
- **Ask:** reword header line 2 and line 5 and the PR body (for example "commits only if nothing but blank lines follows pass 2, up to EOF or a `\.` line"), and add the post-commit rc-3 case to the header's rc-3 list.

### G422-3 (Low): when the script is missing from the stream, the documented reverse prints `rc=0` having done nothing
- **FOUND:** ON_ERROR_STOP is set only by the script (`.sql` 109); the documented psql lines (77-79) do not pass `-v ON_ERROR_STOP=1`.
- **TESTED** (`literal.py`, `bash_s.py`, `stream_attacks2.sh`):
  - The documented reverse run LITERALLY from a wrong working directory: `cat scripts/…` fails, the base64 lines reach psql as SQL (syntax errors) and the `\.` line errors. Result: **`rc=0`**, db unchanged, no SUMMARY line.
  - The same inside a `bash -s` body on a simulated box with `KS2366_REC` set: `rc=0`, and a 0600 output file is left on the "box".
  - A stream of only `\.`, or empty stdin: rc 0.
  - Comparison: the same wrong-directory run with `-v ON_ERROR_STOP=1` added to the psql line gives rc 3.
  - Dry and apply from a wrong directory fail at their `<` redirect (rc 1), which is correct.
- **Impact:** fails safe (nothing changes), but the printed rc says success. The header's "read the counts from the SUMMARY line" mitigates it.
- **Ask:** add `-v ON_ERROR_STOP=1` to the three documented psql lines (header and body).

### G422-4 (Low): G421-7 holds for line-based readers only; Unicode line and space separators are printed raw
- **FOUND:** `to_json` escapes C0 controls but not U+0085, U+2028, U+2029, NBSP or U+3000 (`.sql` 256-267 ROW, 135-136 BEGIN, 549-551 REVERSE_OF, and the manifest line 422-425, which is jsonb text).
- **TESTED** (`tsq.sql` rows Q_*, database gq1): anchorIds and networks carrying those characters plus a fake SUMMARY.
  - grep, awk and `split('\n')` see exactly 1 SUMMARY in each output, and every ROW line keeps 14 space-split fields.
  - Python `str.splitlines()` sees 5 SUMMARY lines in the dry output (the real one is last) and 15 in the apply output (inside the manifest line).
  - `str.split()` gives 14, 15 or 16 fields.
  - The reverse's own parser splits on `\n` and is unaffected; A1 still guards apply.
- **Impact:** a Python reader taking the first SUMMARY, or splitting fields on Unicode whitespace, can be misled by stored text. The product never writes such anchorIds or networks.
- **Ask:** escape every non-ASCII character as `\uXXXX` in printed fields (for example a `regexp_replace` over `[^\x20-\x7e]`), or tell readers in the header to split on `\n` and read the last SUMMARY.

### G422-5 (Low): suite gaps on the fix round's new code (10 of my 12 surviving mutants are observable)
The mutants were run through the builder's suite (`_work/out/mutants_g422.json`), then judged by my own attacks on the head and on the mutant (`judge.sh`, `_work/out/att/judge/`).

| my mutant (one edit) | builder suite | gate judge (head → mutant) |
|---|---|---|
| X:tail_ignores_comments (a `--` line after pass 2 counted as blank) | survived | trailing comment: rc 3 unchanged → **rc 0 COMMITTED** |
| X:diff_md_subset / X:diff_cm_subset (BEFORE may lack a key outside blockchain) | survived | BEFORE dropping a key: refused → **COMMITTED** |
| X:class_ctype_key (`?` instead of `->> IS NOT NULL`) | survived | a forged row whose certificationType is JSON null (U_CTYPE_JSONNULL): refused → **COMMITTED** |
| X:end_any_order (an END line anywhere counts) | survived | END line before the manifest: refused → **COMMITTED** |
| X:box_db_ci (case-insensitive db) | survived | db name in another case: refused → **COMMITTED** |
| X:ts_frac_unbounded (7+ fraction digits) | survived | R_TS_7FRAC and T_FRAC10: REFUSE → **WRITE** |
| X:leap_no_100 (every 4th year a leap year) | survived | 1900-02-29 and 2100-02-29 pass the guard and the cast raises: **the whole dry run aborts** |
| X:network_no_space_escape | survived | a network with a space: 2 ROW lines lose their 14-field shape |
| X:reverse_of_unquoted_user | survived | a hostile superuser name: REVERSE_OF goes from 4 fields to 5 |
| X:no_cr_trim | survived | a CRLF apply file: COMMITTED → refused (stricter, the safe direction) |
| X:leap_no_400 | survived | 0 verdict changes on my rows (only 2000-02-29 and similar; refuses, the safe direction) |
| X:tail_allows_one, X:pass2_no_begin, X:refused_needs_two, X:dup_by_pair, X:drift_counts_already, X:tx_unquoted, X:first_manifest_only | **killed** (L4:s_e, L4:s_e, F3, F12, D2, C5, F9) | - |

None of these is a defect at the head. Each is a guard that a later edit could remove without the suite noticing.

### G422-6 (Note): the PRECONDITION's "why" sentence, and DESIGN_ADDENDUM row 8, describe a mock mechanism the code refutes
- Header 44-46 and PR body 43 say the MockAnchoringProvider "stores a bare 64-hex sha256 as the 'transaction', status confirmed". The addendum's row 8 says it "confirms the row's own id … and NO chain".
- The lines they cite (`cardano/index.ts` 270-273) show demo-mode `submitAnchor` returning only `{ txHash, fee }`. The row is then written `submitted` (`anchorSubmission.ts` 855), and nothing confirms it (W-1 below).
- The PRECONDITION stays, as commissioned: the running image over the stuck range is unverified, and a refuted mechanism is not a refuted defect. The sentence should say what the code shows.

### G422-7 (Note): smaller observations, all fail-safe or cosmetic
- **"Names THIS box"** compares database and user NAMES only (`.sql` 508-509). Kintsugi and demo both run `-d secuura` as their POSTGRES_USER, so a demo manifest passes the box check on Kintsugi.
  - Harmless: other ids drift (nothing is written, rc 3), and a true copy of the box restores the same values.
  - The header wording overclaims. Wednesday's F13 is met only for a copy under another database name.
- **A row that became a lineage document after apply** makes a GENUINE manifest refuse WHOLE (`live_row_outside_class`), not drift as header line 63 describes for "a row changed since". Fail-safe.
- **BEFORE metadata:** a genuine manifest restores SQL NULL exactly (whole-database hash equal). A forged BEFORE of `{}` for an original NULL is accepted (the diff check treats NULL as `{}`) and restores `{}`.
- **Two reverses at once:** the second reports `COMMITTED_WITH_DRIFT drift=20`, rc 3, although the restore is complete.
- **Locks:** pass 2 holds its row locks until stdin closes. Under a stream held open 6 s, a writer timed out at 2 s. The documented commands close stdin.
- **`expected=0020`** is accepted as 20 and commits the right count.
- **Base64:**
  - CRLF base64 lines with an LF `\.` line fail closed ("end-of-copy marker does not match previous newline style");
  - CRLF throughout works.

## The reverse mechanism (item 1), as run

**(a) Literal commands** (`_work/g422/literal.py`, `_work/out/literal/`):
- PR body text == header text for all three; the docker wrapper occurs once in each.
- Run under zsh, bash and /bin/sh, each from Blockchain/Dev, parent umask 022:

| command | result (identical in each shell) |
|---|---|
| dry | rc 0, `stuck_class=54 write=20 refuse=33 live=1`, file 0600 |
| apply | rc 0, COMMITTED 20, 0600 |
| second apply | rc 1, "file exists" / "cannot overwrite existing file"; the apply file is unchanged |
| reverse | rc 0, reversed 20, whole database equal to before apply, 0600 |
| second reverse | refused by `set -C` |

- The run text differs from the documented text only by the wrapper and `<N>` (diff asserted by program).

**(b) Stream attacks** (`stream_attacks.sh`, `stream_attacks2.sh`, `trunc_sweep.sh`):

| stream | rc | database | message |
|---|---|---|---|
| base64 cut mid-line | 3 | unchanged | file_not_base64_of_utf8_text |
| cut mid-quartet | 3 | unchanged | file_not_base64_of_utf8_text |
| cut at a line/quartet boundary inside the manifest | 3 | unchanged | apply_output_incomplete, manifest_not_json |
| cut after the manifest, before END | 3 | unchanged | apply_output_incomplete |
| `\.` missing | 3 | unchanged | end-of-copy marker corrupt |
| pass 1 twice | 3 | unchanged | same |
| third pass appended | 3 | unchanged | same |
| pass 2 missing | 3 | unchanged | reached EOF without … \endif |
| script alone | 3 | unchanged | same |
| pass 2 = 329fae8c's script | 3 | unchanged | its own refusal |
| pass 1 = 329fae8c's script | 3 | unchanged | same |
| the whole stream twice | 3 | unchanged | |
| the manifest file is the script | 3 | unchanged | no_manifest_line |
| two apply outputs concatenated | 3 | unchanged | more_than_one_manifest_line, box_db_differs |
| another database's apply output | 3 | unchanged | box_db_differs |
| trailing tails | | | as in G422-2 |
| pass 2 truncated after every line 1..597, and mid-line for lines 441..598 (755 cuts) | 0 of 755 rc 0 | 0 changed | control: the full stream rc 0, changed |
| pass 2 = a mutated copy (stream-end check off) + junk | 0 | **changed** | expected: the stream's author supplies the SQL |

Can ANY stream make reverse commit a partial or wrong restore? Not from a genuine manifest: every partial stream I built changed nothing. A FORGED manifest can (G422-1). A `\.` tail runs extra SQL after a correct commit (G422-2).

**(c) Injection** (`inject.sh`):
- A manifest with the hostile set in every JSON value, in keys and nested keys inside BEFORE's blockchain, in `box.applied_at` and in `anchor_id`. The control set: quotes, `\`, `$$`, `:'manifest'`, `\!`, backticks, `$(...)`, an embedded newline + `\.`.
- Hostile lines before and after the manifest line: a bare `\.`, `\! touch`, an UPDATE, backticks, `$(...)`, `\set x '`…`'`, `:x`, `'; DROP TABLE documents; --`, `$$`, `\copy … to`.
- Documented (base64) stream: rc 0, reversed 20. **0 canary files, 0 injected rows.** The restored `certification_metadata` equals the manifest's hostile BEFORE exactly (20 of 20). REVERSE_OF stays one line with 4 fields.
- RAW control (the same file, no base64): the `\!` canary was created and the UPDATE ran. The test can fail.
- Hostile NAMES: database `g422'"\$$:'x' `d`` and superuser `g422u'"\$$ :'y'`. Dry, apply and reverse all rc 0. BEGIN and REVERSE_OF print the names as quoted JSON. The whole database returns to its pre-apply hash.

**(d) argv and files** (`argv.py`):
- While the literal reverse waited on a row lock (1 session in a Lock wait at the sample), none of these appeared in `ps -A -ww` args, nor in `ps -E` args+environment: the manifest marker, a JSON key, a cert uuid, base64 at the start and middle, applied_at.
- Positive control in the same sample: a psql given `-v manifest=G422PSQLCTL` WAS seen, as was `mode=reverse`. (My second control, a `sleep` carrying a marker, exited on a usage error before the sample, so it proves nothing.)
- Files 0600, and a second apply cannot overwrite: as in (a).

**(e) Stdin ownership** (`bash_s.py`):
- The header (89-96) and the PR body (72-74) say plainly not to paste these commands into a `bash -s` body, and name the ssh form NOT RUN. That is honest.
- What I saw, on a simulated box (an empty directory) with the documented reverse pasted into a `bash -s` body:
  - with `KS2366_REC` unset: rc 1 (the output redirect fails), nothing ran;
  - with it set: **rc 0, nothing done**, an output file left on the box (G422-3).
- The header's prose form (stream on the seat's machine, `ssh <box>` with the docker part quoted once more, redirect on the seat's side), built by me with a fake ssh that does what sshd does: rc 0, reversed 20. It works, but the header gives it only in prose, not as a command (text in `_work/out/literal/ssh_form_gate_built.txt`).

**(f) base64** (`b64variants.sh`). GNU coreutils is not installed here; its 76-column wrap was emulated with `base64 -b 76` and with `fold -w 76`.

| input | result |
|---|---|
| macOS default (one line, 29,780 chars) | decodes, reversed 20 |
| `-b 76` | decodes, reversed 20 |
| `-b 64` | decodes, reversed 20 |
| openssl (64) | decodes, reversed 20 |
| leading or trailing spaces, a blank line inside | decodes, reversed 20 |
| URL-safe alphabet on this data | decodes, reversed 20 |
| CRLF lines + a CRLF `\.` | decodes, reversed 20 |
| the whole stream CRLF | decodes, reversed 20 |
| CRLF lines + an LF `\.` | rc 3, unchanged |
| a bad alphabet | refused |
| padding stripped | refused |

## Item 2: one forgery per guard term (`forge_attacks.sh`; each against a freshly applied copy, whole-database hash before and after)

Every row below: rc 3, 0 rows changed, `KS2366_REPAIR_REFUSED mode=reverse checks=[…]` naming the check.

| forgery | checks named |
|---|---|
| box.db changed | box_db_differs |
| box.user changed | box_user_differs |
| box missing | box_db_differs, box_user_differs |
| duplicate id | duplicate_cert_id |
| duplicate id under another tenant | duplicate_cert_id |
| metadata: extra key | metadata_differs_outside_blockchain |
| metadata: key dropped | metadata_differs_outside_blockchain |
| certification_metadata: changed value | certification_metadata_differs_outside_blockchain |
| certification_metadata: changed certificationType | certification_metadata_differs_outside_blockchain |
| out-of-class row (U_NO_CTYPE) | live_row_outside_class |
| a genuine row whose external_id became non-null after apply | live_row_outside_class (whole refusal) |
| non-uuid id | row_field_invalid |
| upper-case uuid | row_field_invalid |
| rows an object / a string / null / missing | manifest_rows_not_an_array |
| zero rows | manifest_has_no_rows |
| manifest a JSON array / a string | rows_not_an_array + box_* |
| a row that is a string / an array | row_field_invalid |
| before_metadata absent | row_field_invalid |
| BEFORE metadata SQL NULL, genuine | rc 0; restored as SQL NULL; whole database equal to pre-apply |
| the same forged as `{}` | accepted (G422-7) |

- **Drift:** an updated_at-only touch on W_BASE gives `COMMITTED_WITH_DRIFT reversed=19 drift=1 drift_ids=["a4210000-…0001"]`, rc 3. W_BASE is left confirmed and the other 19 are restored.
- **Repeat:** `reversed=0 already_reversed=19 drift=1`, rc 3 (the drift remains). A clean repeat: rc 0, `ALREADY_REVERSED`.
- **The masking pair, both ways** (`pair.sh`, 7 refusal forgeries each):
  - integrity flag removed alone: 7 of 7 unchanged;
  - ROLLBACK replaced by COMMIT alone: 7 of 7 unchanged;
  - both removed (arm A3): 6 of 7 CHANGED, the zero-row case writing nothing anyway.

  **Each alone is in fact sufficient.** The builder's claim holds: neither is equivalent to absence, and no cell can tell either half's removal apart.

## Item 3: timestamps and quoting
- **Timestamps:** my rows in gq1, each a clone of W_BASE with one change. Every shape below reads REFUSE `payload_timestamp_malformed,payload_timestamp_outside_issue_window`; the control T_OK_CONTROL reads WRITE.
  - day 00, month 00, 2025-02-29, 1900-02-29, 2100-02-29;
  - `12026-…` and `+12026-…`, `-2026-…`;
  - 10-digit fraction, `+00:00`, `+11:00`, ` UTC`;
  - T24:00:00, second 60;
  - a JSON number, `infinity`, `epoch`, Arabic-Indic digits.

  Dry rc 0 (the whole database unchanged). Apply expected=32 rc 0 COMMITTED. Reverse rc 0 reversed 32.
- **Brute force:** 1,995,840 strings through the head's exact guard expression: 0 raises, 78,912 accepted, each accepted value equal to its own fields, and Feb 29 accepted only in 1600, 2000 and 2024 among the years tried.
- **Quoting:** as G422-4. A space, a newline and a CR in anchorId, and a space+newline network, keep every ROW line at 14 space-split fields and one SUMMARY for line readers.

## Item 4: unchanged guarantees (`unchanged.sh`, database gu1 = gate 421's fixtures)
- **Dry:** no mode means dry. Every table is unchanged (a per-table hash of all 115 tables). It also runs on a `default_transaction_read_only=on` session. Control: apply on that session fails with rc 3.
- **Count guard:**
  - 19, 21 and 0 give ROLLED_BACK;
  - `20 `, `x`, `1e1`, `-20`, 19 digits, 20 digits, unset, and a mode injection are all refused;
  - every one rc 3 with all tables unchanged.
- **Apply expected=20:** COMMITTED, REREAD 20 of 20. The documents rows changed equal the dry run's WRITE set exactly (20). The only table changed is `documents`. Key sets are exactly confirmedBlobOf's (with or without threadToken), and the metadata copy equals the certification_metadata copy.
- **Re-run:** the dry run then gives write=0, and apply expected=0 commits 0 rows.
- **The real product code** (the builder's own `_cells.ts` over my rows): R6 confirmedBlobOf equal 20 of 20, R7 false→true 20 of 20. The 43 non-written rows: anchored=false 43 of 43.
- **Reverse:** every table is equal to before apply. A repeat gives ALREADY_REVERSED, rc 0.
- **Predicate diff, term by term** (`_work/out/cls_329.sql` against `cls_head.sql`; the two head copies are byte-identical):
  - The ONLY changes are four selected columns (`row_tx`, `row_block`, `row_slot`, `row_network`; printed, used in no verdict) and the timestamp guard.
  - The guard's meaning changed only where 329fae8c either RAISED (impossible dates, year 0000, hour 25, month 13) or accepted what Postgres accepts but the product never writes (T24:00, second 60).
  - Every other term and the WHERE are identical. Gate 421's 54 verdicts are identical at both heads (`v_329.txt` = `v_head.txt`).

## Item 5: PRECONDITION and the W-1 claim
- The PRECONDITION is present and correct in substance in the header (42-48) and the body (39-43): it requires non-DEMO_MODE or an on-chain look-up, and a seat that can show neither does not apply. It claims no detection. Its "why" wording is G422-6.
- The dry run prints tx, block, slot and network per row, WRITE rows included.
- The G421-4 limit sentence is present and honest.
- **W-1, re-derived from develop 4764b2cf: TRUE.** On the code, a DEMO_MODE mock row is never taken to confirmed:
  - **The mock's confirmation has one use, and that use has no caller.** `MockAnchoringProvider.waitForConfirmation` is used only at `cardano/index.ts` 336, inside `submitAndConfirmAnchor` (326). `git grep -w submitAndConfirmAnchor` finds 1 occurrence (the declaration) at 4764b2cf, at fa887f382 (develop as of 2026-09-17), at fb6a2f984 (where the mock was wired) and at e50dbde98. `git log -S` lists only e50dbde98, so the count never changed.
  - **Demo-mode submission returns only the hash.** Demo-mode `submitAnchor` (270-273) returns only `{ txHash, fee }`. anchorSubmission then writes `status: 'submitted'` with that hash (855).
  - **Every confirmed write needs a chain answer.** The writers are `confirmRowWith` 476 (via `pollMember` and `deps.confirm`), 612 and 866 (`deps.confirm`). `deps.confirm` is `waitForConfirmation` (index.ts 1180, 2008), as are index.ts 2187 and the reconciler's `checkTx` (index.ts 2376, used at `reconciler.ts` 218 and 324). All of these end in `getTransaction`.
  - **There is no chain client in demo mode.** `getTransaction` returns `undefined` with no Blockfrost client (`provider.ts` 477-479); at fa887f382 it returned `null` and `confirmation.ts` confirmed only `if (tx)`. The client is created only by `initProvider` (`cardano/index.ts` 93; 78 at fa887f382), in the non-demo branch after the demo branch has returned (60-69).
  - **The other confirmed sites do not confirm a mock row.** The `mock_tx_` and `mock_batch_tx_` writers (index.ts 2072-2096, 2277-2300) sit behind `isCardanoReady()` returning first (2054, 2136; demo sets ready true). They write prefixed hashes, which the predicate refuses anyway.
  - **Limits:** two code points, not the running image. Merge-commit diffs are not walked by `-S`. Nothing was executed. Writers outside anchoring (the demo seed, the legacy copy) insert no payload and are refused by E1.

## Item 6: evidence
- **New suite at the head:** 133 of 133, rc 0, 31 s, with the docker stub first on PATH (`_work/out/suite_head_run1.log`). Then 20 more runs under `/bin/bash` (3.2.57), stub on PATH: 20 of 20 rc 0, 133/133 each (`_work/out/suite_repeat20.txt`). The builder's claim of 133/133 and 20 clean repeats is confirmed.
- **run-shell-suites.sh WHOLE** (`_work/out/run_shell_suites.txt`, 08:52:58Z to 09:16:38Z, load about 8 to 12): `shell suites: 134 passed, 0 failed, 0 skipped (of 134)`, rc 0. The builder's 134 of 134 is confirmed.
- **docs-fragments check:** `OK` (flow 117 legacy + 323 new, cheat 112 + 323; the same 2 ADVISORY lines gate 421 saw).
- **Portability rules on a copy of the suite outside `__tests__`:** `OK — 7 portability rules hold`, rc 0. A planted `readarray` gives rc 1. The real `__tests__` gives rc 2, "vacuous". All three of the builder's results reproduce.
- **No service file in the PR:** `git diff --name-only 4764b2cf af5e35fb -- Blockchain/Dev/services packages migrations`: 0 files. `services/` is identical at the head and at develop.
- **Mutants** (`_work/g422/mut_g422.py`, which imports the builder's edit list verbatim from its `mutants_w79.py`, sha16 9dfe90be4d4cd12b; results in `_work/out/mutants_g422.json` and suite logs in `/private/tmp/g422/mut/`). Each mutant got a probe first, in which dry, apply and reverse must reach their SUMMARY (a parse failure is not a kill), then the builder's suite through its seam. The real file's sha256 was unchanged after every mutant.
  - **The builder's, 31 sampled, all KILLED, and each named killer is among the red cells:**
    - the 9 former survivors: `G:class_status_strnull` (R1 "1 O_* rows were listed"), `G:blob_sim_zero_ok` (R1:N_BLOB_SIM_ZERO), `G:anchorid_join_ci` (R1:N_ANCHORID_CASE), `G:rowhash_no_lower` (R1 WRITE set, R6), `G:paydoc_ci` (R1:N_PAYDOC_UPPER), `G:pt_upper_half_s` (R1:N_TS_LATE_HALF), `G:ts_regex_offsets` (R1:N_TS_OFFSET), `G:reverse_cas_no_updated_at` (R5b), `G:blob_network_const` (R2, R6);
    - the two apply terms: `G5:apply_tenant_term` (R10c), `G5:apply_external_id_term` (R10b);
    - the reverse guards: `C1:box_db` (F3), `box_user` (F4), `dup` (F5), `diff_md`, `diff_cm` and `class_live_ctype` (F1), `class_live_extid` (F17), `stream_end` (L4), `pass1_if` (D2, R4), `drift_exit` (D1);
    - the command, timestamp and quoting edits: `C2:noclobber_apply` (L1), `C3:dim_check` ("R1: the dry run exited 3"), `C3:second_range` (R1:N_TS_SEC60), `C3:leap_rule` (R1 WRITE set, R6), `C4:quote_anchor` and `C4:space_escape` (R1:N_AID_NEWLINE), `C5:slot_printed` (Q2);
    - the older guards: `apply_count_guard` (A1), `reverse_cas_guard` (D2), `p_row_tx64` (R1:D37).
  - **The declared pair:** `C1:refuse_flag_where` and `C1:refuse_rollback` each SURVIVED (0 red), as declared. My direct test (item 2) shows each alone is sufficient.
  - **Mine, 19:** 7 killed (`tail_allows_one`, `pass2_no_begin`, `refused_needs_two`, `dup_by_pair`, `drift_counts_already`, `tx_unquoted`, `first_manifest_only`). 12 survived the builder's suite, 10 of them seen by my judges (G422-5).
- **Red-first:**
  - **Arm A:** 329fae8c's script through the seam, with the head's suite. 79 cells red and the run aborts. The red is behavioural: R9 and R9b fail on `ERROR: date/time field value out of range` from the old cast on the new fixtures (G421-6), and the header, reverse and literal cells fail because the old script has neither the text nor the file-consuming reverse.
  - **Arm A3:** the head with both refusal defences removed. 17 red, F1 first. The red is behavioural: F1 to F17 write their forged rows, and my own forgeries changed the database in 6 of 7 cases.
  - The builder's middle arm (329fae8c plus only the timestamp guard) was not reproduced; the commission required the first and third arms.

## Item 7: docker
- **Exec sites read** (the suite at the head, every line naming `docker`, `bash -c`, `bash -s`, `sh -c` or `eval`):
  - Every database call goes through `$PGBIN/psql`.
  - The only places that execute header text are `lrun` (test.sh 479-483) and the two STDIN bodies (500, 503). Each refuses unless the substitution check passed AND the text no longer names `docker` (481-482, 500, 503).
  - `eval` (473) only assigns a variable.
  - No line invokes docker.
- **Positive control:** the recording stub (`/private/tmp/g422/stub/docker`, which appends its argv to a log and exits 97) recorded `ps` when called through the same PATH (`control_calls.log`).
- **Runs with the stub first on PATH, all with 0 calls** (no `docker_calls.log` was ever created):
  - 21 runs of the suite at the head;
  - arm A (329fae8c's script; it aborts before L1, so it does not reach the guard);
  - a copy of the head whose reverse header line reads `docker  exec` (two spaces), so the substitution cannot match: 6 L1/STDIN cells print `NOT RUN` and 7 cells fail, and docker is never called.
- **The builder's declared slip is fixed:** the suite cannot run a docker command from the header, even when the header and the substitution disagree.
- **Not met:** "on a machine where Docker IS running". The Docker daemon on this Mac is not running, and I did not start it (it is shared with other seats). The stub stands in, and it would record any call whether or not a daemon is up.

## NOT TESTED (listed, not attempted)
- Any box (Kintsugi, demo, production); the box container's busybox `sh` and its psql; `docker exec` itself; a real ssh hop (the prose form only through a fake ssh).
- GNU coreutils `base64` (not installed here; its 76-column wrap was emulated).
- The anchoring service running; any chain lookup; the running image's commit over the stuck range (W-1 is a code reading at two commits).
- The verify ROUTE over HTTP (the real rule functions were driven over tsx instead).
- The four platform suites; originate jest, tsc and shared vitest (no product file in the PR; gate 421 ran them at the parent head).
- The builder's other 54 mutants.
- A real Docker daemon: it is NOT running on this Mac (`docker info`: cannot connect), so item 7's "with Docker running" condition could not be met. The recording stub stands in for it.

## Process disclosures
- **Files:** I wrote only inside this gate folder (`verdict.md`, `STATUS.md`, `_work/`) and under `/private/tmp/g422` (cluster, sockets, scratch, mutant copies, the stub). Everything else was read only, including the builder's trees `s-w79-*` and its REC (node_modules were copied out of `s-w79-fix` with `cp -c`), and gate 421's `_work/g421` (four files copied, never edited).
- **Clone:** I cloned into `_work/repo` with gh as kksecura and fetched af5e35fb there. gh was otherwise read-only; the token was read inside python and never printed.
- **Nothing outward:** nothing pushed, commented, written to Linear or GitHub, merged or deployed. No box, ssh, keyscan or docker contact.
- **Shell rules:** no `cd` in any command I ran; one heredoc that contained `cd /dev/null` was REFUSED by the hook before it ran. No `rm`: old outputs were moved. No shell word starting with `=`. Every time is from `date`.
- **Slips:**
  - **Discarded stderr.** One watch loop used `pgrep -f 'run-shell-suites.sh' >/dev/null 2>&1`, which discarded stderr against the rule and selected by a text pattern. It only read, killed nothing, and its result was not used.
  - **rc misread.** In two places I read `rc=$?` after a pipeline or a command substitution (the `cp -c` loop's `| tail`, and the stub-arm echo where `$(basename …)` came first). Those rc values were not used as evidence: the copies were checked by listing, and the arms by their cell lines.
  - **Shared database name.** One `unchanged.sh` run let `expected=0020` commit into the shared database, which scrambled that run's sequence. I re-ran it with that case moved to a fresh copy, and both results are reported.
- **Postgres:** my cluster (`/private/tmp/g422/pg`, socket only) was stopped by `pg_ctl stop`, rc 0, at 09:18:19Z. After that, 0 processes reference `/private/tmp/g422`. The data directory is kept. No other postgres was touched; I selected by data directory, not by name.
