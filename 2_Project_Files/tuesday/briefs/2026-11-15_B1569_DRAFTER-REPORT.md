STARTABLE: YES (for PCOMP-128 items 3 and 4 only, with the exact words in the kit; items 2 and 5 are carved out; the slot PART-WORDS needs Tuesday's read of THE WORDS)

# B1569 drafter report: Security Composer lane C, PCOMP-128 (DEPLOY.md)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1569_SEAT-C101_composer-lane-c-deploy-guide.md` (131 lines; sidecar `.measured` 84 lines, `stamp_check.py` rc 0). Drafted 11:42 to 11:49 AEDT (`date` printed 11:42:45 at start, 11:48:50 last).

## BLUF
- PCOMP-128 has five items (Jira GET, 0 comments, Backlog, label `plan-comp-479`). Item 1 is "correct as written". Items 3 and 4 (the Route B bullets of the 0023, 0026 and 0027 sections, `DEPLOY.md:401-403`, `:626-628`, `:673-675`) say "as above ... UNMEASURED" while the project's own evidence says the one-step restore exited 0 (`1_Project_Definition/Briefs/2026-11-11_B1504_evidence/runs/p21c-0022-0027.txt`, lines 57-59 and 67-69 for 0026/0027; the 0023 block above them). The kit builds exactly these three bullets, with the replacement text written out byte for byte in the kit ("THE WORDS"), so the seat invents no word.
- NOT in the kit: item 2 (0022 section form, `:354-:360`: needs its own measurement on a throwaway database, a docker harness, a separate kit) and item 5 (line 169, the grammar line: "needs approved wording"; the product owner's 2026-11-11 ruling does not approve it, `CLARIFICATIONS.md:2733`). Line 687 (planner/index) is excluded by the ticket itself.
- The seat never runs `az`, `pg_restore` or any hosted call. Its checks: `prettier --check` (the repo's `.prettierignore` has no `md` entry, so `DEPLOY.md` is checked), `scripts/secret-scan.sh --tree`, and `scripts/test-db.sh` (the two tests that READ `DEPLOY.md`: `b616-deploy-commands.db.test.ts:11` and `b778-route-b-script-complete.db.test.ts`).
- The one gap that could stop it: the wording is new operator-guide prose (measurement-only, no customer-facing word). Tuesday decides at the stamp (Q-1).

## Facts re-measured (instrument; control)
| Fact | Instrument | Result |
|---|---|---|
| origin main | `gh api -X GET git/ref/heads/main`, `commits/main` | `68975c10ad4d5b65fcdcacba9029ffeb12cc53e1`, 2026-11-13T02:59:18Z, author `88359143+kamilDatasec@users.noreply.github.com` |
| open PRs | `gh api -X GET pulls?state=open` | 1: #85 draft held `b330/sm316-content-catalogue` |
| #85 touches DEPLOY.md | `pulls/85/files --paginate` | 57 names; `DEPLOY.md` 0; control `document-pdf.ts` 1 |
| DEPLOY.md at main | raw `contents?ref=` | 758 lines; last commit `879facda` (2026-11-11), same as the ticket's basis |
| stale lines | `grep -n -i` over raw file | `as above for 0019` on 354, 401, 626, 673; `UNMEASURED` on 360, 402, 627, 674, 687 (count 5) |
| CI | repo tree (1044 paths): no `.github` path (control `codeql` filter fires on one test file); `scripts/ci.sh` read (144 lines) | local ci.sh only; CodeQL hosted; `prettier --check .` reads DEPLOY.md |
| readers of DEPLOY.md | 77 raw files (50 ts, 22 sh, 5 mjs), `grep -l -F DEPLOY.md` | 12 name it; 2 read it; 0 pin the 0023/0026/0027 bullet words; control b778 15 hits |
| Composer panes | `tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'` | 0 Composer panes; MPS, HPSM-POC, NexusAI live |
| seat id | `ls briefs | grep -o SEAT-C[0-9]+ | sort -V | uniq | tail` | highest SEAT-C100, so C101; no B1569 file existed |
| ports 9860-9869 | `lsof` (0 lines, control 31 listeners); word-boundary scan of 34 non-`.pre-` SEAT kits of 11-14/11-15 | 0 hits (control `97xx` 5) |
| model | `model-routing.md:92` (row C2), gate `:109` (G2), `models_latest.json:23` | claude-sonnet-5-5; no docs-only builder row exists, C2 is nearest |
| heavy lock | `ls -d .tools/composer-heavy.lock` | absent (rc 1); `.tools/b1551/scripts/heavy.sh` 1724 bytes, 3 lines name b1551/c99 |
| local checkout | `git cat-file`, `ls-remote` through its config | STALE: object `68975c10` missing, and its `core.sshCommand` points at `/Volumes/Laptop-DEV/...` (not accessible). The kit tells the seat to use the explicit `-c core.sshCommand` with the Datasec_DEV key (exists, 419 bytes) |

## Chain-step inputs (rule 4)
| Step | Inputs | Produced by |
|---|---|---|
| 0 | this kit, STAMP slots, repo, deploy key | exists at BASE / Tuesday's stamp |
| 0b | origin refs, PR list, Jira ticket | exists |
| 1 | `DEPLOY.md` at BASE, B1504 STATUS and evidence file | exist at BASE / in the records repo (read-only) |
| 2 | clone at BASE, CI image tag `pc-b1569-node:base`, heavy.sh copy | Step 0 (clone), this step (image) |
| 3 | THE WORDS (in this kit), clone, python compare script | kit; Step 0; Step 3 writes the script before use |
| 4 | commit from Step 3, image from Step 2 | Steps 2 and 3 |
| 5 | commit, base counts from Step 2, head counts from Step 4 | Steps 2-4 |

## D-decisions
- D-1: carve the kit to items 3 and 4. Reason: 2 needs a docker measurement, 5 needs approved wording; both are named in the ticket as such.
- D-2: THE WORDS are written by the drafter from the evidence file's lines (exit 0, no output, ledger rows, postgres 16.15, fixture of 3 engagements, date 2026-11-11). The seat compares each fact to the evidence and writes nothing else; any mismatch is STOP. The frame caveat (one fixture) is carried as "a fixture of 3 engagements" in the sentence.
- D-3: 0023/0026/0027 bullets keep their first line byte for byte; the other two lines become four, net +6 lines (758 to 764), diff 12 insertions, 6 deletions, 3 hunks.
- D-4: no new test (nothing pins the words; the kit forbids editing tests).
- D-5: no CodeQL pre-scan row: the diff is markdown only and the repo's CodeQL is hosted; the kit leaves it to Tuesday's gate.

## Q-questions for Tuesday (each with a default)
- Q-1: Do you accept the three four-line blocks (THE WORDS) as the wording, since the ticket says words need approval only for item 5? Default: yes, BUILD (they state only measured facts and the gate reviews the diff). If not, stamp DROP and the seat does nothing.
- Q-2: Item 2 (the 0022 measurement on a throwaway database) as a later kit? Default: yes, a separate kit; the harness the B1504 seat used is `1_Project_Definition/Briefs/2026-11-11_B1504_evidence/harness/p21c.sh`, a readable claim only.
- Q-3: Gate tier? Default: G2 (docs), CodeQL read on the PR by you, no Opus gate.

## UNMEASURED
- The drafter ran no docker, prettier, test, secret scan or restore; whether `prettier --check DEPLOY.md` is green at base is the seat's Step 2.
- The measured claim itself (restore exit 0 at 0023/0026/0027) is RELAYED from the B1504 seat's evidence on a throwaway database with one fixture; nobody re-ran it for this kit.
- The 0023 evidence block lines were read in the earlier listing; the line numbers named in the kit are for 0026 (`:57-:59`) and 0027 (`:67-:69`) as printed.
- Whether the hosted site's operators read `DEPLOY.md` from main (deploy state) is outside the fences.
- The sidecar's default lines (about 50 of 84) are instruction literals the seat runs, not values it must match; each says so and carries a count over the kit.

## Outside-the-fences disclosure
None breached. Read-only: the project repo through `gh api -X GET`, Jira GET (own helper `d1569/jget.py`, credentials read in-process by name, never printed), project records (`CLARIFICATIONS.md`, B1504 STATUS and evidence), `tmux list-panes`, `lsof`. One local git read of the project checkout (`cat-file`, `grep`, `ls-remote`) was attempted; `ls-remote` tried ssh with the stale config and was refused (no write, no key used). One of my bash calls was refused by a hook (a `rm -f /dev/null` mistake, nothing ran); I used a quarantine move (`d1569/_quarantine_2026-11-15/measured.init.bak`) for the first sidecar skeleton. Scratch only in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s277/d1569/`. No Jira write, no mail, no az/ssh/docker, no hosted HTTP.

DRAFTED B1569: kit 131 lines, sidecar rc 0, questions 3
