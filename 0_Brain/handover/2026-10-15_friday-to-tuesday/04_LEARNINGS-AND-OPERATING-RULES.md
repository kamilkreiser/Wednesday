---
date: 2026-10-15
type: handover
from: Friday → Tuesday
client: Datasec only (Friday's ledger was measured: 42 Datasec mentions, 0 of any other client: /usr/bin/grep -ci, same file)
status: live
---

# Friday's learnings and operating rules, for Tuesday

Kam asked that "all learnings about operation, and the project are shared with tuesday". Here is how they reach you, and the
distilled rules Friday learned running these three projects (2026-09-23 → 2026-10-15).

## 1. How the learnings reach you (mechanism, not copying)
All three seats share ONE brain repo (`kamilkreiser/Wednesday`). When Friday pushes, every file below is in your tree after `git pull`.
- **Lesson files** (`0_Brain/learnings/*.md`): already shared. Your boot digest (`_boot_digest_by_tier.md`) is generated from the
  same folder, so every W-tier lesson Friday wrote is in your boot from your next launch. The Friday-written ones that matter most
  for these projects:
  - `2026-09-23_build-seats-run-in-cockpit-panes.md`: build seats are visible cockpit panes, never hidden subagents
  - `2026-09-23_fix-it-yourself-talk-to-sister-seats-directly.md`
  - `2026-09-24_decisions-go-on-the-fleet-activity-panel.md`: **anything needing Kam goes on a fleet-activity card**
    (re-ruled 10-08 09:20:26: *"anything that you need from me always goes on the fleet activity cards"*)
  - `2026-09-27_hpsmpoc-every-hp-ask-is-its-own-email-plus-a-register.md`: P-tier, Datasec/HPSM-POC
  - `2026-09-29_datasec-github-commits-go-through-codeql.md`: every datasecau change goes through CodeQL; never bypass,
    never ask for an exception
  - `2026-10-03_hp-security-manager-azure-deploy-grant.md`
  - `2026-10-06_push-to-demo-when-ready-no-card.md`: the grant itself is Friday's; re-confirm with Kam (see 00)
  - `2026-10-08_sonnet-trials-and-a-shared-model-routing-definition.md`
  - `2026-10-10_merge-and-archive-when-done-and-ready.md`
  - `2026-10-12_be-more-careful-with-coding-files-and-deploys.md`
- **Friday's correction ledger** `0_Brain/learnings/_ledger_friday.md`: 127 rows, every one tagged `[W]` or
  `[P-Datasec/<project>]`. **Read the `[P-Datasec/HPSM-POC]`, `[P-Datasec/MPS-Calculator]` and `[P-Datasec/Security-Composer]` rows
  whole** (they are project knowledge), and the `[W]` rows as headlines. It contains no other client's material, so reading it
  whole is safe under hard rule 2.
- **Friday's daily notes** `0_Brain/daily_friday/2026-09-23 … 2026-10-14.md`: the episodic record (every launch, gate, merge
  and deploy with its SHA). Read on demand; 10-13 and 10-14 hold the latest project detail.
- **Friday's pickup** `0_Brain/tasks/NEXT-PICKUP-FRIDAY.md`: 470 KB of rotation blocks. **Don't read it whole.** The handover
  files distil its newest blocks (10-13 → 10-14 07:2x) plus everything measured live today.
- **Friday's briefs** `2_Project_Files/friday/briefs_drafts/`: every brief as launched, B-numbered per project. These are the best
  templates for your next briefs (newest: HPSM-POC B248, MPS B97, Composer B152/B153).

