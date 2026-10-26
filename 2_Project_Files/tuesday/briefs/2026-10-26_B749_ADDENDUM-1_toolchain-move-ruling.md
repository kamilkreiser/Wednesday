From Tuesday (the product owner's Datasec coordinator seat) to Datasec/HPSM-POC-D32, B749 only. ADDENDUM-1, the answer to your STOPPED: NEEDS TUESDAY line (FINAL 18:41:29).

RULING: YES. Deploy the exact CI package of 68ebdbf762c9a793fb3d1f3b7bcbaa6aef5dc3d8 (api.zip sha256 a822e12ec8a18c48673e91c43060fee7f461300039c400d86d65503fd19af94b, web.zip sha256 2fec56811e78970016e2f8a2b864b19348001fb890af1e01458aa42fba12dd11, run 40284150506 attempt 1) to UAT, under every other line of your brief unchanged.

WHY (Tuesday's reasons, so you can check each against your own evidence):
1. You proved one cause for both items from the files themselves: the PDB compilation options name compiler 5.9.0-1.26523.112 and runtime 10.0.14-servicing in the new package against 5.9.0-1.26505.111 and 10.0.13-servicing in OLD, and the apphost's embedded version moved 10.0.1326 -> 10.0.1426 at the same size. That is the CI runner's SDK servicing move 10.0.402 -> 10.0.403 that B729 and B733 also recorded.
2. Zero api/src paths of Api, Feedback, Reporting or Rules are in the 17-commit range, so no source change of ours sits in those differences.
3. HpsmPoc.Api.runtimeconfig.json and appsettings.json are EQUAL, so the framework the app asks for did not change.
4. CI run 40284150506 built and tested this exact package: api (ASP.NET Core) and the three SQL Server jobs success.
5. The rollback kit is proven runnable and UAT is the review site, not production.

THE CLASS THIS ADDS TO BUILD 3's closed list, stated as a property: a binary that differs ONLY because the CI toolchain moved, where (a) the cause is read from the binary itself (PDB compilation options, or the apphost's embedded version string), (b) no source path of that assembly is in the range, and (c) the CI run that built this exact package is green. It covers exactly: HpsmPoc.Api.dll, HpsmPoc.Modules.Feedback.dll, HpsmPoc.Modules.Reporting.dll, HpsmPoc.Modules.Rules.dll, their PDBs, and the native apphost HpsmPoc.Api. Any other shape: prove it meets this property or STOP again.

CONDITIONS (all binding):
1. Your START SAFETY step runs BEFORE any hosted write, on the NEW api package: the app starts from this package as its runtime would run it, and reaches its listening line plus one health read on loopback. Quote the lines. A failed start is a STOP, not a rollback (nothing is deployed yet).
2. Read the slip items you listed under PRIOR WORK ("Not yet read") before the deploy starts, as you said you would.
3. Hard stop unchanged: no deploy START after 21:00:36 AEDT. If you cannot start by then, end STOPPED with the reason; UAT stays on OLD.
4. The AFTER live checks, the rollback rule (ruling 6 of the stamp) and UAT ONLY are unchanged. Record this addendum's class in your STATUS under the API package section, with the evidence paths.

Last line of your STATUS, as before: DEPLOYED: / ROLLED BACK: / STOPPED: .
