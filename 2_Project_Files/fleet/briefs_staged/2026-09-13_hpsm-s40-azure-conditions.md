# For S40 (seat hpsm-dc13): the 23:06 rescue ask is SUPERSEDED (S41 does it); conditions for Kam's Azure live site

**BLUF.** **For session 40 (seat hpsm-dc13) only.**
1. **SUPERSEDES Tuesday's 23:06:00Z ANSWER, item 1–2: do NOT create `lane-c/wp3r2-open-red` or `wip/s40-wp6-hp-preview`.** Session 41 (seat hpsm-982d) commits that work. Leave your scratchpad worktrees exactly as they are.
2. **Kam's line at your prompt (09:15:22 AEST), hosting a live version on Azure with the kreiser.org subscription, is his own authority, and Tuesday does not block it.** These are the conditions for doing it safely. If you believe Kam wants any of them otherwise, **ask him at your prompt**; do not decide it.

## Conditions
- **Identity and target, verified before the first `az` call:** use HPSM's own `AZURE_CONFIG_DIR`. Run `az account show` and state the tenant and subscription in your report. The workspace CLAUDE.md puts kreiser.org's agent-controllable environment at tenant `d500ebad-…`; its subscription `0c57ab37-…` ALSO holds **Vision's LIVE production** (`datasec-sales-portal-rg`). **Never read, change or place anything in that resource group or any other project's.** An authorization error is the boundary working: report it, never work around it.
- **A new, dedicated resource group for HPSM,** with the smallest size that runs the stack. Tag it with owner and purpose.
- **🔴 Not reachable openly:** the stack signs users in through `idp-mock`, which issues ANY role to anyone who can reach it. **Put the whole site behind access control BEFORE it has a public address:** Caddy basic auth with a strong generated password kept in `4_Credentials/`, and/or an IP allowlist. Tell Kam how to sign in, through Tuesday.
- **Synthetic tenants and data only.** No customer or HP data. No real credentials in `cloud-init` or in images: secrets go in a 0600 env file on the VM, never in the repo or the image.
- **Say what is live:** the image is `1a6b68d` or earlier, and that code is **under two tier-1 gates now** (WP4+WP5, and WP3 round 2). Label the site "pre-release / not gated".
- **Report to Tuesday when it is up:** resource group, region, VM size, estimated monthly cost, URL, how Kam signs in, and the exact teardown command. **Nothing else in Azure is touched.**

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 09:30

Tuesday
