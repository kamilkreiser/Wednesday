# Harness widening — open-PR-only builder refusal + ascii_proxy line-keyed sites (2026-09-17)

Written by Wednesday from the builder agent's final message. The verbatim arms outputs are copied beside this file.

## BLUF
1. **`night/build_input.sh` refuses only OPEN attached PRs.**
   - It reads GitHub REST `pulls/<n>` with the Secuura GH_TOKEN, and prints each attached PR's state (merged / closed, not merged / OPEN).
   - An unreadable state REFUSES rc 2 (fail closed). `NIGHT_GITHUB_API` is a test seam, http/https only.
   - The PR gate now runs BEFORE the archived/state/assignee gates, so an open PR on an In Progress ticket is refused for the PR.
   - Backup `build_input.sh.pre-0917-widen`, swapped 15:47:35.
   - Arms `tests/build_input_open_pr_arms.sh`: **10/10** (agent 16:12:21; **Wednesday's own re-run 16:14:11: 10/10**).
2. **ascii_proxy for line-keyed `-` sites that carry non-ASCII.**
   - A must-change bullet may end `ascii_proxy U+2014=--`. The model writes the ASCII stand-in.
   - `tasks/code_patch/a3b_proxy.py` (run before A2) substitutes the tip's real bytes ONLY when the `-` line is byte-equal to the stored proxy text AND the hunk's own old-side context places it at the site's number (the header is ignored).
   - MISPLACED or TEXTMISMATCH → `FAIL A3b PARTIAL FIX`, and RETRY-ONCE fires.
   - The builder refuses proxies outside a line-keyed Where, on stays sites, with a bad or absent map, non-ASCII neighbours within 3 lines, or non-ASCII `+` lines.
   - `a3b_line.py` compares quotes after substitution.
   - Backups `checker.sh.pre-0917-widen`, `a3b_line.py.pre-0917-widen`, `build_input.sh.pre-0917-widen2`; swapped 16:02:56.
   - Arms `tests/a3b_ascii_proxy_arms.sh`: **21/21**. It proves KS-839's REAL outputs still FAIL, a wrong-line proxy FAILs (MISPLACED), a one-character-off proxy FAILs (TEXTMISMATCH), the golden PASSes 7/7, and the OLD checker FAILs A2 on the golden.
3. **Regressions on the installed files:** a3b 19/19 · a3i 11/11 · retry routing 15/15.
4. **Proof brief and input:** `night/briefs/KS-839-proxy.md` + `night/inputs/code_839proxy.json`, NOT queued. A Claude seat owns KS-839 by hand.

## NOT TESTED
- A missing GH_TOKEN.
- A non-github.com pull URL.
- A closed-unmerged PR.
- A live model round on a proxy brief.
- A correct proxy in drifted context: refused as MISPLACED, a usefulness limit, not a safety one.
- Builder refusals for a proxy equal to a real tip line, and for non-ASCII neighbours (no arm).

## Ruling requests — Wednesday's rulings (16:1x)
1. **Retry feedback for proxy sites** carries `text_at_tip` (with the em dash) into `missed_sites`. It should carry `ascii_proxy.text`. **OWED: a `night_run.sh` edit plus an arm, by a later seat, before the first proxy brief is queued.**
2. **Gate order** (PR gate before state gate): **ACCEPTED.** A ticket with an open PR belongs to that PR's lane whatever its state, so refusing it for the PR is the more informative reason.
3. **Strict byte compare for proxy text:** **KEEP STRICT.** A substitution that restores bytes the model never wrote must only fire on an exact match. Looseness here would be the dangerous direction.
