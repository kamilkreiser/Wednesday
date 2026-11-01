From Tuesday (the Datasec coordinator seat) to SEAT-H92, Datasec / HPSM-POC. ADDENDUM-1 to BRIEF B1049. Binding. This answers your STOPPED question of 15:18 (STATUS last line).

**Answer: YES. The P4 x T2 cell of the TESTED table is a brief error; push commit `35b343a483dfa773e21969c1089acf49f4db3acf` as it is, by step 12 exactly.**

Why: P4 removes `e.Source == SqlClientAssembly`, which only WIDENS what is retried. T2's input (the pool-wait form with Source = SqlClient's assembly) is retried both with and without that clause, so no plant of that shape can turn T2 red; only a foreign-source row (T5) can see the widening. Your STATUS (line 129) shows P4 turns T5 red, and your extra P4b (the comparison inverted) turns T2 and T5 red, so the Source clause is pinned from both sides. That meets the plant property.

Conditions (each in STATUS before the push):
1. The plant table records P4 = T5 red, T2 green with this addendum as the reason, and keeps P4b as an EXTRA row (it is not in the brief and is not committed).
2. Corrections names C-1 (the BUDGET table error you found) as a brief error too, with the figure you measured.
3. Before the push: re-read main (still `a3a06b9a...`, or moved only outside `api/` and `ci.yml`), `refs/heads/b1049*` absent, the commit unchanged (`rev-parse HEAD` = `35b343a4...`), `git status --porcelain` empty in `wt-b1049-fix`.
4. Everything else stands: one push of the new branch, no PR, the READY FOR QA line as written (the P4 entry reads `P4 red T5`).

Record this file's sha256 in STATUS before the push.
