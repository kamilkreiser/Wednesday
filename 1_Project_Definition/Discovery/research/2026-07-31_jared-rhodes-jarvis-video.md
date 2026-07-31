# Research: Jared Rhodes' "Jarvis" system (the YouTube video Kam referenced)

Date: 2026-07-31 · Source video: https://youtu.be/RGiGdMYIznQ ("Meet Jarvis: The AI
Agent That Runs My 3 Businesses", Jared Rhodes / @jaredrhod, 2026-07-02, 37:44 live
stream). Kam's framing: *not* the structure to follow, but a basis for guiding
discovery.

## What the system is

Jarvis is **just a Claude Code session + an Obsidian vault** — no plugins, no vector
DB, no framework — plus a voice layer. Rhodes' line: "The vault IS the Jarvis…
strip away vault + tools and I'm just a guy with amnesia."

## Architecture

**Memory ("AI Memory Vault"):**
- Claude Code's fragmented auto-memory gets harvested into the vault and
  consolidated — one canonical note per topic (his real case: 107 notes → 17).
- Boot chain: `CLAUDE.md` (outside the vault; identity + hard rules + vault path)
  → read `VAULT-INDEX.md` (a *map*, never the whole vault) → fetch only the note
  needed. "Memory on demand": unlimited memory outside the context window.
- Daily notes = episodic long-term memory, timestamped; new sessions boot on
  yesterday's + today's notes ("somebody left you a really good journal").
- **"Checkpoint" command** (anti-drift): one word triggers daily-note update +
  re-verification that every vault note touched today is still source-of-truth.

**Recurring work ("Jobs" + "AI priming"):**
- One note per recurring task; before executing, the agent reads linked priming
  notes (skill + customer avatar + brand guide + knowledge base). Short prompts →
  consistent output. Sales page: 2 weeks → ~10 minutes.
- **The agent writes/maintains all vault notes itself.** Rhodes never edits
  Obsidian; he gives conversational feedback and the agent updates the Job note.
  ~10–15 iterations to perfection. Corrections go into the note, not the chat, so
  improvement compounds. ← *This is the mechanism closest to Kam's parent–child
  learning intent.*

**Multi-agent:**
- Second agent "Smith" (coding) in its own folder; both share the same vault +
  daily notes — the shared log is how they talk. Each agent's CLAUDE.md tells it
  the other exists and refers work across. No orchestration framework.

**Voice/face (repos):**
- Voice Line: push-to-talk, local whisper.cpp transcription → Claude Agent SDK →
  Fish Audio TTS reply. Family can literally phone Jarvis.
- Visualizer: fullscreen browser face with 5 states (idle/listening/thinking/
  speaking/alert).

**Cost:** runs on the $100/mo Claude subscription (Claude Code login, not API).

## Repos

- https://github.com/jaredrhod/ai-memory-vault — core; `ai-memory-vault.md` is an
  instruction manual *for Claude Code* (it interviews the user and builds the
  vault). Templates: CLAUDE.md (11 hard rules), VAULT-INDEX.md, daily template.
- https://github.com/jaredrhod/ai-marketing-skills — priming-note packs.
- https://github.com/jaredrhod/prompts — Voice Line, Visualizer.

## Verdict for Wednesday — borrow / skip

**Borrow:**
1. Index-first retrieval (`VAULT-INDEX.md` map, memory-on-demand) — adopt for
   `0_Brain/` as it grows; full-brain reads at boot are fine now but won't scale
   forever. Kam has accepted the token cost at startup, so: full `learnings/` read
   + index for everything else.
2. Checkpoint command — maps cleanly onto the existing end-of-session skill;
   consider a mid-session "checkpoint" too.
3. Corrections-into-notes feedback loop — the concrete implementation of the
   parent–child model.
4. Jobs + priming notes — for Wednesday's recurring duties (email triage, task
   review, project-status sweeps).
5. Shared-daily-note + mutual-CLAUDE.md-awareness as the cheap multi-agent
   coordination layer — matches the planned `projects_index/` design.
6. Voice Line pattern (push-to-talk whisper.cpp → agent → TTS) — reference
   architecture for upgrading beyond Whisperflow + `say`.

**Skip / differ:**
- Kam already has a mature multi-project vault with client isolation — Rhodes has
  one flat vault, no client boundaries. Wednesday's brain stays separate from the
  DevMASTER vault; isolation rules stay.
- Fish Audio / phone line: later, not now (macOS `say` first).
- His vault-building interview flow is superseded by our own discovery process.
