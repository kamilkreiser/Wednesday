# mutants.py — "break the thing, see red". (Round 4: the grants filter's mutants went with the filter;
# in their place, mutants that drop, cut, move or reword a register row, and one per new lock guard.)
# Each entry breaks ONE behaviour in a scratch copy of the tools and names
# the check(s) that must then fail. run_tests.py --mutants applies each, runs the named group, and requires the red.
# (name, [(file relative to the lane, needle that must occur exactly once, replacement)], group, [check ids])
# The entries marked Q.. are the checker's mutants that round 2's suite missed (verdict.md, m8).

M = []


def add(name, edits, group, must):
    M.append((name, edits, group, must))


HC, HS, WP = "handover_core.py", "handover.sh", "wake_pack.py"
HA, HB = "proposed/launcher_hunk_A.sh", "proposed/launcher_hunk_B.sh"
DOC = "proposed/doctor_check_snippet.sh"

# ── handover: refusals ──────────────────────────────────────────────────────────────────────────
add("cap check off", [(HC, "    if len(block) > cap:", "    if False:")], "H", ["H05"])
add("empty check off", [(HC, '    if not block.strip():\n        return ["the block is empty."], {}, ""', '    if False:\n        return [], {}, ""')], "H", ["H06"])
add("x-clock check off", [(HC, '    if not clocks:\n        return "", ""', '    if True:\n        return "", ""')], "H", ["H07", "H07g"])
add("x-clock override accepted with any reason", [(HC, "    if len(reason) >= XCLOCK_MIN_REASON:", "    if reason:")], "H", ["H07d"])
add("x-clock override never accepted", [(HC, "    if len(reason) >= XCLOCK_MIN_REASON:", "    if False:")], "H", ["H07c"])
add("override reason not carried into the archive heading", [(HC, '(" | x-clock override: " + over) if over else "")', '"")')], "H", ["H07e"])
add("override recorded although the block has no x-clock", [(HC, '    if not clocks:\n        return "", ""', '    if not clocks:\n        return "", (reason or "")')], "H", ["H07f"])
add("missing-part check off", [(HC, "        if n == 0:", "        if False:")], "H", ["H08"])
add("repeated-part check off", [(HC, "        elif n > 1:", "        elif False:")], "H", ["H09"])
add("foreign-heading check off", [(HC, '        if p == "?":', "        if False:")], "H", ["H10"])
add("only '## ' headings are looked at (### / indented / # pass)", [(HC, 'HEADING = re.compile(r"^[\\s%s]*#{1,6}(?:[\\s%s]|$)" % (ZW, ZW))', 'HEADING = re.compile(r"^##(?:[ ]|$)")')], "H", ["H10b", "H10c", "H10d", "H10e", "H10f"])
add("a part name may be followed by anything (look-alike part)", [(HC, '        if plain == "## " + p:', '        if plain.startswith("## " + p):')], "H", ["H10g"])
add("empty-part check off", [(HC, "        elif not body.get(p):", "        elif False:")], "H", ["H11"])
add("--dry writes", [(HC, "    if a.dry:  # a dry run reads and prints; it takes no lock and writes nothing", "    if False:"),
                     (HC, '    if a.dry:\n        print("\\n".join(plan))', '    if False:\n        print("\\n".join(plan))')], "H", ["H12"])
add("write accepted without --stdin", [(HS, 'if [ "$CMD" = "write" ] && [ "$STDIN" != 1 ]; then', "if false; then")], "H", ["H13"])
add("seat hardcoded instead of resolved", [(HS, 'seat_note_dir "$TREE" handover || exit 2', "SEAT_NOTE_SEAT=wednesday")], "H", ["H14", "H14c"])

# ── handover: conservation, one block, hand edits ───────────────────────────────────────────────
add("conservation assert off", [(HC, "        fault = assert_conserved(new_arch, prev_arch, old_body, prefix_len, entry_head, sep)", '        fault = ""')], "H", ["H15"])
add("archive never renamed into place", [(HC, '            guarded_replace(tmps[0][0], arch_path, "archive")', "            pass")], "H", ["H03b"])
add("write stacks the old block under the new", [(HC, "arch_name, used) + block\n", "arch_name, used) + block + old_body\n")], "H", ["H03"])
add("check ignores hand edits", [(HC, '        if fields.get("block_sha256") != sha(body):', "        if False:"),
                                 (HC, '        if fields.get("block_bytes") != str(len(body)):', "        if False:")], "H", ["H17"])
