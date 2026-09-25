#1219 KS-1277: correct two stale on-behalf-of comments in the originate documents route
head 5d5129a03af0bf1586c26403a453ce283ae0be2f

## BLUF

Two comments in `services/originate/src/routes/documents.ts` describe an on-behalf-of shape that **#1060 deleted**. Comment-only, one file, `+11/-7`. No behaviour change.

## What was wrong, and what it says now

**Site 1 — the PLACEMENT block inside `/revoke` (at `:2335` and `:2341` on this base).**

* It named **`handleOnBehalfOf`** as the writer of the `action_provenance` row. #1060 (KS-1264) deleted that function and split it: `checkOnBehalfOf` validates and writes nothing, `recordOnBehalfOf` writes.
* It ended *"Writing it here means a row exists only for a call that was going to succeed"* — a sentence sitting above the **check**, while the row is now recorded after `updateDocument`.
* Both are replaced with what the code does: the check is placed after the refusals for the PII reason the block already gives, and KS-1264 moved the **write** below `updateDocument`, so a row exists only for a revoke that actually happened.

**Site 2 — the KS-480 §6 docblock (`:60-67`).**

* It said the hook *"appends the provenance row fire-and-forget"* — untrue since KS-1228.
* It listed `lifecycle-events` as a caller and omitted `/revoke`. **Measured at this base:** `checkOnBehalfOf` has exactly four call sites — `/transfer-custody` `:1612`, `/version` `:1971`, `/share` `:2160`, `/revoke` `:2344`. `/lifecycle-events` is not one of them.

## Two things deliberately left alone

* **`:124`** — *"`handleOnBehalfOf` **was** the ONLY writer … and **fired** ONLY when"*. Past tense, an accurate record of a 2026-08-22 measurement, and excluded by the ticket.
* The ticket's exclusion list also names **`:2341`**, but those numbers are from its filing revision `3c447abc7`. At this base `:2341` is the second of the two sentences the ticket's own bullet 1 asks to fix, so it **is** in scope. Position is part of the claim and the lines moved.

## Test Evidence

* **Touched:** `services/originate/src/routes/documents.ts` — comment lines only.
* **Ran:** originate `jest --runInBand` → **74 suites / 863 tests, rc 0**, identical to the bare serial baseline taken in a clean worktree at this base (**74 / 863**). `tsc --noEmit` rc 0. `packages/shared` `vitest run` → **46 files / 918 tests, rc 0** (those guards read service sources by text, so they run on every head).
* **NOT run:** nothing behavioural — this change alters no executable byte. The integration config (`jest.integration.config.js`) was not run; it needs a live Postgres and nothing here reaches it. No image rebuilt.
* **Migrations + config:** none.

Refs KS-1277

🤖 Generated with [Claude Code](https://claude.com/claude-code)

