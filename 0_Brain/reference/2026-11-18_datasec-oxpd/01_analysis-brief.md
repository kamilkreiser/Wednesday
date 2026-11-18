# Datasec / OXPd — analysis brief for every analysis lane (read this WHOLE first)

Client: Datasec. Project: OXPd (porting the HP Authentication Suite from HP Workpath to HP OXPd). This file is from Friday (Kam's laptop coordinator). It is the common brief; your own lane is in the message that sent you here.

## What Kam asked for (his words are in `00_kam-brief_verbatim_2026-11-18.txt` in this folder: read it)
In short: Datasec ships a suite of printer apps on HP Workpath (apps that run ON the printer): HP Authentication Manager (sign-in to Microsoft Entra at the device, token shared with the other apps), Mailflow (Outlook mail), Teams, OneDrive, SharePoint, Universal Print, and one or two more. The new project recreates the same suite for printers that use OXPd, where the solution runs on a SERVER (he says: a localised server rather than a web deployment) and drives the printer remotely. It must work with OXPd 2 AND with OXPd 1 (whatever the latest 1.x is), and live beside the existing Workpath apps because some customers have mixed fleets. The deliverables that follow this analysis: an architecture document, a specific plan of attack and build (deployment methods, integration with Entra environments, integration with the existing Workpath product, the components of the solution), and a list of questions for Kam.

## The library you analyse (READ-ONLY, never change, move or delete anything in it)
`/Volumes/Laptop-DEV/!CODING/Datasec/OXPd/` — start with its `START-HERE.md`, `README.md` and `README-INDEX.md` (short; read them whole whatever your lane is). About 31,000 files, 5.2 GB. Do not unpack archives into it, do not build in it, do not run its scripts or binaries, do not open files in a GUI app. If you need scratch space use `/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/d534540a-a4f0-44ac-a3a3-685bcd5abffc/scratchpad/oxpd_<your lane id>/`.

## Rules of this session (hooks enforce some of them)
- Never use `cd` in a command: absolute paths. No `echo ====` separators. No git write verbs anywhere. Prefer the Read and Grep tools; quote every path (the paths contain spaces and `!`).
- SECRETS: source code and config in this library may hold client secrets, keys, tokens, passwords, connection strings, certificates or tenant ids. NEVER copy any such value into your report or your messages, not even partly. Report only that one exists and where (`path:line`, "a client secret is hardcoded"). The same for personal data of real people.
- HP material is under partner and beta licence terms: quote at most a sentence or two at a time; describe and cite, do not transcribe.
- This is a Datasec artefact: it names no other client of Kam's and nothing from outside this library.

## How to work
- Be exhaustive inside your lane and honest about coverage: list what you read WHOLE, what you sampled (and how you chose the sample), and what you did not open. A folder that exists is not a folder that was read. For large trees first build an inventory (file counts by type and by directory) with a command, then read the files that carry behaviour.
- Every factual statement carries its source as `relative/path:line` (relative to the library root) or `path` for a whole document. A statement you infer is marked "(inferred)". A statement taken from a document that may be wrong (marketing page, auto-caption transcript, a guide that says it was AI-produced) is marked with that caveat. Where code and documentation disagree, say so and give both; the code is the source of truth for current behaviour.
- Never state a mechanism you have not read. "Not found" needs the search you ran and a positive control showing the search can find something.
- Think about the port while you read: for each behaviour of the existing product, what does it need from the device (UI on the panel, card reader input, scan, print, device identity, storage, network), and for each OXPd capability, what exactly is offered, by which service and call, with what limits, on which platform version.

## Your report
Write ONE Markdown file: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-18_datasec-oxpd/analysis/<lane id>_<short-name>.md` (the exact name is in your lane message). Plain, exact prose, tables where they carry data. Sections, in this order:
1. **BLUF**: ten lines at most: what this lane holds and the five facts that most shape the port.
2. **Coverage**: read whole / sampled / not opened, with counts.
3. **Inventory**: what is there (components, versions, languages, entry points, build and packaging).
4. **Findings**: the substance of your lane (your lane message says what to extract), with sources.
5. **What this means for the port**: requirements, constraints, reusable parts, traps; each tied to a finding.
6. **Contradictions and doubts**: where sources disagree or look stale.
7. **Questions for Kam or his team**: only what the library cannot answer; each with why it matters and what you would assume if unanswered.
8. **Secrets and sensitive items seen** (locations only), and anything that looks like a security weakness in the existing product that the port should not carry over.
Aim for depth over length, but do not cut substance to be short: 300 to 900 lines is the expected range.

Your final message back: the report path, the BLUF, your coverage numbers, and the three most important questions. Do not ask questions back; where something is ambiguous, decide and say what you decided.
