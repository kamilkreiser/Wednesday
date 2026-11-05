# Gate 199 commission — Secuura / Blockchain, PR 2009 (KS-1938: gdprService.ts remaining unguarded thrown-value reads), TIER 1, ROUND 1 of 2

Written by Wednesday 2026-11-05 18:0x AEDT (the 18:00 successor seat). Model: Opus (routing v1.0, tier 1: data-destruction file — the erasure function lives in gdprService.ts). QA GATE: findings only; fix nothing; write nothing outside this folder; no box; post nothing to Linear or GitHub.
Write `verdict.md` here EARLY as a stub (line 1 `NO GO (INCOMPLETE: killed before the verdict)`), overwrite at the end. Final line 1 is exactly `GO`, `GO WITH NOTES` or `NO GO (<reason>)`.
Read first, whole: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md (method: clone by SHA into a subfolder HERE; only read-only git verbs against the shared checkout /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files — never fetch/worktree/merge-tree there), then `ready_2009.txt` here (Seat V 20th's READY FOR GATE, verbatim).
Recursive grep/find: scope to your clone; never over 0_Brain/reference, local-model/ or 5_Project_History trees (a hook refuses it). Never pipe a command that can write through head/tail.

## Subject (Wednesday's `git ls-remote origin`, 18:01:11 AEDT)
refs/pull/2009/head = `86eb3152af4638d05b287d83a3424520d131076c`; develop = base = `5fc5569ed96ac61f64823cc9e1fa841899aa1f62`. Seat V 20th (Sonnet). 4 files per the READY (+549/-15).
KS-1938's ask: every catch in gdprService.ts that reads the thrown value without a guard answers its documented outcome when the thrown value is unreadable (revoked Proxy; Error whose message getter throws). Seat's claim: 14 sites changed + the updateDSRStatus err?.code guard; 2 already guarded by PR 1935; 1 HELD.
**Line 670 (erasure step 5c, subject-email resolution) is DELIBERATELY UNCHANGED by Wednesday's ruling** (its guard would turn a loud abort into a quiet erasure completion; it goes to KS-1953). Verify it is byte-equal to base. Do NOT report its absence as a finding; DO report if any OTHER change in the erasure function alters which steps run or what it returns.

## Questions (measure; the READY's figures are claims)
1. Scope: exactly the 4 paths; enumerate every hunk in gdprService.ts and show each is a guard around a thrown-value read (or the err?.code guard) and nothing else: no change to SQL, step order, transaction boundaries, returned shapes, or log levels except the new "unreadable thrown value" line. Count sites independently: how many catch blocks in the file read the thrown value at base; how many are guarded at head; list any unguarded at head other than line 670.
2. Behaviour, base vs head, per site: ordinary Error -> same documented answer at both; unreadable value -> TypeError/reject at base, documented answer at head. Use the seat's cells AND at least three cells of your own (one in the erasure function, one export section, consent).
3. Erasure function (data destruction): for an ordinary Error and an unreadable value at each guarded erasure site, the set of steps that run and `success` are identical between base-with-ordinary-Error and head-with-unreadable-value. No path at head completes MORE of the erasure (or returns success true) where base aborted with an ordinary Error. "N of M".
4. Logging: the new log line never echoes the thrown value or any PII (plant a marker in the message and an email in a field; search every logged argument; expect 0).
5. Mutants: reproduce 3 of the seat's 15 tampers plus two of your own: (i) guard at line 670 added (expect the step table V wrote: success true; prove the gate WOULD catch it if someone adds it later); (ii) a guard that swallows and returns success where base returned failure at one erasure site.
6. Suites at base and head: originate unit suite (jest), tsc --noEmit for the service, eslint on the changed files, docs-fragments check, each with a planted-defect control. Classify any failure as same-on-base or new.
7. Merge tree in your clone: rc and tree id.
8. PR body (gh may be unavailable: say so): states the held line 670 and its pointer to KS-1953, the per-site table, Node v26 not 24, the NOT-run list (no real Postgres/stack, hook legs 3/4/8 skipped).

## Output
`verdict.md` (verdict line, BLUF, findings F1..Fn with severity, file:line, evidence path, fix), evidence files here. Final message: the verdict line and one line per finding.
