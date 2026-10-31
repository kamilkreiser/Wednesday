STARTABLE: yes, after the stamp (Q-1 to Q-3 below have defaults; nothing blocks the launch).

# B979 drafter report (read-only; Sat 31 Oct 2026 12:4x AEDT)

BLUF: Kit `2026-10-31_B979_SEAT-H81_hpsmpoc-407-binding-rule-rows.md` (90 lines, unstamped, 9 four-underscore lines, 0 non-ASCII, 0 at-token lines). Lane: HPSMPOC-407 items 1 and 3 only, one path `infra/tests/test_security_baseline.py`, one commit on a new branch `b979/hpsmpoc-407-binding-rule-rows` off main `8ce48527`, no port, Sonnet. Items 2 and 4 are named as NOT BUILT (no fix-shape, a ruling). Nothing was run, written to a project, or sent; no Jira write.

## Measured
- main = `8ce485275455e07eaa39c46a50e62e7f7f2b3c83` (gh GET, 2026-10-31T01:33:56Z). Open PRs 0. `heads/b979` 0 (control `heads/b937` 1). `.tools/b979` and `.tools/wt-b979-base` absent.
- Panes: tuesday, Datasec/Security-Composer-R95, Datasec/MPS-M52, fleet-monitor; no H81. `LC_ALL=C uptime` load1 7.36 at 12:38 (expect a wait at the heavy gate). Sonnet id `claude-sonnet-5-5` (models_latest.json line 23).
- Test file raw at main: 2758 lines, sha256 `7f9af34f364016e4779f8785d754faa91ca3c9320fe2a12bb2c9da8736339a0b`; `    def test_` count 131 (no-such control 0). Survivor line 1195 (`not isinstance(picked, bool)`, once). Existing rows at 1898, 1912 (the landed non-bool row), 1927 (insertion anchor). Stale comments at 1240 (trailing, on the `RULES` close) and 1628 (whole-line): both still name only rbac, keyvault, appservice; the block at 1105 lists eight calls.
- Jira HPSMPOC-407 read whole by GET (Backlog, 0 comments); items 1 to 4 match the sweep. Sources B961-1 and B943-2/-3/-5 read; B961 line 128 gives the cells.
- ci.yml: infra job line 575 runs `bash infra/scripts/validate.sh` on ubuntu-latest; no `python-version` pin (count 0), so the runner Python is UNMEASURED. Kit therefore asks 3.14, 3.9 and `-X dev` as B951 did. Expected counts: file 131 -> 132, whole infra 309 -> 310 (builder re-measures).
- Q-1 helper hashes (b916) equal the B951 kit's: run_infra.sh `7583a58b187a8621f491e1344e9e176f67d1b747fe55970214c049b00bdfa9eb`, repeat20.sh `c65c5e8f59f21952d165b18c9f24e9e60d7e2750813fb2c45268850b0376ed72`, modrun.py `ee23053f89c344a7b8a62dbd16e4b90140cefdd644eb936909896c9f87be9c26`. (The kit abbreviates them; full values here.)
- The checkout's `git ls-remote` failed here (deploy key path not on this machine); main was read by gh instead. The builder's own seat must show the real `ls-remote`.

## Points to know
- The ticket calls the neighbour "falsy-only" but its expression `(picked is None or bool(picked) and not isinstance(picked, bool))` takes both branches for None and a TRUTHY non-bool; a falsy non-bool picks by truthiness, so only scoped-SECOND falsy forms slip through. The kit says this and asks both subtests to be scoped second. Under m16 B961 measured the same falsy-second shapes differing from the pin, so the kit predicts the new method red under m16 too; the builder measures.
- Item 3 changes exactly 2 existing lines (comments only), so "numstat removed = 2", not 0; the byte-equal check is tokenize with comments dropped plus AST segments. This is stricter than B951's pure insertion; the gate should be told.
- New method (not subtests inside the landed row) so the landed row stays byte-equal; the ticket's "two more subtests" is met inside the new method.

## Questions (defaults)
- Q-1: reuse the three b916 helpers read-only (YES).
- Q-2: record items 2 and 4 as declined-for-now with no build (YES; they stay in Backlog notes).
- Q-3: gate tier 2, round 1 (default; test-only).

## Stamp values (suggested)
- STAMP: STAMPED <clock> AEDT Sat 31 Oct 2026 by the Tuesday seat; kit and this report read whole; Q-1 YES, Q-2 YES, Q-3 tier 2 round 1.
- KEYS: HPSMPOC-407; items 2 and 4 recorded declined-for-now by the records seat.
- LAUNCH WINDOW: launch_when_cool at load1 below 7 (12:38 read 7.36); beside R95 and M52.
- Launch authority: 2026-10-16 HPSM-POC grant, 2026-09-13 as-many-agents, 2026-10-24 every-boot-works-tickets, Datasec CodeQL policy, 2026-10-22 Sonnet-first, usage grant.
- Hard stop and target READY: Step 0 + 120 and + 75 minutes.
- Main and refs at launch: `8ce485275455e07eaa39c46a50e62e7f7f2b3c83`, no `refs/heads/b979*`, open PRs 0 (re-read at launch).
- Model receipt line: `model: claude-sonnet-5-5 -- Sonnet first: a test-only pin of a rule a prior tier-2 gate measured (model-routing.md row C2 line 92, class row L6 line 85, gate row G2 line 109, the product owner's 2026-10-22 Sonnet-first grant)`; load1 read at launch.
- Last line: `READ-WHOLE-BY-TUESDAY: DONE <clock>`.
