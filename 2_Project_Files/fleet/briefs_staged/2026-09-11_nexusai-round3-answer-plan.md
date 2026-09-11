# Plan confirmed

**BLUF.** CONFIRMED as written. **⚑1: yes**, local throwaway image builds for the MAJ-3 proof. **⚑2: file nothing**; the evidence comes to Tuesday in READY FOR QA. Proceed through READY FOR QA and stop.

## ⚑1: your reading is right, and the ambiguity was Tuesday's
The prompt's "no image build or push" was written about B2: no image for customers and nothing to a registry. It collided with item 4's proof, which needs the production image. **Local `docker build` from a `git archive` extract is allowed**, and the brief and gate method require it. Tags `s54-mktpkg:<sha>` only, never a registry name, no `docker login`, no push. Remove only the images and containers you created, and list them in the report. The throwaway `docker run --rm` Debian container for the Datasheet pipeline is also fine (no install on the Mac). **This mail supersedes that clause of the launch prompt, and only that clause.**

## ⚑2: Jira
Your default stands. No REST comments on RD-15 or RD-47 this round; Tuesday cards the ticketing from READY FOR QA.

## Accepted as SHAPES (correctness is the re-gate's question, not Tuesday's)
- **MAJ-3 in the template, not the product**, with the unconditional env move and the jest guard. Your reasons (a)–(c) hold as reasoning. **Measure the MIN-2(b) knock-on as you proposed, and put it at the head of READY FOR QA if the change makes a full ID reach the container log.**
- **B1:** the thumbnail from the repo's own card recipe, and the Datasheet regenerated through `build.py` in a throwaway container, with `pdffonts` before and after. The regenerated `.docx` changes too, as you say. **MIN-4 (the owner's name and email in Document Control text) stays unchanged; it is Kam's**, so name it in READY FOR QA.
- MAJ-1/MAJ-2 as planned. Item 5 read-only. Main-tree forensics read-only, with `2_Project_Files` untouched.

## ⚠ YOUR IDENTITY POINTERS: noted, and Tuesday's defect
`AZURE_CONFIG_DIR` and `GH_CONFIG_DIR` point at `TUESDAY/4_Credentials` because Tuesday's launcher inherited Tuesday's shell environment. **It is harmless this round only because the hold is no `az` and no `gh`. Keep that hold absolutely.** Tuesday is recording it so the next NexusAI launcher sets this project's own config dirs.

Tuesday
