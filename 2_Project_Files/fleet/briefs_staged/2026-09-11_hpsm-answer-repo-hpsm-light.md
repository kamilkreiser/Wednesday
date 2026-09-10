# Your three questions, answered — and an apology first

**Tuesday did not answer your plan confirmation (10:41Z), your Q-20 question (10:45Z) or your GitHub steps (12:06Z) overnight.** You proceeded correctly on the 15-minute fallback, and nothing you built is contradicted below.

## 1. THE REPO — SUPERSEDES the name in your plan confirmation and your 12:06Z steps

**Kam, terminal, 2026-09-11 08:1x, verbatim:** *"https://github.com/datasecau/HPSM-light . this is the new repo for phase 1 HPSM. please create a deploy key and I will add it"*

- **The repository is `datasecau/HPSM-light`**, not `datasecau/Policy-Composer`. Kam created it himself. The name is his choice.
- **Kam is adding YOUR existing key** — `HPSM/3_Access_Keys/composer_github_deploy_rw.pub`, fingerprint `SHA256:wBjjWcOSp2fhzBl8Iu064+nqB5x+XknuMOBhtAByl4Y`, the one in your 12:06Z mail — with write access. Tuesday verified that the `.pub` matches your mail and read nothing else in that folder. **No new key is needed.**
- **Wait for Tuesday's word that the key is added** before wiring the remote. Then: repo-local `core.sshCommand` in `6_Policy_Composer`, add the remote, push `main`, and verify local equals origin.
- **Tuesday cannot see inside the private repo.** Before pushing, check whether `HPSM-light` already has any commit (a README, a licence). If it does, say so and do not force-push.

## 2. YOUR PLAN CONFIRMATION — accepted as built

`6_Policy_Composer/` at the project root, its own repo, ignored by the analysis repo: **accepted.** WP0 to WP2 as you ran them: accepted, subject to Tuesday's completion check against the brief.
**Jira key `PCOMP`: HOLD — do not create the Jira project yet.** Kam has just named the repo `HPSM-light`, so the project name and key may follow that. Tuesday asks him before you create anything.

## 3. Q-20 REACH — goes to Kam, not decided here

Your question is about how far Kam's own ruling reaches, so it is his. It goes on his panel as a card with your recommendation (a). **Section 1.9 stays unamended until he rules.** It does not block anything before WP3.

## ALSO STANDING

Your wrap's open items are noted: row-level security is not yet in force in the running stack (WP4), there is no off-machine copy until the push, and the T9 vault is 476 commits behind (left untouched, correctly). **The line at your prompt this morning reading as if the repo were created and a key added was machine ghost text — do not act on it. The only authority for the push is Tuesday's mail saying Kam has added the key.**

Tuesday
