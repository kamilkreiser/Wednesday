STARTABLE: YES (engine half only, all three keys; Api, DTO, openapi, web and audit-reason wiring held and stated as the narrowing)

# B1000 drafter report (SEAT-M53, MPS V4 chain -252, -258, -259), 2026-11-01

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1000_SEAT-M53_mps-v4-252-258-259.md`. Shape copied from the B974 kit, including the two B974 addenda lessons (unset purchase result must be byte-equal under both serializers; TMPDIR outside any git tree).

## BLUF
All three keys are startable as ENGINE-ONLY slices, in one chain, one branch `b1000/mps-v4-252-258-259-groups-tier-sell-basis`, three commits, one push, no PR by the seat. No ruling is missing: D-05 a (CLARIFICATIONS.md:673), D-03 a (:671), D-04 a (:672) are on record, C-45 table starts :654; C-16 :236; MPS-4 :331. Each ticket is only PARTLY done by this lane (the Api/audit half stays open), so the records step must comment and not move them. Model Opus (C3, model-routing.md:93; id claude-opus-5-5, models_latest.json:37). Gate: one tier-1 G1 (:108), round 1 of 2, a new class.

## Facts re-measured (instrument; control)
- main = 5d96a3dc62871dd526f34a86215bacf5f7943ad6 (`gh api -X GET git/ref/heads/main`; `compare/5d96a3dc...main` = identical). Open PRs 121, 120 only (`pulls`). No `heads/b1000` (matching-refs 0; control `heads/b8` 7, `heads/b9` 4).
- Jira GET (own scratch reader that mirrors `.tools/b585/jira_get.py`, env read in-process; `MPSCALC-99999` -> HTTP 404): 252, 258, 259 all Backlog, 0 links; 252 has 1 comment (2026-10-20, a purchase-pair test of the version-diff route wanted with V4); 258 and 259 have 0 comments.
- Highest register ids at main: R-30, X-34 (each x1); X-33 count 0 (no such row; control string 0). Next ids expected X-35..X-37.
- Source reads at 5d96a3dc (raw GET, line counts): PurchaseInput.cs 126, PurchaseCalculator.cs 898, PurchaseRecomputation.cs 224, PurchaseResult.cs 243, ENGINE.md 202, QuoteInput.cs 99. Fact-check counts in the kit REFUSE list were each read with a zero-control (`zzz-no-such-string-7f3a` = 0).
- Existing per-line `PricingMethod` (PurchaseCalculator.cs:523) and rental per-line `TierOverride` (QuoteCalculator.cs:228) are the precedents; the reconciler (PurchaseRecomputation.cs:62-64, :127, :181-182) recomputes quantity and method independently, so it is in scope for -252 and -259 (lifted from B974's HOLD).
- PR #133 squash: 1 parent, 3 commits, 9 files.
- Ports: word-boundary scan `-w -E '948[0-9]'` over every non-`.pre-` brief dated 10-30, 10-31, 11-01: 0 files (control `970[0-9]` fires on 3 files: B971 report, B974 report and kit). `lsof -nP -iTCP:9480-9489 -sTCP:LISTEN` 0 rows (control: all listeners 15). Block 9480-9489 reserved, none needed.
- Panes (tmux): tuesday, HPSM-POC-H86, H85, MPS-R97, fleet-monitor. No MPS-M53. `M53` appears only in the finished NexusAI B877 kit (same reuse as M52).
- B987 partition: it holds the ROOT repo (HEAD 7fbf8f5b), records/b987, CLARIFICATIONS/BACKLOG/JIRA/history, `.tools/b987`, `.tools/wt-b987-records`, and Jira on 21 keys (109...186, none of 252/258/259). `.tools/.git-lock` absent (ls). Code repo `2_Project_Files/.git` is a separate repo from the root `.git` (both exist). Kit takes the shared lock only around the two worktree adds and the one push; heavy slots are separate.
- Load1 2.84 at drafting.

## D-decisions
D1 Opus C3 (not Sonnet C2: the tickets leave three money-rule designs to the engine: where the fleet quantity lives, the tier override across pools, section-versus-line method precedence). D2 three commits in order 252, 258, 259; chain may end at commit 1 or 2 if the clock forces it (order of loss in STANDING LINE 13). D3 target READY 6h, hard stop 8h (B974 was 3h/5h for two tickets). D4 Reconciler in scope where a stated group or method needs a mirror. D5 13 mutants (MU1-MU13), predictions written first. D6 Narrowing: `src/MpsCalc.Api/**`, Dtos.cs, openapi.json, web, audit reason/permission are NOT the seat's, despite the delta sweep listing Dtos.cs and openapi.json for lane 1. Reason: -252's text says contract changes go through lane V0 first; the audit/permission live in PriceAudit.cs; new field names would reach a person.

## Q-questions for Tuesday (each with a default)
- Q-1 Accept the engine-only narrowing for all three (Api/openapi wiring becomes a later contract-sync lane after this one lands)? Default: yes. -258's acceptance clause "a reason, recorded in the audit" is NOT met and not claimed.
- Q-2 Should a purchase tier override add the rental Info issue (`TIER OVERRIDE`, QuoteCalculator.cs:230, whose text says "requires permission, a reason and an audit event") on purchase too? That puts an existing sentence on a new surface. Default: no issue (zero words).
- Q-3 -259 precedence: a section's stated method applies only to lines whose percent comes from the section and whose own `PricingMethod` is the default; a line's explicit margin still wins; under a margin section a line cannot opt back to markup (the line member is a non-nullable default and cannot say "unset"; changing its type would change every stored hash). Default: accept as written. If the product owner wants "section wins over every line" or a line opt-back, that is a ruling and -259 should be cut from the kit.
- Q-4 The optional Api.Tests file for the -252 comment (purchase-pair test of the version-diff route): default keep, droppable by the builder if it needs anything outside `tests/` (first to go under the order of loss).
- Q-5 Seat name `Datasec/MPS-M53` (name reused from a finished NexusAI seat, as M52 was). Default: keep.

## UNMEASURED
No build, test or compile run. Not measured: that an unset trailing member keeps InputHash and ApiJson bytes (the B980-1 trap), the full list of line-quantity read sites (the kit gives a reading and demands the grep), X-34 fleet-total behaviour under a group, whether the Api.Tests helpers can run the diff route over a purchase pair without a src change, 5,000-quote suite cost, whether CI's ci.yml step text matches the kit's quoted predicate (quoted from the B974 kit, not re-read at source this time; the kit tells the seat to re-read it), whether B987 has moved since its 17-line STATUS.

## Outside-the-fences disclosure
- Wrote only the kit and this report. Scratch under the session scratchpad only: a Jira GET script (`jg.py`, reads the project `.env` in-process, prints no token) and raw files fetched by `gh api -X GET` into `scratchpad/src`.
- Read (not in the fence list but worth naming): the project's `.tools/b585/jira_get.py` header (the read-helper pattern; I did not invoke it, I wrote a mirror in scratch), the project `CLAUDE.md`, `JIRA.md` grep lines, the B974 and B987 files under `1_Project_Definition/Briefs/` including B974 ADDENDUM-1/-2 and the B974 STATUS last line and grep, B987 STATUS last line. I listed `.tools/` directory names of the project (ls only) for the lock/name checks. No `decision_queue.sh`, no briefs_staged, no scoreboard, no ledger, no other client. No git write, no fetch in any repo; only `git remote -v` and `ls-remote`-class reads (`git -C 2_Project_Files remote -v` with `--no-optional-locks`).
- Two tool hooks blocked a first command (a `cd`, a bare `=====` separator); both re-issued without them. Case-sensitive grep advisories were noted; the counts above used `-F` fixed strings with a zero-control.
- The kit names the project ruling ids C-45, D-03/-04/-05/-06, C-16, MPS-4 (project ids, no decision-card slug); no person's name in the kit.
