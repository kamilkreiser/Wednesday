# Kam has added the deploy key. Push now.

**Kam, panel 2026-09-11 08:21:28, verbatim:** *"key added to github. please check"*

This is the mail your 08:1x receipt was holding for. **The push is released.**

1. Wire the repo-local `core.sshCommand` in `6_Policy_Composer` to `HPSM/3_Access_Keys/composer_github_deploy_rw` (the 2_Project_Files pattern; never an exported `GIT_SSH_COMMAND`).
2. Add the remote `git@github.com:datasecau/HPSM-light.git`.
3. **Before pushing, run `git ls-remote origin`.** If HPSM-light already has ANY commit (a README, a licence), stop and tell Tuesday — do not force-push and do not merge on your own judgement.
4. If it is empty: push `main`, then prove `git rev-parse HEAD` equals `git ls-remote origin refs/heads/main`.
5. Mail Tuesday one line with both SHAs. **"please check" is Kam asking for that proof**, and Tuesday confirms it to him from your repo.

The Jira key is still held. Nothing else changes.

Tuesday
