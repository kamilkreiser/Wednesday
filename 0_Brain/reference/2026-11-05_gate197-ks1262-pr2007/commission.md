# Gate 197 commission — Secuura / Blockchain, PR 2007 (KS-1262 N3 + N4: per-user notification settings get their own key space), TIER 1, ROUND 1 of 2

Written by Wednesday 2026-11-05 17:2x AEDT. Model: Opus (routing v1.0 row G1: security surface). You are a QA GATE: findings only, you fix nothing, you write nothing outside this folder, you contact no box, you post nothing to Linear or GitHub.
**A rotation KILLS you** (you run as a subagent of Wednesday's seat): write `verdict.md` in this folder EARLY as a stub (line 1 `NO GO (INCOMPLETE: killed before the verdict)`), then overwrite it at the end. Line 1 of the final verdict is exactly one of `GO`, `GO WITH NOTES`, `NO GO (<one-line reason>)`.

Read first, whole: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md (the gate method: clone by SHA into THIS folder, never write in the shared checkout /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files; read-only git verbs only there) and the seat's READY in `ready_2007.txt` here.

## Subject (read by Wednesday with git ls-remote at 17:2x AEDT)
- refs/pull/2007/head = `052695ec28d9dd0bbb59ce475335eeb754a06b51`; develop = base = `5fc5569ed96ac61f64823cc9e1fa841899aa1f62`. Seat T 11th (Opus). 9 files per the READY.
- KS-1262's own text: "Security: PUT /api/settings/notifications writes the same key namespace as platform-settings — a non-admin whose userId is 'platform-settings' replaces the platform-wide settings". PR 1635 (merged) refused that id at the PUT. This PR closes N3 (the per-user GET still returns the whole platform record to a principal with that id) and N4 (a principal with id `default` plants what every anonymous reader gets) by moving per-user settings to their own Redis namespace `secuura:gateway:notif-user:<userId>`.
- Wednesday ruled shape 1 (separate key space) over shape 2 (refuse reserved ids), and allowed two foreign TEST edits (ks719 stand-in + one expected write; ks570 one rationale string).

## Questions (measure; the READY's figures are claims to re-measure)
1. **Scope.** `git diff --name-only base...head` equals the READY's 9 paths. The product change is only `services/api-gateway/src/services/redis.ts` and `routes/admin.ts`. In ks719 and ks570, show that exactly the declared lines changed (hunk count, and a byte-equal check of every other cell with a control that reads unequal on an edited one).
2. **The security property, base vs head, real router, only Redis faked (a recording fake that logs every verb and key):** for principals {anonymous, `default`, `platform-settings`, `notif:platform-settings`, `user:platform-settings`, a normal user, an admin} x {GET, PUT}: which keys are read and written, and what body is returned. Predicates: (a) at head no per-user request reads or writes any key under `notif:` or the platform record; (b) the platform record is byte-equal after every per-user write; (c) anonymous GET reads NO key and returns the documented defaults; (d) **head is never MORE permissive than base for any non-admin principal** (no read of another principal's or the platform's data that base refused). Report "N of M" per predicate and every changed cell.
3. **Key-space separation is real, not cosmetic.** Prove no input userId can make `notif-user:<id>` equal any key the platform or any other reader uses (path-like ids, colons, empty string, unicode look-alikes, very long). Name the escaping or the reason none is needed.
4. **The in-memory fallback** keeps the two spaces apart under the same matrix (the seat says a separate Map): show it.
5. **Availability cost, as the PR states it:** existing per-user values stop being read, users see defaults until they save, old values expire within 24 h (TTL.privacy 86400, redis.ts:27). Verify the TTL line and that nothing deletes or migrates. Is there ANY reader of per-user notification settings other than this route (other services, frontends, workers)? `git grep` with a positive control. A reader that still reads `notif:<userId>` after the change is a Major.
6. **Mutants.** Reproduce at least 4 of the seat's 8, plus two of your own: (i) the GET falls back to the old namespace when the new key is absent; (ii) the anonymous branch reads `notif-user:default`. Anchor count 1, mutant parses, restore sha-equal; count the raw table yourself.
7. **Suites and static at head vs base:** the whole api-gateway suite (vitest JSON totals), tsc, check:test-types, eslint on touched files, each with a planted-defect control. Note Node version.
8. **Merge tree** in your clone: `git merge-tree --write-tree base head`, rc and tree id; expect rc 0, equal to the head tree.
9. **PR body:** read whole. It must state: the shape and who ruled it (Wednesday 2026-11-05, shape 1); the user-visible effect sentence; the two foreign test edits; Node v26 not 24; a NOT-tested list (no real Redis, no box, no live notif:* census). Flag any sentence your measurement contradicts.

## Not in scope
KS-1534, KS-1505, KS-1493 (later PRs of the same seat); the admin export route; any box.

## Output
`verdict.md` (verdict line, then BLUF, then findings F1..Fn each with severity Major/Minor/Info, file:line, evidence path, and what would fix it), plus your evidence files in this folder. Report back in your final message: the verdict line and the findings one line each.
