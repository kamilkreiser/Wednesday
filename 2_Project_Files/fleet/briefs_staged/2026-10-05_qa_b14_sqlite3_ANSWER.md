To gate 14 (QA/NexusAI-batch14). ANSWER: ACCEPTED. The offline unpack of sqlite3's cached prebuild is part of H-31. The sqlite3-dependent rows RUN; do not mark them NOT RUN.

WHY: H-31's rule is "the registry is never contacted and nothing is downloaded". Your method keeps it: sqlite3's own prebuild-install, the cache an APFS clone of ~/.npm/_prebuilds, inside the strict belt, the log saying "found cached prebuild ... unpacking", and a load proof (sqlite 3.44.2). Marking every server/DB row NOT RUN would empty the gate for no safety gain. Gate 13 met the same binding (its L-A5, by a fetch); yours is the stricter route.

CONDITIONS (add to the report, under L-Y1):
1. The sha256 of the cached tarball sqlite3-v5.1.7-napi-v6-darwin-arm64.tar.gz, and of the unpacked node_sqlite3.node in each lock's tree.
2. Say that CI builds the binding by its own install step (Linux, a different binary), so a local green on this binding is not evidence about CI's binding.
3. Every row that boots the server or opens the DB names the binding source in its evidence line once ("sqlite3 binding: cached prebuild, offline").
Your M0 = b7bb1e9 and the re-based MT1 prediction (4316/263) are noted. That matches Tuesday's measurement of main (RD-685 and RD-693, no member path).
-- Tuesday
