# mutants.py — "break the thing, see red". Each entry breaks ONE behaviour in a scratch copy of the tools and names
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
add("seat hardcoded instead of resolved", [(HS, 'seat_note_dir "$TREE" handover || exit 2', "SEAT_NOTE_SEAT=wednesday")], "H", ["H14", "H14b", "H14c"])

# ── handover: conservation, one block, hand edits ───────────────────────────────────────────────
add("conservation assert off", [(HC, "        fault = assert_conserved(new_arch, prev_arch, old_body, prefix_len, entry_head, sep)", '        fault = ""')], "H", ["H15"])
add("archive never renamed into place", [(HC, "            os.replace(tmps[0], arch_path)", "            pass")], "H", ["H03b"])
add("write stacks the old block under the new", [(HC, "arch_name, used) + block\n", "arch_name, used) + block + old_body\n")], "H", ["H03"])
add("check ignores hand edits", [(HC, '        if fields.get("block_sha256") != sha(body):', "        if False:"),
                                 (HC, '        if fields.get("block_bytes") != str(len(body)):', "        if False:")], "H", ["H17"])
add("Q05 trailing newline no longer ensured on the block", [(HC, '    if block.strip() and not block.endswith(b"\\n"):\n        block += b"\\n"\n', "")], "H", ["H22"])
add("Q15 check ignores a header naming another seat", [(HC, '        if fields.get("seat") != a.seat:', "        if False:")], "H", ["H23"])
add("Q17 an unreadable state file is treated as absent", [(HC, "    except OSError as e:\n        raise ReadFault(path, e)", "    except OSError as e:\n        return None")], "H", ["H24"])
add("test seams honoured for any tree (handover.sh)", [(HS, '] && ! tree_is_temp "$TREE"; then', '] && false; then')], "H", ["H25"])
add("engine accepts any seat for any tree", [(HC, "    if os.path.basename(tree).lower() != a.seat or ", "    if False and os.path.basename(tree).lower() != a.seat or ")], "H", ["H25c"])
add("engine honours HANDOVER_TEST_BREAK for any tree", [(HC, '    if os.environ.get("HANDOVER_TEST_BREAK") and not under_temp(a.tasks_dir):', "    if False:")], "H", ["H25d"])
add("the lock is never released", [(HC, '        os.remove(os.path.join(lock, "owner"))\n        os.rmdir(lock)', "        pass")], "H", ["H03"])

# ── handover: the lock, races, a death part-way (group R) ───────────────────────────────────────
add("B1: the lock is removed (acquire returns at once)", [(HC, "    deadline = time.monotonic() + lock_wait()\n", "    return\n    deadline = time.monotonic() + lock_wait()\n")], "R", ["R01", "R02"])
add("a second writer proceeds UNLOCKED after the wait", [(HC, "            if time.monotonic() >= deadline:\n                raise LockBusy(", "            if time.monotonic() >= deadline:\n                return (")], "R", ["R02", "R04"])
add("a stale lock is removed silently", [(HC, '            if pid is not None and o.get("host") == host and not pid_alive(pid):\n',
                                         '            if pid is not None and o.get("host") == host and not pid_alive(pid):\n                os.remove(os.path.join(lock, "owner"))\n                os.rmdir(lock)\n                continue\n')], "R", ["R03", "R05b"])
add("a stale lock is waited on instead of reported", [(HC, '            if pid is not None and o.get("host") == host and not pid_alive(pid):', "            if False:")], "R", ["R03"])
add("Q01 rename order swapped: state first, archive second",
    [(HC, "        if new_arch is not None:\n            os.replace(tmps[0], arch_path)\n        os.replace(t2, state_path)\n",
      "        os.replace(t2, state_path)\n        if new_arch is not None:\n            os.replace(tmps[0], arch_path)\n")], "R", ["R05"])
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

