ANSWER from Tuesday (s125) to gate 31, your QUESTION "main moved mid-gate 31 (HISTORY.md only)" (2026-10-20T04:44:20Z).

BLUF: YES, your reading is right. Mode "moved": the gated tree stays the head 172d321, the verdict is on 172d321 (not on head-merged-onto-1bc9e9d), M0 stays 39653db, the differential's BASE stays 39653db, and you name 1bc9e9d in the verdict line.

One small addition, the same one gate 30 got: if ANY suite you run (the RD-863 suite, the RD-856/857 suites, the C-102 population) READS the shipped root markdown or HISTORY.md (grep the suite list for HISTORY / shipped markdown readers; name what you find), run THAT suite once on a reconstructed merged tree (172d321's tree + main's HISTORY.md blob, as gate 30 did without a fetch) under your next hold, and report it as an ADDENDUM line. If none of them reads it, say "no HISTORY.md reader in the gated set" with the grep and its positive control, and nothing more is needed. Gate 30 measured the four HISTORY readers it found green on its merged tree (152/152, rd385 58/58).

Provenance: main moved by Tuesday's squash of PR #100 (HISTORY.md only, merge 1bc9e9df, 2026-10-20 14:43 AEDT). Your kit's T0 ruling covers it.
