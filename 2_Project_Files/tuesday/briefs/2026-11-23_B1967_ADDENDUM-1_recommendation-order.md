# B1967 ADDENDUM-1 (Tuesday, s315): the order of the coordinator's recommendation in the document

Binds seat `Datasec/NexusAI-N166`. Read whole before Step 5; name it in ADDENDA READ.

**Why:** the product owner's ruling asked to see "darker values for each fill from the brand tokens". The frozen `mkdoc.py` puts the outline first and the tokens second. The coordinator overrules the order (the drafter's Q-1): the three darker graphic-kind tokens come FIRST and the outline is the second choice, offered to keep today's toner colours. Prose only. No figure, table, measurement, candidate or screenshot changes.

**What you do (between Step 4 and Step 5):**
1. Copy `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1967_ADDENDUM-1_recommendation-order.py` to `.tools/b1967/frozen/addendum1.py` with `cp -n`, then `cmp`.
2. Run it to write a NEW file: `python3 -I .tools/b1967/frozen/addendum1.py <EV>/data/mkdoc.py <EV>/data/mkdoc_a1.py` (absolute paths). It must print `OK: 3 replacements, 1 swap`. Any other output is a STOP. The frozen `mkdoc.py` stays unchanged: print its sha256 before and after.
3. In Step 5 run `mkdoc_a1.py` in place of `mkdoc.py`, with the same arguments. Everything else in Step 5 and Step 6 is unchanged. `scans.py`'s expected block still holds: no section, token row, image or "card" word changes.
4. Check the result: in `RD-1032_options.md`, the BLUF line beginning `- **Coordinator's recommendation` says the three graphic-kind tokens first. In section 8, item `1.` begins `**First choice, the darker values you asked to see:**` and item `2.` begins `**If you would rather keep today's toner colours: N2b`. Print both lines into STATUS.

**Tested by Tuesday before this addendum was issued:** the patch was run on the kit's own `mkdoc.py`, extracted by your Step 2 `awk` form; `cmp` reads equal to the drafter's `r3/mkdoc.py`. The patched program was then run on the drafter's `r3` data and wrote 207 lines. The two lines read as in item 4.
