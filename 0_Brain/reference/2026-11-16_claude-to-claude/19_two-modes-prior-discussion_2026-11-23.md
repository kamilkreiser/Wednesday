---
date: 2026-11-23
type: reference
source: an in-session Opus reader commissioned by Friday (read-only search), its report condensed by Friday; the quotes are as the reader reported them from the files named, NOT re-opened by Friday line by line
status: live
---

# Where Kam's "two modes" were discussed before 2026-11-23 (General / Claude to Claude)

**Why this file exists:** on 2026-11-23 10:24 Kam wrote (card `general-c2c-windows-agent-permission-mode-1123`, C-1 in the project's CLARIFICATIONS): "Naturally, the final product will have the two modes we discussed - allow and monitor, approve and monitor". A card to him about those modes must rest on what was said, not on a guess.

## Finding
- The exact phrases "allow and monitor" and "approve and monitor" appear NOWHERE dated before 2026-11-23 10:24 (pattern `allow and monitor|approve and monitor|allow.{0,5}monitor|approve.{0,5}monitor|two modes`, case-insensitive, over reference files 00 to 18, the daily notes of November, the prompt log, decisions.json, and a recursive search of 0_Brain and 1_Project_Definition; positive controls: "two modes" found in `03_architecture-design.md:12,243`, "acceptable risk" in `daily_friday/2026-11-23.md:37`).
- His own earlier words on modes of this kind (4 passages before 23 Nov):
  1. 2026-11-16 15:02, terminal, `1_Project_Definition/Discovery/00_prompt-log.md:2831`: "Once connected, there should be 2 modes 1)controlled. Under this mode, the user should be able to monitor every file, folder or service that is being interacted with and approve it. … 2) option 2 is approvewd trust. Once trust is given, the user gets to follow what is going on but no longer has to approve things. The user should always be able to jump in and pause, ask questions or revoke approval." (R-CONTROLLED and R-TRUST, `00_requirements.md:8-9`.)
  2. 2026-11-18, note on card `general-c2c-policy-worktree-and-remote-agent-1118` (`daily_friday/2026-11-18.md:69`): "yes but there should be an option to bypass permission."
  3. 2026-11-18 about 09:59, terminal (`daily_friday/2026-11-18.md:97`; `11_both-agree-bypass-mode-design.md:11`): "what I meant by bypass permission.  the same setting as in claude.  if both users agree to let the agents work, monitoring but no approval for any aciton necessary"
  4. 2026-08-21 19:49, dashboard chat (`00_prompt-log.md:1175`): "A) everything is permission-based so nothing is done without express permission; and B) the administrator on the other side would be able to see everything that's done and, in most cases, approve calls, actions, or commands."

## What the documents define, and what is built (the reader's reading of the documents)
| Mode | Defined | Built |
|---|---|---|
| CONTROLLED (every new thing is asked) | `03_architecture-design.md:245, 276-288`; `04_design-revision-rulings.md:215-255` | The decision core in the policy crate (`docs/POLICY.md:40-115`). The daemon lacks session binding, held requests, learning the owner's answer, the audit log (`13_next-round-plan-2026-11-20.md:104`; `docs/DAEMON.md` "Not in the preview"). |
| APPROVED TRUST (a signed, scoped, time-limited grant; live stream; Pause, Stop, Revoke) | `03:289-339` | Grant checking in the policy crate only (`POLICY.md:103`). No console, no live stream. |
| "Both agree" (approvals off, people watch, every member consents) | `11_both-agree-bypass-mode-design.md:9-31`, monitoring `:197-213`; review `12_…` | Policy-crate rules only, SHIPPED DARK (`POLICY.md:64-92`). The review found 6 Blockers in the rest of the design; plan 13 `:110` says design 11 needs a revision and eleven answers from him first. |

Stale line found by the reader: `docs/POLICY.md:204-205` at main 3164374 still says his bypass note "has been asked and not answered"; he answered on 18 Nov.

## The reader's mapping (ITS reading, not Kam's words; Friday has not ruled it)
- "approve and monitor" = CONTROLLED (close match to his 16 Nov words).
- "allow and monitor" = either the both-agree mode (closest in words: "monitoring but no approval") or APPROVED TRUST (his original mode 2). The documents define THREE modes and none says whether both-agree replaces Approved Trust, sits beside it, or merges into it. **That is a question for Kam, not for a card's premise.**
- What "monitor" needs that no document defines: one monitoring design common to both modes (today: two separate streams in two designs); what monitoring means on native Windows (no sandbox; the gate there is unbuilt); monitoring of the development set-up he allowed today (all prompts skipped on the PC: nothing records or streams what that agent does).

## Conditions on building
- No sentence of Kam's says "design first, then my word": that condition is in Friday's and the design's words (`11:5`, `daily_friday/2026-11-18.md:99`). His card rulings D1, D2, D3 of 2026-11-20 07:11 on the both-agree mode: "Yes, they all still hold", "Only with the sandbox on", "Every member, observers included".

## Not opened by the reader
His November board messages at source (they reach this file only through the daily notes' verbatim quotes); chat_tuesday and chat_wednesday; design documents 01, 02, 05 to 10, 14 to 18 beyond a search; 11, 12, 13, 03, 04 beyond the mode sections; the source code beyond a search.