add("Q05 trailing newline no longer ensured on the block", [(HC, '    if block.strip() and not block.endswith(b"\\n"):\n        block += b"\\n"\n', "")], "H", ["H22"])
add("Q15 check ignores a header naming another seat", [(HC, '        if fields.get("seat") != seat:', "        if False:")], "H", ["H23"])
add("Q17 an unreadable state file is treated as absent", [(HC, "    except OSError as e:\n        raise ReadFault(path, e)", "    except OSError as e:\n        return None")], "H", ["H24"])
add("test seams honoured for any tree (handover.sh)", [(HS, '] && ! tree_is_temp "$TREE"; then', '] && false; then')], "H", ["H25"])
add("engine accepts any seat for any tree", [(HC, "    if os.path.basename(tree).lower() != a.seat or ", "    if False and os.path.basename(tree).lower() != a.seat or ")], "H", ["H25c"])
add("engine honours HANDOVER_TEST_BREAK for any tree", [(HC, '    if os.environ.get("HANDOVER_TEST_BREAK") and not under_temp(a.tasks_dir):', "    if False:")], "H", ["H25d"])
add("the lock is never released", [(HC, '        os.remove(os.path.join(lock, "owner"))\n        os.rmdir(lock)', "        pass")], "H", ["H03"])

# ── handover: the lock, races, a death part-way (group R) ───────────────────────────────────────
add("B1: no mutual exclusion (the lock path is different for every process)",
    [(HC, '    return os.path.join(tasks_dir, "STATE-%s.lock.d" % seat)', '    return os.path.join(tasks_dir, "STATE-%s.lock.d.%d" % (seat, os.getpid()))')], "R", ["R01", "R02"])
add("a second writer proceeds after the wait instead of refusing",
    [(HC, "        if time.monotonic() >= deadline:\n            o = lock_owner(lock)", '        if time.monotonic() >= deadline:\n            return "0-mutant"\n            o = lock_owner(lock)')], "R", ["R02", "R04"])
add("a stale lock is removed silently",
    [(HC, "            if stale_look(lock, host) == seen:\n", '            if stale_look(lock, host) == seen:\n                os.remove(os.path.join(lock, "owner"))\n                os.rmdir(lock)\n                continue\n')], "R", ["R03", "R05b"])
add("a stale lock is waited on instead of reported", [(HC, "        if seen is not None:", "        if False:")], "R", ["R03", "R15"])
add("N2a: STALE is reported on the FIRST look (no second look)", [(HC, "            if stale_look(lock, host) == seen:", "            if True:")], "R", ["R09"])
add("N2b: the temp files live in the tasks directory again (a displaced writer can rename them into place)",
    [(HC, '            t = os.path.join(lock, "archive.tmp." + token)', '            t = arch_path + ".tmp." + token'),
     (HC, '        t2 = os.path.join(lock, "state.tmp." + token)', '        t2 = state_path + ".tmp." + token')], "R", ["R10", "R11"])
add("N2b: the owner file is not re-read before a rename",
    [(HC, '        if not holds(lock, token):\n            raise LockLost("before the %s rename', '        if False:\n            raise LockLost("before the %s rename')], "R", ["R12"])
add("N2c: a writer whose lock is gone at release still says written and exits 0", [(HC, "    if rc == 0 and not released:", "    if False:")], "R", ["R13"])
add("Y01 release removes a lock that is not this call's", [(HC, '        if not token or o.get("token") != token:', "        if False:")], "R", ["R12", "R14"])
add("a writer stopped by LOCK LOST leaves its temp files inside a lock directory another writer owns",
    [(HC, "        left = set_aside()\n        if left:\n            eprint(\"  this call's temp file(s) were moved out", "        left = []\n        if left:\n            eprint(\"  this call's temp file(s) were moved out")], "R", ["R12"])
add("N3: an owner-less lock is never stale, however old", [(HC, "    if time.time() - st.st_mtime > OWNERLESS_STALE_SECONDS:", "    if False:")], "R", ["R15"])
add("N3: an owner-less lock is stale at any age (a fresh one too)", [(HC, "    if time.time() - st.st_mtime > OWNERLESS_STALE_SECONDS:", "    if True:")], "R", ["R04"])
add("N4: a number beyond a C int is taken as a pid (traceback)", [(HC, "    return n if 0 < n <= PID_MAX else None", "    return n")], "R", ["R16"])
add("Y02 STALE is declared for a dead pid on ANY host", [(HC, '        if o.get("host") == host and not pid_alive(pid):', "        if not pid_alive(pid):")], "R", ["R03c"])
add("Q01 rename order swapped: state first, archive second",
    [(HC, '        if new_arch is not None:\n            guarded_replace(tmps[0][0], arch_path, "archive")\n        guarded_replace(t2, state_path, "state")\n',
      '        guarded_replace(t2, state_path, "state")\n        if new_arch is not None:\n            guarded_replace(tmps[0][0], arch_path, "archive")\n')], "R", ["R05"])