# ── wake pack: the grants filter ────────────────────────────────────────────────────────────────
add("glob exclusion off", [(WP, 'SKIP = ("(conflict_on_", ".pre-")', "SKIP = ()")], "W", ["W10"])
add("dead-marker drop off", [(WP, "    if dm and not struck and not REVIVED.search(first):", "    if False:")], "W", ["W05b"])
add("dead marker anywhere in the row", [(WP, '    dm = DEAD_FORM.match(lead(first))\n    if dm and not struck and not REVIVED.search(first):\n        return "dead", "first cell starts with %s %s" % (dm.group(1), dm.group(2))',
                                         '    if any(x in line for x in DEAD_WORDS):\n        return "dead", "mutant"')], "W", ["W05"])
add("Q07 dead marker needs no date and no word boundary (CLOSED PRs, DEADLINE, CLOSED-LOOP dropped)",
    [(WP, "    dm = DEAD_FORM.match(lead(first))", '    dm = re.match(r"(DEAD|EXPIRED|ENDED|LAPSED|CLOSED|RETIRED)()", lead(first))')], "W", ["W05"])
add("a struck-through marker still counts", [(WP, "    if dm and not struck and not REVIVED.search(first):", "    if dm and not REVIVED.search(first):")], "W", ["W05"])
add("a marker followed by REOPENED / REVIVED still counts", [(WP, "    if dm and not struck and not REVIVED.search(first):", "    if dm and not struck:")], "W", ["W05"])
add("the three markers added in round 2 removed", [(WP, '"LAPSED", "CLOSED", "RETIRED", "END EVENT REACHED")', '"LAPSED")')], "W", ["W05b"])
add("PREMISE ENDED restored as a dead marker", [(WP, '"RETIRED", "END EVENT REACHED")', '"RETIRED", "END EVENT REACHED", "PREMISE ENDED")')], "W", ["W05"])
add("other-seat drop off", [(WP, "    if owners and seat not in owners:", "    if False:")], "W", ["W05b"])
add("other-seat drop ignores 'ALL SEATS' / fleet", [(WP, " and not names_seat(line, seat) and not ALL_SEATS.search(line)\n", " and not names_seat(line, seat)\n")], "W", ["W05"])
add("other-seat drop looks for this seat in the first cell only", [(WP, "not names_seat(line, seat) and", "not names_seat(first, seat) and")], "W", ["W05"])
add("other-seat drop ignores this seat's client", [(WP, '\n                and not any(re.search(r"\\b%s\\b" % re.escape(c), line, re.I) for c in clients)):', "):")], "W", ["W05"])
add("Q08 other-seat match needs no separator (TUESDAY 2026-.. kick-off dropped)",
    [(WP, '\\b\\s*(?::|\\(|\\u2014|\\u2013|-(?![\\w])|,)" % (SEAT_ALT, SEAT_ALT))', '\\b" % (SEAT_ALT, SEAT_ALT))')], "W", ["W05"])
add("a weekday stamp counts as naming the seat", [(WP, '    text = re.sub(WEEKDAY_IDIOM % (seat, seat), " ", row, flags=re.I)', "    text = row")], "W", ["W05b"])
add("the weekday-stamp exclusion swallows the text after it (a real seat name lost)", [(WP, "(?:`date[^`]*`:\\s*(?:%s)\\b)|", "(?:`date[^`]*`:\\s*(?:%s)\\b[^|]{0,12})|")], "W", ["W05"])
add("the seat's short name (WED) is not looked for", [(WP, "    return bool(short) and re.search(", "    return False and re.search(")], "W", ["W05"])
add("a ticket id (WED-170) counts as naming the seat", [(WP, '\\b(?!-\\d)(?!,?\\s+\\d)" % short', '\\b" % short')], "W", ["W05b"])
add("'NOT DEAD' after a dead marker is ignored", [(WP, "STILL LIVE|LIVE AGAIN|NOT DEAD|BACK ON", "STILL LIVE|LIVE AGAIN|BACK ON")], "W", ["W05"])
add("a seat serving every client still drops other seats' rows (line 26 for friday)", [(WP, '"friday": None}', '"friday": ("secuura", "datasec")}')], "W", ["W19"])
add("past-date drop off", [(WP, "            if (end is not None and end < today and", "            if (False and")], "W", ["W05b"])
add("past-date boundary wrong (today counts as past)", [(WP, "end is not None and end < today and", "end is not None and end <= today and")], "W", ["W15"])
add("a bare date at the start of EXPIRES counts as an end", [(WP, "        if em and (em.group(1) or em.group(2) or em.group(3)):", "        if em:")], "W", ["W05"])
add("more than one date in EXPIRES is allowed", [(WP, " and isos == set([em.group(4)]) and", " and")], "W", ["W05"])
add("a second date written in words is ignored", [(WP, " and not WORD_DATE.search(exp)\n", "\n")], "W", ["W05"])
add("EVENT in the row is ignored", [(WP, "                    and not EVENT.search(line) and", "                    and")], "W", ["W05"])
add("keep-alive words in the row are ignored", [(WP, " and not ROW_KEEPS.search(plain)):", "):")], "W", ["W05"])
add("the stock phrase 'not renewed' keeps a past row alive", [(WP, '            plain = NEGATED.sub(" ", line)', "            plain = line")], "W", ["W05b"])
add("four-cell guard removed", [(WP, "    if len(cells) == 4:", "    if len(cells) >= 4:")], "W", ["W05"])
add("expired-heading flag ignored", [(WP, "            if b.trust_expired:\n", "            if False:\n")], "W", ["W06"])

