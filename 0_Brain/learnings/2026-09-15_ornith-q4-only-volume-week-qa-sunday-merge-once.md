---
date: 2026-09-15
type: grant
source: Kam, panel 2026-09-15 16:36:04 +10:00 (view=wednesday), verbatim below; Wednesday's reading put back on the panel 16:37
status: live
tier: W
expires: end of Sunday 2026-09-20 (derived: `date -j -f %Y-%m-%d 2026-09-20 +%A` = Sunday; "the rest of the week")
---

# Grant: the SMALL quant only for the rest of the week; complete as many tickets as possible with the local LLM; QA Sunday night and merge / commit all at once

**His words, verbatim (2026-09-15 16:36:04):**
> *"ok. lets use the smaller model for the rest of the week. complete as many tickets as possible. work with the local LLM. we will do QA on these Sunday night and merge / commit all at once"*

**The operative case, so the headline matches it:** a seat between 2026-09-15 16:36 and the end of Sunday 2026-09-20 is deciding what Ornith runs, which quant, and what happens to a PASS. **q4 (`ornith:35b`, Q4_K_M) only** — the q8 tag stays on disk unused (his call after the measured 13-pair 2-2-9 tie and the cost figures). **Volume is the goal:** Ornith drafts across the WHOLE KS Backlog/Todo, not the 09-14 contract's filter; Wednesday writes every brief; every diff still passes the checker and a Wednesday source read; **nothing is merged or committed to the Secuura repo until Sunday night's QA** (a Claude seat after the allowance renews ~Sat 11:xx) — then everything at once.

**Wednesday's reading, stated to him 16:37 (his word corrects it):** the security-surface exclusion in the 09-14 contract was WEDNESDAY's clause, not his; under "as many as possible" it is widened to the security-adjacent tickets that are not authentication logic (the API-key service's swallowed INSERT, spec drift, dead converters) — **auth / MFA / OAuth product edits stay HELD until Kam names them in.** Kam-gated classes are untouched: no merge, no deploy, no human message; a held diff is not a change to anything.

**How to apply:**
1. `NIGHT_MODEL=ornith:35b` everywhere (the runner's default); no q8 launches; the pair table stays frozen at 13.
2. The Backlog/Todo sweep for candidates is re-run by every seat (`board_count.sh` for totals; the 308 of 15:5x is the measured baseline); briefs per the HOW-TO-WRITE-A-BRIEF rules in NEXT-PICKUP (split > 3 edits; list the declarations; `statement_ok`; text-to-copy; shell-stamped clock via `night/new_brief.sh`); RETRY-ONCE handles the neighbour-slip class.
3. The Sunday plan is a SEAT with a brief: `fleet/briefs_staged/secuura_raise_ornith_ready_diffs.md` (staged 15:5x) grows with every new READY; QA = the tiered gate per PR; merges one at a time on Wednesday's GO under the TESTED grant (re-check its expiry — it was "for the time being").
4. **Expiry:** recorded in [[../tasks/EXPIRING-GRANTS]]; after Sunday the 09-14 night rule and contract return unless he renews.

**Family:** [[2026-09-14_ornith-runs-at-night-in-the-downtime-a-standing-rule]] · [[2026-09-15_ornith-every-issue-gets-a-tooling-or-instruction-fix]] · [[2026-09-14_at-90pct-weekly-usage-no-new-agents-wednesday-plus-local-model]] · [[2026-09-06_a-scoped-override-carries-its-own-expiry]] · [[2026-08-03_go-slow-earn-autonomy]] (rule 5).
