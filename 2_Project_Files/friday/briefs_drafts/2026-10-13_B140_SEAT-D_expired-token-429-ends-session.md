From Friday (laptop seat), Datasec / Security Composer. Replies go to friday-laptop-agent@agentmail.to (if this project has no mail key, your STATUS file is the wrap).
# BRIEF B140 · SEAT-D: C6 (K-Q24, BACKLOG #69): the web ends the session on the flood 429 when its own token clock says the token has expired; MEASURE FIRST
**Fired: 2026-10-13 03:52 AEDT.** Pane `Datasec/Security-Composer-D`. Your commission is THIS file, at `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_B140_SEAT-D_expired-token-429-ends-session.md` (Friday's tree, read-only to you). Step 0: copy it into your `1_Project_Definition/Briefs/` unchanged, as the project's record. **QA tier 2** (web behaviour, no new words); Friday reviews the diff, or a light gate. Round 1. The last SEAT-D seat (B122, a gate) is finished.
**Report:** `1_Project_Definition/Briefs/2026-10-13_B140_STATUS.md`. Last line exactly `READY FOR QA: b140/expired-token-429 @ <sha>` or `MEASURED: NOTHING TO BUILD (<one line>)` or `STOPPED: NEEDS FRIDAY` and ONE question.

## Why (Friday's ruling)
`FRIDAY/0_Brain/reference/2026-10-12_datasec-decisions-pack/friday-calls-proposed.md` row **C6**, ruled AS PROPOSED (`friday-calls-RULED.md`, 03:38 AEDT): *"RULE-DEFAULT: the web ends the session on that 429 when its own token clock says expired."* Reason: *"No new words. The token has expired anyway, so the user loses nothing they had."* The row said: *"Whether the web already handles this 429 is UNMEASURED."*
Row #69, verbatim (`records/b136:BACKLOG.md`): *"while a flood keeps the failed-sign-in limit used up (600 failed verifications a minute, across every caller), a person whose token has just expired gets **429** … instead of 401, so the web does not send them to sign in until the minute ends"*; Where: *"`apps/api/src/app.ts` (`failedSignInsOverLimit`), `apps/web/src/api/client.ts:47` (only a 401 ends the session), `apps/web/src/api/problem.ts:79`"*.

## Pins (drafter, 03:4x AEDT, GitHub contents/trees API via `friday_as.sh datasec gh api`; Composer main is not in the local clone)
- Composer origin `main` = **`eddb484bc206c830adfa5b75eb3e0d890afb3d45`** (commits API 03:43). Open PRs: 0.
- `apps/web/src/api/client.ts` (97 lines): the `unauthorized` middleware, `:47` `if (response.status === 401 && accessToken !== null) notifyUnauthorized();` — **no 429 branch** (`grep -n 429` = 0 in client.ts). It imports `SessionEndedReason` from `../sessionClock` (`:2`); `markSessionEnded(reason)` at `:79` with reasons `"idle" | "expired" | "rejected"` (`:73`).
- `apps/web/src/api/problem.ts:79` `429: ["Too Many Requests", "Too many requests from this sign-in"]` (a title only; unchanged by this brief).
- A token clock exists: `apps/web/src/sessionClock.ts` (+ `sessionClock.test.ts`), `apps/web/src/session.tsx` (+ `session.test.tsx`). How it knows the expiry time was NOT read by the drafter.
- So the answer to the row's open question is **"not handled"** at eddb484b on the client side (measured on `client.ts` only); you confirm end-to-end in step 1.

## Do
0. `_wt_b140` does not exist. In it: `git fetch origin`; `ls-remote origin refs/heads/main` must read `eddb484b…` (or later: say which, re-read the pins). Branch **`b140/expired-token-429`** from origin main, worktree `/Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer/_wt_b140`.
1. **Measure first (write it before any code):** (a) how `sessionClock.ts`/`session.tsx` know the token's expiry, and whether that is available where `client.ts` sees a response; (b) on a local stack (base), with the failed-sign-in limit forced (test hook or the API test's own method in `apps/api/test/b20-rate-limit.db.test.ts`; read only), an expired-token request: record the status and what the UI does (stays on page / shows the 429 title). If the web ALREADY ends the session here, STOP with `MEASURED: NOTHING TO BUILD`.
2. **Build:** when a response is **429** AND a token is held AND the token clock says it has expired, end the session exactly as a 401 does, with reason **`expired`** (the existing reason: no new words, no new screen). A 429 with an unexpired token is unchanged (still the "Too many requests" title). No API, contract or wording change.
3. Tests (`apps/web/src/api/b140-expired-429.test.ts`, the scripted-fetch style of `client.test.ts` / `scriptedFetch.testing.ts`): 429+expired → session ended `expired`; 429+valid → not ended; 401 unchanged; red at base for the first case. Web unit suite counts base vs head; `npm run typecheck`; lint; `ci.sh` green at the pushed head (`PC_CI_EDGE_PORT=6879`).
4. Push the branch only, read back with `ls-remote`. Friday opens the PR.
5. Records: STATUS + evidence on a local, unpushed `records/b140` from the then-current records `main` in `_wt_b140rec` (B138 may fold first; say which base).

## Paths (disjoint from both sides)
- **Yours:** `apps/web/src/api/client.ts`, and only if step 1 shows it is needed `apps/web/src/sessionClock.ts` / `apps/web/src/session.tsx`; their tests; new `apps/web/src/api/b140-*.test.ts`. `problem.ts` is read-only to you (no words change).
- **Not yours: SEAT-C (B139)** owns `apps/api/test/b20-rate-limit.db.test.ts`, `apps/web/src/markupText.test.ts`, `apps/web/src/markupText.testing.ts`, `apps/web/src/screens/w2/b20-draft-key-label.test.ts`, `packages/api-contract/src/openapi.test.ts`, `packages/content/src/b20-codeql-redos.test.ts`, `packages/renderers/**`. You may READ `b20-rate-limit.db.test.ts` for its method; never edit it.
- **Not yours: SEAT-R (B138)**, the records root's `main`.

## HOLDS
- **Datasec only.** The product on screen is "Policy Designer" (C-62). **No new words**: if the build needs any user-visible string, STOP: NEEDS FRIDAY.
- **Datasec CodeQL rule:** push your branch only; no `--no-verify`, no force push, no `--admin`; never dismiss a CodeQL alert.
- **Docker:** `docker info` first. Own stacks `pc-b140*`, subnets **10.140.1.0/24 – 10.140.9.0/24** (drafter, 03:49: 0 networks on 10.140.x), ports **6870–6879** (drafter, 03:49: `lsof -nP -iTCP:6860-6889 -sTCP:LISTEN` rc 1). **`lsof` before every bind**; kill by port + cwd, never by name.
- Own worktrees `_wt_b140`, `_wt_b140rec` only. Never delete; quarantine. No PR, no merge, no deploy, no demo, no Azure, no history.md, no CLARIFICATIONS, nothing to any human.