## 2. Friday's tooling (in `2_Project_Files/friday/`, shared repo)
| Tool | What it does | Before you use it |
|---|---|---|
| `brief_seat.sh` | Runs a Claude build seat inside a cockpit pane in a project folder, with the brief as its commission | Read its header; it resolves Friday's paths. Run it from YOUR tree's copy. |
| `merge_when_green.sh <owner/repo> <PR> <head-sha>` | The one way to merge a Datasec PR: waits for every check, refuses if the head moves, merges, prints the merged SHA | It runs `gh` under the Datasec identity via `friday_as.sh datasec`. **Point it at your own Datasec gh config** (Tuesday's identity), never Friday's. |
| `watch_status.sh <seen-file> <glob>…` | Wakes the coordinator when a seat's STATUS file gets a final-line token (READY FOR GATE/REVIEW/QA, DONE, STOPPED) | It matches `NEEDS FRIDAY`. Brief your seats to write `STOPPED: NEEDS TUESDAY` and add that pattern. |
| `seat_idle.sh <pane>` | Has a seat's turn finished? Ask it before telling a seat something is missing | — |
| `seat_rung5.sh` | Did a launched seat actually RECEIVE its commission? (reads its transcript) | — |
| `name_addendum.sh` | Names an ADDENDUM file so the tap gate accepts its tap | — |
| `friday_as.sh <client> <cmd>` | Runs one command under one client's identity | Friday-only; you are single-client. Use your own Datasec config. |

## 3. Operating rules Friday learned (each one paid for at least once)
**Delegation flow**
1. Tier 1 = build seat → **independent** QA gate seat (fresh; never the builder) → coordinator completion check → PR → merge.
   Tier 2 (tiny, e.g. a package pin or 3 word fixes) = build seat → coordinator reviews the diff AT SOURCE (GitHub compare API) and
   re-runs the red-proof → PR → merge. A gate round is capped at 2 fix rounds; a NO GO on round 2 means the item doesn't ship this
   round. Ticket it.
2. **Read every brief WHOLE before launch**, even one your own drafter wrote. Drafters relay false absences and stale SHAs
   (10-13 row: a drafter's false absence went into B243 and the gate refuted it).
3. **Re-pin heads by `git ls-remote` at every launch, before every PR, and after every READY.** Never trust a SHA from a note.
4. **Never type an ID from memory**: PR numbers, run IDs, SHAs, ticket keys. Parse them from the tool's own output (w=3, 10-13).
5. **Check the brief's final-line token against your watcher regex BEFORE launch** (w=3, 10-13). Gate STATUS files often live in
   the seat's records worktree (`_wt_b<nn>rec/…`, `.tools/wt-*/…`), so glob both places. Keep a pane-idle fallback armed.
   **Re-arm the watcher after every wake** (10-06: a non-re-armed watcher left five finished seats idle for ~35 min).
6. After every merge: the commits API must show parent = old main and tree = the gated tree. Then read main ci TO THE END. A red main
   is fixed in code, never dismissed (B248, 10-14: an advisory published overnight turned main red).
7. CodeQL sometimes doesn't start on a reopened PR. The fix: an empty commit with the identical tree, pushed via the API,
   fast-forward only.
8. Before closing a seat's pane: confirm IDLE (`seat_idle.sh`) and take a listener snapshot (open ports before/after). A dead
   process holding a port once survived a count-only check.
9. Check load before launching (`sysctl -n vm.loadavg` as its OWN command; hold a launch while load1 > ~30 on 12 cores). Each
   seat gets its own 10-port block.

**Kam-facing**
10. Anything you need from Kam goes on a **fleet-activity card**, action-first, with the link. Never only in chat. One question per
    card. **Measure every premise in a card before posting it** (w=3, 10-12: cards about deploy targets must state what they
    will show, measured). Never pre-fill `_override_prior`; post, read the refusal, then override with the reason (w=3, 10-11).
11. Run `kam_rulings_today.sh` before any card, brief or ruling. Kam's rulings on these projects were given on the FRIDAY tab, so read
    that view too until he re-homes them.
12. Every word a customer will see is Kam's. Gather new words into a pack, put them on a card, and have a gate sweep for NEW
    WORDS. (10-06, Kam on Composer: *"Some work from the Security Composer has been disappointing and I want to make sure this is
    done properly."*)
13. Nothing goes to Paul, HP or any human without Kam's explicit send. When he says send, send from your own inbox, CC him,
    and read it back from the sent folder.
14. Praise on record: 10-13 18:45 *"So far, the feedback from HP has been outstanding - thank you for coordinating and getting this
    project…"*; 10-08 *"the HPSM POC is looking fantastic!"* The method above is what earned it, so keep it.

**Repo hygiene**
15. **Code repo ≠ records repo.** HPSM-POC records push to `HPSM-POC-analysis`; MPS and Composer records repos are **local only,
    with no remote**. Never tell a records seat to push those (10-11 MPS B30, 10-13 Composer B151).
16. Seats work only in their own worktree. The root checkout gets read-only verbs (B152 broke this, 10-14). In another project's
    repo, even `git status` writes the index; use `git --no-optional-locks` (10-05).
17. Commit your own data files before any `git pull --rebase` on the brain repo (10-04). If an autostash conflicts on the two
    generated digests, regenerate both (`boot_digest.py --by-tier` and bare), `--check`, and keep the stash (10-10, again 10-15).
18. Never rewrite a script in place while a run of it is live (10-04, merge_when_green).
19. The Bash tool is **zsh**: no bare `echo ===` separators (zsh `=word` expansion), and no unquoted `$VAR` expected to word-split.
    The fleet hooks refuse both now (w=3/w=4, 10-06 → 10-13).
