# KS-972 R16B-BANNER - re-brief at develop 8c2f7b3fd of READY_KS-972_ornith35b-q4_BASHPATCH-REANCHORED-PASS-7of7_2026-09-16.diff.md (written 2026-09-22 09:47:00 AEST by Wednesday's feed8 drafter; the product hunk and the new suite are the old READY's PASS 7/7 output re-anchored at the tip, every '+' line and every suite line made ASCII: the cell glyph is the word RED, em-dashes are hyphens; every context and '-' line asserted byte-exact at the tip at the line numbers below)

File: `Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh`
Tip: 8c2f7b3fd4fde915b2a24542bc32259b24e092a0
Runner: bash (the shell suite runner - `bash <file>` under /bin/bash 3.2; the checker runs the suite alone at the tip, then again after the script hunk)

## What is wrong (one paragraph)
`Start_Up/start-secuura.sh` ends every successful start with a Credentials block (:710–:712) that still prints
`    Admin:   admin@secuura.com / admin123` — a login that has returned 401 since PR #888 retired the published SYSTEM_ADMIN default
(KS-966). The banner hands every operator a credential that does not work, on the one screen they read. The ticket's own suggested
fix: print the MECHANISM instead of a value. **This task: line 712 becomes a pointer to where the admin is provisioned per run,
plus one new shell suite proving the banner no longer prints the retired credential while the issuer line and the script's syntax
are untouched.** NOT in this task: the admin login CHECK at :610–:620 (it also carries `admin123` — KS-966 item 3's sweep, a Claude
seat's), any other line.

## The exact change - 1 hunk(s) in `Start_Up/start-secuura.sh` (1 '-' line(s), 1 '+' line(s), one '+' group per hunk)
Copy the block below BYTE FOR BYTE as the first file of your diff: the two file-header lines, each `@@` header, every context line (a leading space, copied from `files[product_file]`), every `-` line and every `+` line, in this order. Do not add, drop, re-indent or reword a line; do not add a trailing comment; do not mark a context line as `+`. Every `+` line is ASCII - a double quote or a backslash on a `+` line is copied as written, never escaped.
```
--- a/Start_Up/start-secuura.sh
+++ b/Start_Up/start-secuura.sh
@@ -709,7 +709,7 @@
 echo ""
 echo -e "  ${BOLD}Credentials:${NC}"
 echo -e "    Issuer:  demo@secuura.io / demo123"
-echo -e "    Admin:   admin@secuura.com / admin123"
+echo -e "    Admin:   provisioned per run - see systemTest/fixtures/provision-actors.ts (KS-966: no shared admin credential is published)"
 echo ""
 # KS-666: state, on screen, who now holds this stack — so the next person does
 # not have to run a destructive command to discover it is occupied.
```

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:712` - **must change**: `echo -e "    Admin:   admin@secuura.com / admin123"`
* `:709` - (correct) `echo ""` - stays
* `:710` - (correct) `echo -e "  ${BOLD}Credentials:${NC}"` - stays

## The test - CREATE THE NEW FILE `Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh`

File: `Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh`

bash 3.2. It lives under `Blockchain/Dev/scripts/__tests__/` beside the reference `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` (full content in `files[...]`) and locates the subject from `${BASH_SOURCE[0]}` exactly as the block below does. It creates nothing outside `mktemp -d` and never edits the repo's real files.

**Reproduce the file below EXACTLY as written - every line, in order (78 lines).** Do not invent a helper, do not rename a variable, do not reword a message, do not add or drop a cell. Every value a cell reads is assigned above the first cell. **Your diff for this file is a NEW-FILE diff: `--- /dev/null`, `+++ b/Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh`, ONE hunk header `@@ -0,0 +1,78 @@`, then EVERY line with a leading `+` (a blank line is a lone `+`) - no context lines, no `-` lines: you are not diffing the reference.**

```
#!/usr/bin/env bash
# =============================================================================
# TESTS for Start_Up/start-secuura.sh Credentials banner (KS-972)
# =============================================================================
# The defect: line 712 still prints `Admin: admin@secuura.com / admin123` - a
# login retired by PR #888. Every operator reads it as valid; every attempt to
# use it returns 401. This task replaces the value with a pointer to where the
# admin is actually provisioned per run and adds one shell suite proving the
# change took effect without touching any other line.
#
# Usage: bash Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh
# =============================================================================
set -uo pipefail
TOTAL_CELLS=4

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
SUBJ="${START_SECUURA_SH-$REPO_ROOT/Start_Up/start-secuura.sh}"
[ -f "$SUBJ" ] || { echo "FATAL: start-secuura.sh not found at $SUBJ" >&2; exit 2; }
[ -r "$SUBJ" ] || { echo "FATAL: START_SECUURA_SH is not readable at $SUBJ" >&2; exit 2; }
printf 'SUBJECT %s\n        sha256 %s\n\n' "$SUBJ" "$(shasum -a 256 "$SUBJ" | cut -d" " -f1)"

pass=0; fail=0
ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
bad() { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }

# ---------------------------------------------------------------------------
# CELL 1 - RED. Untouched script has exactly one hit of the retired credential
# in its own source. After the fix there must be zero hits.
# ---------------------------------------------------------------------------
banner_hits="$(grep -c 'Admin:.*admin123' "$SUBJ" || true)"
if [ "$banner_hits" = 0 ]; then
  ok "the Credentials banner no longer prints the retired admin credential ($banner_hits hits)"
else
  bad "the Credentials banner no longer prints the retired admin credential" \
      "found $banner_hits hit(s) of 'Admin:.*admin123' in $SUBJ"
fi

# ---------------------------------------------------------------------------
# CELL 2 - RED. The new mechanism-pointer text must appear exactly once.
# ---------------------------------------------------------------------------
mech_hits="$(grep -c 'Admin:.*provision-actors.ts' "$SUBJ" || true)"
if [ "$mech_hits" = 1 ]; then
  ok "the banner names the provisioning mechanism instead of a value ($mech_hits hit)"
else
  bad "the banner names the provisioning mechanism instead of a value" \
      "expected 1 hit, got $mech_hits"
fi

# ---------------------------------------------------------------------------
# CELL 3 - CONTROL (green on both trees). Issuer line untouched.
# ---------------------------------------------------------------------------
issuer_hits="$(grep -c 'Issuer:  demo@secuura.io / demo123' "$SUBJ" || true)"
if [ "$issuer_hits" = 1 ]; then
  ok "CONTROL - issuer line untouched (demo@secuura.io still authenticates)"
else
  bad "CONTROL - issuer line untouched" \
      "expected 1 hit, got $issuer_hits"
fi

# ---------------------------------------------------------------------------
# CELL 4 - CONTROL (green on both trees). Script parses under bash -n.
# ---------------------------------------------------------------------------
if bash -n "$SUBJ" >/dev/null 2>&1; then
  ok "start-secuura.sh parses (bash -n)"
else
  bad "start-secuura.sh parses (bash -n)" \
      "$(bash -n "$SUBJ" 2>&1 | head -5 | tr '\n' ' ')"
fi

printf '\n  %d passed, %d failed (of %d cells)\n' "$pass" "$fail" "$TOTAL_CELLS"
# A cell that never ran is not a pass: the ratio must add up.
if [ "$((pass + fail))" -ne "$TOTAL_CELLS" ]; then
  printf '  INCOMPLETE - %d of %d cells ran\n' "$((pass + fail))" "$TOTAL_CELLS"
  exit 1
fi
[ "$fail" -eq 0 ] || exit 1
exit 0
```

Cells, in file order (a RED cell FAILS at the untouched tip by assertion and PASSES after the script hunk; a CONTROL cell passes on both trees):
- `# CELL 1 - RED. Untouched script has exactly one hit of the retired credential`
- `ok "the Credentials banner no longer prints the retired admin credential ($banner_hits hits)"`
- `# CELL 2 - RED. The new mechanism-pointer text must appear exactly once.`
- `ok "the banner names the provisioning mechanism instead of a value ($mech_hits hit)"`
- `# CELL 3 - CONTROL (green on both trees). Issuer line untouched.`
- `ok "CONTROL - issuer line untouched (demo@secuura.io still authenticates)"`
- `# CELL 4 - CONTROL (green on both trees). Script parses under bash -n.`
- `ok "start-secuura.sh parses (bash -n)"`

## Output
Exactly ONE ```diff block with TWO files: `--- a/Start_Up/start-secuura.sh` / `+++ b/Start_Up/start-secuura.sh` (1 hunk(s), copied from `## The exact change`), then `--- /dev/null` / `+++ b/Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh` (one hunk, `@@ -0,0 +1,78 @@`, every line a `+`). No prose before or after the block.

## Premises (measured at develop 8c2f7b3fd4fde915b2a24542bc32259b24e092a0 by the feed8 drafter, scratchpad `--shared --no-checkout` clone, 2026-09-22 09:47:00 AEST)
- `Start_Up/start-secuura.sh` at the tip carries every context and `-` line of the hunk(s) above BYTE FOR BYTE at the line numbers in `## Where` (asserted by rebrief.py against `git show 8c2f7b3fd:Start_Up/start-secuura.sh`); the rebuilt product section applies STRICT (`git apply --check -p1` rc 0 in the clone).
- The new suite `Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh` is ABSENT at the tip (`git cat-file -e` rc 1). The reference suite `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` is present.
- Every `+` line of the product hunk(s) and every line of the suite is ASCII (non-ASCII 0, asserted); the FEED 8 ruling (Wednesday, 2026-09-22 09:3x) WAIVES the `"` 0 / `\` 0 rule for bash_patch - the guard is the checker's B3b (every brief `+` line present in the script hunk, whitespace-stripped) and B4/B5 (RED at the tip, GREEN after).
- Golden precheck through the real `tasks/bash_patch/checker.sh` in the clone: see `runs/2026-09-22_feed8-drafter-precheck/BANNER/checker.log` (the verdict is quoted on the queue line, never here by hand).
- Ticket KS-972 on the Secuura board at 2026-09-22 09:47:00 AEST: Backlog, not archived (`board_states.log`). The product file is on neither 18th seat's GROUPING list (Seat B: shared/anchoring/auth/originate; Seat C: api-gateway).
