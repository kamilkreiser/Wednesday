GATE B1504: GO WITH FINDINGS @ 311c69a on main b14467e

Gate: independent QA, tier 2 (Sonnet), Security Composer, 2026-11-11 16:11 to 16:22 AEDT. Own clone and scratch under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s267/gate1504/` (push URL invalid, nothing pushed). Heavy lock taken by mkdir for every docker or node job and released by mv into the gate's own quarantine folder; planted-lock control waited (rc 75), free-lock control took it. Load1 16.7 to 22.6 at the reads (two reads 4 s apart, not independent). No Blocker, no Major. Four Minors.

# Refs and scope
- `git ls-remote` (deploy key): branch `b1504/composer-lane-c-stack-deploy-hygiene` = `311c69a176bde29c80b303e810d797bc427277ab` = the READY sha; main = `b14467e20402f955a81b95b929490ff557ec5c2c` (read at start and again at the end). Merge-base of the branch and main = main.
- Three commits on main. Changed paths (6): `DEPLOY.md`, `scripts/ci.sh`, `scripts/up.sh`, `scripts/stack-diagnostics.sh`, new `scripts/objects-pin-test.sh`, new `scripts/objects-volume-hint-test.sh`. All 6 of 6 are inside the lane's PARTITION. No existing test file is edited (`git diff --name-status` shows only M on the 4 owned files and A on the 2 new tests). No `compose.yaml`, `package*.json`, `docker/`, `packages/` byte.
- Open PRs #85, #86, #91 (fetched by `refs/pull/<n>/head` through the deploy key, not through the API): file lists 57, 2, 2 files; overlap with the 6 lane paths = 0 for each (control: #85 holds `document-pdf`, count 1). Other kits of this sweep were not read: overlap with them not checked.
- Identities: all three commits `88359143+kamilDatasec@users.noreply.github.com | same`, as stamped. One trailer per message (count 3 of 3).

# Merge
`git merge-tree --write-tree origin/main <head>`: rc 0, tree `f8d255d7baf911c26efaf5af64503d5167a41d7c`, which equals the head tree. The merge is clean and equals main plus the head blobs.

# Findings
| # | Sev | Finding | Evidence |
|---|---|---|---|
| 1 | Minor | The 0020 section still says Route B is "as above" at `DEPLOY.md:144-145` (`**Route B** and **roll forward** are as above`), two paragraphs above the new sentence that says Route B exited 1. The new sentence is true, but the section as a whole is not made consistent by lines 150-151 alone. This was foreseen by the answer and is outside the partition; the builder lists it. Same pattern at `:462` (0025, measured to refuse by the builder's Part 21b; I did not re-measure 0025). | `sed -n 144,152p DEPLOY.md` at head |
| 2 | Minor | Three words of the hint (`hint`, `stopped`, `because`) are not in `compose.yaml` at base or in the ticket text, so the kit's property wording ("every word in compose.yaml, the ticket or the volume's name") does not hold literally. They are in the WORDS-27 slot's own text, which the stamp returned `AS PROPOSED`, and the printed line equals that text byte for byte. Not a STOP. | word trace below |
| 3 | Minor | Coverage edge, disclosed by the builder and unchanged by this gate: on an empty root-owned volume the real image prints `file access denied`, not `Unable to write to the backend`, so no hint fires. The hint covers the documented hazard (a volume with data the old pin wrote as root). Adding the other phrase is a new trigger and new words. | builder's `runs/p27-real-image-control*.txt`; not re-run (needs the image and objects run) |
| 4 | Minor | Builder-side claims I did not reproduce: the objects-only real-image runs (a, b, c), the registry read of P-26a, and the 0021, 0022-0027 Route B measurements. Reading their evidence files, they are internally consistent (controls fired); marked not shown by this gate. | see Claims |

# Press points

## (a) DEPLOY.md
- `git diff -U0 origin/main <head> -- DEPLOY.md`: one hunk `@@ -150,2 +150,3 @@`: main's lines 150-151 replaced by 3 lines; 3 added, 2 removed; nothing else. Control: the hunk header names the two lines, and the removed text is exactly the old last sentence ("Not yet run end to end on a seat stack (B61 ran the database test only)").
- The new sentence: "Measured on 2026-11-11 on a throwaway database, not a seat stack: restoring a 0019 dump onto a 0020 database exited 1 on the foreign key that 0020 adds on `content_release_pkey`, and nothing changed." It carries no command, no step, no instruction, no exclamation mark, and no word about a live environment.
- Truth, at source: `packages/db/migrations/0020_generate_issues_kept.sql:20-21` adds `last_generate_content_release_id uuid CONSTRAINT policy_version_last_generate_content_release_id_fkey REFERENCES content_release`. The builder's run `p21-run1.txt`: Route B exit 1, `cannot drop constraint content_release_pkey on table pc.content_release because other objects depend on it`, ledger still 20 ("nothing changed"), positive control (0019) exit 0, negative control (0021) exit 1, planted fault seen.
- **Independent spot-check of the 0020 refusal (the one the commission allowed), re-run by this gate** in a different harness (a throwaway `postgres:16` at the project's digest, `--internal` network `pc-g1504-scnet`, container `pc-g1504-sc`, bootstrap.sql and the product's migrations 0001-0019 applied as `pc_owner` by psql, `pg_dump -Fc` = 512 list entries, 0020 applied, then `pg_restore -U composer -d composer --clean --if-exists --single-transaction --exit-on-error`): exit 1; first line `pg_restore: error: could not execute query: ERROR:  cannot drop constraint content_release_pkey on table pc.content_release because other objects depend on it`; DETAIL `constraint policy_version_last_generate_content_release_id_fkey on table pc.policy_version depends on index pc.content_release_pkey`; the six `last_generate*` columns still present (6). This reproduces the builder's exit code, subject and "nothing changed". (This harness applies the SQL files by psql and does not write the ledger, so it does not re-measure the ledger count; the builder's run does.)
- `prettier --check DEPLOY.md` at head (host node, scratch copy): rc 0; control (a misaligned table file) rc 1.
- The two DEPLOY.md readers (`packages/db/test/b616-deploy-commands.db.test.ts`, `b778-route-b-script-complete.db.test.ts`), run on the host with vitest 4 against a throwaway `postgres:16` (container `pc-g1504-pg`, published only on 127.0.0.1:9681), at base and at head, compared by file, name and status with `python3 -I`: base 170 passed 0 failed; head 170 passed 0 failed; lost 0, added 0, changed 0. Control that can fail: a plant in a scratch copy (a double-quoted `!` added to a command in the 0026 section) makes 3 rows fail (167 passed, 3 failed). Honest limit: a plant on the Route B command (line 101) and one on a 0021 "Proven on" word were NOT seen by these readers (170 still pass), so the readers do not read lines 150-151 or the 0019 Route B command; they cannot be sensitive to this change, which is the expected reason they stay green. A census: the two files are the readers; the builder's census found the same two.

## (b) The two new shell tests, red under the plant, green restored
Scratch copies of head (via `git archive`), one plant each; the real clone is untouched.
| Test | Plant | Result |
|---|---|---|
| `objects-volume-hint-test.sh` | remove the `print_objects_volume_hint <<<"$logs_text"` call in `print_failed_services` | rc 1, 1 FAIL: "the phrase in the objects log: output differs from the expected text" |
| `objects-volume-hint-test.sh` | the hint is applied to every other service's log too | rc 1, 1 FAIL: "the phrase in another service's log: the hint was printed" |
| `objects-volume-hint-test.sh` | the function prints for any text (`cat >/dev/null; if true`) | rc 1, 5 FAIL (no-phrase, other-service, function-unit x2, `up.sh` no-phrase) |
| `objects-volume-hint-test.sh` | `up.sh` stops piping the logs to the function | rc 1, 2 FAIL (`up.sh` hint row, rc 7 row) |
| `objects-volume-hint-test.sh` | base scripts with head's test | rc 1, 8 FAIL / 8 PASS (reasons: `print_objects_volume_hint: command not found`, no hint after the objects logs, `up.sh` read no objects logs) |
| `objects-pin-test.sh` | one digit of the compose.yaml comment digest changed (`...7090` to `...7091`) | rc 1, FAIL "the two digests differ: scripts/ci.sh has ... and compose.yaml has ...", "objects-pin-test: RED" |
| Restored (head, untouched) | none | `objects-volume-hint-test: GREEN` rc 0; `objects-pin-test: GREEN` rc 0 (14 rows) |
The pin test has no red at base by design (nothing is wrong at base); its own planted-pair controls are in the file (equal pair accepted; one character apart, a missing side on each file, a short digest, a long digest and another image each refused; readers on planted files: right shape, absent, twice), and the builder's `p26b-wrong-function.txt` shows them red against an always-accept function. Not repeated by this gate beyond the digest plant above.

## (c) Unedited existing test and ci.sh lines
- `scripts/stack-diagnostics-test.sh` is not in the diff. It is GREEN at base (rc 0) and at head (rc 0).
- `scripts/ci.sh`: `git diff --numstat` = 2 added, 0 removed. Base lines 111, 123, 124 appear at head byte for byte (full-line `grep -x -F` count 1 each, at head lines 111, 125, 126; the two added `step` lines sit between 111 and the following step). The test's row 4, which reads these three lines by their whole text, is green.
- `bash -n` ok on all 5 touched scripts. `shellcheck`: not on the PATH, not run.

## (d) Hint words and secrets
- The printed hint (`scripts/stack-diagnostics.sh:35`), after unescaping the quotes, equals the kit's WORDS-27 text byte for byte (`[ "$line" = "$kit" ]` true; the kit text was taken from the WORDS CARD proposal, which the stamp returned as `AS PROPOSED`). Word trace (case-insensitive fixed-string, c = in `compose.yaml` at base, t = in the ticket text quoted in the kit): `objects` ct, `it` ct, `cannot` c, `write` ct, `to` ct, `its` c, `volume` ct, `Unable` ct, `the` ct, `backend` ct, `Recovery` t, `chown` ct, `-R` ct, `65532:65532` t, `on` ct, `or` ct, `use` ct, `a` ct, `new` ct, `project` ct, `name` ct; not traced: `hint`, `stopped`, `because` (Finding 2). The volume name `${PC_COMPOSE_PROJECT}_objects-data` is right: `compose.yaml:174` declares `objects-data`, `scripts/common.sh:14` runs `docker compose -p "$PC_COMPOSE_PROJECT"`.
- Added lines (401) and the three commit messages: secrets scan with the project's own `scripts/gitleaks.toml` through host gitleaks over the six changed files: "no leaks found"; control (an AKIA-shaped key and a URI credential in a scratch file) "leaks found: 1". My pattern scan for key shapes, URI credentials, UUID or tenant ids, `new RegExp(`, `innerHTML`, `child_process`: 0. Hosts: the only hit is the planted-pair test's `quay.io/minio/minio@sha256:abab...` image name (a digest-shaped fixture, not a live reference). The three secret-shaped names in added lines (`db_secret`, `PC_DB_PASSWORD="$db_secret"`) take a value from `openssl rand` at run time; the test assembles the URL `@` at run time (as the builder's STATUS says its first commit attempt was refused for that reason and fixed). Hint output carries no credential: the test has a row for that, with a control that the fake log does carry one.
- Name scan, underscore-aware `(?<![A-Za-z])<name>(?![a-z])` with `re.I`: the standard ban list (Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite) and the builder's 8-name list (read from its `names.txt`): 0 hits each over added lines plus messages; each name's planted `x_by_<name>_y` control fires. Cf characters: 0; non-ASCII in added lines and messages: 0. B-number, PCOMP, coordinator and weekday words in added lines and messages: 0 (control `B1504` fires).
- CodeQL pre-scan over added lines: no JavaScript or TypeScript added; `new RegExp(`/`innerHTML`/`child_process` = 0; the only regexes are in bash. No hit. Hosted CodeQL is not claimed.

# Claims (builder's STATUS)
| Claim | Grade |
|---|---|
| Refs: branch at `311c69a1`, three commits, main `b14467e2` | true |
| `DEPLOY.md` diff only main's lines 150-151 (3 added, 2 removed) | true |
| New sentence is a measured fact with no command | true |
| Route B refuses at 0020 with the content_release_pkey error | true (independent re-run, exit 1, same error) |
| Both DEPLOY.md readers: 170 rows at base and head, lost 0 | true (170 and 170, lost 0, host run; not the project's node 22 image) |
| `stack-diagnostics-test.sh` green unchanged; `ci.sh` lines 111/123/124 intact | true |
| `objects-volume-hint-test.sh` red at base (8 FAIL / 8 PASS), green at head (16 rows), plants red | true (8/8 at base; both plants red) |
| `objects-pin-test.sh` 14 rows green; digest plant red; always-accept function red | true for the first two; third not shown by this gate |
| Hint equals WORDS-27 byte for byte | true |
| P-26a: the pin resolves, amd64 and arm64, all-zero control exit 1 | not shown by this gate (registry read not repeated; the evidence file is internally consistent) |
| P-27 (v) real-image control (a)-(c) and the "empty root-owned volume gives `file access denied`" edge | not shown by this gate (needs the pinned image; evidence read, consistent) |
| Part 21b: 0022, 0024, 0025 refuse; 0023, 0026, 0027 restore | not shown by this gate (0020 only was re-measured) |
| lint / format:check / typecheck / build rc 0 at head | not shown (only `prettier --check DEPLOY.md` re-run here, rc 0) |
| `secret-scan.sh --tree` rc 0 | true for the changed files (host gitleaks, project config); whole-tree scan not run |

# NOT RUN
- The project's CI-stage Docker image (node 22): `docker build` of `docker/Dockerfile --target ci` with `--network none` failed at `npm ci` (the layer was not cached), and a build with network would reach the npm registry, which this gate may not. The DEPLOY.md readers were run on the host (node 26.13, the project's older `node_modules` copied into a scratch tree) instead. Hosted checks and the project's own runs remain the proof for the full `ci:node` and `ci:db` suites.
- `scripts/ci.sh` whole (starts a stack and copies the product owner's text into a container; the kit says never), `npm run lint`, `format:check` for the whole repo, `typecheck`, `build`, the whole-tree `secret-scan.sh --tree`, `compose-db-healthcheck.test.ts` (the workspace project; this change does not touch `compose.yaml`).
- P-26a registry re-read (one anonymous read was allowed; not used), the objects-only real-image runs, Route B at 0021 to 0027, `shellcheck`, an amd64 run, `up.sh` for real.
- Overlap with the other kits of the same sweep; the open/closed state of PRs other than #85, #86, #91 (no API call was made).
- CodeQL: hosted only, Tuesday reads it on the PR. A merge of this branch triggers no deploy (Composer deploys only on the product owner's card; the repo has no deploy workflow, per the kit).

# Resources of this gate
Containers `pc-g1504-pg`, `pc-g1504-sc`; networks `pc-g1504-scnet` (and the build attempts left no image); all gone (`docker ps -a` and `docker network ls`, count 0 each). Ports 9680-9689: listening 0 after. The project lock was taken and released five times, always by mv of the lock directory into `gate1504/quarantine/`; none left under `.tools/`. Scratch copies (including copied `node_modules`) remain under `gate1504/scratch/` (the hook forbids deleting; nothing outside the gate folder was written).