add("Q02 changed-on-disk check removed", [(HC, "        if read_bytes(state_path) != cur or read_bytes(arch_path) != prev_arch:", "        if False:")], "R", ["R06"])
add("Q03 temp-file read-back checks removed", [(HC, "            if read_bytes(t) != new_arch:", "            if False:"),
                                              (HC, "        if read_bytes(t2) != new_state:", "        if False:")], "R", ["R07"])

# ── handover: seed ──────────────────────────────────────────────────────────────────────────────
add("seed ignores an existing state file",
    [(HC, '    if os.path.lexists(state_path):\n        eprint("handover: REFUSED — a state file already exists', '    if False:\n        eprint("handover: REFUSED — a state file already exists'),
     (HC, "    if must_be_first and cur is not None:", "    if False:")], "S", ["S03"])
add("seed writes without --run", [(HC, "    if not a.run:\n        sys.stdout.buffer.write(block)", "    if False:\n        sys.stdout.buffer.write(block)"),
                                  (HC, '    if a.cmd == "seed" and not a.run:\n        return cmd_seed(a, state_path, arch_path)',
                                   '    if a.cmd == "seed" and not a.run:\n        a.stamp = "MUTANT"\n        a.run = True\n        return cmd_seed(a, state_path, arch_path)')], "S", ["S01"])
add("seed maps OWED bullets to the wrong part", [(HC, '    if "OWED" in u:\n        return "OWED"', '    if "OWED" in u:\n        return "FLOOR"')], "S", ["S01b"])
add("seed drops what it cannot map", [(HC, '        elif l.startswith("- "):\n            cur = "FIRST WORK"\n            unmapped += 1\n', '        elif l.startswith("- "):\n            unmapped += 1\n            continue\n')], "S", ["S01c", "S06"])
add("seed takes the whole legacy file, not its newest block", [(HC, "    end = idx[1] if len(idx) > 1 else len(lines)\n    body = lines[idx[0] + 1:end]", "    end = len(lines)\n    body = lines[idx[0] + 1:end]")], "S", ["S06"])
add("seed uses another seat's legacy file", [(HC, '"tuesday": "NEXT-PICKUP-TUESDAY.md"', '"tuesday": "NEXT-PICKUP.md"')], "S", ["S07"])
add("M5: seed leaves the standing sections' lines behind", [(HC, "        parts[tgt].extend(sect)", "        pass")], "S", ["S09"])
add("M5: seed carries a dated block because its heading mentions OWED", [(HC, 'kind = "OWED" if h.upper().startswith("OWED") else', 'kind = "OWED" if "OWED" in h.upper() else')], "S", ["S09b"])
add("M5: seed --run writes an over-cap block's refusal without the list", [(HC, "        by_hand()\n        return 3", "        return 3")], "S", ["S10"])

# ── wake pack: the register is carried WHOLE (round 4). A mutant that drops, cuts or moves any row must go red. ──
add("glob exclusion off", [(WP, 'SKIP = ("(conflict_on_", ".pre-")', "SKIP = ()")], "W", ["W10"])
GW = '          [sec(rel, b.size(rel), head + text + tail, label=rel + " (whole, verbatim)")])'


def carried(expr):
    return [(WP, GW, GW.replace("head + text + tail", "head + %s + tail" % expr))]