# ── wake pack: parts, budget, sidecar, check, failed builds ─────────────────────────────────────
add("budget check off", [(WP, "    over = tok(total) > a.budget_tokens", "    over = False")], "W", ["W09", "W09b"])
add("identity truncated", [(WP, '"### %s (verbatim)\\n\\n%s" % (rel, text)', '"### %s (verbatim)\\n\\n%s" % (rel, text[:20])')], "W", ["W02"])
add("family lines leak into the pack", [(WP, '        if top_text is None and name.lower().startswith("most reinforced"):', "        if top_text is None:")], "W", ["W03"])
add("whole legacy pickup instead of its first block", [(WP, "    end = idx[1] if len(idx) > 1 else len(lines)", "    end = len(lines)")], "W", ["W04"])
add("ledger rows not reduced", [(WP, '    return "- %s | **%s** | %s" % (date, headline, rule)', "    return line")], "W", ["W07"])
add("sidecar not written", [(WP, "        for path, body in ((side, side_text), (out, text)):", "        for path, body in ((out, text),):")], "W", ["W17"])
add("sidecar lists only one class", [(WP, "            counts[verdict] += 1\n            b.dropped.append((verdict, lineno, why, c0[:80]))",
                                      '            counts[verdict] += 1\n            if verdict == "dead":\n                b.dropped.append((verdict, lineno, why, c0[:80]))')], "W", ["W17"])
add("sidecar cell not cut at 80 characters", [(WP, "b.dropped.append((verdict, lineno, why, c0[:80]))", "b.dropped.append((verdict, lineno, why, c0[:60]))")], "W", ["W17"])
add("--check ignores newer sources", [(WP, "                if os.stat(src).st_mtime_ns > pm:", "                if False:")], "W", ["W11b"])
add("--check ignores the pack's content (m1)", [(WP, "                if sha(have) != sha(want):", "                if False:")], "W", ["W11d", "W11h"])
add("--check skips every line that starts 'generated: ' (round 2's hole, m1)",
    [(WP, "                want = make(stamp)[0]\n                if sha(have) != sha(want):",
      '                want = make(stamp)[0]\n                if sha("\\n".join(x for x in have.split("\\n") if not x.startswith("generated: "))) != sha("\\n".join(x for x in want.split("\\n") if not x.startswith("generated: "))):')], "W", ["W11h"])
