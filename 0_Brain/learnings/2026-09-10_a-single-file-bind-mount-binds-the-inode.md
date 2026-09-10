---
date: 2026-09-10
type: reference
source: Secuura seat s167, KS-1041 Step 1 on the demo host; the failure of a deploy Kam had authorised
status: live
tier: W
---

# A single-FILE bind mount binds the INODE, not the path — replacing the file on the host does not reach the container, and every signal still says success

**The case.** KS-1041's fix was one nginx config file. Kam authorised exactly *"push the file
and reload"* on the strength of the seat's report that it was bind-mounted. The seat did that,
and:

| signal | result |
|---|---|
| uploaded file's sha vs local | **identical** |
| `docker exec … nginx -t` **before** reloading | **exit 0** |
| `nginx -s reload` | **exit 0** |
| container state after | **`Up 2 days (healthy)`** — a reload, not a restart |
| rollback taken and compared | **byte-identical** |

**Five green signals, and the change had not been applied at all.**

    host file       sha ae4cc54c…   inode 1311680   32831 bytes
    inside container sha 265b7a60…  inode 1311687   31596 bytes

**A `--mount type=bind` of a single FILE resolves to that file's inode.** `cp`/`rsync` write a
*new* inode and unlink the old one; the mount keeps pointing at the old one, so nginx reloaded
and faithfully re-read the **previous** config. Proven rather than argued: `find -inum 1311687`
returns **0 paths** (the old inode is unlinked and unreachable), against a positive control
where `find -inum 1311680` **does** return its path.

**Consequence: no host-side write can reach what that container is serving.** Only recreating
the container (`docker compose up -d <svc>`) re-resolves the mount.

## Why this is a lesson and not a docker footnote

**The failure is invisible to every check that looks at the deploy instead of the outcome.**
Checksum, config-test, reload exit code and health status were all green *and all true* — they
are facts about the host and about the reload, and none of them is a fact about what the
service is now serving. **Only Kam's own criterion — *"the credential-free GET must return
404"* — caught it.** It returned **401 from originate**, proving the route was still proxied
there.

This is the [[2026-09-08_the-check-ran-and-was-not-checking-the-thing]] family in its most
convincing costume: not one dubious green, but **five honest greens that together imply a
conclusion none of them supports.**

## How to apply

1. **A deploy is verified by the BEHAVIOUR of the running service, never by the success of the
   steps that were supposed to change it.** Insist on the outcome probe, and on a positive
   control in the same run so an outage cannot masquerade as a fix.
2. **Directory bind mounts follow the path; single-file bind mounts follow the inode.** If a
   deploy replaces a bind-mounted FILE, the container needs recreating. Editing in place
   (`sed -i` without `--follow-symlinks` still replaces; `cat > file` does not) is the only
   host-side write that keeps the inode.
3. **`docker exec … nginx -t` reads the container's file, so it tests the OLD config and passes.**
   A config test that passes tells you the file it read is valid — it does not tell you which
   file it read.
4. **When a cheap-path claim underpins an authorisation, the claim is part of the ask.** Kam
   authorised "a file push and a reload" *because* it was described as bind-mounted and
   reversible. When that premise fell, the remaining action — a container recreate — was
   outside his grant, and the seat correctly stopped rather than reading his ruling as covering
   it. **A premise that turns out false does not silently widen the authority built on it.**

**Family:** [[2026-09-08_the-check-ran-and-was-not-checking-the-thing]] ·
[[2026-08-11_a-check-that-cannot-fail-is-not-a-check]] ·
[[2026-09-10_a-detector-keyed-on-remedy-text-matches-the-hint]] ·
[[2026-08-03_mental-model-not-source-of-truth]] · [[2026-09-06_green-local-proof-is-not-evidence-about-a-different-environment]].