add("whole register: rows marked DEAD are dropped again", carried(r'"\n".join(x for x in text.split("\n") if not x.startswith("| **DEAD"))'), "W", ["W05", "W05b"])
add("whole register: ONE row is dropped (a struck-through one)", carried(r'"\n".join(x for x in text.split("\n") if not x.startswith("| ~~**FRIDAY"))'), "W", ["W05"])
add("whole register: another seat's rows are dropped again", carried(r'"\n".join(x for x in text.split("\n") if not x.startswith("| **TUESDAY:") or b.seat == "tuesday")'), "W", ["W05", "W05h"])
add("whole register: everything under the Expired heading is cut off", carried('text.split("## Expired")[0]'), "W", ["W05", "W05b"])
add("whole register: only the first table is carried", carried('text.split("\\n\\n## ")[0] + "\\n"'), "W", ["W05"])
add("whole register: cut to fit (the last 300 bytes trimmed)", carried("text[:-300]"), "W", ["W05", "W05b"])
add("whole register: the rows are carried sorted, not in file order", carried(r'"\n".join(sorted(text.split("\n")))'), "W", ["W05", "W05b"])
add("whole register: a row's text is reworded (emphasis stripped)", carried('text.replace("**", "")'), "W", ["W05"])
add("whole register: only table rows are carried (the file's headings and prose dropped)", carried(r'"\n".join(x for x in text.split("\n") if x.startswith("|")) + "\n"'), "W", ["W05b"])
add("whole register: a file that is not valid UTF-8 is carried with replacement characters", [(WP, '    if text.encode("utf-8") != raw:', "    if False:")], "W", ["W18p"])
add("whole register: the intro's sha256 is of something else", [(WP, "hashlib.sha256(raw).hexdigest()[:16], rel))", 'hashlib.sha256(b"").hexdigest()[:16], rel))')], "W", ["W05c"])

# ── wake pack: parts, budget, sidecar, check, failed builds ─────────────────────────────────────
add("budget check off", [(WP, "    over = tok(total) > a.budget_tokens", "    over = False")], "W", ["W09", "W09b"])
add("identity truncated", [(WP, '"### %s (verbatim)\\n\\n%s" % (rel, text)', '"### %s (verbatim)\\n\\n%s" % (rel, text[:20])')], "W", ["W02"])
add("family lines leak into the pack", [(WP, '            top_text = "\\n".join(body).rstrip("\\n") + "\\n"', "            top_text = card")], "W", ["W03"])
add("whole legacy pickup instead of its first block", [(WP, "    end = idx[1] if len(idx) > 1 else len(lines)", "    end = len(lines)")], "W", ["W04"])
add("ledger rows not reduced", [(WP, '    return "- %s | **%s** | %s" % (date, headline, rule)', "    return line")], "W", ["W07"])
add("a second file is written beside the pack again", [(WP, "        os.replace(tmp, out)\n", '        os.replace(tmp, out)\n        open(out[:-3] + ".dropped.txt", "w").close()\n')], "W", ["W05d"])
add("--check ignores newer sources", [(WP, "                if os.stat(src).st_mtime_ns > pm:", "                if False:")], "W", ["W11b"])
add("--check ignores the pack's content (m1)", [(WP, "                if sha(have) != sha(want):", "                if False:")], "W", ["W11d", "W11h"])
add("--check skips every line that starts 'generated: ' (round 2's hole, m1)",
    [(WP, "                want = make(stamp)[0]\n                if sha(have) != sha(want):",
      '                want = make(stamp)[0]\n                if sha("\\n".join(x for x in have.split("\\n") if not x.startswith("generated: "))) != sha("\\n".join(x for x in want.split("\\n") if not x.startswith("generated: "))):')], "W", ["W11h"])
add("N5: --check does not look at the stamp line's format", [(WP, "            elif not STAMP.fullmatch(stamp):", "            elif False:")], "W", ["W11k"])
add("N6 / Y09: the pack carries a STATE file that `handover.sh check` refuses",
    [(WP, '        if faults:\n            raise BuildFail(part, "%s is not one clean', '        if False:\n            raise BuildFail(part, "%s is not one clean')], "W", ["W20a", "W20b", "W20c", "W20d", "W20e"])
add("N6: check_faults forgets the header's seat (the pack and `check` share the function)", [(HC, '        if fields.get("seat") != seat:', "        if False:")], "W", ["W20b"])
add("N6: a state file is carried unchecked when the engine cannot be loaded",
    [(WP, "        mod.check_faults\n        return mod\n    except Exception as e:", "        mod.check_faults\n        return mod\n    except ZeroDivisionError as e:")], "W", ["W20f"])
