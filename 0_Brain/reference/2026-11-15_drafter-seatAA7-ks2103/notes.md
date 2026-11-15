# Drafter notes, Seat AA 7th / KS-2103, 2026-11-15 22:5x

- develop pin read: 8095a4d20497b3b9af04a3ef5d1c38c2e6ff13df (22:53 AEDT). PR 2081 head 17c453253d68, open, mergeable.
- KS-2103: Backlog, High; one comment = card 1110 ruling (strict: only 404/null or object with block hash is an answer). Brief carries both 1107 and 1110.
- Code at develop: cardano/confirmation.ts waitForConfirmation :77-99 (call :79, polled :80, lastAnswered :83-84, `if (tx)` :86); cardano/provider.ts getTransaction :463-473.
- PR 2081 rewrites the same lines (:79-84) and getTransaction's first line/comments: overlap real; recommend WAIT for 2081.
- Callers of getTransaction: waitForConfirmation, index.ts(cardano):294 lookup, index.ts:2029 txInfo; both fail safe on a throw.
- Open anchoring PRs: 2081, 2194 (no provider/confirmation), 649, 575 (package.json bumps). 76 open, not 77.
- Scratch copies and lists in _work/. lin.py reads the Linear key in-process, prints nothing secret.
- Deviation: no scratch git clone (used gh api contents instead; nothing under !CODING was written).

UNMEASURED
- Whether any real Blockfrost reply shape is newly refused; the 2081 cells' clock-injection mechanism; docs-fragments.mjs path; current pre-push hook branches; when 2081 merges; PRs with file lists over the API cap; the box.
