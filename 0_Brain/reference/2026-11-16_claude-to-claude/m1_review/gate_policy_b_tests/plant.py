# QA-POLICY-B: apply ONE plant or mutant to a tree at the head (exact text, each old text found exactly once).
# usage: python3 -B plant.py <tree> <id>     (prints the ids with no argument)
import sys, os
A = "crates/coagent-policy/src/action.rs"
S = "crates/coagent-policy/src/shell/mod.rs"
P = {
 # the builder's six, re-made from its patch files (changed lines read; applied by the check's own edits)
 "P1": [(S, "        cap: max_pieces.saturating_add(1),", "        cap: 100, // PLANT P-1: the free-text cut at 100 pieces, silent"),
        (S, "        over: scan.pieces.len() > max_pieces || sink.work > max_work,", "        over: sink.work > max_work, // PLANT P-1")],
 "P2": [(A, "            let head: String = s.chars().take(FREE_TEXT_CHECK_CHARS).collect();", "            let head: String = s.chars().take(10).collect(); // PLANT P-2")],
 "P3": [(S, "            cap: PIECE_CAP,\n", "            cap: crate::action::MAX_FREE_PIECES + 1, // PLANT P-3\n")],
 "P4": [(S, "            for w in &snapshot {\n                for (i, _) in w.match_indices('@') {\n                    add_piece(&w[i + 1..], &mut scan, &mut sink);\n                }\n            }",
            "            let _ = &snapshot; // PLANT P-4: scan B's @ pass dropped")],
 "P5": [(S, "        over: scan.pieces.len() > max_pieces || sink.work > max_work,", "        over: false, // PLANT P-5: the bound cuts silently")],
 "P6": [(A, "    let b = shell::scan_free_text(&windows, &a_pieces, MAX_FREE_PIECES, MAX_FREE_WORK);",
            "    let b = shell::scan_free_text(&windows, &a_pieces, usize::MAX - 1, u64::MAX - 1); // PLANT P-6")],
 # the check's three LOOSER plants
 "L1": [(A, "            a_pieces.push(piece.clone());\n            targets.push(Target::Path {\n                role: PathRole::InText,\n                path: lexical_only(&piece, cwd_path, env),\n            });",
            "            a_pieces.push(piece.clone()); // PLANT L-1: scan A's InText targets not pushed")],
 "L2": [(A, "    let oversize = oversize.or(b.over.then_some(FREE_TEXT_TOO_LARGE));",
            "    let _ = oversize;\n    let oversize = b.over.then_some(FREE_TEXT_TOO_LARGE); // PLANT L-2: the command's own oversize dropped")],
 "L3": [(A, "pub const MAX_FREE_WORK: u64 = 8_000;", "pub const MAX_FREE_WORK: u64 = u64::MAX; // PLANT L-3 (in the constant)")],
 # mutants of item 7
 "M1": [(S, "        if it.next() == Some('u') {\n            for _ in 0..4 {\n                if it.peek().is_some_and(|h| h.is_ascii_hexdigit()) {\n                    it.next();\n                }\n            }\n        }",
            "        it.next(); // MUTANT M1: the four hex digits after \\u not skipped")],
 "M2": [(S, "        out.push(' ');\n        if it.next() == Some('u') {", "        out.push(' ');\n        if it.peek() == Some(&'u') { // MUTANT M2: the escaped character not consumed")],
 "M3": [(S, "        for word in text.split(|c: char| c.is_whitespace() || c.is_control()) {", "        for word in text.split(' ') { // MUTANT M3: split at ' ' only")],
 "M4": [(S, "            if word.contains(\"$'\") {\n                scan_one(&decode_ansi_c(word), &mut scan, &mut sink);\n            }", "            // MUTANT M4: B's $'..' decode removed")],
 "M5": [(S, "        for q in quoted {\n            if q.contains(char::is_whitespace) {\n                add_piece(q.trim(), &mut scan, &mut sink);\n            }\n        }", "        let _ = quoted; // MUTANT M5: the quoted-span step removed")],
 "M6": [(S, "        seen: already.iter().cloned().collect(),", "        seen: { let _ = already; std::collections::BTreeSet::new() }, // MUTANT M6: scan A's pieces not seeded")],
 "M7": [(S, "        over: scan.pieces.len() > max_pieces || sink.work > max_work,", "        over: scan.pieces.len() >= max_pieces || sink.work >= max_work, // MUTANT M7")],
 "M8": [(A, "            let head: String = s.chars().take(FREE_TEXT_CHECK_CHARS).collect();", "            let head: String = s.chars().take(1000).collect(); // MUTANT M8")],
 "M9": [(A, "        Some(other) => {\n            let mut c = String::new();\n            crate::hash::canonical_json(other, &mut c);\n            Some(c.chars().take(FREE_TEXT_CHECK_CHARS).collect())\n        }",
            "        Some(_) => None, // MUTANT M9: a non-string prompt not read")],
 "M10": [(A, "pub const MAX_FREE_WORK: u64 = 8_000;", "pub const MAX_FREE_WORK: u64 = 2_500; // MUTANT M10")],
 "M12": [(S, "        + p.chars().filter(|c| *c != '/' && *c != '\\\\').count() as u64 / WORK_CHARS", "        // MUTANT M12: the character term removed")],
 "M13": [(S, "            let snapshot: Vec<String> = scan.exact[e0..]\n                .iter()\n                .chain(scan.pieces[p0..].iter())\n                .cloned()\n                .collect();",
             "            let _ = p0;\n            let snapshot: Vec<String> = scan.exact[e0..].to_vec(); // MUTANT M13: @ pass on exact words only")],
 "M14": [(A, "        windows.push((bounded, ESCAPES_BLANKED));\n    }", "        if !text.starts_with('{') && !text.starts_with('[') { let _ = bounded; continue; } // MUTANT M14: URL windows dropped\n        windows.push((bounded, ESCAPES_BLANKED));\n    }")],
 # a deliberately too-strict guard for the item 3 positive control (lowered so one ordinary row flips)
 "G1": [(A, "pub const MAX_FREE_WORK: u64 = 8_000;", "pub const MAX_FREE_WORK: u64 = 1_000; // CONTROL G-1: guard lowered (scratch only)")],
 # timing control: scan B run twice
 "T70": [(A, "    let b = shell::scan_free_text(&windows, &a_pieces, MAX_FREE_PIECES, MAX_FREE_WORK);",
             "    let b = shell::scan_free_text(&windows, &a_pieces, MAX_FREE_PIECES, MAX_FREE_WORK);\n    if !windows.is_empty() { let s = std::time::Instant::now(); while s.elapsed() < std::time::Duration::from_millis(70) { std::hint::spin_loop(); } } // CONTROL T-70: 70 ms extra per call with free text")],
 "T2": [(A, "    let b = shell::scan_free_text(&windows, &a_pieces, MAX_FREE_PIECES, MAX_FREE_WORK);",
             "    let b = shell::scan_free_text(&windows, &a_pieces, MAX_FREE_PIECES, MAX_FREE_WORK);\n    let _b2 = std::hint::black_box(shell::scan_free_text(&windows, &a_pieces, MAX_FREE_PIECES, MAX_FREE_WORK)); // CONTROL T-2")],
}
if len(sys.argv) < 3:
    print(" ".join(P)); sys.exit(0)
tree, pid = sys.argv[1], sys.argv[2]
for f, old, new in P[pid]:
    p = os.path.join(tree, f)
    s = open(p).read()
    c = s.count(old)
    assert c == 1, f"{pid}: {f}: old text found {c} times"
    open(p, "w").write(s.replace(old, new))
print(f"applied {pid} to {tree}")
