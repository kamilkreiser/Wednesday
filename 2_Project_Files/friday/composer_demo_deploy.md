# Datasec / Security Composer — redeploying the live demo from the laptop (Friday's runbook)

Recorded 2026-09-24 after two deploys (5c0490d at 14:40, c018e07 at 16:4x AEST) because the first one was written only as
prose and the second had to rediscover every name. **A deploy of the demo needs Kam's word every time** (demo = his class).

## Names (measured 2026-09-24; re-check with `az vm list` before relying on them)
- Subscription `0c57ab37-…`, tenant `d500ebad-…`; Kam's login lives in `Datasec Security Composer/4_Credentials/.azure`
  → `export AZURE_CONFIG_DIR=".../Datasec Security Composer/4_Credentials/.azure"`; `az account show` must say kreiser.org@me.com.
- VM `hpsm-demo-vm`, resource group `HPSM-DEV-RG`, public IP `4.196.153.103`, user `hpsm`, NSG `hpsm-demo-vmNSG`.
- Standing NSG rules: `default-allow-ssh` (1000, one fixed IP) and `allow-http-https` (1010). The laptop is NOT allowed by default.

## Steps
1. **Merge** the reviewed branch on `datasecau/HPSM-light` head-pinned (`friday_as.sh datasec gh pr merge N --squash --match-head-commit <sha>`),
   then compare TREE shas (`gh api repos/datasecau/HPSM-light/commits/<sha> --jq .commit.tree.sha`) of the reviewed head and the squash.
   (A three-dot compare measures from the merge base and will show every file; it is the wrong instrument.)
2. **Temp access:** a fresh ed25519 key in the session scratchpad; `az network nsg rule create … -n friday-laptop-ssh-temp-<date> --priority 1001
   --source-address-prefixes <laptop public IP>/32 --destination-port-ranges 22 …`; append the public key with
   `az vm run-command invoke … RunShellScript` after backing up `/home/hpsm/.ssh/authorized_keys` to `.pre-friday-<date>`.
3. **Archive:** `gh api repos/datasecau/HPSM-light/tarball/<sha>`, extract, re-root (drop the top directory), repack with
   `COPYFILE_DISABLE=1 tar --no-xattrs --no-mac-metadata -czf composer-<short>.tar.gz -C <top> .`. Entry count ≈ the previous
   archive's real files (5c0490d = 695; its archive on the VM carries AppleDouble twins, 1,390).
4. **Deploy:** `scp` to `/opt/hpsm/`, then on the VM: `cd /opt/hpsm && ./remote-update.sh /opt/hpsm/composer-<short>.tar.gz secrets/demo-switch.env`.
   It keeps `composer.prev` (the rollback), runs migrations, recreates edge. Expect: all services healthy, "migrations applied: …",
   the content release line, **PREFLIGHT: GREEN**, `{"status":"ok"…}`.
5. **Verify live** behind Basic auth (`COMPOSER_DEMO_URL/USER/PASSWORD` in the project's `4_Credentials/.env`): page 200, and the new
   CSS/JS bundle carries a class that ONLY the change adds (c018e07: `pc-menu-button`).
6. **Remove temp access and PROVE it:** strip the key line via run-command (backup `.pre-friday-removal-<date>`, `grep -c` = 0),
   `az network nsg rule delete …`, list the rules (only the two standing ones), and `ssh … true` must time out.
7. Record the deploy on the card (`--delivered`), in Composer CLARIFICATIONS, and in the daily note.
