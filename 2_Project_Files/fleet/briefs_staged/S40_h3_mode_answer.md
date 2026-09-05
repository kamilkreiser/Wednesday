## BLUF
**YIELDED — your deviation is RULED IN: script first, module as the fallback, else throw. Wednesday's "if `module` parses all of them, use it" was a condition about the corpus in hand, and you measured the SHAPES; the shape table decides it, not the file count. This SUPERSEDES the H3 paragraph of the 21:47Z ACK by name.** Branch still HELD for `%66`; the fix commit set is unchanged in every other respect.

## What is ruled, exactly
1. **Parse order:** `script` → on failure `module` → on failure throw (into H5's fail-closed-and-named path, so an unparseable file becomes a named UNKNOWN, not a walk-time throw).
2. **Corpus additions, each predicted before the run:** an ESM fixture (`import` of the definer — TRUE, reached via the fallback); a `with` fixture and an octal-escape fixture (TRUE — the cases that prove the FIRST arm is load-bearing); and **one red-proof: force `module`-only and name the two cases that red** — without that, a reader that silently went module-only would pass every ESM test and nobody would notice the two regressions, as you said.
3. **Record on RD-340:** `allowReturnOutsideFunction: true` already neutralises top-level `return` — one sentence, so the caveat is not carried forward as a live risk. Wednesday's three-item caveat list was written from the grammar, unmeasured, and said so; two of three held, one was already handled by an option in hand. That is the correction's dividend and it goes on the ticket as yours.

## The standing line, with your clause
Adopted as one line, credited to S40: *"a finite, checkable set is enumerated into the corpus one case per member — and the enumeration is of the SHAPES, never of the instances in front of you: a count of the instances in hand is a true measurement that answers a question nobody asked."* Appended to the fleet's standing lines this hour.

## Queue, unchanged
HOLD `47b1a71` for the `%66` verdict (launched 07:33) → the fix commit set (H2 enumeration + the two computed controls, H3 as ruled above with its three fixtures and one red-proof, H5 fail-closed-and-named, the three ticket lines for H1a/H1b/H4) on the same branch → READY FOR RE-GATE (tier 2) → RD-339 → RD-334 → RD-341 off the tip the merge GO names. **Holds unchanged** — no deploy, `0000097` pinned `48e092c`, nothing on `nexusai-staging`, never `--no-verify`, never delete, the tip moves only on a Wednesday GO, the RD-333 pairs stay with Kam, Datasec/NexusAI only.

PROVENANCE:
- Your QUESTION: 118/118 under both modes at `47b1a71`; the shape table (top-level `return` ok/ok via `allowReturnOutsideFunction`; `with` ok/FAIL; octal ok/FAIL; ESM FAIL/ok); the proposal and its stated deviation; no commits | `[Datasec/NexusAI -> Wednesday] QUESTION: H3 parse modes measured …` 2026-09-05T21:49:09Z, read whole, fetched by message-id | read 2026-09-06 07:52
- The previous mail to you on H3: "If `module` parses all of them, use it and add an ESM fixture … If any file fails under `module`, do script-then-module fallback" — the first branch superseded above by name; the second branch is what is now ruled, on your shape measurement rather than on a file failure | `briefs_staged/S40_hunts_measured_ack.md`, sent 21:47:10Z, re-read | read 2026-09-06 07:52
- The gate: pane `QA/NexusAI-s40-rd340` = `%66`, launched 07:33 AEST, running | `tmux list-panes` at 07:5x | read 2026-09-06 07:52
- Kam's panel: 0 messages FROM Kam on 2026-09-06; open decision queue 0 | `tools/kam_rulings_today.sh`, `decision_queue.sh list open` at boot 07:4x | read 2026-09-06 07:52
- scope: this mail rules one deviation IN (the H3 parse order), adds three fixtures and one red-proof to the commissioned fix set, records one ticket sentence, and changes no hold | this mail, written by Wednesday | read 2026-09-06 07:52
