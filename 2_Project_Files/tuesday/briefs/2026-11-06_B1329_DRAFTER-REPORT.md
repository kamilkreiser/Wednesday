STARTABLE: YES, after Tuesday fills the slots (S2 = `ecb097a3305d33230666073c8fc270fed40ab1e4`, S3 state). The branch tip and the open-PR list were re-read at 14:19; re-read both at the stamp (a moved tip refuses the seat).

# Drafter report: B1329 SEAT-H132, comment-only forward commit on b1320/hpsmpoc-retire-demo-repo-paths (drafted 14:19-14:30 AEDT 2026-11-06)

## BLUF
1. Kit `2026-11-06_B1329_SEAT-H132_hpsmpoc-retire-demo-comment-fixes.md` (87 lines, ASCII, 12 four-underscore runs: eleven slots and the last line) plus `2026-11-06_B1329_slots.json`. Sonnet, C2 (`model-routing.md:92`), `BRIEF_SEAT_LEVEL=sonnet` inside the launch quotes, tier 3 comment corrections riding under the branch's G1 gate; the binding hold is the second paragraph of the kit.
2. **Measured: the fix works.** The shellcheck v0.11.0 release asset (digest checked) gives base rc 0, head rc 1 (SC1073, SC1072 at `validate.sh:10`), edited copy rc 0 (`# SC2068: ...`), over the 6 `*.sh` of each tarball.
3. **Measured: the demo comments are comment-only and safe.** With the five comment edits applied in a scratch copy, bicep `main.json`, `dev` and `uat` parameters are byte-equal to the head's (`cmp` rc 0; control uat vs dev rc 1) and `validate.sh` ran 312 of 313 tests ok (the one error is a tarball having no git work tree; identical at the head).
4. Decision: `Program.cs:47` is **included** (one comment line, in a file the branch does NOT edit; see "wrong in what you told me" 1).

