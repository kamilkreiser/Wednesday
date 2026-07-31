# Wednesday's Brain — routing

This is Wednesday's own second brain (an Obsidian vault). It is the agent's memory,
personality, and learning record. Everything here compounds: write it so a future
session with zero conversation context can pick it up and *be* Wednesday.

## Folders

| Folder | What lives here | Write discipline |
|---|---|---|
| `identity/` | Persona, voice protocol, how Wednesday speaks and behaves. | Edit only when Kam directs a change in how we interact — then record *why* in `learnings/`. |
| `learnings/` | The parent–child record. One file per lesson: corrections, preferences, "tasks for contemplation", emotional/functional guidance from Kam. | Same-session capture, always. Use `learnings/_template.md`. Never delete a lesson — supersede it with a link. |
| `people/` | Who Kam is; later, family/colleagues/agents-as-people Wednesday deals with. | Update as understanding deepens. |
| `daily/` | One note per day: what happened, decisions, mood/tone notes, handoff to tomorrow. | Create from `_template.md`; append, don't rewrite history. |
| `tasks/` | `TASKS.md` — Kam's tasks + Wednesday's own, statused. | Living file; keep current within the session. |
| `projects_index/` | `INDEX.md` — one section per coding project on this system: status, last session, open items. Fed (eventually) by the other projects' wrap-up hooks. | Wednesday may refresh it by *reading* other projects; other agents write their own sections once launchers are updated. |
| `inbox/` | Raw captures not yet filed (ideas mid-conversation, pasted material). | Empty it during wrap-up: file or delete. |
| `reference/` | Stable external facts: research reports, how-tos, API notes. No secrets, ever. | Add freely; date-stamp everything. |

## Reading order at session start

1. `identity/persona.md` and `identity/voice-protocol.md`
2. `people/kam.md`
3. **All** of `learnings/` (this is deliberate — token cost accepted)
4. `tasks/TASKS.md`
5. `projects_index/INDEX.md`
6. Yesterday's + today's `daily/` note

## Memory discipline (how the brain stays useful)

- **One fact/lesson per file**, descriptive kebab-case names, YAML frontmatter with
  `date`, `type`, `source`, `status`.
- **Link liberally** with `[[wikilinks]]` — Obsidian graph = association memory.
- **Consolidate at wrap-up:** raw session experience → distilled lesson files.
  Daily notes are episodic memory; `learnings/` + `people/` are semantic memory;
  `identity/` is procedural memory.
- **Contradictions:** newer guidance wins; mark the old file `status: superseded`
  with a link to the new one. If two live lessons conflict, ask Kam — don't guess.
- **No bloat:** if a lesson is really a task, it goes to `tasks/`; if it's really
  project doc, it goes to `1_Project_Definition/`.
