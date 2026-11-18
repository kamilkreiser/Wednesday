---
date: 2026-11-18
type: index-spec
source: Kam, Friday's terminal 2026-11-18, "please implement the 5 recommendations" (the lesson digest is too large to read at boot)
status: live
---

# Rules index — one row per lesson file; the short boot card is GENERATED from it

**Nothing here replaces a lesson.** The lesson files stay the source of truth and are never cut. This index is a sidecar:
`_rules_index.tsv` holds one row per `learnings/20*.md` file, and `2_Project_Files/tools/rules_card.py` generates from it
(a) a short per-seat card read WHOLE at boot, (b) the rules for one moment of action (`--at <trigger>`).
`rules_card.py --check` FAILS when a lesson file has no row or a row names a missing file, so a new lesson needs a row the same session.

## Columns (TAB separated, one line per lesson, no tabs or newlines inside a field)

1. `file` — the lesson's file name exactly (e.g. `2026-08-07_a-check-that-cannot-fail.md`).
2. `status` — `live` · `dead` (its subject no longer exists: a returned machine, an ended one-off grant, a retired mechanism) · `superseded` (the file's own frontmatter or body says a newer lesson replaced it; put the newer file name at the start of the rule field as `-> <file>:`). Partly superseded = `live`, and the rule states only the half that still holds.
3. `seats` — `all`, or a comma list of `wednesday`, `tuesday`, `friday`. Wednesday = the Studio seat (Secuura + general, owns the local models Ornith, night runs). Tuesday = the Mac mini seat (Datasec). Friday = the laptop seat (both clients, no local models). Default `all`; narrow ONLY when the lesson is about a thing one seat alone owns.
4. `family` — one slug from the seed list below; if none fits, `other:<short-slug>`.
5. `triggers` — comma list from the fixed vocabulary below: the moments at which this rule must be in front of the seat. `always` only for a rule about general conduct with no specific moment.
6. `enforced_by` — `-`, or the repo-relative path of the hook/tool/gate that ENFORCES the rule (refuses or does it mechanically). Only when you have opened that file and found the enforcing lines. A tool that merely helps is `-`. Never from the lesson's claim alone: the lesson is a representation, the script is the source.
7. `rule` — ONE line, at most 260 characters, plain words, written from the OPERATIVE CASE: "When <what I am about to do>: <what to do / never do>." It must be actionable without opening the file, must carry any load-bearing exception or scope word, and must not be the incident story. For a grant: who may do what, until when, and what stays Kam's. No client project names, ticket ids or people other than Kam unless the rule is unusable without them.

## Trigger vocabulary
`boot` `brief` (writing or sending a brief, addendum or instruction to an agent) `launch` (starting or relaunching an agent or seat) `pane` (reading or typing into an agent's pane or prompt) `review` (judging delegated work, scoring, gates) `merge` `deploy` `card` (a decision card for Kam) `kam-message` (any message, ask or steps for Kam) `mail` (agent mail, inboxes) `report` (stating a count, state, cause or time to anyone) `verify` (checking that something worked) `tooling` (writing or changing a script, hook, watcher) `git` `rotate` (context, handover, rotation) `wrap` (session end, notes, ledger) `lesson` (writing or filing a lesson, ledger row) `identity` (credentials, accounts, tenants, client separation) `drive` (sync, paths, portability, delete or clean up) `usage` (model choice, usage gauge) `wait` (waiting on an agent, a wake or Kam) `always`

## Seed families
`sources-not-representations` · `checks-that-can-fail` · `enforcement-in-the-path` · `brief-provenance-and-pointers` · `headline-and-bluf-writing` · `authority-and-classification` · `counts-caps-and-selectors` · `ghost-text-and-pane-prompts` · `kam-communication` · `autonomy-grants-and-signature-classes` · `client-isolation` · `identity-and-credentials` · `coordinator-role-and-delegation` · `qa-gate-and-merge` · `context-and-rotation` · `rituals-wrap-and-notes` · `never-delete-quarantine` · `drive-sync-and-portability` · `launch-evidence` · `waiting-and-wakes` · `learning-loop` · `model-routing-and-usage` · `dashboard-and-cards` · `relayed-rulings-and-retractions` · `shell-and-script-hygiene` · `relationship-and-contemplation` · `time-scoped-grants` · `local-models`

## More than one rule per lesson (`#n` rows)

A lesson that holds two or three separate rules for different moments may have more than one row. The first rule is the plain row (`file` = `2026-08-15_a-cap-is-never-neutral.md`) and must exist. Each further rule is its own full 7-column row whose `file` field is `<lesson file>.md#<n>` with n = 2, 3, 4 ... (e.g. `2026-08-15_a-cap-is-never-neutral.md#2`), carrying its own triggers and rule (and its own seats / family / status when they differ).
- `--check` faults: a `#n` row with no plain row for the same lesson; a `#n` row whose lesson file does not exist; n that is not an integer >= 2; the same full key twice (`x.md#2` twice). `x.md` plus `x.md#2` is not a duplicate. "Lesson file with no index row" is judged on base file names.
- Weight: a `#n` row shows the SAME reinforcement weight as its lesson (the ledgers cite the lesson, not the rule line). `--weights` and its summary count lessons, not rows. A `-> target:` target is always a base file name; only a lesson's plain row passes its weight on, and a `#n` row may itself be `dead` or `superseded`.
- Card: a `#n` row appears like any row, in its own family, as `- [×N] <rule> — \`<file>\` (rule 2)`. "Most reinforced" lists at most one line per lesson (the plain row). The counts line reads `Counts: <lessons> lessons, <rows> rule lines, ...`.
- `--at <trigger>`: a `#n` row is matched by its own triggers and printed with `(file, rule n)`. `--stats` adds a lessons vs rule-lines line.
