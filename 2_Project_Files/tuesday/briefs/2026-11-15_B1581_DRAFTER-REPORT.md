STARTABLE: YES once Tuesday fills the WORDS slot (NO as it stands for the cover's words: the new zone label is customer-readable and C-71 approves no word for COMP-15; W-b adds none, W-a needs a ruling or Tuesday's acceptance)

# B1581 drafter report: Security Composer lane A, PCOMP-82 (policy PDF cover date in Sydney time)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-15_B1581_SEAT-C103_composer-lane-a-pcomp82-cover-date-sydney.md` (112 lines; 14 four-underscore slot lines including the last line; sidecar `.measured` 99 lines, `stamp_check.py` rc 0). Drafted 15:54 to 16:05 AEDT (`date` printed 15:54:25 at the tarball, 16:04:56 last).

## BLUF
- **The commission assumed a brand-profile migration. None is needed, and the kit builds none.** What the renders call "the brand profile" is a code constant, `DATASEC_DEFAULT_BRAND` (`packages/renderers/src/brand.ts`). `apps/api/src/outputs.ts:244` says so ("no tenant brand binding exists") and `:316` passes it. `pc.brand_profile.tokens` is a jsonb with no shape CHECK, and nothing that renders reads it. So the ruling ("(a) Brand profile, Sydney time, cover only", C-71 COMP-15, `CLARIFICATIONS.md:1311`) comes down to one field on `BrandProfile.document` (`model.ts:37`-`:44`) plus its value on the default brand. There is no migration, no contract change and no `DEPLOY.md` line. That makes it routing row C2 (Sonnet, `model-routing.md:92`), not the Opus deploy-bearing row the sweep expected. Tuesday confirms this at the MIGRATION slot (Q-2).
- **Scope:** three source files (`policy-summary.ts`, `model.ts`, `brand.ts`) and one new test file. Only the cover's Date line changes (`policy-summary.ts:259`-`:260`). `dateWords` (`:75`) keeps its UTC rule, so the PR #85 file `b59-policy-pdf-cover.test.ts` needs no edit. That file's `:130` fixture is 06:00Z, the same day in Sydney, and its `:286`-`:288` rows pin `dateWords` itself. The policy PDF is the only output with a cover (`policy-document.ts:890`), and no digest golden pins a policy PDF (`s41-synthetic-generation.test.ts:47`). The brand hash moves on purpose, and every test computes it rather than pinning a literal.
- **The one real gate is words.** The cover today reads `(released, UTC)` and `(draft generated, UTC)`. Once the day is Sydney's, "UTC" is false. Whatever replaces it is customer-readable, and C-71 (`:1293`) keeps new words on cards. The kit offers W-a (`(released, Sydney time)`, with the words stored on the brand profile beside the zone), W-b (`(released)`, no new word) or DROP. It builds only what the WORDS slot says.
- No PR #85 path and no B1580 path is touched. Ports 9960-9969 are free. No Composer pane is live. The heavy lock is free (B1580 may take it in this wave, and the kit tells the seat to wait for it).

