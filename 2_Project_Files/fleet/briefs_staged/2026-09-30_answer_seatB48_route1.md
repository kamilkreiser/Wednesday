# ANSWER (Seat B 48th): continue with ROUTE 1: make the ROOT lock take undici 7 by a re-resolving command, measured against your pristine control; then legs 6/7/contract in a git+install runner. ctx:39% at 2026-09-30 10:14

## BLUF
**Your ctx: ctx:39%** (Wednesday read of pane %79, 2026-09-30 10:14 AEST). **Continue, route 1.** An excellent STOP: the `up to date` banner-vs-bytes catch, and the pristine-control attribution of the 12 root drift entries, are exactly the discipline this needs. **Kam has still not ruled** (his panel: 0 today), so everything stays in scratch worktrees: nothing pushed, raised or filed.

## ROUTE 1: the commands, tried IN THIS ORDER, stopping at the first that moves the root undici
Run each in your override worktree AND the identical command in `s-b48-ctrl` (the pristine control). Print npm/node versions in the same run; use a parent mount if `EMISSINGTARGET`.
1. `npm update undici --package-lock-only --ignore-scripts` at `Blockchain/Dev` (the verb that re-resolves a named package; B 47th's js-yaml precedent).
2. If it is inert: `npm dedupe --package-lock-only --ignore-scripts` at `Blockchain/Dev`.
3. **If both are inert: STOP and mail.** Do NOT hand-edit a lock and do NOT delete lock entries. Route 2 (overriding the `@connectrpc/connect-node` edge) is Wednesday's next ruling, not yours.

**The acceptance test for a command that moves it:**
- In the root lock, relative to the control, ONLY undici-related entries differ (undici 5.29.0 → 7.30.0; `@fastify/busboy` removed; deduped nested undici). Show the set.
- The 12 known drift entries are set-equal in both trees, so they are attributed to npm, not to you.
- ANY other entry differing from the control is a STOP.
- `integrity` and `resolved` match the registry for 7.30.0, with your False control.

## THEN, only if the root lock moved: the legs, honestly
- **Approved: a third worktree `s-b48-suites`** (`--detach`, never `-b`) with an install sufficient for the audit scripts (it has `git`; the `node:24-alpine` container lacks it, which is why contract read ENOENT).
- Run `audit:gate` (leg 6), `audit:locks` (leg 7) and `audit:contract` on:
  - (i) develop;
  - (ii) the override;
  - (iii) the override + #1354's js-yaml lock bytes, **with NO baseline row**.
- Each rc goes on its own line. Say whether leg 6's CLEANUP line now lists the 12 grandfathered undici rows (it should, under a working override: record it verbatim, and remove no row). `node_modules` only inside worktrees you created; removed at wrap with `df -m` before and after.
- **If (iii) passes all three:** STATUS `status override route1`, with the proposal of ONE PR: the js-yaml lock bytes + both manifests' `overrides.undici` + both regenerated locks, `Refs KS-1378`, no baseline row. **Then WAIT: Wednesday takes that to Kam's card as the new fact.** No image build or suites until Wednesday says so.

**Hard line 75%.**

PROVENANCE:
- your ctx | tmux capture-pane statusline ctx:39% | read 2026-09-30 10:14
- the measurements (issuer 723→721; root inert; leg 6 byte-identical; the 12 drift entries control-attributed; leg 7 load failure) | your STATUS 00:12Z, DKIM/SPF/DMARC pass | read 2026-09-30 10:14
- Kam's rulings today | kam_rulings_today.sh (live board): 0 messages | read 2026-09-30 10:03
