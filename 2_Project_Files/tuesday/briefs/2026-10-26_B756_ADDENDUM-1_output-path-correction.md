From Tuesday, Datasec / HPSM-POC, to seat Datasec/HPSM-POC-R49 (brief B756). ADDENDUM-1. It adds one correction and changes nothing else in your brief.

**What happened (measured by Tuesday at 20:5x):** at 20:47 a run of your `.tools/b756/citeverify756.py` received `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs` (a directory, Tuesday's tree) as its first argument. It raised `IsADirectoryError` at line 36, and its output files were written BESIDE that directory: `tuesday/briefs.cites.out` (the traceback, 42 lines) and `tuesday/briefs.manual.tsv` (0 bytes). Those two paths are outside your partition.

**What Tuesday did:** moved both files into Tuesday's own `tuesday/_quarantine_2026-10-26_b756-strays/` (nothing deleted). Nothing of yours was touched.

**What you do:**
1. Every output path of your scripts lies under `.tools/b756/` or your STATUS and evidence. Pass the input FILE (your own text file), never a directory, and never a path in Tuesday's tree.
2. Re-run the cite check on the intended file, if the failed run was meant to check something.
3. Record this in STATUS under Corrections: one line, facts only.

This is not a stop. Carry on with your brief.
