---
date: 2026-09-20
type: correction
source: Tuesday (Datasec seat) — found RD-516's design + cells unversioned while sizing the ticket
status: live
tier: W
---

# In this workspace's layout the git repo is ONE subdirectory of the project folder — so most of where an agent works is outside version control, and agents put deliverables there

**The lesson:** every project here is `<Project>/` with the git repo at
`<Project>/2_Project_Files/`. Everything beside it — `1_Project_Definition/`,
`5_Project_History/`, `session-tools/`, `qa-worktrees/`, and any scratch directory a session
invents — is a **sibling of the repo, not an untracked path inside it.** No `git add`, no
`git status`, no pre-commit hook and no push from inside the repo can ever reach them. A file
there is protected by the drive and nothing else.

**This is fine for scratch and dangerous for deliverables, and agents cannot tell the difference
from where they sit** — their working directory is the project folder, so `session-tools/x` and
`2_Project_Files/x` look equally like "in the project".

**The case.** Sizing RD-516 (a minimum-set security blocker, anonymous SSRF via ai-test) I found
zero commits and zero branches and nearly wrote "not started". The prior-work check found ~151 KB
that already existed:

- `5_Project_History/2026-09-18_S65_rd516-ssrf-design.md` — **99,937 bytes** of design
- `session-tools/s70/rd516-cells/` — a 33 KB cell file, an 8.7 KB harness preload and a 9.6 KB
  README, authored that morning, all NOT RUN and correctly labelled so

None of it tracked. `git grep -l -i rd516` over main's tracked tree returned only `HISTORY.md` and
a cross-reference inside another ticket's test file — with an `rd545` control firing correctly, so
the zero was real. 173 origin heads, none containing "516". The authoring seat had wrapped.

**Three days earlier the same shape had already cost us OT1–OT6**, "prepared" in a session
scratchpad and ruled *do not re-author*. That one was survivable only because the RD-549 gate
re-derives the work by its own requirement. **RD-516 has no gate and no branch — nothing
re-derives it.**

## Why the existing lesson did not cover it

[[2026-09-20_prepared-in-a-scratchpad-is-lost]] is about the **handover sentence** — calling
something "prepared" is a claim about a path, and the successor should check it. That fires when
someone *reports* the work. It does not fire on the work itself, and it points at the seat that
wrote the handover rather than at the layout that made the trap. **The structural fact is that
four of a project's directories are outside version control by design and agents write
deliverables into them anyway.** It will keep happening.

## The rule

1. **Before calling any ticket "not started", run the prior-work check across the PROJECT folder,
   not the repo.** `find <Project> -iname "*<TICKET>*"` and a grep of the sibling directories, not
   only `git log --grep`. A git-only search answers "is it committed", and the question is "does
   it exist" ([[2026-09-07_a-census-complete-over-a-frame-that-is-not]] — the instrument answered
   about the frame).
2. **Any deliverable found outside `2_Project_Files/` is rescued the same session** — committed to
   a branch by the project's own agent, keeping whatever NOT-RUN/ungated labelling it carries. A
   rescue branch is not a change to the suite: do not regenerate counts on it.
3. **A rescue is the project agent's action, never mine** — hard rule 1, and the git hooks enforce
   it. My job is to find it, measure it, and commission the commit.
4. **When commissioning anything that produces an artefact, name where it lands** — a repo path,
   not "prepare X". "Prepared" with no tracked path is the failure this file and
   [[2026-09-20_prepared-in-a-scratchpad-is-lost]] both describe, from opposite ends.
5. **Check with a control.** "Nothing tracks it" is an absence claim: run the same search for a
   ticket you know IS tracked, in the same command
   ([[2026-09-08_a-false-absence-is-usually-my-own-instrument]]).

## The part that generalises past this workspace

Whenever a tool's protection boundary is NARROWER than the directory people work in, the gap
fills up with real work — because nothing in the daily experience marks the edge. Ask of any
safety mechanism: *what is the widest thing a person can be doing while believing this protects
them?* Here, an agent can spend an hour authoring a security ticket's entire test suite inside
the project folder, with git working perfectly, and be protected by nothing.
