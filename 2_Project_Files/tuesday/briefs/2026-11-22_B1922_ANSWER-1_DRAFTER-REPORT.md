STARTABLE: YES

# B1922 ANSWER-1 DRAFTER REPORT (the re-cut for seat X34)

Answer: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1922_ANSWER-1_recut.md`. Tools: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s311/d1922/answer1/` (ten files). Drafted 21:50 to 21:58 AEDT.

## BLUF
- Three sentences change, and nothing else in the patch does.
  - **E14** (line 63-64) now states the strict reading as a choice for now, to be looked at again once a printer's traffic is seen. Source: C-63, `CLARIFICATIONS.md:610-624`, read at source.
  - **E1** no longer claims the vault holds the new value. A rotating refresh in flight also writes, and the last write wins (`DeviceTokenHolder.cs:58`, `:65-66`, `:373`, `:377`).
  - **E9** no longer calls a wrong-length read a SHA-256 (`CallbackCredentials.cs:20`, `:147`, `:55`, `:178`).
- E4 (the late grant) stays "an open question". No clarification touches it: `refresh` 0, `late` (word) 0, `timeout` 0, `grant` (word) 1, the C-68 reading. Controls: `tolerant` (word) 2 and `Keep both strict for now` 2.
- New patch sha256 is `bc903822...973a8f` (+49 -1); the README after it is `e17e251b...dee8` (156 lines). It applies on a fresh clone of main `4a0a9717`, which I re-read by GET at 21:56:37: `--check` rc 0, the second check rc 1, and `cmp` against my edited README rc 0.
- Proofs, control first: `PROOFS-CONTROL: 68 of 68 FAILED when moved`, `PROOFS: 68 of 68 PASS`, `CENSUS: 13 of 13 as required`.
- Words: `WORDS: clean (2 files)`, and a planted "decided" fires. gitleaks rc 0.

## Questions for Tuesday (each with a default)
- QA1: the E14 wording. Default: as written. It is word for word the example in Tuesday's message.
- QA2: E4 stays open. Default: yes. The grep proves no ruling.

## UNMEASURED / NOT RUN
- No dotnet job ran for the answer. The kit's runs stand: README text is read by no build or test.
- Nothing hosted ran.

## Outside the fences
- I wrote only these two briefs files and, under my scratch, `answer1/`, `clone2/`, logs and a quarantined plant.
- The seat's lane, pane, STATUS and the project were read only. I read STATUS lines 1-30 and its last lines, and `CLARIFICATIONS.md` lines 610-624 plus greps.
