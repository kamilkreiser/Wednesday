STARTABLE: YES

# B903 drafter report (Thu 29 Oct 2026, drafted 18:2x to 18:5x AEDT, Sonnet 5.5, read-only)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-29_B903_SEAT-H55_hpsmpoc-240-round2-sideways-scroll-and-focus-ring.md` (89 lines, long ones; the ~150-line budget held).

## BLUF
Startable once stamped. Two findings, one lane, same branch, forward commits. B900-2 is deterministic and fully specified (scoped nav-link rule, red-first row, control rows, plants). B900-1 is a diagnose-then-fix loop because the overflowing element is genuinely unknown: the kit makes the builder measure it on the CI runner first, caps it at three pushes, and STOPs if the cause is a page-body file.

## Facts re-measured (instrument; control)
- Branch head `66a760a05abee8365f6ce0896be1703096b2b0c6` (`gh api git/ref`); main `885692995df9f650b80dd4827fa0827349a7f619`; open PRs: #240 and #241 (head `59625e5f`). Control: the two refs differ.
- `required_status_checks.strict` = false (gh GET): no merge of main needed. Required contexts read: 5 names (quoted in the kit).
- Ports 9940-9949: `lsof` rc 1 (nothing). Positive control: a python listener on 9941 counted 1. Kit scan, 10-28/10-29 non-`.pre-` SEAT kits, word-boundary: 0 hits; control (971x) found the B885 kit. Panes: tuesday, NexusAI-M56, HPSM-POC-G204, G203, NexusAI-G198, fleet-monitor. No live seat claims the block, no H55 pane.
- Routing: C2 line 92 (S55 1st), G1 line 108; sonnet id `claude-sonnet-5-5` at models_latest.json line 23.
- Source at 66a760a0 (raw `gh api`): `globals.css:65-69` unlayered `:focus-visible`; `GlobalNav.tsx:107` carries the utilities; `tokens.css:58` `--ds-nav-focus: #ffffff`; `shell-sidebar.spec.ts:186` is the row; `axe.ts:49-67` `noSideScroll`; `AppShell.tsx:162-165` flex row and content column; `CustomerManagement.tsx:161` page `main`, `:248` the `data-scroll-x` table wrapper; `WorkspaceScreen.tsx:3` re-exports CustomerManagement.
- CI: `web e2e` job runs `node scripts/e2e.mjs --shard` on ubuntu-latest (`ci.yml:484,515`), retries 1 in CI (`playwright.config.ts:50`); `web (Next.js)` aggregate at `ci.yml:527`. The failing message from the evidence file: `customers 1024: 1083px > 1024px ` with an EMPTY culprit list.

## Findings that shaped the kit (new beyond the gate text)
1. The empty culprit list is itself the clue: `noSideScroll` excludes anything with `closest("[data-scroll-x]")`, and `closest` includes the element itself. So a widened scroller, or its content, is invisible to the helper. The kit's diagnostic therefore must not use that filter (and goes in the spec file, not in `axe.ts`, which other specs share). This is a hypothesis, marked UNMEASURED.
2. The Customers page body (`CustomerManagement.tsx`) is a page-body file. If the culprit is there, the builder must STOP; the kit also forbids the masking fixes (`overflow` hidden/clip on html/body/row/column, moving the `lg` breakpoint) because they would make the row green while hiding content.
3. The drawer foot (Sign out, Reset demo) sits on a LIGHT `bg-surface` panel inside the same `aside`. A white ring scoped to the whole aside would vanish there. The kit scopes the fix to the nav links and adds a control row for the foot, plus a control row for a page link.
4. Moving the global `:focus-visible` into a layer would change every page's ring: forbidden; scoped unlayered rule after it instead.
5. CI cannot be reproduced on this Mac, so CI is the verifier (Tuesday's ruling on Q-B900-2 is written in as acceptance). A fourth push for B900-1 is a STOP.

## D-decisions (drafter)
- D-1 One seat, Sonnet (row C2); tier-1 round 2 of 2 follows.
- D-2 The diagnostic is its own commit, removed in the fix (default) so lines 186-194 equal 66a760a0 byte for byte.
- D-3 Fix B900-2 first (deterministic), then diagnose B900-1 while nothing else blocks; the two may share a push if the builder judges it safe, but the diagnostic push must be read from CI before the fix.
- D-4 No `axe.ts` edit and no new Playwright project.

## Q-questions for Tuesday (each with a default)
- Q-1 Gate round: kit says "tier 1 round 2 of 2 on the class 'the shell decides which pages each role reaches'". Default: as written. Confirm at stamp.
- Q-2 Keep the diagnostic in the spec after the fix? Default: NO, remove (row stays as at 66a760a0).
- Q-3 Menu toggle ring over the open drawer at 390: include (data attribute from `drawerShown` plus one scoped rule, one row, one control)? Default: YES, because this is the last gate round and the gate named it. The toggle sits on a light button over navy; its painted contrast there is UNMEASURED.
- Q-4 If the culprit is a page-body element (the likely STOP): who owns the fix? Default: Tuesday commissions the Customers page lane or approves a one-line page change in this lane; the shell does not mask it.
- Q-5 Windows: drafter suggests target READY 150 min and hard stop 240 min after Step 0 (two or three CI cycles). Tuesday sets the real times.
- Q-6 KEYS: no ticket key is needed by the builder; Tuesday fills the PR text (the gate's B900-3).

## Slot count with control
Four-underscore pattern on the kit: 9 lines (8 slots + the last line). Control: a scratch file with one such line reads 1. At-sign token count `@[A-Z_]+@`: 0; control (a scratch `@FOO@` line) reads 1. Non-ASCII bytes in the kit: 0 (python byte scan). "decision-card" appears 4 times only as the rule text "no decision-card id", no actual id; no person's name.

## UNMEASURED
The overflowing element on the runner; the toggle's painted contrast over the drawer; whether hover plus keyboard Tab keeps the hover state in Chromium for the hover-link row (builder proves in step 3a); the CI duration of the shard on the new head; the three-hop `actions/jobs/<id>/logs` GET (assumed to work with `gh api`, not exercised here).

## Outside-the-fences disclosure
Read: DRAFTER_RULES, B900 STATUS (whole), B900 evidence `c9-ci-e2e-failure.txt`, the B885 kit (whole) and a listing of the B885 STATUS size, model-routing rows, models_latest.json lines. Raw GETs at 66a760a0 of the files named above, plus `git/trees` (recursive) for a file listing and one `search/code` query for `data-scroll-x` (a GET against the repo). Wrote scratch copies under the session scratchpad `.../scratchpad/b903/` (outside the two deliverables, not in any repo). No clone, no npm, no run, no Jira, no decision-queue, no hosted host contacted, `lsof` and `tmux list-panes` read only. Two Bash calls were refused by hooks (a `cd`, and an unquoted `======`) and re-issued correctly.
