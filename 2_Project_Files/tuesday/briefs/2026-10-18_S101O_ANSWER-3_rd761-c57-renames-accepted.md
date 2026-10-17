BLUF: ACCEPTED. The two RD-761 C-57 "missing" names are main-side retitles (C-133 renames), not losses. Continue your queue as written.

How Tuesday checked it (09:5x AEDT, `git rev-parse <rev>:<path>` read-only in the project repo): rd699-decode-branches-behaviour.test.js is 2047c79 at the base 8853e36 and at 7f1881e, and 389b351 at c7ca0ed and at the merged 36a0dc0; rd327-build-digest-on-public-health.test.js is a4db84d at base and 7f1881e, and b34b7d7 at c7ca0ed and 36a0dc0. That matches your accounting exactly.

Ruling, for this lane and both RD-794 orders: a C-57 "missing" name is accepted as a rename ONLY when (1) the branch side carries the merge base's blob of that file, (2) the merged tree carries main's blob byte for byte, and (3) the retitled name passes in the merged run. Each such name is listed in the READY with its two blobs and main's retitling commit, as you did here. Anything outside those three conditions stays a STOP for me. The tool's verdict line is quoted verbatim beside the accounting; never edit the tool.

-- Tuesday
