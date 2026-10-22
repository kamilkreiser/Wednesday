# B454 drafter report (read-only drafter, 2026-10-22 about 13:20 AEDT)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-22_B454_SEAT-G4_mps-b446-gate-tier1.md` (123 lines, shape of B451, 9 checks C1-C9).

Stamp slots: 5 slot lines plus the last line = 6 by the stamp grep (control reads 1). Slots: main, head, time, launch authority and model receipt, pane, word-pack location (an extra slot the user did not list; Tuesday may write "none").

MEASURED (read verbs on the shared object store, 13:18-13:25): 0 2 ahead/behind; 8 paths and numstat equal the request; DevStubAuth.cs diff is exactly three one-line prefix additions with the text after the prefix unchanged; overlap of B446's 8 paths with b444 (26), b445 (25), b450 (1) = 0, 0, 0; no WaitForTicket in the new tests; the default lives in code (`FeedbackEndpoints.DefaultPerHour = 20`, key `MpsCalc:Feedback:RateLimit:PerHour`); API.md and the three appsettings*.json and infra carry no file for it.

Open points for Tuesday:
1. The builder brief's premise "default lives where API.md says (appsettings*.json)" is not supported by API.md (it names no file). Brief treats the code default as a Note, not a defect.
2. API.md ("seconds until one more item may be stored") and openapi ("until the oldest counted item leaves") Retry-After wordings differ when stored items exceed the limit; brief sets this as a Note unless code contradicts both.
3. Retry-After is computed after the store lock is released (small window); brief sets a Note unless it can be 0 or negative.
4. The builder ran its 165 mutants at the pre-restack 0bee58c; brief has the gate re-run them at head.
5. Builder spawned a refusing child process (port 0) despite "no API process"; brief records it as a Note and tells the gate to start no process of its own.
6. Not read by the drafter: test bodies, FeedbackAttachments.ReadMultipart, the dialog test (all RELAYED).
7. B452 and B453 gate trees already exist under .tools, so B454 is free (no qa-b454*).
