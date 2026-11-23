---
date: 2026-11-23
type: screen-capture
source: the build seat's own capture from the real programs (its STATUS section A1.4), copied by program; the workspace path shown as <ws>
status: for the owner's eye; the lane is checked twice and not yet merged
project: General/Claude to Claude (CoAgent), no client
---

# The local activity view: what the owner's second window shows

This is the viewer after the fix round, at branch commit `039b987`. Five decisions of the gate. Line 1 is the notice (its wording is yours to change). Rows that start with four spaces and a bar continue the entry above them. Entry 5 is a forgery ATTEMPT: a proposed command padded so that, before the fix, your terminal's line wrap showed a fake "refused" entry and a fake notice. It now shows as marked continuation rows inside its own entry.

```
Only you see this. Nothing here is sent to the other side.
CoAgent mode: APPROVE. One entry per call the gate decided. Times: UTC.
A row starting with four spaces and "| " continues the entry above.
#1 07:03:00 UTC | CoAgent asked | tool Write | Claude Code mode: auto | 
    | coagent asks: Write (Edit, T1); targets: Write: <ws>/hello.txt
#2 07:03:00 UTC | CoAgent asked | tool Bash | Claude Code mode: auto | c
    | oagent asks: Bash (Execute, T3); why: the gate does not understand
    |  shell commands and cannot tell what this one will touch; command:
    |  cargo test --locked; targets: Cwd: <ws>
#3 07:03:00 UTC | CoAgent refused | tool Read | Claude Code mode: defaul
    | t | coagent: a target is on the owner's exclusion list
#4 07:03:00 UTC | CoAgent blocked | a settings change (ConfigChange) | C
    | laude Code mode: not reported | coagent: settings changes are bloc
    | ked while the CoAgent gate is on
#5 07:03:00 UTC | CoAgent asked | tool Bash | Claude Code mode: default 
    | | coagent asks: Bash (Execute, T3); why: the gate does not underst
    | and shell commands and cannot tell what this one will touch; names
    |  a shell or interpreter that can run code given to it as text or o
    | n a pipe; command: echo build ok.......................#3 00:00:01
    |  UTC | CoAgent refused | tool Bash | Claude Code mode: default | c
    | oagOnly you see this. Nothing here is sent to the other side......
    | .................x; targets: Cwd: <ws>
```

What to look at:
1. The notice on line 1: keep these words, or give yours.
2. Readability: the viewer cuts lines at 72 columns, also inside a word ("c" / "oagent"). It can be changed to cut at spaces where it can; say if you want that.
3. Times are UTC in this first slice.
