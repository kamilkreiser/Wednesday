STARTABLE: YES (measurement always; the DEPLOY.md edit only if the seat's own run meets OUTCOME A and PART-WORDS reads BUILD)

# B1604 drafter report: Security Composer lane PC-C, PCOMP-128 item 2 (the 0022 Route B form)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1604_SEAT-C104_composer-lane-pc-c-0022-route-b-measure.md` (142 lines; sidecar `.measured` 115 lines, `stamp_check.py` rc 0). Drafted 08:05:40 to 08:12:47 AEDT (`date` printed both).

## BLUF
- **The sweep's framing is partly wrong, and the kit corrects it.** The sweep says "measure it the way B1569 measured 0023: one-step restore, ledger rows read back". The one-step command at 0022 was ALREADY measured on 2026-11-11 and refuses (exit 1, `cannot drop schema pc because other objects depend on it`, ledger 22; B1504 evidence `p21c-0022-0027.txt:14-17`). The ticket's own item 2 says so: the one-step refuses, "but the form this section gives has not been run". The form the 0022 section gives is 0021's two-step block with `DROP FUNCTION IF EXISTS pc.assert_exception_scope_in_engagement();` added to its piped drop line (`DEPLOY.md:357-358`). That is what the kit measures; the one-step is re-run only as M1 (to print its DETAIL lines, which the old evidence lacks).
- Kit = 4 controls (K1 0019 one-step positive, K2 0021 one-step negative, K3 the 0021 two-step block as written, K4 planted fault) + M1 (one-step at 0022), M2 (reading A, the section's own words), M3 (reading B, report only), M4 (the block without the new statement), on throwaway `postgres:16` containers on an `--internal` network. Seat rebuilds the harness from `p21.sh` and `p21-node.mjs` because **B1504's `p21c.sh` is not in its evidence folder** (`ls harness | grep -c p21c` printed 0).
- **Words are frozen before the measurement, with three slots** (`{DATE}`, `{PGV}`, `{RCX}`); every other number in them is a frozen prediction that the run must reproduce. The OUTCOME table makes a mismatch a STOP with no edit (B: M1 differs; C: the section's form fails a frozen check, which then needs the product owner; D: the added statement was unnecessary). Edit = two places in `DEPLOY.md` (`:355`, 1 line out and 1 in; `:360`, 1 out and 8 in): 764 to 771 lines, 9 insertions, 2 deletions, 2 hunks. No new command, no step.
- Sonnet seat, row C2 (`model-routing.md:92`), `claude-sonnet-5-5` (`models_latest.json:23`). One path, one branch `b1604/composer-deploy-guide-0022-route-b-measured`, plain push, no PR, nothing deployed.

## Facts re-measured (instrument; control)
| Fact | Instrument | Result |
|---|---|---|
| main | `gh api -X GET commits/main`, `git/ref/heads/main` | `b4681297d974ac3d8e74a4a12baeb9ea41962c52`, 2026-11-15T05:56:15Z, author `88359143+kamilDatasec@users.noreply.github.com` |
| open PRs | `pulls?state=open` | 1: #85 draft held; `pulls/85/files`: `DEPLOY.md` 0, control `document-pdf.ts` 1 |
| DEPLOY.md | raw `contents?ref=main`, `wc -l`, `shasum` | 764 lines, sha256 `c5169c14...faa26`; 0022 section `:324`-`:373`; `UNMEASURED` (-i) on `:360` and `:693` only; `expected and not run` on `:355` only; control: `as above for 0019` on 4 lines, `measured` on 24 |
| 0022 migration | raw + `shasum -a 256` | 80 lines, `8195ecb7...b539717`, equal to the checksum the section prints; function `:44`, triggers `:70`, `:79` |
| 0021 block | `awk NR` over raw | fence `:236`-`:247`, three `echo $?` (control count 3), drop line `:243` |
| old evidence | `p21c-0022-0027.txt` | 71 lines, `:14` exit 1, `:15` the refusal text, `:17` ledger 22; DETAIL lines 0 (control: refusal text 1) |
| harness | `ls` | `p21c.sh` 0 of 3 p21 files; `p21.sh` 133 lines, `p21-node.mjs` 63 |
| readers of DEPLOY.md | raw `b778`, `b616`, `b322-0022-down`: `grep -i -c -F` | 0 hits of `expected and not run`, `UNMEASURED`, `addition that is`; control `DEPLOY.md` 15, 10, 1; b778 reads the 0021 section only (`:15`, `:64`) |
| prettier | `package.json`, `.prettierignore` | `prettier --check .` 1; `.prettierignore` 15 lines, `md` 0: DEPLOY.md is checked |
| ticket | Jira GET (python `-I -B`, own copy of the B1569 helper, creds in-process) | PCOMP-128 Backlog, 1 comment (41207, items 3 and 4 landed); item 2 quoted in the kit |
| holds | `grep -c -i -F` over the pickup + 11-15/11-16 notes for PCOMP-128 (4), Guided (4), PC-C (1), B1604 (1), 0022 (5) | read each: the only hold is the Guided one (lane B, PCOMP-75); it does not cover DEPLOY.md migration 0022 |
| Composer panes, ports | `tmux list-panes`, `lsof` | 0 Composer panes (`%0 tuesday`, `%1 fleet-monitor`); 12 listener lines; kit needs no port |
| prior refs | `gh api git/matching-refs/heads/b1604` | 0; control `b1569` 1; `.tools/b1604` absent, `.tools/b1569` present |
| heavy lock | `ls -d` | absent; `heavy.sh` 1724 bytes, `b1551|c99` on 3 lines |
| model rows | `awk NR` | `:92` C2, `:109` G2, `:110` G3 "No gate: the builder's own red-proof" |
| seat id | `ls briefs | grep -o SEAT-C[0-9]+ | sort -V` | highest SEAT-C103, so C104 |

## Chain-step inputs (rule 4)
| Step | Inputs | Produced by |
|---|---|---|
| 0, 0b | kit, stamp slots, repo, deploy key, Jira | exist / Tuesday's stamp |
| 1 | DEPLOY.md at BASE, 0022 migration and down recipe, `p21.sh`, `p21-node.mjs`, B1504 evidence | exist at BASE / in the records repo (read-only) |
| 2 | clone at BASE (Step 0), heavy.sh copy | Step 0 |
| 3 | `pc-b1604-node:base` image, `p22.sh`, `p21-node.mjs` copy, the 0021 block extracted from the clone's DEPLOY.md | Step 2 (image, harness), Step 0 (clone) |
| 4 | Step 3 log (slot values), THE WORDS | Step 3, kit |
| 5 | commit of Step 4, base counts | Step 4; base checks are taken in Step 2 on the unedited clone (Q-4) |
| 6 | commit, Step 5 results | Steps 4, 5 |

## D-decisions
- D-1: measure the section's form, not the one-step (see BLUF). The one-step is M1 only.
- D-2: two readings of "add to the line it already pipes": A (both statements in one echo, the section's words, and the 0024 section's form) is the claim; B (only the new statement) is report only. Reason: for a dump at 0021 the 0021 function is in the dump, so B may also work; the words claim only A.
- D-3: words state only frozen results (exit codes, rows, objects gone, previous-build migrate line, same checksum, the control block's non-zero exit). Schema equality to a 0021-only database is measured (M2) but NOT claimed; B1504's 0024 measurement found `AND`-grouping differences in CHECKs, so a claim there needs its own read.
- D-4: line `:354` (`as above for 0019, with one addition`) stays byte for byte; M1 will show it is not the one-step command. That is a wording matter (a new operator command is approval-class, and the 11-11 ruling does not cover 0022): the kit makes the seat say so in FOR TUESDAY, not fix it.
- D-5: `PART-WORDS` and the outcome table: the seat can end with no edit (`PARTIAL B1604: none | done measurement | not done edit (...)`), which is a complete and useful result.

## Q-questions for Tuesday (each with a default)
- Q-1: Do you accept E1 and E2 (THE WORDS) as measurement-only words, conditional on OUTCOME A? Default: BUILD. If not, stamp DROP: the seat measures and writes STATUS only.
- Q-2: Gate tier. The commission says G3, but `model-routing.md:110` G3 is "No gate", and B1569 (same kind of DEPLOY.md measured-words change) ran G2. Default: G2 (docs), CodeQL read by you on the PR.
- Q-3: `:354` ("as above for 0019, with one addition") and the 0022 two-step prose: if M2 passes, should a later lane ask the product owner whether the 0022 section is to be rewritten into the 0021/0024/0025 two-step block form? Default: yes, a card after the PR lands; not in this kit.
- Q-4: Base checks. The kit's Step 5 takes prettier/lint/secret-scan/test-db at head and says "rc as at base", but only Step 2 builds the image; the seat must run the base checks on the unedited tree (head is base until Step 4). FIXED in the kit after drafting: Step 2 now records the base checks on the unedited clone (default stands, nothing for you to do). Also: no port block assigned (none needed); HARD STOP slot is yours.

## UNMEASURED
- Everything the seat measures: the drafter ran no docker, no `pg_dump`, no `pg_restore`, no migration, no test. Every frozen M1/M2/M4 value other than M1's (relayed from B1504 evidence) is a prediction. Whether reading A passes is unknown.
- Whether the one-step refusal's DETAIL lines name only `pc.assert_exception_scope_in_engagement()`: the old evidence has none (0 DETAIL lines).
- A restore of a database holding exception rows with a scope: the harness fixture has none (named in the kit).
- Docker daemon state and the heavy-lock holder at launch (Tuesday's slots).
- `p21-node.mjs`'s `post` op and `fixture` on 0021/0022 databases: read, not run.
- Sidecar: about 60 of 115 lines are instruction fragments (grep count over the kit text), the same convention as B1569's; the substantive literals (refusal text, log line `:12`, checksum, line pointers, model rows, panes, refs, `echo $?` count 3) were measured by real runs, 4 sidecar entries corrected after a verification pass (08:13).

## Outside-the-fences disclosure
None breached. Read-only: the project repo through `gh api -X GET` under the project `GH_CONFIG_DIR`; Jira GET through a copy of an earlier drafter's GET-only helper (`d1604/jget.py`, creds read in-process by name, never printed); project records (CLARIFICATIONS.md, B1504 STATUS/evidence/harness, `.tools/b1551/scripts/heavy.sh`); the pickup and the 11-15 and 11-16 notes; `tmux list-panes`, `lsof`. No docker, az, ssh, hosted HTTP, `decision_queue.sh`, ledger, Artifact tool. Two of my Bash calls were refused by hooks before running (a `cd`, and an unquoted `=====`); nothing ran. Scratch only in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s281/d1604/` (`raw/`, `pcomp128.txt`, `jget.py`, `words.py`, `fill.py`). Wrote only the kit, its sidecar and this report.

DRAFTED B1604: kit 142 lines, sidecar rc 0, questions 4
