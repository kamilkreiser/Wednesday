# B440 drafter report (read-only; two files written)

**Brief:** `2026-10-22_B440_SEAT-F2_hpsmpoc-telemetry-224-fixround3.md` (about 35 KB, clone of the B432 shape). Round 3 of HPSMPOC-224 on `b429/telemetry-224`, pane `Datasec/HPSM-POC-F2`, Opus, ends at READY FOR QA. Authority = Kam's tap 09:27:03 (quoted verbatim, option a text verbatim). Drafted about 09:25-09:45 AEDT 2026-10-22.

## What I read (whole unless marked)
- B432 brief, ADDENDUM-R1, ADDENDUM-Q2 (whole). B436 STATUS (whole). B431 STATUS `:150-250` (findings, FOR TUESDAY, NOT TESTED; the first 150 lines not read). B432 STATUS `:70-76` and `:151-200` only (BLUF, ADDENDUM-Q2 section, final line); its middle (findings, class hunt table, TESTED) NOT read. B429 brief (whole), ADDENDUM-Q1, ADDENDUM-CKPT (whole).
- HPSM-POC `CLAUDE.md` (whole). `CLARIFICATIONS.md`: first 60 lines plus a grep for `telemetry|CodeQL|landing`: the grep printed only one line (`:62`, unrelated verbatim taps), so no telemetry C-entry and no landing-rule text was found in that file by grep. A landing rule and CodeQL rule in the file under other wording are UNMEASURED.
- B438 and B439 briefs: grep of the partition / branch / ownership lines only (not whole).
- Source at `39d4d1a2` via `git show`: `TelemetryScrub.cs:95-175`, `scrub.ts:55-125`, `TelemetrySetup.cs:25-125`. Other telemetry files not read.

