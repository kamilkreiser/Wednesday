# DRAFT comment for KS-1397 (Wednesday, 2026-10-01). Gate it before posting; post on the GO; then move KS-1397 to Done.

## BLUF
Kamil's ruling (2026-10-01): **accept the `Server: nginx` header, with this recorded reason.** No gateway change will be made.

## The reason
- The nginx **version** is already hidden: `Blockchain/Dev/docker/nginx-gateway/nginx.conf:24` reads `server_tokens off;` at develop `723dc0722b68`.
- Upstream `Server` headers are already stripped: `nginx.conf:142` reads `proxy_hide_header Server;` at the same commit.
- So what remains is the bare product name `nginx`. It discloses little, and removing it needs the headers-more module, which means an image change on every nginx target. That cost is not justified for a LOW finding.

## What follows
Per option 2 in this ticket, the harness side (KS 492) may add this finding to the Akto known-false-positive allowlist, quoting this ruling as the reason. Nothing else is silenced.

Not re-measured here: the live responses on slot 4 (taken from this ticket's own "Verified" section) and the Akto template's matching rule.