## Facts re-measured (instrument; control)
1. Refs 14:19:43 (`gh api -X GET`): `matching-refs/heads/b1320` one row `ecb097a3...`; main `6d592ede...`; open PRs: #291 (b1312) whose files are `web/e2e/mock-rows.spec.ts` only (`pulls/291/files`, 14:26).
2. Tarballs of tip and of main (`gh api -X GET tarball/<sha>`): `diff -rq` 29 files (equals the B1328 report's count).
3. Shellcheck: asset `336391359` (darwin aarch64 v0.11.0), `shasum -a 256` `339b930feb1ea764467013cc1f72d09cd6b869ebf1013296ba9055ab2ffbd26f` = the release listing's digest; the listing's linux x86_64 digest `b7af85e4...` = `ci.yml:590` (positive control). **Which copy:** I downloaded it again into a new scratch directory and `cmp`'d the binary with the copy the B1328 drafter left in the shared scratchpad (`.../scratchpad/sc_bin/shellcheck-v0.11.0/shellcheck`): identical. Run as `ci.yml:605-609` (`bash -n` each, then `--format=gcc` over all): base rc 0, head rc 1 (`validate.sh:10:1` SC1073, `:10:16` SC1072), edited rc 0. The file set was `find -name '*.sh'` (6 each), not `git ls-files` (a tarball has no index): a frame difference, named in the kit.
4. Edited scratch copy vs head: `diff -r` shows exactly 7 changed lines (+7 -7) in 5 files, all comment lines or the one README row. Bicep (project `.tools/bicep/bicep` 0.47.16): `main.json` equal (`bd5d77574390`), `dev` equal (`f3edc8ff2135`), `uat` equal (`6109d2272916`); `demo.bicepparam` is a retired stub that does not build as a parameters file (BCP337) at the head: untouched, not compared.
5. `validate.sh` on the head copy and on the edited copy: both `Ran 313 tests`, both one error `test_hidden_characters.NoRawHiddenCharacters` (`git rev-parse` rc 128 in a tarball). My first per-file run of the Python tests with `python3 -I` failed on imports of `test_security_baseline` (a `-I` artefact of my own); the `validate.sh` run is the one that counts.
6. Nothing reads the old wording: the runner test strips comments before reading `playwright.config.ts`; a fixed-string search of the head for the old phrases found only the lines named (DERIVED for web tests, which I did not run).
7. Author e-mail on recent main commits: `88359143+kamilDatasec@users.noreply.github.com` (six of six; the committer is the GitHub web flow); the branch's own commit author is a `.localdomain` machine default (`commits/ecb097a3`).
8. Model and id: `model-routing.md:92` (C2), `:110` (G3), `models_latest.json:23`, `brief_seat.sh:24` default Opus. Ports: `lsof -nP -iTCP:9360-9369 -sTCP:LISTEN` 0 at 14:28:58 (control 11 overall); none needed.

## D-decisions
- D-1 Wording of `validate.sh:10`: `# SC2068: ...` (the form the B1328 drafter measured), not main's `# HPSMPOC-109 (shellcheck SC2068)`, because a ticket key is a provenance token the branch has been removing.
- D-2 `Program.cs:47` included, with a leave-it-out clause if the seat finds it is not comment-only or is pinned.
- D-3 `appservice.bicep:146` and `:209` ("on in uat and in demo") left: they are true of the template.
- D-4 Time: READY Step 0 + 45, HARD STOP + 60 (a five-file comment commit with one validate.sh run and a web lint/typecheck/unit run).
- D-5 Checks: shellcheck, `bash -n`, `validate.sh`, bicep `cmp`, lint, typecheck, whole unit `npm test`; no e2e, no dotnet suite.

## Q-questions for Tuesday (each with a default)
- **Q-1** Include `Program.cs:47` (a file the branch does not edit)? Default: yes, as the kit says.
- **Q-2** Drop the `B59:` token from the README row as well as the demo-notice words? Default: yes (the added line carries no `B###`).
- **Q-3** Gate order: this commit changes the head the B1328 tier-1 gate was drafted against (`ecb097a3`, count A = 1). Default: stamp B1328's S2 with the new head and A = 2 after this seat's READY, not before.
- **Q-4** The template still sets the open sign-in switch on for `demo` while both locks refuse it (fail closed). Default: Note only, outside this kit.
- **Q-5** Hold wording: the kit says "the product owner's open question on the SOW's Demo environment" and forbids the commit text from mentioning it. Default: as written.

## UNMEASURED
The web `lint`, `typecheck` and `vitest` runs; `dotnet build` (no `dotnet` on my machine, `command -v dotnet` printed nothing); `validate.sh` in a git work tree (the one test that needs git); `git ls-files '*.sh'` as the file set; the push, hosted CI, CodeQL, SQL Server shards; whether the seat's clone can fetch the branch by deploy key; anything about the hold or the product owner.

## Anything wrong in what you told me
1. `Program.cs` is **not** a file the branch already edits (`diff -rq` of main vs tip: 29 files, `Program.cs` not among them). Your "decide by reading" covered it; I included it as a new one-line touch and said so in the kit.
2. B1328's report calls the `validate.sh` fix `# SC2068:` rc 0; confirmed. But the B1328 drafter's file set and mine are tarballs; only the seat's `git ls-files` run is the CI frame.
3. "PR #291 touches only `web/e2e/mock-rows.spec.ts`": confirmed (files list), at 14:26.
4. The stale demo-notice words are in `playwright.config.ts:8` and `README.md:60` as you said; the README row also carries a `B59:` token, which the kit removes.
5. Nothing else differs. The count of stale-comment edits is five (playwright 1, README 1, Program 1, bicep 2) plus the `validate.sh` line.

## Outside the fences (disclosure)
- Downloaded and ran locally the shellcheck v0.11.0 darwin release asset (`gh api -X GET` of koalaman/shellcheck, public GitHub, not an HP host) into the session scratchpad; executed the project's `.tools/bicep/bicep` (read-only compile into scratch, three builds each of the head and the edited copy) and `bash infra/scripts/validate.sh` on scratch tarball copies (no `az`, `WHATIF=0`); the `python3` test files ran from scratch.
- Extracted tarballs (tip and main) into scratch (untrusted data, never run from inside); `rm`/`sed -i` were used only on my own scratch scripts; a pre-existing copy of the shellcheck binary and an earlier drafter's `bo/`-style scratch files were present in the session scratchpad and were compared, not trusted.
- Read the B1313 `.pre-stamp` kit and `.pre-tuesday` slots (shape), the B1328 report (facts), `DRAFTER_RULES.md`, `model-routing.md` lines 92 and 106-111, the B1320 STATUS grep for item 5 (`:171` only, not read whole), `brief_seat.sh:24`, `lsof`, `tmux list-panes`.
- No `decision_queue.sh`, ledger, briefs_staged, scoreboard, Jira, Artifact, mail, `az`, docker, ssh, HTTP to any hosted host, and no write outside the three B1329 files and the session scratchpad.
