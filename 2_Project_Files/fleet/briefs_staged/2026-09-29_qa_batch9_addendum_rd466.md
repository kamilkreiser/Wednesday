BLUF: ADDENDUM — RD-466 IS NOW A MEMBER of batch 9. This SUPERSEDES the launch prompt's "RD-466: not a member". Its READY landed at 02:44Z, two minutes after your launch; adding it here instead of a second gate is the batch-gates rule.

RD-466 @ 3f7e263bf69f571d79aeae6ecc7b48ce6730d4c2 on rd-466-image-case-names-s86o (Tuesday's ls-remote at 12:4x AEST). Built by NexusAI-O. Base 40b7eae (an ancestor of dd15ce1). TIER 1: it decides which secret-shaped files ship in the CUSTOMER image. Its own verdict line: `RD-466: <verdict> @ 3f7e263`.
READY, read whole by Tuesday: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-29_nexusai-rd466-READY-mail.txt

Apply your brief's §OPT (o1-o4) in full, plus:
- o1 note: the READY says the removed wildcard is Dockerfile:19 (base stage), `COPY package*.json ./` -> `COPY package.json package-lock.json ./`. Verify that is the only COPY change.
- o2 as your brief wrote it (measure WHICH cell reddens on the restored wildcard, plus the converse remove-one-more arm). That is the check Tuesday wants.
- The READY's 7 mutations (M1-M7: env/rc/id_rsa/db lower-case, .aws removed, package*.json restored, re-include moved above the env rules) re-derived independently; M7 (the RD-391 `!**/.env.example` order) is the one that matters most.
- The re-anchored checks in image-content-exposure (RD-391 ARM ~:349, S51 ANCHORED + ARM 1, the floor) are TEST changes that loosen or move guards: for each, show it still fails on the defect it names (a stale-anchor plant). A guard that went hollow is a Major under C-40.
- C-187: RD-466's base is 40b7eae, not 1904765. Measure whether the image-content-exposure pair question arises at all (RD-466 CHANGES that file), and run C-57 on the merged tree with it in.
- Merged tree: M0 + RD-723 + RD-618 + RD-466 (your order to recommend); re-base counts. RD-466 adds no tests (READY: 4191/252 unchanged).
- The real-image pair (base vs head, file-set diff) is O's measurement. You MAY re-derive it ONLY through NexusAI's own docker lock (session-tools locks, queue-docker), `--network none`, in your own mktemp context, never pushing or tagging to any registry. If docker is not available to you, name it NOT RUN; the through-code legs above are required either way.
- Holds stay as briefed: no Azure, no registry, no demo, no Partner Center.
-- Tuesday