add("Q11 --check ignores a sidecar whose content differs", [(WP, "                    if sha(shave) != sha(swant):", "                    if False:")], "W", ["W11i"])
add("--check ignores a missing sidecar", [(WP, "            if not os.path.isfile(side):\n                faults.append(", "            if not os.path.isfile(side):\n                (lambda x: None)(")], "W", ["W11g"])
add("--check ignores the build date", [(WP, "            if not m or m.group(1) != today.isoformat():", "            if False:")], "W", ["W11e"])
add("M2: an empty source is accepted", [(WP, "        if not data.strip() and not allow_empty:", "        if False:")], "W", ["W18f", "W18l"])
add("M2: a rules card without 'Most reinforced' builds with a placeholder", [(WP, "    if top_text is None:\n        raise BuildFail(", '    if top_text is None:\n        top_text = "(none)\\n"\n    if False:\n        raise BuildFail(')], "W", ["W18c"])
add("M2: a grants file without its table header is read anyway", [(WP, "    if not any(GRANTS_HEADER.match(l) for l in all_lines):", "    if False:")], "W", ["W18h"])
add("M2: indented grant rows are silently skipped", [(WP, "    if indented:\n", "    if False:\n")], "W", ["W18i"])
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
add("M3: the fallback is silent in the prompt", [(HB, ' if [ "${WAKE_PACK_OK:-0}" != "1" ]; then', " if false; then")], "P", ["P04", "P04b", "P04c", "P16", "P17"])
add("M3: the notice is appended at the END of the prompt, not its first lines",
    [(HB, '    "ultrathink${WAKE_NL}${WAKE_NL}"*) INITIAL_PROMPT="ultrathink${WAKE_NL}${WAKE_NL}${WAKE_NOTICE}${WAKE_NL}${INITIAL_PROMPT#"ultrathink${WAKE_NL}${WAKE_NL}"}" ;;',
      '    "ultrathink${WAKE_NL}${WAKE_NL}"*) INITIAL_PROMPT="${INITIAL_PROMPT}${WAKE_NL}${WAKE_NOTICE}" ;;')], "P", ["P04"])
add("M3: the notice gives no reason", [(HB, "Why: ${WAKE_FAIL:-no reason was recorded}", "Why: see the terminal")], "P", ["P04", "P04c"])
add("a text proposal quotes text that is not in its target", [("proposed/06_wrap_step.md", "1. Distil the session: new learnings", "1. Distil the day: new learnings")], "P", ["P10"])
add("M4: a proposal's new text is worded for every seat", [("proposed/03_brain_CLAUDE_md.md", "**On a seat that boots on a wake pack**", "**On every seat**")], "P", ["P18"])
add("M4: proposal 2 deletes Kam's lesson-load sentence again",
    [("proposed/02_root_CLAUDE_md.md", "1. Read this file → `0_Brain/CLAUDE.md` → `0_Brain/identity/persona.md` +\n```\n\n```new",
      "1. Read this file → `0_Brain/CLAUDE.md` → `0_Brain/identity/persona.md` +\n   `voice-protocol.md` → `0_Brain/people/kam.md`.\n2. Read ALL of `0_Brain/learnings/` (token cost is explicitly accepted — Kam wants\n```\n\n```new")], "P", ["P18"])
add("m6: the gitignore proposal ignores the whole out/ directory again", [("proposed/05_gitignore.md", "2_Project_Files/wake/out/WAKE-*\n", "2_Project_Files/wake/out/\n")], "P", ["P19"])
add("proposal 9 loses its all-seats marking", [("proposed/09_prompt_backtick.md", "**ALL SEATS: needs Tuesday's and Friday's agreement.**", "Wednesday decides.")], "P", ["P20"])

# ── doctor proposal ─────────────────────────────────────────────────────────────────────────────
add("doctor snippet ignores a stale pack", [(DOC, 'if [ "$WP_RC" -eq 0 ]; then', "if true; then")], "D", ["D03"])
add("doctor snippet ignores a stacked handover", [(DOC, 'if [ "$HO_RC" -eq 0 ]; then', "if true; then")], "D", ["D04"])
add("doctor snippet takes the seat from a default, not the tree", [(DOC, "  WK_SEAT=\"$(printf '%s\\n' \"$WK_OUT\" | sed -n 's/^seat: *//p')\"", '  WK_SEAT="wednesday"')], "D", ["D05"])
add("M3: doctor is silent when a cut-over seat has no pack", [(DOC, '    elif [ -f "$WK_STATE" ]; then', "    elif false; then")], "D", ["D06"])
add("m7: doctor discards handover.sh's stderr", [(DOC, '  WK_OUT="$(bash "$HO" --where 2>&1)"; WK_RC=$?', '  WK_OUT="$(bash "$HO" --where 2>/dev/null)"; WK_RC=$?')], "D", ["D07"])
