# B382 drafter report (2026-10-21 ~07:50 AEDT)

Brief: `2026-10-21_B382_SEAT-D14_hpsmpoc-lane3-feedback-api.md` (119 lines, 3 unfilled stamp slots). Shape copied from B372 (standing lines, HP Restricted-docs STANDING HOLD verbatim, PRIOR-WORK CHECK, CodeQL, STATUS last-line formats) and `BRIEF_SKELETON.md` (its RULED/PROVENANCE gate literals are NOT used, as in B372; the RULED BY KAM and RULED BY TUESDAY paragraphs are bold labels, not gate lines).

## Headline
By my census Lane 3 is **small**: of HPSMPOC-226's N-1..N-9 plus the three B177 notes, **1 item is open and buildable** (the N-9 pin: a test that the privacy export lists each attached file's five facts and never its bytes). N-8 is ACCEPTED (C-119), left alone. B177 N-1 is a customer-words change (Kam's), not built. N-6, B177 N-2 and the BFF halves of N-1/N-2 are BFF, out of lane. HPSMPOC-99: N-7 and N-8 merged (PR #109); N-4 is Kam's; N-9 (per-process limiter) is handled comment-only because a shared limiter needs a table, a migration and a scale-out. HPSMPOC-109 O-2 is excluded (Lane 5, `ci.yml`) and is probably **already built**: Jira says PR #105 / main `0a85b89`, and `ci.yml:569-580` at main carries the pinned shellcheck. Lane 5 should read its Done-when before building anything.

## Questions for Tuesday (each with a recommended answer)
1. Q1. Launch this lane at all, or fold the one test row into another seat (it is about one hour of Sonnet work, mostly waiting on load)? Recommend LAUNCH: it is disjoint from every other lane and gives the census a measured home. The alternative costs a re-brief.
2. Q2. Include optional commit 2 (comment-only note on the per-process limiter, FeedbackModule.cs:171-175 plus one README sentence)? Recommend YES, separate commit, dropped if the hunk exceeds 6 lines; it touches `api/src` but comments only, proved by program, tier stays 2.
3. Q3. Gate tier 2 (G2) with an `api/src` non-comment STOP? Recommend YES. Counter-view: the module is handed to client testers (G1 wording); the diff adds a test and comments only, so G2 applies.
4. Q4. Model row C2 (Sonnet 5.5), as B372? Recommend YES. L6 (test-only) is local-eligible, but P4 says Datasec has no local tier.
5. Q5. Mutants live in the worktree, restored byte-equal, never committed (three: mA add bytes, mB drop size, mC rename type; one control gf)? Recommend YES, same as B372.
6. Q6. B177 N-1 (slow-sender words): file nothing, draft nothing, one line in FOR TUESDAY? Recommend YES; it is Kam's words and may be BFF. If Kam wants it before Thursday, Tuesday drafts the wording as a card.
7. Q7. Jira: one comment on HPSMPOC-226 only, no comment on -99? Recommend YES; the records seat covers -99 and the Done transitions.
8. Q8. Target time for READY FOR QA? Recommend Wed 21 Oct 14:00 AEDT, so a tier-2 gate and a merge fit before the 23:59 freeze. I did not put a time in the brief; Tuesday adds it in the Stamp.
9. Q9. Sibling-lane ids and panes go in the third slot (sibling-lane list), since I do not know B379-B381/B383+ numbers for the other lanes. Fill it with each lane's brief id, pane and ports.

## Measurements (instrument + control)
| Fact | Instrument | Control |
|---|---|---|
| Main = `54fbceac12393f503fae8c5810af9609bac44548` | `git ls-remote origin refs/heads/main`, 07:41:29 AEDT | local `rev-parse origin/main` reads `6818896b` (stale), `cat-file -t 54fbceac` fails locally, so code was read by `gh api` at the sha |
| `b382*` refs on origin: 0 | `ls-remote 'refs/heads/b382*' \| wc -l` | `b36*` returned 2 |
| `.tools/b382` absent | `ls .tools` listing | same listing shows b372, b375, b377, b378 |
| Open PRs: 0 | `gh pr list --state open` | `--state merged --limit 3` = #167 `54fbceac`, #166 `fa8416de`, #165 `6818896b` |
| Files changed 6818896b..54fbceac: ImportFailGuardTests.cs, PkcsInPackageTests.cs, Hpsmpoc290Tests.cs | `gh api compare` | tree has 1534 entries, `truncated: false` |
| Feedback src/test file list (13 src, 12 test files) | `gh api git/trees/<sha>?recursive=1` | `truncated: false` |
| -226 Backlog, 5 comments, last 2026-10-19T21:11:38 | Jira GET | -214 read by the same code returned Done with 2 comments (differs, so the reader discriminates) |
| N-4 `FeedbackFiles.cs:125-130, 136-140, 205`; N-5 `:160-162, :191`; N-7 `FeedbackDispatcher.cs:76-84`, `IFeedbackSink.cs:23`, `AutomationWebhookSink.cs:26`; N-3 `AutomationRouteTests.cs:52-53` | `gh api` raw file at the sha, `sed -n`, line numbers from `cat -n` | symbol names matched the ticket's cited lines (4 of 4 ticket cites agree) |
| N-9 gap: export test asserts names only, `FeedbackAttachmentTests.cs:499-501`; export code `FeedbackPersonalData.cs:35-48` | same | the Erasure test at `:490` is the ticket's cited test (ticket said `:490-501`) |
| B177 A1-N1 fixed: `ContractTests.cs:54` says "contract 0.14.0", `0\.12\.0` count 0 | `/usr/bin/grep -c -i` | 98 lines match `contract`; line 54 positive |
| -99 N-9 limiter `FeedbackModule.cs:176-209`, singleton `:98`; README has no per-process line for it | `gh api` raw + case-insensitive grep | README does say "per process" for the form gate at `:34` |
| `ci.yml:569-580` has pinned shellcheck v0.11.0 | `gh api` raw + grep | `-n` hits at 387/456 are unrelated `shellcheck disable` comments |
| `AGENTMAIL_API_KEY` absent from `.env` | `/usr/bin/grep -c '^AGENTMAIL_API_KEY='` = 0 | `^JIRA_API_TOKEN=` = 1; no value printed |
| helpers `jira.py post.py read.py lock.sh gl.sh` present in `.tools/b372` and `.tools/b300` | `ls` | n/a (listing) |
| load 11.24 / 8.48 / 6.62 at 07:41:29 | `uptime` | over the brief's 8 threshold: stated in the brief |
| `levels.sonnet.model_id` = `claude-sonnet-5-5`, `warnings` = [] | read `models_latest.json` | not typed into the brief |

## Could not verify (all marked UNMEASURED in the brief)
No `dotnet` was run: baseline count, whether the new row is green at main, and the red set under each mutant. Whether the contract's `PersonalDataExport` tolerates an extra key (decides which assertion fires first). BFF halves of N-1/N-2/N-6/B177 N-2 (not read, out of lane). Whether ports 7420-7429 are free (no `lsof`). Live panes. Hosted instance count. The Feedback-lane tests were not run, so "built" for N-4/N-5/N-7 is code-read plus test-presence, not a green run.

## Fences kept
Wrote only the two B382 files. No Artifact, Docs, mail, board, upload. Git reads: `ls-remote`, `rev-parse`, `cat-file` (local), `gh api`/`gh pr list` GETs. No fetch/pull/checkout/commit. No HTTP to a hosted host. Jira GET only. Scratch files under the session scratchpad (`jira_*.txt`, `src/`, `tree.json`, `l3_*`).