## Facts re-measured (instrument; control)
| Fact | Instrument | Result |
|---|---|---|
| origin main | `gh api -X GET commits/main` | `27adb70991ff3d7ec13f0732de6ecdcb1aab8043`, 2026-11-15T02:16:26Z; author `kamilDatasec` / `88359143+kamilDatasec@users.noreply.github.com` |
| tarball | `gh api tarball/27adb709` into `d1581/src/` | 973 files; `/.github/` 0 (control `codeql` 1) |
| open PRs | `pulls?state=open` | 1: #85 draft HOLD, 57 files (`pulls/85/files --paginate`) |
| #85 vs my paths | `grep -c -x -F` over the 57 names | `policy-summary.ts` 0, `model.ts` 0, `brand.ts` 0; controls `document-pdf.ts` 1, `b59-policy-pdf-cover.test.ts` 1 |
| UTC words | `awk NR` / `grep -n` over the raw tarball | cover `:259`, `:260`; summary `:282`, `:283`; `dateWords` `:75`/`:82` (UTC getters); other `dateWords` uses `:421`, `:472` (date-only) |
| brand at render | `grep -n` `outputs.ts` | `:244` comment, `:316` `brand: DATASEC_DEFAULT_BRAND,` |
| brand in db | `grep -n brand_profile` over all migrations | only 0001/0003/0004/0007; `tokens jsonb NOT NULL` (`0001:401`), no CHECK on shape; contract `tokens: { type: "object" }` (`document.ts:1432`, the api-contract one, not #85's renderers `document.ts`) |
| pins of the old shape | `grep -rn -F` for `UTC)`, `released, UTC`, `draft generated, UTC`, `dateWords` over packages/apps/scripts/content | 16 lines, 5 files (`d1581/census_utc.txt`): REWRITE only `policy-summary.ts:259`-`:260`; the rest UNAFFECTED (table in kit FACT 5) |
| brand literals | `grep -rn DATASEC_DEFAULT_BRAND` | 51 lines, 16 files; every test brand is a spread; no `Object.keys/values`/`toEqual` of it (that grep returned nothing; its frame is the 51 lines) |
| brand hash pins | `grep -rn -E 'brandProfileHash|brand_profile_hash'` | all computed; no 64-hex literal of the default brand's hash |
| calendar facts | host `node` v26.13.0 (ICU 79.1, tz 2026e) under `TZ=America/Los_Angeles`, `Intl.DateTimeFormat formatToParts` | 10-03T20:00Z: UTC 3 Oct, Sydney 4 Oct; 06-30T15:30Z: 30 Jun / 1 Jul; 06-30T13:59:59Z: 30 Jun both; 2027-04-03T13:30Z: 3 Apr / 4 Apr; `Mars/Olympus` throws RangeError |
| template version | `commits/<sha>` files of `d84aa46e` and `de95b413` (the two summary-word commits) | both touched `policy-summary.ts` and not the template constants: no bump precedent (the constants are in `policy-document.ts`, a #85 file) |
| prior work | `branches` (199), `pulls?state=all` (129) | 0 hits (controls `^b1569` 1, `deploy guide` 12); Jira PCOMP-82 0 comments; `BACKLOG.md:152` same text as the ticket |
| ports 9960-9969 | `lsof` at 15:58:57 and 16:04 | 0 lines, rc 1 (control: 25 listeners); kit scan of 28 non-`.pre-` SEAT kits of 11-14/15: 0 files (control `99[2-3][0-9]` 2) |
| panes | `tmux list-panes` 16:04 | no Composer pane; `%1` displays `fleet-monitor` |
| heavy lock | `ls -d` | absent; `.tools/b1569/scripts/heavy.sh` 1726 bytes, 3 lines name b1569/c101 |
| toolchain | `ls .tools` (37 entries); `docker/Dockerfile:3` | no drive-local node/dotnet; CI image `node:22-bookworm-slim@sha256:83f487e0...`; host node v26 is not the pin |
| model ids | `models_latest.json` | `:17` claude-opus-5-5, `:23` claude-sonnet-5-5 |

## Chain-step inputs (rule 4)
| Step | Inputs | Produced by |
|---|---|---|
| 0 | this kit, Stamp slots, repo, deploy key | exist at BASE / Tuesday's stamp |
| 0b | origin refs, PR list, Jira PCOMP-82, CLARIFICATIONS.md | exist |
| 1 | clone at BASE, the census patterns | Step 0 (clone); patterns are in the kit |
| 2 | clone, image tag `pc-b1581-node:base` (built here, then used for the FACT 6 node re-measure), heavy.sh copy | Step 0; this step |
| 3 | WORDS slot, the new test file (written first), the image | slot; Step 3(a) itself; Step 2 |
| 4 | commit from Step 3, image rebuilt at head, base counts | Steps 2 and 3 |
| 5 | commit, base and head counts, identity slot | Steps 0, 2-4 |

## D-decisions
- D-1: No migration, no contract, no `DEPLOY.md` (FACT 3). Building a database column that no render reads would add a deploy-bearing change and change no behaviour. The kit makes a stored brand row reaching a render a STOP, so the seat cannot quietly route around this.
- D-2: A new zone-aware function sits beside `dateWords`, and `dateWords` stays unchanged. This keeps the #85 file's rows green unedited, and the summary, the expiry dates and the Preview stay UTC, as "cover only" says.
- D-3: The zone comes from the brand profile (`document.time_zone`), with no constant in the code path (mutant M4 checks this). An invalid zone refuses with `RenderRecordError` and never falls back silently (M5).
- D-4: Month words come from the file's own `MONTHS`. `Intl` supplies numbers only, so the output does not depend on ICU locale data, only on ICU's zone data.
- D-5: No template version bump. The two earlier word-only changes to the summary did not bump it, and the constant lives in a #85 file.
- D-6: Gate tier and SUMMARY-SCOPE are left as slots (Q-3, Q-4).

## Q-questions for Tuesday (each with a default)
- Q-1 (WORDS): What replaces "UTC" on the cover? **Default: W-b (`(released)` / `(draft generated)`)**, the only choice that adds no customer-readable word, so it is buildable under C-71 without a card. W-a (`(released, Sydney time)`) is the clearer text, but it is a new phrase and needs the product owner's card or Tuesday's judgement that the ruling's own words "Sydney time" approve it. DROP if the label should wait.
- Q-2 (MIGRATION): Confirm NONE (FACT 3)? **Default: NONE.** If a stored, tenant-bound brand profile is wanted, that is a new feature (a binding plus a migration). It needs its own ruling and an Opus kit.
- Q-3 (SUMMARY-SCOPE): Should the cover change alone, or also the executive summary's first sentence (`:282`/`:283`, "released on <day> (UTC)")? **Default: cover only**, the ruling's literal words. Side effect for Tuesday or the product owner to know: for a release between 00:00 and about 10:00/11:00 Sydney, the cover shows the Sydney day and the summary's sentence shows the UTC day with "(UTC)". Both are labelled, but they differ.
- Q-4 (GATE-ROUND): **Default: a G2 gate**, the separate kit after READY (round 1 of 2 on class PCOMP-82 cover date), with CodeQL read on the PR by Tuesday. This matches the last Composer product builds (B1559, B1569). G1 instead if Tuesday counts the policy PDF as something handed to the client tester.

## UNMEASURED
- No docker, build, test, lint or typecheck was run. Whether the new rows go red and green as predicted, and whether the base red set matches B1569's, is for the seat (Step 2/3).
- The calendar facts come from host node 26 / ICU 79.1. The CI image's node 22 ICU zone data is re-measured by the seat.
- Whether any API path compares a stored output's `brand_profile_hash` with a fresh render's (FACT 4) is settled by the seat's Step 1 census and is a STOP if found.
- Whether the longer W-a line fits the cover column without wrapping is clause (12), the seat's.
- The summary sentence literal in clause (9) is DERIVED from `:283` and the UTC day, not rendered. The kit marks it so.

## Outside-the-fences disclosure
- Read-only throughout: `gh api -X GET` (commits, tarball, branches, pulls, pulls/85/files, pulls/9999, commits?path=), one Jira GET of PCOMP-82 (my copy of the prior drafter's GET-only helper, `d1581/jget.py`, credentials read in-process by name, never printed), the project records (`CLARIFICATIONS.md`, `BACKLOG.md`, `JIRA.md`, `CLAUDE.md`; one `git log -1` read of the records repo), `tmux list-panes`/`display`, `lsof`, `ls`. No docker, az, ssh or hosted HTTP. No card read, no `decision_queue.sh`.
- Host `node` ran one scratch script (`d1581/tzcheck.mjs`) for calendar arithmetic only, with no project code.
- Three slips, none deleted, none in a project tree: (1) one `ls ... > /tmp/x` redirect wrote a briefs-folder listing to `/tmp/x` (left in place, harmless). (2) I made a `.pre-stamp` copy of the kit beside it, which is Tuesday's file to make. I moved it, unchanged, to `d1581/_quarantine_2026-11-15/kit.pre-stamp.copy`, so the briefs folder holds no `.pre-stamp` for B1581. (3) The sidecar was regenerated twice: first after I reworded two kit literals: an apostrophe that did not match the record byte for byte, and one derived literal now marked DERIVED; then after I moved the FACT 6 node re-measure from Step 1 to Step 2 (it needs the image Step 2 builds; a forward dependency I found while writing the chain table). The old sidecars are at `d1581/_quarantine_2026-11-15/measured.first.bak` and `measured.second.bak`.
- Scratch only under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s278/d1581/`.

DRAFTED B1581: kit 112 lines, sidecar rc 0, questions 4