add("N13: a pack path that is a directory leaves a temp file behind", [(WP, "    if os.path.isdir(out):", "    if False:")], "W", ["W21"])
add("--check ignores the build date", [(WP, "            if not m or m.group(1) != today.isoformat():", "            if False:")], "W", ["W11e"])
add("M2: an empty source is accepted", [(WP, "        if not data.strip() and not allow_empty:", "        if False:")], "W", ["W18l"])
add("M2: a rules card without 'Most reinforced' builds with a placeholder", [(WP, "    if top_text is None:\n        raise BuildFail(", '    if top_text is None:\n        top_text = "(none)\\n"\n    if False:\n        raise BuildFail(')], "W", ["W18c"])
add("M2: a grants file without its table header is carried anyway", [(WP, "    if not any(GRANTS_HEADER.match(l) for l in lines):", "    if False:")], "W", ["W18h"])
add("M2: a ledger without its table header is read anyway", [(WP, '    if not any(LEDGER_HEADER.match(l) for l in text.split("\\n")):', "    if False:")], "W", ["W18k"])
add("M2: no state and no pickup builds with a placeholder", [(WP, "    if pick is None:\n        raise BuildFail(", '    if pick is None:\n        pick = "## none\\n"\n    if False:\n        raise BuildFail(')], "W", ["W18m"])
add("m3: an unreadable source is a traceback, not a refusal", [(WP, '        except OSError as e:\n            raise BuildFail(part, "source unreadable', '        except ZeroDivisionError as e:\n            raise BuildFail(part, "source unreadable')], "W", ["W18o"])
add("over budget prints no final FAILED line", [(WP, '        eprint("wake_pack: FAILED — over budget:', '        (lambda *x: None)("wake_pack: FAILED — over budget:')], "W", ["W09"])

# ── census ──────────────────────────────────────────────────────────────────────────────────────
add("census drops a file from the total", [("wake_census.sh", "  TOTAL=$((TOTAL + n))", "  TOTAL=$((TOTAL + 0))")], "C", ["C01"])
add("census does not take the conflict copies out of the second total", [("wake_census.sh", "CLEAN=$((TOTAL - ENT_CB))", "CLEAN=$TOTAL")], "C", ["C07"])

# ── launcher proposal ───────────────────────────────────────────────────────────────────────────
add("launcher change not confined to wednesday", [(HA, 'if [ "$AGENT" = "wednesday" ]; then', "if true; then"),
                                                  (HB, 'if [ "$AGENT" = "wednesday" ]; then', "if true; then")], "P", ["P01", "P02"])
add("launcher slice marker reworded", [(HB, 'WAKE_M1="FIRST ACTIONS (token cost is accepted"', 'WAKE_M1="NO SUCH MARKER"')], "P", ["P03"])
add("notes-on-demand branch slices at the wrong marker", [(HB, '    WAKE_M2="${WAKE_NL}6. If DevMASTER is mounted: "', '    WAKE_M2="${WAKE_NL}6. NO SUCH STEP"')], "P", ["P12"])
add("hunk A ignores the build's exit code", [(HA, '    if [ "$WAKE_RC" -eq 0 ] && [ -s "$WAKE_PACK" ]; then', "    if true; then")], "P", ["P04"])
add("m2: hunk A trusts exit 0 without looking for the pack file", [(HA, '    if [ "$WAKE_RC" -eq 0 ] && [ -s "$WAKE_PACK" ]; then', '    if [ "$WAKE_RC" -eq 0 ]; then')], "P", ["P16"])
add("Q14 hunk A ignores the exit code when a pack file is on disk (an OLDER pack is booted on)", [(HA, '    if [ "$WAKE_RC" -eq 0 ] && [ -s "$WAKE_PACK" ]; then', '    if [ -s "$WAKE_PACK" ]; then')], "P", ["P21"])
add("Y11 hunk A accepts an EMPTY pack file (-e, not -s)", [(HA, '    if [ "$WAKE_RC" -eq 0 ] && [ -s "$WAKE_PACK" ]; then', '    if [ "$WAKE_RC" -eq 0 ] && [ -e "$WAKE_PACK" ]; then')], "P", ["P22"])
add("M3: the fallback is silent in the prompt", [(HB, ' if [ "${WAKE_PACK_OK:-0}" != "1" ]; then', " if false; then")], "P", ["P04", "P04b", "P04c", "P16", "P17"])
add("M3: the notice is appended at the END of the prompt, not its first lines",
    [(HB, '    "ultrathink${WAKE_NL}${WAKE_NL}"*) INITIAL_PROMPT="ultrathink${WAKE_NL}${WAKE_NL}${WAKE_NOTICE}${WAKE_NL}${INITIAL_PROMPT#"ultrathink${WAKE_NL}${WAKE_NL}"}" ;;',
      '    "ultrathink${WAKE_NL}${WAKE_NL}"*) INITIAL_PROMPT="${INITIAL_PROMPT}${WAKE_NL}${WAKE_NOTICE}" ;;')], "P", ["P04"])
