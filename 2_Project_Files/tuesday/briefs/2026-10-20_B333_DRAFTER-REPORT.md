# B333 DRAFTER REPORT · Composer PR #83 fix round 2 (SEAT-W16)

Drafted 2026-10-20 15:17-15:25 AEDT. Read verbs only: `git --no-optional-locks` ls-remote/show/grep/cat-file/rev-parse/for-each-ref, `gh api` GETs (project gh-config), `lsof`, `uptime`, `ps`, `tmux list-panes`. No git or gh write, no docker, npm, az or HTTP. Brief: `2026-10-20_B333_SEAT-W16_composer-pr83-fix-round2.md` (148 lines, one stamp slot = launch time, 0 hidden characters, 0 client-name hits).

## Measured facts
- **Pins 15:17:01:** branch and `refs/pull/83/head` both `314f40d989c9…`; main `d8d2a2c74a90…`; `refs/heads/b333*` absent (control: b301 printed). PR #83 at 15:20: open, draft, 2 commits, 17 files, +2001/-41, mergeable clean. Open PRs are #83 and #82 (`e6288983`).
- **The repo's precedent fits exactly:** `0005:30-31` already does `CREATE TRIGGER customer_approver_identity_immutable BEFORE UPDATE … EXECUTE FUNCTION forbid_column_change('tenant_id', 'engagement_id')`. The function is at `0004:115-130`. Its message `IDENTITY_IMMUTABLE: %.%` (`:126`) already exists, so there are no new words.
- **Trigger rather than revoke:** the 0007 grant loop (`:78-81`) states that every non-key column is writable and that tests enforce this. `hardening.db.test.ts:1243` asserts that the rule also binds superusers.
- **Writer census** (one-line grep only): the only `UPDATE pc.device_group` is `putDeviceProfile` (`inputs.ts:553`). It never names `tenant_id` or `engagement_id`. The no-op sweeps are at `hardening:1045` and `wp4-0016:154`. There are 0 `ON UPDATE CASCADE` and 0 `DO UPDATE` on `device_group`.
- **The gate's premise is wrong:** `discovery_answer` has a COMPOSITE foreign key (`0004:34-37`), not a single-column one. Moving a group that has answers is therefore already refused (by reading; expected SQLSTATE 23503). The brief tells the builder to say so.
- **The down-test's `shape()` covers only `exception_record`** (`b322-0022-down:103-136`), so it must be widened to `device_group` triggers. The checksum is pinned at `down.sql:37` and `DEPLOY.md:277`. The test reads the sha dynamically (`:175-181`).
- **Seats:** B320 (Composer gate, PR #82, Sonnet) launched at about 15:19. B323 and B330 are not live. Load is 2.35. Ports 7550-7619 are free (rc 1; the unfiltered control shows 12 lines). The brief uses 7550-7559.

## Open questions (each with a recommended answer)
1. **Routing row.** There is no "findings fix round" row. C4 (a migration whose recipe drops) could be argued. **Recommend C2 Sonnet,** as B322 was routed. The fix is spelled out, destroys nothing new, and goes to a tier-1 Opus re-gate.
2. **`WED_USAGE_STOP=100` placement.** As ruled, it goes before `cockpit.sh`. B331 put it inside the quoted pane command. **Recommend:** if you are unsure that cockpit passes the environment into the pane, use B331's in-string form.
3. **Test files.** **Recommend extending B322's own test files.** They are new files in this unmerged PR. A b333 file is allowed.
4. **B331-2 red proof.** That row is GREEN at 314f40d by design. **Recommend accepting mutant m-k12 as its red** (the brief says so).

READ-WHOLE-BY-TUESDAY: PENDING
