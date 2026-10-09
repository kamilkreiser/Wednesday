## BLUF
**Plan confirmed, all of it, and the three new questions ruled as you recommend.** Ctx **24%** (your pane's statusline, read by Wednesday at 03:27:22Z, mid-turn); usage 20%. Do the re-key and its controls now as you proposed (record folder only), then send `STATUS: raise base (Seat K 1st)` with a FRESH develop; I accept the base BY NAME before your worktree. develop at Wednesday's read 03:27:22Z = `81d2e5f4c4151f5291a7a9c186d93a02dc5d38d6`, unmoved; R 22nd will move it when it squashes #1427, so re-read it and re-check the store at your raise base exactly as you said.

## Rulings on the new questions
1. **Q-COMMENTS = YES.** Extend your declared block to `:1567-1574` and `:1786-1787`, COMMENTS ONLY, and declare both in the pathgate. Correct them in place with WHY + `KS-1402` + the prior behaviour (the file's own KS-536 / KS-1312 precedent); delete nothing. `:2146` (/share) and `originate.openapi.ts:1488` stay untouched, as you measured.
2. **Q-HOIST = (i).** Hoist the `getReqTenantId(req)` read and the `db` handle above `:1664` as a pure move; every later use stays intact. (ii) is refused for the reason you gave: it would change the observable order of answers (`RECIPIENT_NOT_FOUND` before `NOT_FOUND`), and nobody asked for a contract change. Pin the order with a cell if one does not already exist.
3. **Q-739-COUNT = 20 dispositions, and name the executed count (25).** Your `it.each` finding is accepted; a `^\s*it\(` count is a census over the wrong frame.

## Accepted findings (your measurements, not re-run by Wednesday)
- **Q-KEY's two conditions** (`PII_ENCRYPTION_KEY` gates `initFromEnv`; `PII_LOOKUP_HMAC_KEY` gates the lookup key, with nothing refusing start without it). C9 pins the request-time answer. Say it in the PR body.
- **The ruled mechanism is STRICTER than auth's path** (`users.ts:306` skips the tenant compare when either side is falsy). That sentence goes in the PR body beside Kam's ruling. KS 1406 stays NOT COVERED and is already filed; file nothing.
- **RLS stated honestly:** the bound predicate is the enforcement, the GUC is belt-and-braces; do not claim two working layers.
- **`pushg1.sh:233` is decorative in TWO ways** (a missing file AND a piped verdict). Your fix (existence assert with a planted-absence control, an unpiped rc read, and a decision on that rc) is approved for `pushk1.sh`. Note it in your handover for the next G-kit user.
- **`searchIssues` is not an absence instrument** (a fabricated term returned 20): accepted and recorded.
- **KS-1402 `updatedAt` 2026-10-09T02:07:01Z with comments unchanged:** unmeasured by Wednesday; not a STOP. Mention it in your READY; do not investigate further.
- Your two self-caught instrument faults (`$"..."` vs `$'...'`, the `\s` control) are noted as caught; nothing rested on them.

## Floor (Wednesday's `tmux list-panes`, 03:27:22Z)
`%0` wednesday · `%1` fleet-monitor · `%8` Seat R 22nd (`Secuura/Blockchain-R`, #1427, lock `.push-lock-d8`, STEP 2 released at 03:22Z; it will push and then squash, moving develop) · `%9` you.

## Model
You are on `claude-opus-5`. Wednesday types `/model claude-opus-5-5` at your NEXT IDLE prompt and confirms by mail. Do not wait for it.

PROVENANCE:
- develop | `env -u GIT_SSH_COMMAND git -C <Secuura checkout> ls-remote origin refs/heads/develop`, by Wednesday, 03:27:22Z | read 2026-10-09
- ctx 24% | `tmux capture-pane -p -t %9`, by Wednesday, mid-turn | read 2026-10-09
- every finding above | your plan mail 03:26:11Z (302 lines), read WHOLE by Wednesday; your measurements, not re-run | read 2026-10-09

SELF-CHECK: re-read end-to-end for contradictions | 14:27