add("M3: the notice gives no reason", [(HB, "Why: ${WAKE_FAIL:-no reason was recorded}", "Why: see the terminal")], "P", ["P04", "P04c"])
add("a text proposal quotes text that is not in its target", [("proposed/08_nas_staleness.md", "$SEAT_DIR/0_Brain/tasks/NEXT-PICKUP.md", "$SEAT_DIR/0_Brain/tasks/NEXT-PICKUPS.md")], "P", ["P10"])
add("M4: a proposal's new text is worded for every seat", [("proposed/03_brain_CLAUDE_md.md", "**On a seat that boots on a wake pack**", "**On every seat**")], "P", ["P18"])
add("M4: proposal 2 deletes Kam's lesson-load sentence again",
    [("proposed/02_root_CLAUDE_md.md", "1. Read this file → `0_Brain/CLAUDE.md` → `0_Brain/identity/persona.md` +\n```\n\n```new",
      "1. Read this file → `0_Brain/CLAUDE.md` → `0_Brain/identity/persona.md` +\n   `voice-protocol.md` → `0_Brain/people/kam.md`.\n2. Read ALL of `0_Brain/learnings/` (token cost is explicitly accepted — Kam wants\n```\n\n```new")], "P", ["P18"])
add("m6: the gitignore proposal ignores the whole out/ directory again", [("proposed/05_gitignore.md", "2_Project_Files/wake/out/WAKE-*\n", "2_Project_Files/wake/out/\n")], "P", ["P19"])
add("proposal 9 loses its all-seats marking", [("proposed/09_prompt_backtick.md", "**ALL SEATS: needs Tuesday's and Friday's agreement.**", "Wednesday decides.")], "P", ["P20"])
add("N3: the gitignore lock pattern no longer covers a set-aside lock directory", [("proposed/05_gitignore.md", "0_Brain/tasks/STATE-*.lock.d*\n", "0_Brain/tasks/STATE-*.lock.d/\n")], "P", ["P19"])
add("N9: proposal 2 again reads the pack in place of Kam's lesson-load step", [("proposed/02_root_CLAUDE_md.md", "whole in place of steps 1 and 3 below; for step 2 see the question put to Kam", "whole in place of steps 1 to 3 below; see also the question put to Kam")], "P", ["P23"])
add("N3: proposal 6 again says a refused write is simply run again", [("proposed/06_wrap_step.md", "waits, then refuses (rc 5) and says which of two things it met. **LOCK BUSY**: a\n   write is running; run the command again. **STALE LOCK**: a write died and left", "waits, then refuses (rc 5) and is simply run again. Or a write died and left")], "P", ["P24"])
add("N10: the stuart_weekly proposal quotes lines that are not in the script", [("proposed/10_stuart_weekly.md", "n>1{exit}' \"$PROJECT_DIR/0_Brain/tasks/NEXT-PICKUP.md\" | head -60", "n>1{exit}' \"$PROJECT_DIR/0_Brain/tasks/NEXT-PICKUP.md\" | head -50")], "P", ["P10"])

# ── doctor proposal ─────────────────────────────────────────────────────────────────────────────
add("doctor snippet ignores a stale pack", [(DOC, 'if [ "$WP_RC" -eq 0 ]; then', "if true; then")], "D", ["D03"])
add("doctor snippet ignores a stacked handover", [(DOC, 'if [ "$HO_RC" -eq 0 ]; then', "if true; then")], "D", ["D04"])
add("doctor snippet takes the seat from a default, not the tree", [(DOC, "  WK_SEAT=\"$(printf '%s\\n' \"$WK_OUT\" | sed -n 's/^seat: *//p')\"", '  WK_SEAT="wednesday"')], "D", ["D05"])
add("M3: doctor is silent when a cut-over seat has no pack", [(DOC, '    elif [ -f "$WK_STATE" ]; then', "    elif false; then")], "D", ["D06"])
add("m7: doctor discards handover.sh's stderr", [(DOC, '  WK_OUT="$(bash "$HO" --where 2>&1)"; WK_RC=$?', '  WK_OUT="$(bash "$HO" --where 2>/dev/null)"; WK_RC=$?')], "D", ["D07"])
add("N3: doctor says nothing about a standing lock directory", [(DOC, '    [ -e "$WK_LOCK" ] || [ -L "$WK_LOCK" ] || continue', "    continue")], "D", ["D08"])
add("N3: doctor's lock warning gives no recovery line", [(DOC, "mv -n '$WK_LOCK' '$WK_LOCK.stale-$(date +%Y%m%d-%H%M%S)'", "ask Kam")], "D", ["D08"])
