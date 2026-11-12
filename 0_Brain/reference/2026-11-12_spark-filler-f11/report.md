# Spark filler F11: numstat PR 2214 (KS-2166), 2026-11-12 -> done_accepted, MATCH (Spark 7.37 s)
- FOUND: A 29th READY mail vs GitHub API: 10 files, +507 -9, index.ts +54 -0; every number matches. API head = eb7315988de5c63cd6f9a1d96a89cb131b2643be (state open), equals Wednesday's ls-remote.
- Looseness (same as F08): per-file claims named by short labels (ks2166 test, ks849, ks1868 x4, ks1931, fragments); the checker matched them by counts, not path. The two fragment files (+22, +21) both resolved to one API filename in the matched text. Deletions null for the ks2166 test and fragments.
- TESTED: counts only. NOT tested: diff content vs prose.
- HOW: GH_CONFIG_DIR=Secuura Blockchain .gh-config, gh api (read only) pulls/2214 and --paginate pulls/2214/files -> filler/inputs/pr2214.{meta,files}.json; mail copied to inputs/mail/pr2214_ready_a29.txt; tasks/F11-numstat-pr2214.json; queue row; tunnel check UP; bash drain.sh rc 0.
