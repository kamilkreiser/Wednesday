hits: 1
SUBJECT: [Secuura/Blockchain -> Wednesday] QUESTION: secuura-test-discipline 5f Done rule vs the brief's on-merge Done
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TS: 2026-09-16T17:47:55.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}
----
Seat A

## Context
The worktree carries a project skill, .claude/skills/secuura-test-discipline/SKILL.md, which loaded when I entered the KS-871 files. Two of its rules bear on this seat's flow. Its own section 1 says: where sources disagree, say so rather than pick one.
- Section 5f: "A runtime-behaviour change is not done — and the ticket does not move to Done — on offline quality-gate green alone. It needs a live sweep on the correct host, against a fully torn-down and rebuilt environment, with all containers verified up."
- Seat A's brief, "Ticket state on merge": Done if the PR delivers the ticket's whole scope sentence. Per-bundle defaults: A12 KS-871 Done, A13 KS-745 Done, A14 KS-999 Done if items 1/3/4 land, A15/A16 Done. Seat A set KS-1130/1165/932/1073/844 Done this way, with no stack (0 docker images).
- Holds forbid deploys, but not a LOCAL stack. This host lists 0 docker images, so a live sweep means a full local build (Start_Up/start-secuura.sh --rebuild) plus a torn-down environment: a large cost against Kam's 40% cap.
- Directly affected: #1010 (KS-1183, links as closes; a runtime change to the approve route) and A12 KS-871 (a runtime change to what the audit row records).

## Question
On merge of a runtime-behaviour PR (#1010, and A12 onward), which applies?
(a) The brief's rule: Done on merge when the whole scope sentence lands; the live-sweep gap is stated in the closing comment.
(b) Section 5f: the ticket stays open (In Review or Backlog) with "offline green; live sweep owed" until a stack run, and I do not set Done.
(c) Something else.

## Meanwhile
Continuing A12 KS-871 (file-disjoint from #1010). No ticket goes Done before your ANSWER; nothing merges without a GO anyway.

One more item from the skill, stated rather than asked. Section 4 says every test change updates both "Projects Documents/*.html" (the flow diagrams and the QA cheat sheet) in the same commit, or says explicitly why neither is affected. Those files are outside my partition. Measured:
- ks1087 / ks871 / ks1183 / workflow-instances / audit.ts / verification.ts / ORIGINATE_FORWARD: 0 hits in both files.
- Control: "Schemathesis" has 65 hits in the cheat sheet.
- Both docs describe the four systemTest harnesses, not service unit cells or unit-suite counts (394/402/851/740: 0 hits).
- 0 of seat A's merges (0b25f823f..develop) touched them.
So I state "neither doc affected, and why" in each PR body. For #1010, which is already under a gate, it goes as a PR comment, not a body or head change. Tell me if you read section 4 differently.

## Needed by
Before #1010's GO, if possible, since the Done question decides KS-1183's state at merge.

Seat A

