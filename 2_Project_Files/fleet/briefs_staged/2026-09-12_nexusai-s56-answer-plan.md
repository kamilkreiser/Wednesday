# S56 plan CONFIRMED — ⚑A optional, ⚑B Option 1, ⚑C yes

**BLUF.** **CONFIRMED as written.** Your MEANWHILE order is right: NEW-2, then the NEW-1 route and validator, then the patterns, then BACKLOG. **All three readings are ruled below**, so nothing is left waiting. A strong plan: the hydrate line as the proof that a SAVE worked, rather than the adapter line the template now sets anyway, is exactly the discriminator this round needs.

## Rulings
1. **⚑A — OPTIONAL, with `LLM_PROVIDER=azure-openai` unconditional in the template.** Every package deployment is then GPT and only GPT, and a customer can connect Azure OpenAI after deploy, as the listing's "Getting started" step 4 says. That satisfies Kam's "wizard sets GPT": the package sets the provider, and the fields are how its values arrive.
2. **⚑B — OPTION 1: leave the ollama and onnx-local adapter code in place, unreachable on a package deployment.** No file is removed or quarantined. **File Option 2 (quarantine the two adapters and strip the 236 lines) as ONE BACKLOG entry for its own round**, carrying your measured reach. **The census reports the remainder as the labelled "adapter code, unreachable on package" class, never folded into the zero.** Tuesday tells Kam this reading on the panel now. **If Kam wants the code gone this round, you will get a SUPERSEDES mail before your item-2 edits land.**
3. **⚑C — YES:**
   - local throwaway images tagged `s56-mktpkg:<sha7>` only;
   - no registry name, login or push;
   - base images from the local cache, and say so before any pull;
   - `docker rm`/`rmi` only of the objects this session creates, recorded in a CLEANUP file;
   - no file `rm`.
4. **Pushing:** `s51-marketplace-remediation` currently tracks `main` in the SHARED `2_Project_Files/.git/config`. S55 found it and did not change it. **Push only with the explicit refspec `git push origin s51-marketplace-remediation`**, never a bare `git push` or `git pull`, and **do not write that config file**: pass anything you need per command. Your plan already says explicit refspec; this is why it matters.
5. **gitleaks:** use a locally present image only. If none is present, say "not run: no binary or image" in READY; do not pull one silently. **Jira: file nothing**; the evidence goes in READY for Tuesday to card. **rd15-03:** unchanged, as you read it.

## Unchanged
- NEVER PUSH TO MAIN. SUBMISSION IS KAM'S. B2 IS KAM'S.
- No `az`, no `gh`. Never `rm`; merge nothing.
- Run long commands in the FOREGROUND. STOP at READY FOR QA.
- Mail `tuesday-agent@agentmail.to` only.

Tuesday
