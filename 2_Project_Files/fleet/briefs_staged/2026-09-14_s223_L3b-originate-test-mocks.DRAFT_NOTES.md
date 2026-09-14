# DRAFT_NOTES — s223 L3b originate-test-mocks (drafting subagent, 2026-09-14 12:03–12:4x AEST)

Everything below was read at source in the window stated; nothing was written outside the three output files. Read verbs only on the Secuura checkout (`ls-remote`, `log`, `show`, `diff`, `ls-tree`, `rev-parse`, `rev-list`, `merge-base`, `grep`, `reflog`, `status --porcelain`, `config --get`); no fetch/checkout/worktree/merge-tree. GitHub + Linear read-only via scratch copies of the gate984 method (token/key by NAME, never printed; controls `/pulls/99999` → 404, Linear `number: 999999` → `[]`).

## A. Facts re-read at source (instrument · time)
| Fact | Value at source | Instrument · time (AEST) |
|---|---|---|
| origin develop | **M21 `5210ddf317b2b1ed547e5d8488c3d011ceb087e1`** (#799 squash, 02:00:24Z; parent M20 `a5334350`; tree `16ea40dc3`) | `git ls-remote origin` 12:03:30 and 12:15; `/branches/develop` 12:05:42 |
| develop chain | M21 ← M20 `a53343502` (#903, KS-991) ← M19 `6e78961e1` (#982) ← M18 `8861e6216` | `git log --format='%H %P %T %cI %s' -n 6 refs/remotes/origin/develop` 12:04 |
| local refs | `refs/remotes/origin/develop` = M21 (fetched 12:01:14 by another seat); `refs/heads/develop` = M20; main checkout `feature/ks-597-b-…` @ `355d82c8b`, porcelain 0 | `rev-parse`, `reflog show`, `status --porcelain` 12:03–12:04 |
| #931 head | `f2e0cb3c125d117b1c9f8157bad28399f16b5e8e` (= `refs/pull/931/head` = origin branch = local branch); 1 commit; merge-base with M21 `d4cf7e3cf`; 114 behind / 1 ahead; 12 files | `ls-remote`, `merge-base`, `rev-list --left-right --count`, `diff --numstat` 12:04; REST 12:05:42 |
| #931 API | open, `mergeable None/unknown`, 0 reviews, 0 review comments, 2 issue comments (`5603139964` bot; `5651278796` kksecura 09-13 05:02Z), body 3,267 chars, Test Evidence present, `compare develop...head` ahead 1 / behind 114 | `gh_l3b.py` 12:05:42 |
| #720 head | `fcc611d29401cf4642852b6ba80a16851ddb5b95` (= `refs/pull/720/head` = origin branch; local branch `0932c3f9f` one behind); 8 commits (7 + the 09-08 merge); merge-base with M21 `400517aaf`; 172 behind / 8 ahead; 2 files (`BACKLOG.md` 184/30, ks444 9/0) | same, 12:04–12:05 |
| #720 API | open, **`mergeable None/unknown`** (sweep: `dirty`), 0 reviews, 0 review comments, 5 issue comments incl. Peter `5479494525` (08-31, 9,799 chars) and `5600892508` (09-09, 8,761 chars) — both read whole and quoted | `gh_l3b.py` 12:05:42 |
| #985 | open, head `fcd8a01e4`, **`mergeable False/dirty`** since M21 (the squash-stack shape), 17 files vs M18; its ks695 hunk = +4 lines at `:36-39` (3 comment lines + the `normaliseOrgId` pass-through) | REST 12:05:42; `git diff 8861e6216 fcd8a01e4 -- ks695` 12:08 |
| #965 / #799 | #965 merged 2026-09-13T05:04:47Z (head `d63b27ab3`); #799 merged 2026-09-14T02:00:24Z (head `6da848891`) = M21 | REST 12:05:42 |
| open PRs | **45**; `/pulls/N/files` walked for all 45 — under `originate/src/__tests__/`: #931 (12), #720 (ks444), #985 (ks695, ks764, ks780), #937+#912 (ks1004, ks1058, ks535), #937 (ks1059), #919 (ks739), #939 (ks1068); `BACKLOG.md`: #985, #942, #720; the helper: #931 only | `gh_l3b.py` 12:05–12:07 |
| root factories at M21 | **12** files: gdprService.erasure:37 · ks1103:45 · ks444:52 · ks445:28 · ks563:40 · ks584-p3-auth:28 · ks584-p3-verify-list:52 · ks584-verify-row-selection:39 · ks695:26 · **ks764-admin-api-keys-revoke-route-contract:97** · ks914:30 · qa-f4:31 | `git grep -n -E "jest\.mock\(\s*'@secuura/shared'\s*,"` at M21, 12:07 |
| root factories at #931 head | 10, all `() =>` helper form; `makeSharedMock` in 12 files (control) | same at `f2e0cb3c1`, 12:07 |
| ks1103 at develop | blob `816f13d24` (M18 = M20 = M21), 264 lines, root `jest.mock('@secuura/shared', () => ({ runWithTenantId…, queryWithTenantGuc… }))` at `:45-48`; ABSENT at #931 | `ls-tree`, `show`, grep on the saved copy 12:07 |
| ks764 test at develop | blob `5a78c4181`, 293 lines, root factory `:97-105` with `...actual` spread; same blob at #985's head; ABSENT at #931 | `ls-tree`, `show` 12:08 |
| ks444 at develop | blob `b00744574` (M18 = M21), 132 lines; **`assertSafeOutboundUrl` already in the factory `:52-57` under a KS-927 comment `:36-51`** (landed `b1cb8466f` 2026-09-12, #926); `'3 of 5'` 0 hits; `toHaveBeenCalled` 4 (all `mockExecuteRaw`); no `from '@secuura/shared'` import | `show`, `/usr/bin/grep -c -i` on the saved copy, `git log -- file` 12:11 |
| ks444 at #931 / #720 | `20383b359` (helper form of the THREE-key factory) / `d4f958bec` (+9 with the "3 of 5" comment); `diff --numstat M21 fcc611d29 -- ks444` = `9 18` | `ls-tree`, `diff` 12:11 |
| ks695 at develop / #985 | `d377aa8c2` / `6d55452f2` | `ls-tree`, REST files list 12:08 |
| qa-f4 file | develop `2dbc65f4c` (101 lines), #931 `146fed176` (+6 −4 at `:31-37`); filename referenced by NO file content at M21 (`git grep -i 'resolveonbehalfof-org-normalisation'` rc 1, 0 lines; control `makeSharedMock` → 12 files); 1 `qa-*` file among 59 `.test.ts` at M21 (52 at #931) | 12:12–12:13 |
| BACKLOG.md | develop M21 1,036 lines (`:182-200` KS-721 row with provenance at `:193`; `:313-314` the unticked webhooks-500 row); branch 1,127 lines (`:138-160+`, `:315`, `:609-616`); #720's BACKLOG diff 278 lines / 7 hunks; the struck-through `services/shared` row says "KS-657 stays In Review for exactly this" | `show`, `sed -n`, `/usr/bin/grep -n -i` 12:11–12:13 |
| audit-baseline.json | `03d1680e3` at M21 and #931; **`33bc6f29a` at #720** | `ls-tree -r` 12:14 |
| originate runner | JEST (`package.json:10`); `jest.config.js` testMatch/ignore; `packages/shared` `main: dist/index.js` | `show` 12:14 |
| worktrees | 103 dirs / 105 `.git/worktrees`; `s223-*` 0 (control `s221-*` 4); `rebase-720` detached at `fcc611d29`, porcelain 0, mtime 09-08; no HEAD holds the ks-1061 or ks-487 branch ref (60 HEADs hold a `ref:`) | `ls`, `cat HEAD`, `status --porcelain`, `/usr/bin/grep -l` 12:13 |
| seat id | s223: 0 hits in history.md (controls s222 3, s221 5, s220 9), 0 briefs, 0 worktrees, 0 dirs; **s224 exists** (STACK seat, `-B`, launched 12:09:16; brief line 41 reserves s223 for L3b; records dir `2026-09-14_s224/` mtime 12:11) | `/usr/bin/grep -c -w -i`, `ls -t` 12:10–12:13; daily note 12:10 block |
| history.md headings | s221 (24), s222 (35), s219 (48), s216 (59), s215 (76), s218 (94), s217 (105), s214 (119), s213 (141), s212 (145), s211 (168); 14,754 lines | `/usr/bin/grep -n -i -E '^## '` 12:10 |
| Linear | KS-1061 In Review/Medium/**UNASSIGNED**/1 comment/#931; KS-487 In Progress/High/board acct/21 comments (newest Peter `12765a04` 09-09); KS-657 In Review/Medium/board acct/4 comments (08-17)/#720 #717 #714; KS-777 Todo/Medium/board acct/1 comment/0 attachments; KS-658 Backlog/Medium/board acct; KS-721 archived 09-05; KS-485 31 comments newest `57b488ad` 01:12:55Z; KS-764/KS-1103 Done+archived; KS active **102** (40/25/32/5) | `linear_l3b.py` 12:09:03–12:09:26 |
| board searches | `sharedModuleMock` 1 · `makeSharedMock` 1 · `F-926-2` 2 · `ks1103-verify-hash-field` 1 (KS-1118) · `ks764-admin-api-keys-…` 0 · `qa-f4-resolveonbehalfof` 0 (the ticket spells it `qa-f4-…`) · `threadTokenMint` 5 · `assertSafeOutboundUrl` 2 · `ks444-…` 8 · `mock completeness` 0 | same |
| decision queue | **19** ruled-undelivered `secuura-` cards (listed in the brief) | `decision_queue.sh list ruled --undelivered secuura-` 12:08 |
| Kam today | 11 messages, 4 Decisions (dedupe `b`; fourteen-merged `close-by-residue`; 881-dismiss `dismiss`; launcher-ssh-keepalive `delegate`) | `kam_rulings_today.sh` 12:08 |
| L5 gate | originate at M21's tree: 56 suites / 598, ks444 pair green | report line 38, 12:14 |
| instruments | node v24.7.0; `/bin/bash` 3.2.57 only; `push_protocol.py` sha256 `d2a5309661d5f961…` — non-fast-forward = PROTOCOL-DIFF | 12:12–12:14 |

## B. What the sweep (22:05 09-13, M18) said that is DIFFERENT at source
1. **develop**: sweep M18 `8861e6216`; commission text M20 `a5334350`; **source M21 `5210ddf31`** (12:00:24). M22 (#985) expected, not landed.
2. **#720 `mergeable_state`**: sweep `dirty`; source `unknown` (GitHub dropped the cached value after develop moved; will read `dirty` again).
3. **#720's unit fix is REDUNDANT on develop**: #926 (KS-927, `b1cb8466f`, 09-12) put `assertSafeOutboundUrl` in the ks444 factory with its own comment. The sweep's "files BACKLOG.md + ks444 test" is still the API's list, but after the merge-in the branch's own delta on ks444 collapses to Peter's ask-1 assertion only. Peter's ask 2 ("3 of 5" at `:40`) is MET by develop's text — the brief says report it, do not re-add.
4. **The fold is TWO files, not one**: the sweep (from the builder's 05:02 note) named only `ks1103:45-48`; **`ks764-admin-api-keys-revoke-route-contract.test.ts:97-105` (L5's, landed 12:00 as M21) is a second hand-written root factory** and reds the same guard cell. The brief adds it to Owns as ONE hunk (flagged below for Wednesday's confirmation).
5. **#931's ks444 hunk now CONFLICTS with develop** (the KS-927 block, three-key → four-key factory) — the sweep predicted no conflict for #931 beyond #965's file ("Whether #931 conflicts with #965 … not re-derived"). The resolution (helper form + four overrides under the KS-927 comment) is written out; a T3 tamper makes the one predictable mistake visible.
6. **Peter's five**: the sweep's paraphrase "1 toHaveBeenCalled…; ':40 3 of 5 → 2 of 4'; merge the two threadTokenMint rows; tick BACKLOG.md:315; +1" — the "+1" is NOT an assertion; it is **ask 5: move the `.env` forensics (`BACKLOG.md:611-615`) to KS-658, keep the conclusion**, plus **ask 6: re-run `services/originate` at `fcc611d29` and post the number** (§8 lists six). Quoted verbatim in the brief.
7. **KS-657 does NOT close on #720**: the ticket's acceptance 2 (fold-vs-repair, reserved for "whoever knows the intent behind `cache/connection-pool.ts`") is a decision; #720's own BACKLOG hunk says "KS-657 stays In Review for exactly this". The sweep's "Closes with: 4 tickets" over-counts by one; the class is closer to `f` than `c`. Wednesday routes the decision (Kam / Stuart).
8. **Must-not list**: add `ks1058-anchor-failed-preserves-thread-token.test.ts` (in #912's and #937's file lists — L3a) — the sweep listed ks1004/ks535/ks1059 only.
9. **Peter's review location**: the sweep's "no review" is right for `/pulls/720/reviews` (0) — his asks are ISSUE comments; the brief says so, so the seat does not look for review threads.
10. **Row line numbers moved**: Peter's "develop `:267`" for the unticked row is `:313` at M21; the KS-721 row is `:182-200` at M21.
11. **KS-777's rename target id**: the sweep said "the ks-NNN convention" without an id; the brief picks `ks777-` (the ticket that tracks F-4) and says why.
12. **Open PRs**: 42 (sweep) → 45 (12:07). **KS active**: 108 (sweep) → 102 (12:09).
13. **"rebase"**: the commission says rebase for both PRs; the brief prescribes `git merge --no-ff <develop>` INTO each branch — `push_protocol.py` reads a non-fast-forward move as PROTOCOL-DIFF (STOP), the 07:2x round-2 ruling and today's 02:06:59Z STACK ruling both say "never rebase", and Peter's line-cited heads stay in history. Flagged in section 8(1) of the brief for Wednesday to overrule if she meant a literal rebase + force-push.
14. **The 09-11 TESTED lesson's rule 3** ("the merge is a squash, done by the author seat") vs the commission ("the MERGE SEAT merges, never the lane seat") — the brief follows the commission and names the contrast in PROVENANCE.

## C. Flags for Wednesday BEFORE send (drafter's additions beyond the commission — confirm or strike)
- **F1 — ks764 fold added to Owns** (B.4). Alternative would be leaving #931's own guard red on develop, or weakening the guard — neither is acceptable; but it is an outside-Owns hunk on L5's file (s216 wrapped; #985 carries the same blob and does not edit it). The brief states it as this commission's ruling.
- **F2 — merge-in, not rebase** (B.13).
- **F3 — ask 1 in BOTH 201 cases** (Peter wrote "in a 201 case"); the brief's default is both, with the singular alternative named in 8(4).
- **F4 — KS-657 not closing** (B.7): the merge seat's ADDENDUM for #720 should not archive KS-657; a routing decision for Wednesday.
- **F5 — the KS-1061 assignee write** (UNASSIGNED → board account) is stated as CONFIRMED by this brief per the commission ("KS-1061 unassigned → ours").
- **F6 — the wrap comment on KS-485** with the `@peter` mention per CLAUDE.md step 3 — the brief carries it as the ONE mention; the seat's single PR comment answering Peter's pass has 0 at-signs.

## D. UNMEASURED (and the instrument that closes each)
- Whether the `--no-ff` merge of M21 into `f2e0cb3c1` conflicts ONLY on ks444 (predicted from `diff` reasoning, not run — `merge-tree --write-tree` is a write verb for a drafter). Closes: the seat's own `git merge` output; s224/s220's `merge-tree` if Wednesday wants it pre-measured.
- Whether the merge of M21 into `fcc611d29` conflicts on BACKLOG.md in N regions (predicted MANY; not run). Closes: the seat's merge.
- Whether the ks764 `...actual` spread inside `makeSharedMock` leaves every ks764 cell green (reasoned from the qa-f4 precedent; not run). Closes: the seat's `npx jest` on that file after the fold.
- The originate suite count at `fcc611d29` (Peter's ask 6 — nobody has it). Closes: the seat's run at that SHA before the merge-in.
- The current originate count at M21 by this drafter (the L5 gate's 56/598 is RELAYED). Closes: the seat's baseline.
- Whether GitHub recomputes #720 to `dirty` (expected) — `/pulls/720` after any event.
- Whether M22 (or an L7 squash) lands before the seat's ITEM 1 push — `ls-remote` before each push (in the brief).
- Peter's `services/originate/Dockerfile:62-68` line numbers — relayed from his comment, not re-read.
- The `secuura-launcher-ssh-keepalive` card's delivery mark (absent from the undelivered view; not opened).
- The #965 tier-2 report's exact §8/F-5 text — `report.md` there is read by grep as a binary (an encoding artefact); the fact is carried from the builder's 05:02 comment, which quotes it.

## F. Develop moved AGAIN during drafting (12:29:12 AEST) — folded into the brief
- `ls-remote` 12:29:12 → develop **M23 `dfc63fe48ebaa97271f3ff66315a742ba4d79bc2`** (#924, KS-773, 02:23:32Z, 1 file `scripts/preflight/lockfile-cleanroom.sh`) ← **M22 `f82746f9c`** (#918, 02:15:47Z). Both L7 squashes; neither touches a lane file. #985 still open (`unknown` — s224 mid-merge-in); #925 open. #931/#720 heads UNMOVED.
- The brief's blob/line measurements were taken at M21 and HOLD at M23 (M22/M23 changed `scripts/preflight/` only — from the API's `/commits/` file lists, not a local diff: the two SHAs are not fetched locally). The brief names M23 as the pin at 12:29, keeps M21 as the measurement base, and calls #985's future squash "M#985" (its number unknown) instead of "M22", which the earlier draft had assumed.
- Instrument: `gh_tip.py` (REST `/commits/<sha>`, `/pulls/{985,918,924,925}`) 12:29–12:3x.

## E. Scratch artefacts (read-only copies, session scratchpad, not project writes)
`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/85873ddd-c4f1-4994-8d61-80f2a8670593/scratchpad/` — `gh_l3b.py` + `gh_l3b.out` + `gh/` (PR JSON, bodies, comments), `linear_l3b.py` + `linear_l3b.out` + `linear/` (issue JSON, descriptions, comments), `ks1103_M21.ts`, `ks444_M21.ts`, `backlog_M21.md`, `backlog_720.md`, `pr720_backlog.diff`, `grep_*.out`, `gh_tip.py` + `gh_tip.out`, `selfcheck*.out`.