## Facts and instruments
| fact | instrument | result |
|---|---|---|
| branch head | `git --no-optional-locks -C 2_Project_Files ls-remote origin refs/heads/b429/telemetry-224` 09:29:02 | `39d4d1a25294bf5059cf7a088ac3e7ca5fd8efcf` |
| main head | same, `refs/heads/main` | `01dd9e4b4d9225999a2830343b1d4bf9f29966ac` |
| `b438*`, `b439*`, `b440*` on origin | same, patterns | none (B438 has not pushed; B439's branch is in the other repo) |
| other refs seen | same, `b44*` | `refs/heads/b44/metrics-at-the-showcase` 2c57c4a0 (older, 27 Sep; not a conflict with `b440*`) |
| merge-base | `merge-base 01dd9e4b 39d4d1a2` | `35b2b73ebf570878be3aea999e0af08a3fcbbfbf` |
| ahead / behind | `rev-list --left-right --count 01dd9e4b...39d4d1a2` and `rev-list --count 35b2b73e..39d4d1a2` | branch 17 ahead, main 1 ahead |
| the telemetry paths | `diff --name-only 01dd9e4b...39d4d1a2` | **35** (list in the brief's PARTITION; saved copy `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/c54612f8-a25c-4a1d-944e-26e0bacde43c/scratchpad/p35.txt`); two-dot against main = 38 |
| main's newer paths | `diff --name-only 35b2b73e 01dd9e4b` | `web/src/components/screens/UatStartScreen.test.tsx`, `web/src/components/shell/AppShell.badge.test.tsx`, `web/src/components/shell/AppShell.tsx` |
| ports | `lsof -nP -iTCP:8000-8199 -sTCP:LISTEN`, then 8100-8109 | only 127.0.0.1:8090-8094 (B438's block, live); 8100-8109 empty (rc 1; no bind-and-see positive control run by me) |
| `.tools/b440`, `wt-b440-*` | `ls -d` globs | absent; `.tools/b198` exists |
| model id | `models_latest.json` `levels.opus.model_id` via python | `claude-opus-5-5` |
| B440 STATUS / brief files existing | `ls | grep -c B440` in both Briefs folders | 0 |

## Partition measurement
- Branch's 35 paths vs B438's owned set (`web/src/components/shell/**`, one new `web/e2e/*.spec.ts`): `grep -c` of `^web/src/components/shell/` = 0, of `^web/e2e/` = 0 (planted control reads 1). Intersection **0**.
- vs B439 (records repo branch, `CLARIFICATIONS|BACKLOG|history.md|STYLE|SOURCES|Briefs/`): 0 matches in the 35.
- Main's 3 newer paths vs the 35 (`grep -F -x -f`): 0. So the forward-merge is predicted conflict-free (INFERENCE; I did not run a merge, `merge-tree --write-tree` being forbidden).
- Limits: B438 is not on origin, so its real diff is UNMEASURED; I measured against its declared partition. `web/package.json` / lock are in the 35 and not in B438's set.
- Observation for the brief: `web/e2e/responsive.spec.ts` exists at main (ls-tree), and B438 might extend it; the 35 contain no `web/e2e` path, so no overlap either way.

## Judgement calls to check
1. **B436-4 (mixed / concatenated log template, Major) is NOT in option a's text.** I did not commission it; the brief makes it a residual stated in the README and gives Tuesday a Stamp slot R-1 (YES activates a conditional item 2b: send no log template at all). Note the gate may still log it as an open Major (B431-7) at round 3. My recommendation: YES (cheap, same class "a string leaves because of its shape", inside the telemetry partition), but it widens past Kam's words, so Tuesday decides.
2. **Branch-born name rows.** Option a necessarily makes B429/B432 rows that assert frame names (web `frames.test.ts`, `scrub.test.ts`; API fix-round / scrub tests) wrong. The brief lets the seat replace only those, with a retired-name list, and keeps "tests that exist on main are not edited". "Names lost 0" becomes "names lost = the retired list". Ratify (R-2). I did not read those test files, so the exact rows are UNMEASURED.
3. **Exception TYPE provenance.** Option a keeps "exception type". B436-2 showed `GetType().FullName` of an emitted type leaves, and B436-7 that web `error.name` is code-settable. The brief names the rule (provenance: non-dynamic assembly in an app/framework set, else one constant token; web: identity / exact fixed set, else `Error`) as the seat's measured choice and tells it to flag it. The allow-list soundness (e.g. `Assembly.Load(byte[])` assemblies are not `IsDynamic`) is my reasoning, not measured.
4. **Model line.** You asked for "model claude-opus-5-5 -- C6". At `model-routing.md:96` row C6 is "Deploy"; B429 used it because that seat owned the deploy, B432 said "build C2". B440 does not deploy. I wrote C6 as asked and left Stamp slot R-3 to confirm or switch to C2.
5. **Port block 8100-8109** is my pick (blocks seen in briefs: 8010, 8030, 8040, 8050, 8060, 8080, 8090). Not checked against Tuesday's ledger of blocks; confirm.
6. **Hard stop 13:30, target 12:30** are your numbers; B438's are 13:00 / 12:00, B432's gate-after-fix ran about 3 hours.
7. Slot protocol: the brief uses `____` slots (2 lines: the `## Stamp` section and the final line); the REFUSE check is `/usr/bin/grep -c -E '_''_''_''_'` (verified: reads 2 lines in the unstamped file, control 1, and the check line itself does not match). B432 used `@X@` slots instead; the brief's wording is built for the new form.
8. The brief tells the seat not to open `.tools/b436` (another seat's tree) but to rebuild the gate's canary instruments from the B436 STATUS text and read the committed `B436_evidence/` folder (exists: MEASURED by `ls`).

## UNMEASURED
Whether the merge is conflict-free; the exact current line numbers of the shape rules (I quote B436's and my `show` ranges, which the brief tells the seat to re-measure); the `CLARIFICATIONS.md` landing rule beyond the grep; CodeQL on the head (B436: 0 check-runs); anything dotnet/npm/pytest/HTTP; whether `Briefs/` already holds a file for B440 on the records side; B438's real diff; `web/e2e` contents beyond `ls-tree` names.

## Open questions for Tuesday
1. R-1: include B436-4 (log template) in this round? (recommend YES; text is ready as item 2b.)
2. R-2: ratify retiring branch-born frame-name rows (names lost = the retired list)?
3. R-3: C6 as written, or C2 (build)?
4. Event name `^[\w.-]{1,40}$` (B436-7, name half) and the instance id (B436-9) are left as Notes unless the seat's fix is a fixed set in the same file. Say if you want them forced.

Files:
- /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B440_SEAT-F2_hpsmpoc-telemetry-224-fixround3.md
- /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B440_DRAFTER-REPORT.md
