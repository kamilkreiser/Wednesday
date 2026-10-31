STARTABLE
# B977 drafter report (SEAT-G236, HPSM-POC PR #262, tier 2 round 1 of 2, class "test-only pin row")

## BLUF
Kit written: 25 lines, 8 four-underscore lines (S1-S7 plus the last line), 0 non-ASCII bytes, 0 at-sign slot patterns (all by program). Startable once Tuesday fills the seven slots. Read-only: no fetch, no worktree, nothing run, nothing sent. Note: main is now feb3da65 (#261 landed), so the head is 1 ahead and 0 behind: the landing tree equals the head's tree unless main moves.

## Measured (Sat 31 Oct 2026 12:07-12:12 AEDT, gh api -X GET under the project config dir)
- PR #262 open, not draft, mergeable true, mergeable_state blocked, created 2026-10-31T01:07:15Z. Head ef4a7e686e49de3fe083d4fdb4572272ae28ca13, base.sha feb3da65, 1 commit, 1 file (web/src/components/security/SecurityDashboard.test.tsx) +33 -1, matching the builder. Title and body read (body names the finding id B965-1 and says "measured by the builder": both go in the FOR TUESDAY wording check).
- Main = feb3da655e12f604ef1c2b9ad65d6aaffb69c78f (the #261 squash, 2026-10-30T23:55:39Z); compare feb3da65...main = ahead 0 behind 0. Open PRs: #262 only.
- Check-runs at the head: gitleaks, dependency review, Analyze (actions) completed success; a CodeQL row completed with conclusion neutral (kit says: not a pass until the analyses complete); Analyze (csharp, python, javascript-typescript), api, two api on SQL Server, infra, web build, web unit tests in progress. Open alerts for refs/pull/262/head = 0, control (main analyses list) = 3.
- Round count: 119 STATUS files start GATE VERDICT; none for PR #262 or HPSMPOC-414 (B965 is the round-2 gate of #253, another class). Expect 0 confirmed.
- Panes: tuesday, fleet-monitor, HPSM-POC-R94, HPSM-POC-H79; no G236. Load: LC_ALL=C uptime at 12:07 load1 2.23.
- Ports: every 10-block in 9600-9999 is named by some 30-31 Oct kit (grep over briefs/2026-10-3*_SEAT-*.md; 9980-9989 by B970 and B969, 9990-9999 by B973 and B969). No kit names anything in 9000-9599 (control: the same grep finds 80xx ranges, so it does see ranges). lsof on 9500-9599 and 9980-9999: 0 listeners. Chosen 9500-9509.
- Sonnet id: models_latest.json line 23, claude-sonnet-5-5 (control: 4 lines mention sonnet).
- Builder claims read whole (66-line STATUS and the commission): rows A and B in a new nested describe; p18h both red, p18 both red, unplanted 7/7 green; suite base 249 files 3607 vs fix 3609; lint and typecheck rc 0; the builder also notes existing held rows in SecurityAssessments.test.tsx are green under p18h (the gap this PR closes). The finding source B965 STATUS line 30 and p18h-proof.txt read: unplanted 1 passed, p18h planted 1 failed ("not to contain 'Open held title'").
- Line anchors in useSecurityData.ts at feb3da65 confirmed by git show: line 94 the reviewed const, line 103 the shorthand `reviewed,` (the kit's plants are written against them).

## Decisions and Q-questions (defaults in brackets)
- Q-1 Port block: every 600-999 block is named by a prior kit, so the kit uses 9500-9509 (unnamed; 0 listeners). Vitest binds no port, so it is a reservation only. [Default: accept 9500-9509; otherwise name another block.]
- Q-2 Landing tree: main equals the PR base, so the gate judges the head merged onto the main read at Step 0 (identical tree unless main moves). [Default: yes, with a refuse if main moves onto the five paths named.]
- Q-3 Mock-bypass grading: the kit makes "a plant that changes what the held branch returns leaves a row green" a Blocker, and a surviving p18h/p18 a Major. [Default: as written.]
- Q-4 Tier: tier 2 stands; escalate to tier 1 only on a product byte (diff is test-only and the mechanism was measured by the B965 and B973 plants). [Default: tier 2.]
- Q-5 The CodeQL row reads neutral already at 12:07 while the Analyze rows run; the kit treats neutral as pending until the analyses complete. [Default: as written.]

## Stamp values Tuesday fills
S1 STAMPED <time> AEDT 2026-10-31 by <seat>, Q answers above. S2 window and load1 (2.23 at 12:07). S3 the reading seat and Q-1 to Q-4. S4 grants (in-clone fetch of two refspecs, npm ci in own worktrees, scratch plants never pushed, ports 9500-9509, own gitleaks). S5 target 75 and hard stop 120 minutes from the gate's Step-0 date. S6 head ef4a7e68 and main feb3da65 (re-read), pane list, check-run table. S7 model: claude-sonnet-5-5 -- G2 -- gauge <n>% from usage_tuesday.json and load1.
Launch: the kit's Launch line (pane Datasec/HPSM-POC-G236, BRIEF_SEAT_LEVEL=sonnet).

## Not measured by the drafter
Jira ticket body (not read; the kit tells the gate to quote the builder commission or GET it); whether CodeQL neutral later flips; PR body wording checked only by reading it.
