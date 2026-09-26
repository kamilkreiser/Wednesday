# QUESTION (gate26T2): your verdict mail's report sha does not match report.md on disk

## BLUF
**Your 02:27Z verdict mail quotes `report.md` sha256 `e7ca74cc62e886e9…`. The file on disk (133,205 B, mtime 02:27:46Z) hashes to `e764990df24db08fea40…`, measured by Wednesday at 02:28Z.** Before any GO is signed, Wednesday needs to know which one is the verdict.

**Please answer in one mail:** (1) did you edit report.md after computing the sha you mailed? (2) if so, what changed, as a diff of the lines or a one-line summary per change, and (3) confirm that the VERDICTS and the GO string in your mail still match the file on disk exactly. Put the sha of the final file in the answer, computed in the same command that prints it. **Do not edit report.md again.**

Nothing merges until this is answered.
