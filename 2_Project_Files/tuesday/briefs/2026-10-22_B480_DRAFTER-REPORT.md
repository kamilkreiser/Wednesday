# B480 drafter report (Sonnet, read-only), 2026-10-22 about 21:15-21:35 AEDT

Brief: `2026-10-22_B480_SEAT-W2_hpsmpoc-b465-fixround1.md` (111 lines), fix round 1 of 2 on `b465/hpsmpoc-148-310-words` from `c65a5ab6`, pane `Datasec/HPSM-POC-W2`, Sonnet C2, ports 8310-8319. Shape cloned from B475.

## Read
- B474 STATUS (173 lines, whole): findings :143-151, FOR TUESDAY :154-162. B475 brief + drafter report (shape). B465 brief (scope, partition). Did NOT open the B474 gate kit (the report carried the checks I needed).
- `git show c65a5ab6:` of `dates.ts`, `dates.test.ts`, `followup/api.ts`, `ClientFollowUpScreen.tsx` (+ test :1-40,120-215), `api.failure.test.ts`, `ActionPlanScreen.tsx` :40-125, `ActionPlanScreen.test.tsx` :160-225, `playbook-partner.spec.ts`, `playbook-event-states.spec.ts`, `vitest` config name, `package.json` scripts.

## Item -> file:line map (all at c65a5ab6)
| B474 id | B480 item | where |
|---|---|---|
| 1 BLOCKER | 1 | `dates.test.ts:16` (instant built in process zone), `:12` (beforeEach switches to Sydney), row `:15-22` |
| 2 MINOR | 2 | `dates.test.ts:8-12`, rows `:30-57`; `dates.ts:7,21-31` if the optional-zone route is taken |
| 3 MAJOR | 3 | W4 `ActionPlanScreen.tsx:100`; C4 `ClientFollowUpScreen.tsx:136`; existing rows `ActionPlanScreen.test.tsx:199-219`, `ClientFollowUpScreen.test.tsx:200-211` |
| 7 MINOR | 4 | `ClientFollowUpScreen.tsx:60` -> `api.ts:85-94` (stale branch :86 before 401 :92); load sentences `api.ts:123-130` |
| 4 MINOR | 5 | card id in 10 places (below) |
| 5 MINOR | 6 | `playbook-b17-clicks.spec.ts:81,126`, `playbook-burger-menu.spec.ts:24`, `playbook-quality.spec.ts:19`, `playbook-partner.spec.ts:13,137,308` (helper :37 shared), `playbook-event-states.spec.ts:50` (helper :62 shared) |
| 6, 8, 9 | not in scope | named in the brief's NOT list |

## Things B474 did not map or got wrong
1. **B474-4 undercounts the card id.** `git grep` at the head finds 10 lines; the report lists 9 and misses `ClientFollowUpScreen.test.tsx:139`. The brief uses 10 and a positive control of 10.
2. **The card id is also in the two Jira comments** (39890, 39891; B474 Check 3 (iii)). Not code; B480 does not touch them; the brief says Tuesday's. Decide whether to edit them.
3. B474-5 names "five e2e specs"; there are 8 title-assertion lines, and two of them (`partner.spec` :137/:308/:13 via helper :37, `event-states` :50 via helper :62) use helpers shared by other screens. The brief tells the builder to make only the Home call exact.
4. B474-7: the report says the pre-B465 load path used `followUpFailure` (Check 1 deleted-lines list) but did not measure the mock's GET statuses. A fixed load 412 reads the partner-addressed sentence (`api.ts:125`) to a client: that is pre-B465 behaviour, so left alone and listed under FOR TUESDAY in the brief. Your call whether that deserves a ruling.
5. B474-3 W4: killing W4 needs a scenario-A ABSENCE row; the race (scenario B) row only pins presence. I forbade pinning what the click makes (it acts on the older result; B474-9 is a ruling). Assumption: that is the right fence.

## Partition intersection (READ verbs only; `git diff --name-only 1d1fa462...<sha>` vs `git diff --name-only a93b926a c65a5ab6`, 19 paths)
```
b461 53052201a968 n=14 shared=0
b466 3eded1128663 n=10 shared=0
b467 d6eba5f68137 n=9  shared=0
control planted (dates.ts appended to b461 list): 1
control self (b465 range vs mine): 19
```
Empty. b461's 14 are B475's list unchanged; b466 touches `web/src/server/mock/*` (not in B480's Yours). b429/b462 not re-measured by me (not live seats on web paths per B474 Check 8, 0 overlap); the brief tells the builder to include them.

## Main vs branch (merge-base, rev-list, legacy merge-tree)
- `merge-base c65a5ab6 1d1fa462` = `a93b926a` (the fork point; unchanged).
- `rev-list --left-right --count 1d1fa462...c65a5ab6` = `3 6` (3 main-only: #181 `4695d7f`, #182 `d70f9dc`, #183 `1d1fa46`; 6 branch-only).
- Main-only paths 9; none in the 19. Legacy `merge-tree a93b926a 1d1fa462 c65a5ab6`: 28799 bytes, 0 `+<<<<<<<` markers (also 0 vs b461). I did not run a firing control for the marker format; B474's control did.
- **Proposal in the brief (Tuesday confirms at stamp): do NOT merge main into the branch** (nine foreign paths in the delta diff and a broken "Yours" check; the PR merge ref tests the combination). Binding merge order in PARTITION: B465 first, then b461.

## Other measurements
- `ls-remote` (21:2x): main `1d1fa462`, b465 `c65a5ab6` (unmoved), b461 `53052201`, b466 `3eded112`, b467 `d6eba5f6`; no `b480*`. `.tools/b480` absent, no `wt-b480-*`. `.tools/b198/lock.sh` and `.tools/b267/waitload.sh` exist.
- Ports: no brief names 831x (`grep -w '831[0-9]'` = 0; control `825[0-9]` hits 7 files). `lsof 8270-8299` rc 1. `lsof -iTCP:8310-8319 -sTCP:LISTEN` rc 1 (nothing) at 21:3x; positive control not run, the builder re-checks. Live panes: A1, G42-G45, H5, R1.
- Callers of `formatMoment`/`formatTime`: 12 component files; grep for by-reference use (`.map(formatTime)` etc.) printed nothing (no positive control run; marked ASSUMPTION, the brief makes the builder re-check before adding an optional parameter).
- CI sets no `TZ` (grep 0). `vitest.config.mts` pins no pool.
- Stamp slots: `grep -c -E '_''_''_''_'` = 8 (seven slots + last line); control `x____` = 1. "the lock" count in the brief = 0 (one hit fixed to a path). Person-name grep (kam|kamil|kreiser) = 0.

## Assumptions (marked)
- The five load-path sentences in item 4 are copied from `api.ts:123-130` by reading; the builder re-reads them.
- `2026-09-25T09:51:24Z` is the right absolute instant: MEASURED after drafting: `date` converts it to 2026-09-25 19:51:24 AEST in Sydney (DST starts 4 Oct), so it is right.
- Model row Sonnet per your routing statement; I did not read `model-routing.md`.
- Hard stop/target left to you in the stamp. I did not create a `.pre-stamp` copy (not in my write fence).
- Gate mutant anchors are at `2026-10-22_B474_evidence/c4_mutants.json`; I did not open it, the brief points the builder to it.
