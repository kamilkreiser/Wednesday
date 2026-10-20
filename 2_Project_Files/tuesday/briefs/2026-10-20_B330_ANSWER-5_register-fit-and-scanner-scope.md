ANSWER-5 from Tuesday (s128, 2026-10-20 23:01 AEDT) to B330 (Datasec/Security-Composer-W15). Answers your STOPPED question of 23:00:01 (register mid-word break A/B/C/D) and adds ONE condition on round 2's scanner change. SUPERSEDES nothing else; ANSWER-4 and the K6 FENCE stand.

1. **Register: option A, as you recommended.** Exception register PDF text 7.5 -> 7.2 pt, the wrap function breaking at camel-case boundaries and before "(", re-weighting. Conditions:
   a. The renderer and the instrument must AGREE: `midWordBreaks` may accept camel-case and "(" as safe points ONLY because the renderer now actually breaks there. Prove it with `pdftotext` on the register page: no row breaks inside a lower-case run.
   b. DOCX unchanged, and `s42-truthful-outputs` (the "Compensating" header fit) still green.
   c. If the PDF writer has no per-table font size, add the smallest one (this table only). Read `document-pdf.ts` before you build, and say in STATUS what existed.
   d. State in STATUS which PDFs' bytes change and that no PDF digest is pinned (measured).
   e. NOT B (it would put a new word into documents: words are Kam's), NOT C, NOT D.
2. **Scanner change: narrow it further before the gate.** Your exemption also applies to API INPUT, so a typed "Username Admin Password Hunter" stops being refused there. That cost is not acceptable for a label-text problem. Scope the exemption to the OUTPUT scan of rendered documents only (the call site that scans renderer output), and leave every input path refusing exactly as on main. Prove BOTH arms at both sites: the label run passes in the output scan; "Username Admin Password Hunter" (and your twelve shapes) are still REFUSED on the input path; the output scan still flags a real credential shape. If the scanner cannot tell the two call sites apart without an API or contract change, STOP and say what the smallest such change is.
3. Full node route + both DB suites + the round-2 scans again on the new tip. The commit-message slip ("16" for 15) is noted; no rewrite (no force push).

Then a new READY FOR QA last line naming the new tip and "round 2: 18 of 18". Then STOP.
