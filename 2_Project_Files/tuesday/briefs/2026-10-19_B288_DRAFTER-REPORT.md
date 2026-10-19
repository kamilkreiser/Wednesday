# B288 drafter report (2026-10-19 ~18:30 AEDT)

Brief: `2026-10-19_B288_SEAT-W6_hpsmpoc-l4-imports-267-275-263.md` (template: B284 brief, read whole).

MEASURED (read-only): main `e4f270ea41bd0f15886ba8a9dc2667eae1305903` by ls-remote; 0 `b288*` refs; no B288 file in either Briefs folder; card `hpsmpoc-import-words-1019` status ruled, choice a (18:20:54); 0 listeners on 7200-7299; load1 10.46 at 18:23.

Corrections to the commission (flag at stamp):
1. Import behaviour tests are in `api/tests/HpsmPoc.Api.Tests/Imports/**`, not the Assessment.Tests project (which has only ImportKeptCopyTests, ImportReaderMinimiseTests). Brief adds the first path as allowed (R-W6-1).
2. The ruling covers the detail sentence AND the field message "The rows could not be saved." (both are text 2). Brief replaces both with `ImportPendingSweep.Reason`; keeps code, 500 and title (R-W6-3).
3. Words NOT in the ruling and left alone, sent to FOR TUESDAY: stored run reason at ImportEndpoints.cs:198 (also says files kept; asserted at ImportPendingSweepLoopTests.cs:1204, ImportRobustnessTests.cs:187), StoreFailed text :386, contract descriptions (Contract/openapi.yaml:181/901/950, mirrored in web/contract and schema.gen.ts).
4. Existing unreadable-form 400 to reuse: ImportEndpoints.cs:71-74 (`import.body`, "The upload could not be read as multipart/form-data.").

UNMEASURED: live Done-whens of -275 and -263 (brief makes the seat read them and stop on migration/contract/new words); PR #162 diff; endpoint 500 itself; baseline counts. Slots left for Tuesday: STAMP_TIME, B_NUMBER_CONFIRM, PORT_BLOCK (proposal 7250-7259). No .pre-stamp copy made (Tuesday does it).
